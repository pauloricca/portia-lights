from events import EVENT_TYPES, Event
from utils import getRandomColour, getRandomPointInSpace

# Go through the basic sequence events and generate programme events
def eventProgrammer(events: list[Event]):
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
                atTime=event.atTime + 0.7,
            ))

        elif event.type == EVENT_TYPES.BOOM:

            # Pre-spark flash
            sparkCentre = getRandomPointInSpace()
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_FLASH,
                atTime=event.atTime - 1,
                params={
                    "centre": sparkCentre,
                    "colour": (255, 255, 255),
                    "radius": 30,
                    "life": 1,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPARK,
                atTime=event.atTime,
                params={
                    "centre": sparkCentre,
                    "colour": getRandomColour(1),
                }
            ))

            newEvents.append(Event(
                type=EVENT_TYPES.PROG_FLASH,
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
                type=EVENT_TYPES.PROG_SCAN_LINE,
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
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
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
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={ "brightness": 0, "transition": 0.2 }
            ))
        
        else:
            # Add event as is
            newEvents.append(event)
    
    return newEvents
