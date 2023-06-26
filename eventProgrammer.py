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
                atTime=event.atTime + 15,
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
            intensity = event.params["intensity"] if "intensity" in event.params else 1
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
            sparkColour = getRandomColour(intensity)
            sparkDelayTime = .3
            sparkDelayCount = 6
            sparkDelayFalloff = .3
            for i in range(sparkDelayCount):
                newEvents.append(Event(
                    type=EVENT_TYPES.PROG_SPARK,
                    atTime=event.atTime + i * sparkDelayTime,
                    params={
                        "centre": sparkCentre,
                        "colour": sparkColour,
                    }
                ))
                sparkColour = [c * sparkDelayFalloff for c in sparkColour]
        
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
        
        elif event.type == EVENT_TYPES.SUNSET:
            brightness = 0.2
            intervalBetweenStages = 22
            stage = 0
            # clouds
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_QUIET_CLOUDS,
                atTime=event.atTime,
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_BACKGROUND_COLOUR,
                atTime=event.atTime,
                params={
                    "saturation": 0,
                    "brightness": 1,
                    "ramp": 2,
                }
            ))
            # blue - blue
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": 0.6,
                    "brightness": brightness,
                    "saturation": 0.8,
                    "hueBottom": 0.5,
                    "saturationBottom": 0.3,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # desaturated green - desaturated yellow
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": 0.6,
                    "brightness": brightness,
                    "saturation": 0.3,
                    "hueBottom": 0.15,
                    "saturationBottom": 0.8,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # grey - desaturated yellow
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": 0.3,
                    "brightness": brightness,
                    "saturation": 0,
                    "hueBottom": 0.15,
                    "saturationBottom": 0.8,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # red - yellow 
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": 0.02,
                    "brightness": brightness,
                    "saturation": 1,
                    "hueBottom": 0.12,
                    "saturationBottom": 1,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # purple - desaturated orange
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": -0.3,
                    "brightness": brightness,
                    "saturation": 1,
                    "hueBottom": 0.1,
                    "saturationBottom": 0.5,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # dark blue - desaturated blue
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": -0.4,
                    "brightness": brightness / 4,
                    "saturation": 0.4,
                    "hueBottom": 0.5,
                    "saturationBottom": 0.3,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # black - black
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": -0.3,
                    "brightness": 0,
                    "saturation": 0.1,
                    "hueBottom": 0.6,
                    "saturationBottom": 0.2,
                    "ramp": intervalBetweenStages,
                }
            ))
            stage += 1
            # reset gradient
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_RGB_GRADIENT,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "hue": 0.5,
                    "brightness": 0,
                    "saturation": 1,
                    "hueBottom": 0.5,
                    "saturationBottom": 1,
                }
            ))
        
        elif event.type == EVENT_TYPES.WHISTLE:
            anticipationTime = 0.5 # time the ghost starts moving before the note
            # (timestamp, height (0 is bottom, 1 is top))
            positions = [
                (424.5, 0.8),
                (432.2, 0.5),
                (439.0, 0.2),
                (451.9, 0.8),
                (454.5, 0.5),
                (460.2, 0.2),
                (466.2, 0.5),
                (471.5, 0.5),
                (475.7, 0.2),
                (480.0, 0.5),
                (484.5, 0.2),
                (488.7, 0.5),
                (493.1, 0.2),
                (497.5, 0.5),
                (502.0, 0.2),
                (506.2, 0.5),
                (511.1, 0.2),
                (514.9, 0.5),
                (519.3, 0.2),
                (522.6, -2),
            ]
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_WHISTLE_GHOST_BRIGHTNESS,
                atTime=event.atTime - 1,
                params={
                    "brightness": 1,
                    "ramp": 2,
                }
            ))
            for (timestamp, position) in positions:
                stepTime = event.atTime + timestamp - positions[0][0] - anticipationTime
                newEvents.append(Event(
                    type=EVENT_TYPES.PROG_WHISTLE_GHOST_POSITION,
                    atTime=stepTime,
                    params={
                        "position": position,
                        "ramp": 0.6,
                    }
                ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_WHISTLE_GHOST_BRIGHTNESS,
                atTime=event.atTime + positions[-1][0] - positions[0][0],
                params={
                    "brightness": 0,
                    "ramp": 2,
                }
            ))
        
        elif event.type == EVENT_TYPES.FIRST_BASS_LINE:
            # (timestamp, brightness, (hue,saturation)-top, (hue,saturation)-bottom)
            steps = [
                (523.6, 1, (0,1), (0.5,1)),
                (527.9, 1, (0.5,1), (0.8,1)),
                (531.5, 1, (0.8,1), (0.4,1)),
                (532.3, 1, (0.4,1), (0.6,1)),
                (536.6, 1, (0.6,1), (0.2,1)),
                (538.8, 1, (0,2), (0.5,1)),
                (541.0, 1, (0.5,1), (0.8,1)),
                (544.0, 1, (0.8,1), (0.4,1)),
            ]
            ramp = 0.3
            anticipationTime = 0
            for (timestamp, brightness, (hue, saturation), (hueBottom, saturationBottom)) in steps:
                stepTime = event.atTime + timestamp - steps[0][0] - anticipationTime
                newEvents.append(Event(
                    type=EVENT_TYPES.PROG_HUE_GRADIENT,
                    atTime=stepTime,
                    params={
                        "brightness": brightness,
                        "hue": hue,
                        "saturation": saturation,
                        "hueBottom": hueBottom,
                        "saturationBottom": saturationBottom,
                        "ramp": ramp,
                    }
                ))

        elif event.type == EVENT_TYPES.PIANO:
            # max brightness with 0 band width (all dark)
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime,
                params={
                    "brightness": 1,
                    "hue": .6,
                    "saturation": .8,
                    "hueSecond": .7,
                    "saturationSecond": .8,
                    "min1": .3,
                    "max1": .3,
                    "min2": .7,
                    "max2": .7,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 1,
                params={
                    "min1": .4,
                    "max1": .5,
                    "min2": .7,
                    "max2": .8,
                    "ramp": 5,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 2,
                params={
                    "hue": 0,
                    "hueSecond": .2,
                    "ramp": 15,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SPEED_BREATHING,
                atTime=event.atTime + 1,
                params={
                    "factor": -20,
                    "every": 4,
                    "count": 30,
                    "length": .5,
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
