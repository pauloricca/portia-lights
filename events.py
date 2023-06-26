from dataclasses import dataclass, field
import time
import copy
from typing import Callable
from constants import *
from utils import getAbsolutePath, playAudio
import json
import sys

# Event names
class EVENT_TYPES:
    # App events
    PLAY_MAIN_SEQUENCE = 'PLAY_MAIN_SEQUENCE'
    CLOCK_SYNC = 'CLOCK_SYNC'
    SYNC_PHASES = 'SYNC_PHASES'
    PHASES_SYNC = 'PHASES_SYNC'
    RESTART = 'RESTART'
    RESET = 'RESET'

    # Mood events (get translated into programme events)
    FAR_RUMBLE = 'FAR_RUMBLE'
    NEAR_RUMBLE = 'NEAR_RUMBLE'
    RHYTHMICAL_SYNTHS = 'RHYTHMICAL_SYNTHS'
    SUNSET = 'SUNSET'
    WHISTLE = 'WHISTLE'
    FIRST_BASS_LINE = 'FIRST_BASS_LINE'
    SECOND_BASS_LINE = 'SECOND_BASS_LINE'
    PIANO = 'PIANO'

    # Effects (get translated into programme events)
    FLASHES = 'FLASHES' # duration frequency
    THUNDER = 'THUNDER'
    BOOM = 'BOOM'
    WAVE = 'WAVE'

    # Programme events
    PROG_QUIET_CLOUDS = 'PROG_QUIET_CLOUDS'
    PROG_RUMBLE = 'PROG_RUMBLE'
    PROG_ACCELERATE = 'PROG_ACCELERATE' # high low duration attack release
    PROG_BREATHING = 'PROG_BREATHING' # factor length (count every)
    PROG_SPEED_BREATHING = 'PROG_SPEED_BREATHING' # factor length (count every)
    PROG_HUE_BREATHING = 'PROG_HUE_BREATHING' # factor length (count every)
    PROG_SPEED_CHANGE = 'PROG_SPEED_CHANGE' # factor ramp
    PROG_SCALE_CHANGE = 'PROG_SCALE_CHANGE' # factor ramp
    PROG_RAIN = 'PROG_RAIN' # duration attack release
    PROG_SCAN_LINE = 'PROG_SCAN_LINE'
    PROG_FLASH = 'PROG_FLASH' # centre colour radius life
    PROG_SPARK = 'PROG_SPARK' # centre colour
    PROG_FAR_ORBS = 'PROG_FAR_ORBS' # (hue brightness saturation ramp)
    PROG_NEAR_ORBS = 'PROG_NEAR_ORBS' # (hue brightness saturation ramp)
    PROG_HIDE_ORBS = 'PROG_HIDE_ORBS' # (ramp)
    PROG_WHISTLE_GHOST_BRIGHTNESS = 'PROG_WHISTLE_GHOST_BRIGHTNESS' # brightness (ramp)
    PROG_WHISTLE_GHOST_POSITION = 'PROG_WHISTLE_GHOST_POSITION' # position (ramp)
    PROG_BACKGROUND_COLOUR = 'PROG_BACKGROUND_COLOUR' # (hue brightness saturation ramp)
    PROG_HUE_GRADIENT = 'PROG_HUE_GRADIENT' # brightness hue saturation hueBottom saturationBottom (ramp)
    PROG_RGB_GRADIENT = 'PROG_RGB_GRADIENT' # brightness hue saturation hueBottom saturationBottom (ramp)
    PROG_NOISE_THRESHOLD = 'PROG_NOISE_THRESHOLD' # (brightness hue saturation hueSecond saturationSecond min1 max1 min2 max2 ramp)


@dataclass
class Event:
    type: str # Event identifier
    params: dict = field(default_factory=dict) # Dict of event params, specific to each event
    atTime: float = None # Timestamp of the event

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
                        params[paramParts[0]] = float(paramParts[1])

                if eventTime >= 0:
                    self.events.append(Event(
                        type=eventType,
                        atTime=eventTime,
                        params=params,
                    ))

    
    # Gets a copy of the events with timestamps relative to the current time
    def getEvents(self, eventProgrammer: Callable):
        currentTime = time.time()
        events: list[Event] = []
        for event in self.events:
            eventCopy = copy.deepcopy(event)
            eventCopy.atTime += currentTime
            events.append(eventCopy)
        return eventProgrammer(events)


class EventManager:
    localEventQueue: list[Event]
    slaveEventQueue: list[Event]
    mainSequence: EventSequence
    isMaster: bool
    eventProgrammer: Callable

    def __init__(self, isMaster: bool, eventProgrammer: Callable):
        self.isMaster = isMaster
        self.eventProgrammer = eventProgrammer
        self.localEventQueue = []

        if self.isMaster:
            self.mainSequence = EventSequence()
            self.mainSequence.loadFromFile(getAbsolutePath(MAIN_SEQUENCE_FILE))
            self.slaveEventQueue = []
    
    # Selects events from the local (or slave) queue that should happen now,
    # processes global events and returns the others
    def popEvents(self, popFromSlaveQueue=False):
        currentTime = time.time() + (SLAVE_ADVANCE_NOTICE_TIME if popFromSlaveQueue else 0)
        currentEvents: list[Event] = []
        futureEvents: list[Event] = []
        for event in (self.localEventQueue if not popFromSlaveQueue else self.slaveEventQueue):
            if event.atTime <= currentTime:
                if self.isMaster and event.type == EVENT_TYPES.RESTART and not popFromSlaveQueue:
                    self.startSequence()
                elif self.isMaster and event.type == EVENT_TYPES.PLAY_MAIN_SEQUENCE and not popFromSlaveQueue:
                    sequenceEvents = self.mainSequence.getEvents(self.eventProgrammer)
                    for newEvent in sequenceEvents:
                        futureEvents.append(newEvent)
                        self.slaveEventQueue.append(newEvent)
                    if len(sys.argv) > 1:
                        playAudio(sys.argv[1])
                    else:
                        playAudio()
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
    
    def startSequence(self):
        self.pushEvents([Event(
            type=EVENT_TYPES.RESET,
            atTime=time.time() + 5,
        )])
        for t in range(1):
            self.pushEvents([Event(
                type=EVENT_TYPES.SYNC_PHASES,
                atTime=time.time() + 5 * t,
            )])
        self.pushEvents([Event(
            type=EVENT_TYPES.PLAY_MAIN_SEQUENCE,
            atTime=time.time() + 10,
        )])

