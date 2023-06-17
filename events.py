from dataclasses import dataclass, field
import time
import copy
from constants import *
from utils import getAbsolutePath, getRandomColour, getRandomPointInSpace, playAudio
import json
import sys

# Event names
class EVENT_TYPES:
    # General
    PLAY_AUDIO = 'PLAY_AUDIO'
    PLAY_MAIN_SEQUENCE = 'PLAY_MAIN_SEQUENCE'
    CLOCK_SYNC = 'CLOCK_SYNC'
    SYNC_PHASES = 'SYNC_PHASES'
    PHASES_SYNC = 'PHASES_SYNC'
    # Mood events (get translated into programme events)
    FAR_RUMBLE = 'FAR_RUMBLE'
    NEAR_RUMBLE = 'NEAR_RUMBLE'
    QUIET_SYNTHS = 'QUIET_SYNTHS'
    # Effects
    THUNDER = 'THUNDER'
    BOOM = 'BOOM'
    WAVE = 'WAVE'
    CALM = 'CALM'
    NERVOUS = 'NERVOUS'
    # Programme events
    PROG_QUIET_CLOUDS = 'PROG_QUIET_CLOUDS'
    PROG_RUMBLE = 'PROG_RUMBLE'
    PROG_SPEED_INCREASE = 'PROG_SPEED_INCREASE'
    PROG_SPEED_DECREASE = 'PROG_SPEED_DECREASE'
    SCAN_LINE = 'SCAN_LINE'
    FLASH = 'FLASH'
    SPARK = 'SPARK'
    GRITTINESS = 'GRITTINESS'
    BACKGROUND_COLOUR = 'BACKGROUND_COLOUR'


@dataclass
class Event:
    type: str # Event identifier
    params: dict = field(default_factory=dict) # Dict of event params, specific to each event
    atTime: float = None # Timestamp of the event
    # every: float = None # Interval between repetitions (in seconds), if repeating
    # repeatTimes: int = 0 # Number of times to repeat the event

    def __repr__(self):
        return json.dumps({
                 "type": self.type,
                 "atTime": self.atTime,
                 "params": self.params 
            })


@dataclass
class EventSequence:
    events: list[Event] = field(default_factory=list) # Events with timestamps relative to the start of the sequence

    # Loads a sequence from file in the format:
    # EVENT_TIMESTAMP EVENT_TYPE PARAM=VALUE PARAM=VALUE
    # Lines starting with # will be ignored
    def loadFromFile(self, filePath: str):
        f = open(filePath, "r")
        fileContents = f.read()
        f.close()
        lines = fileContents.split('\n')

        startTime = 0
        if len(sys.argv) > 1:
            startTime = int(sys.argv[1])
        
        self.events = []
        for line in lines:
            if not line.startswith('#'):
                lineParts = line.split(' ')
                eventType = ''
                eventTime: float = 0
                params = {}
                for i, part in enumerate(lineParts):
                    # Keep initial events at 0, others shift by -startTime
                    if i == 0:
                        eventTime = float(part)
                        if eventTime > 0:
                            eventTime -= startTime
                    elif i == 1: eventType = part
                    else:
                        paramParts = part.split('=')
                        params[paramParts[0]] = paramParts[1]

                if eventTime >= 0:
                    self.events.append(Event(
                        type=eventType,
                        atTime=eventTime,
                        params=params,
                    ))

    
    # Gets a copy of the events with timestamps relative to the current time
    def getEvents(self):
        currentTime = time.time()
        events: list[Event] = []
        for event in self.events:
            eventCopy = copy.deepcopy(event)
            eventCopy.atTime += currentTime
            events.append(eventCopy)
        return generateProgrammeEvents(events)


