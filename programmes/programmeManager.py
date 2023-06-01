from constants import *
from events import GLOBAL_EVENT_TYPES, EventManager, Event
from programmes.sparksProgramme import SparksProgramme
from utils import getRandomColour, getRandomPointInSpace

# Schedules changes in the programmes in response to events
class ProgrammeManager():
    eventManager: EventManager

    def __init__(self, eventManager: EventManager):
        self.eventManager = eventManager

    def step(self):
        newEvents: list[Event] = []

        # Go through all future events and process as needed
        unprocessedEvents = [event for event in self.eventManager.localEventQueue if not event.hasBeenProcessed]
        for event in unprocessedEvents:
            if event.type == GLOBAL_EVENT_TYPES.BOOM:
                newEvents.append(Event(
                    type=SparksProgramme.SPARK_EVENT,
                    atTime=event.atTime,
                    hasBeenProcessed=True,
                    params={
                        "centre": getRandomPointInSpace(),
                        "colour": getRandomColour(1),
                    }
                ))
                event.hasBeenProcessed = True
        
        self.eventManager.pushEvents(newEvents)
