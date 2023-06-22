from random import random
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
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={
                    "hue": 0.6,
                    "ramp": 2,
                }
            ))
        
        elif event.type == EVENT_TYPES.NEAR_RUMBLE:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RUMBLE,
                atTime=event.atTime,
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime - 3,
                params={
                    "hue": 0.15,
                    "ramp": 6,
                }
            ))

        elif event.type == EVENT_TYPES.THUNDER:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPEED_CHANGE,
                atTime=event.atTime,
                params={
                    "factor": 10,
                    "ramp": 0.2,
                },
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={
                    "saturation": 0.2,
                    "ramp": 0.2,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPEED_CHANGE,
                atTime=event.atTime + 0.7,
                params={
                    "factor": 0.1,
                    "ramp": 2,
                },
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime + 0.7,
                params={
                    "saturation": 1,
                    "ramp": 2,
                }
            ))

        elif event.type == EVENT_TYPES.RHYTHMICAL_SYNTHS:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_FAR_ORBS,
                atTime=event.atTime,
                params={
                    "hue": 0.5,
                    "brightness": 1,
                    "ramp": 15,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NEAR_ORBS,
                atTime=event.atTime + 5,
                params={
                    "hue": 0.3,
                    "brightness": 1,
                    "ramp": 15,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={
                    "brightness": 0.1,
                    "saturation": 0.3,
                    "ramp": 10,
                }
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
        
        elif event.type == EVENT_TYPES.FLASHES:
            duration = event.params["duration"]
            flashesPerSecond = event.params["frequency"]
            count = int(duration * flashesPerSecond)
            every = duration / count
            timeJitterAmount = 0.3
            for i in range(count):
                timeJitter = (random() - 0.5) * timeJitterAmount
                newEvents.append(Event(
                    type=EVENT_TYPES.PROG_FLASH,
                    atTime=event.atTime + i * every + timeJitter,
                    params={
                        "centre": getRandomPointInSpace(),
                        "colour": (255, 255, 255),
                        "radius": 30,
                        "life": 0.5,
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
        
        
        else:
            # Add event as is
            newEvents.append(event)
    
    return newEvents