class EventManager:
    localEventQueue: list[Event]
    slaveEventQueue: list[Event]
    mainSequence: EventSequence
    isMaster: bool

    def __init__(self, isMaster: bool):
        self.isMaster = isMaster

        if self.isMaster:
            self.mainSequence = EventSequence()
            self.mainSequence.loadFromFile(getAbsolutePath(MAIN_SEQUENCE_FILE))
            self.localEventQueue = self.mainSequence.getEvents()
            self.slaveEventQueue = []
            for event in self.localEventQueue:
                self.slaveEventQueue.append(event)
        else:
            self.localEventQueue = []
    
    # Selects events from the local (or slave) queue that should happen now,
    # processes global events and returns the others
    def popEvents(self, popFromSlaveQueue=False):
        currentTime = time.time() + (SLAVE_ADVANCE_NOTICE_TIME if popFromSlaveQueue else 0)
        currentEvents: list[Event] = []
        futureEvents: list[Event] = []
        for event in (self.localEventQueue if not popFromSlaveQueue else self.slaveEventQueue):
            if event.atTime <= currentTime:
                if event.type == EVENT_TYPES.PLAY_AUDIO and not popFromSlaveQueue:
                    if len(sys.argv) > 1:
                        playAudio(sys.argv[1])
                    else:
                        playAudio()
                    pass
                elif event.type == EVENT_TYPES.PLAY_MAIN_SEQUENCE and not popFromSlaveQueue:
                    sequenceEvents = self.mainSequence.getEvents()
                    for newEvent in sequenceEvents:
                        futureEvents.append(newEvent)
                    pass
                else:
                    currentEvents.append(event)
            else:
                futureEvents.append(event)
        
        if not popFromSlaveQueue:
            self.localEventQueue = futureEvents
        else:
            self.slaveEventQueue = futureEvents
        
        return currentEvents

    def pushEvents(self, events: list[Event]):
        for event in events:
            self.localEventQueue.append(event)
            
        if self.isMaster:
            for event in events:
                self.slaveEventQueue.append(event)
    
    def removeEvents(self, events: list[Event]):
        for event in events:
            try: self.localEventQueue.remove(event)
            except: pass
            if self.isMaster:
                try: self.slaveEventQueue.remove(event)
                except: pass

# Go through the basic sequence events and generate programme events
def generateProgrammeEvents(events: list[Event]):
    newEvents: list[Event] = []

    for event in events:
        if event.type == EVENT_TYPES.FAR_RUMBLE:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_QUIET_CLOUDS,
                atTime=event.atTime,
            ))
        
        elif event.type == EVENT_TYPES.NEAR_RUMBLE:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RUMBLE,
                atTime=event.atTime,
            ))

        elif event.type == EVENT_TYPES.THUNDER:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPEED_INCREASE,
                atTime=event.atTime,
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPEED_DECREASE,
                atTime=event.atTime + 1,
            ))

        elif event.type == EVENT_TYPES.BOOM:

            # Pre-spark flash
            sparkCentre = getRandomPointInSpace()
            newEvents.append(Event(
                type=EVENT_TYPES.FLASH,
                atTime=event.atTime - 1,
                params={
                    "centre": sparkCentre,
                    "colour": (255, 255, 255),
                    "radius": 30,
                    "life": 1,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.SPARK,
                atTime=event.atTime,
                params={
                    "centre": sparkCentre,
                    "colour": getRandomColour(1),
                }
            ))

            newEvents.append(Event(
                type=EVENT_TYPES.FLASH,
                atTime=event.atTime,
                params={
                    "centre": getRandomPointInSpace(),
                    "colour": (255, 255, 255),
                    "radius": 70,
                    "life": 1,
                }
            ))

        elif event.type == EVENT_TYPES.WAVE:
            newEvents.append(Event(
                type=EVENT_TYPES.SCAN_LINE,
                atTime=event.atTime,
                params={
                    "colour": getRandomColour(1),
                    "axis": 1,
                    "direction": -1,
                }
            ))
        
        elif event.type == EVENT_TYPES.CALM:
            newEvents.append(Event(
                type=EVENT_TYPES.GRITTINESS,
                atTime=event.atTime,
                params={ "level": 0 }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={ "brightness": 0.1, "colour": getRandomColour(1), "transition": 1 }
            ))
        
        elif event.type == EVENT_TYPES.NERVOUS:
            newEvents.append(Event(
                type=EVENT_TYPES.GRITTINESS,
                atTime=event.atTime,
                params={ "level": 1 }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={ "brightness": 0, "transition": 0.2 }
            ))
        
        else:
            # Add event as is
            newEvents.append(event)
    
    return newEvents
