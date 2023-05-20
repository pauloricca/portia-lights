from dataclasses import dataclass, field
import time
import copy
from constants import *
from utils import getAbsolutePath, playAudio

# Event names
class EVENT_TYPES:
    PLAY_AUDIO = 'PLAY_AUDIO'
    PLAY_MAIN_SEQUENCE = 'PLAY_MAIN_SEQUENCE'
    BOOM = 'BOOM'
    WOOSH = 'WOOSH'


@dataclass
class Event:
    type: str # Event identifier
    params: dict = field(default_factory=dict) # Dict of event params, specific to each event
    atTime: float = None # Timestamp of the event
    every: float = None # Interval between repetitions (in seconds), if repeating
    repeatTimes: int = 0 # Number of times to repeat the event


@dataclass
class EventSequence:
    events: list[Event] = field(default_factory=list) # Events with timestamps relative to the start of the sequence

    # Loads a sequence from file in the format:
    # EVENT_TIMESTAMP EVENT_TYPE PARAM=VALUE PARAM=VALUE
    def loadFromFile(self, filePath: str):
        f = open(filePath, "r")
        fileContents = f.read()
        f.close()
        lines = fileContents.split('\n')

        self.events = []
        for line in lines:
            lineParts = line.split(' ')
            eventType = ''
            eventTime: float = 0
            params = {}
            for i, part in enumerate(lineParts):
                if i == 0: eventTime = float(part)
                elif i == 1: eventType = part
                else:
                    paramParts = part.split('=')
                    params[paramParts[0]] = paramParts[1]
            self.events.append(Event(
                type=eventType,
                atTime=eventTime,
                params=params,
            ))
        pass
    
    # Gets a copy of the events with timestamps relative to startTime (defaults to now)
    def getEvents(self, startTime: float = time.time()):
        events: list[Event] = []
        for event in self.events:
            eventCopy = copy.deepcopy(event)
            eventCopy.atTime += startTime
            events.append(eventCopy)
        return events


class EventManager:
    eventBackLog: list[Event]
    mainSequence: EventSequence

    def __init__(self):
        self.mainSequence = EventSequence()
        self.mainSequence.loadFromFile(getAbsolutePath(MAIN_SEQUENCE_FILE))
        self.eventBackLog = self.mainSequence.getEvents()
    
    # Selects events from the back log that should happen now, processes global events and returns the others
    def popEvents(self):
        currentTime = time.time()
        currentEvents: list[Event] = []
        futureEvents: list[Event] = []
        for event in self.eventBackLog:
            if event.atTime <= currentTime:
                if event.type == EVENT_TYPES.PLAY_AUDIO:
                    playAudio()
                    pass
                elif event.type == EVENT_TYPES.PLAY_MAIN_SEQUENCE:
                    for newEvent in self.mainSequence.getEvents():
                        futureEvents.append(newEvent) 
                    pass
                else:
                    currentEvents.append(event)
            else:
                futureEvents.append(event)
        self.eventBackLog = futureEvents
        return currentEvents