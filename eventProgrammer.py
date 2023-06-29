from random import random
from events import EVENT_TYPES, Event
from utils import getRandomColour, getRandomPointInSpace

# Go through the basic sequence events and generate programme events
def eventProgrammer(events: list[Event]):
    newEvents: list[Event] = []

    for event in events:
        if event.type == EVENT_TYPES.FAR_RUMBLE:
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
                    "hue": 0.07,
                    "ramp": 4,
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
            sparkDelayTime = .4
            sparkDelayCount = 4
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
            brightness = 0.07
            intervalBetweenStages = 22
            stage = 0
            # clouds
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_QUIET_CLOUDS,
                atTime=event.atTime - 2,
                params={
                    "saturation": 0,
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
            # clouds disappear
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_QUIET_CLOUDS,
                atTime=event.atTime + stage * intervalBetweenStages,
                params={
                    "brightness": 0,
                    "ramp": 4,
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
            # If the second number becomes the first, gradient goes up (so should the note)
            steps = [
                (523.7, 1, (0,1), (0.3,1)),
                (527.9, .2, (-0.1,1), (0,1)),
                (531.5, 1, (0.2,1), (0.5,1)),
                (532.3, .5, (0,1), (0.3,1)),
                (536.7, .3, (-0.1,1), (0.1,1)),
                (538.9, .6, (0.2,1), (0.4,1)),
                (541.1, 1, (0.3,1), (0.5,1)),
                (544.1, 1, (0.5,1), (0.7,1)),
                (545.4, 0.2, (0,1), (0.5,1)),
                (549.9, 0.5, (0.4,1), (0.7,1)),
                (552.8, 1, (0.8,0.5), (1.2,0.7)),
                (554.2, 0.1, (0.3,1), (0.4,1)),
                (558.5, 0.5, (0.5,1), (0.7,1)),
                (562.9, 0.2, (0.2,1), (0.5,1)),
                (566.4, 0.4, (0.4,1), (0.6,1)),
                (567.4, 0.2, (0.2,1), (0.4,1)),
                (571.6, 0.2, (0,1), (0.2,1)),
                (573.9, 0.3, (0.2,1), (0.5,1)),
                (576.0, 0.5, (0.4,1), (0.7,1)),
                (579.2, 0.6, (0.6,1), (0.9,1)),
                (580.3, 0.2, (0.3,1), (0.5,1)),
                (584.7, 0.4, (0.5,1), (0.7,1)),
                (587.9, 0.8, (0.9,1), (1.2,1)),
                (589.1, 0.1, (0.4,1), (0.7,1)),
                (591.1, 0.08, (0.4,1), (0.3,1)),
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
                        "noiseAmount": 0,
                        "ramp": ramp,
                    }
                ))

        elif event.type == EVENT_TYPES.FIRST_SYNTH_BANDS:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime,
                params={
                    "brightness": 0.3,
                    "ratio": 0.3,
                    "ramp": 5,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime,
                params={
                    "speed": 300,
                    "ramp": 6,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 6,
                params={
                    "ratio": 0.6,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 10,
                params={
                    "speed": 3000,
                    "ramp": 6,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 12,
                params={
                    "ratio": 0.2,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 17,
                params={
                    "speed": 30,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 17,
                params={
                    "ratio": 0,
                    "width": 140,
                    "ramp": 10,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 28,
                params={
                    "ratio": 0.3,
                    "width": 70,
                    "ramp": 2,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 28,
                params={
                    "brightness": 0.05,
                    "ramp": 3,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 32,
                params={
                    "brightness": 0.4,
                    "ramp": 2,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 35.5,
                params={
                    "speed": 3000,
                    "ratio": 0,
                    "ramp": 1,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 35.5,
                params={
                    "brightness": 0,
                    "ramp": 1,
                }
            ))

        elif event.type == EVENT_TYPES.SECOND_BASS_LINE:
            # Reset gradient noise
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HUE_GRADIENT,
                atTime=event.atTime - 1,
                params={
                    "noiseAmount": 0,
                    "phase": 0,
                    "noiseScale": 0.001,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HUE_GRADIENT,
                atTime=event.atTime,
                params={
                    "noiseAmount": 100,
                    "ramp":5,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HUE_GRADIENT,
                atTime=event.atTime,
                params={
                    "noiseScale": 0.02,
                    "ramp": 20,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HUE_GRADIENT,
                atTime=event.atTime + 25,
                params={
                    "noiseScale": 0.001,
                    "ramp": 20,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HUE_GRADIENT,
                atTime=event.atTime + 40,
                params={
                    "noiseAmount": 0,
                    "ramp": 10,
                }
            ))
            # (timestamp, brightness, (hue,saturation)-top, (hue,saturation)-bottom)
            # If the second number becomes the first, gradient goes up (so should the note)
            steps = [
                (628.5, 1,  (0.6,1), (0.7,1)),
                (632.7, .8, (0.3,1), (0.5,1)),
                (636.2, 1,  (0.7,1), (0.8,1)),
                (637.0, 1,  (0.4,1), (0.6,1)),
                (641.4, 1,  (0.0,1), (0.2,1)),
                (643.7, .6, (0.2,1), (0.4,1)),
                (645.9, 1,  (0.5,1), (0.8,1)),
                (648.8, 1,  (0.8,1), (1.2,1)),
                (650.1, .4, (0.3,1), (0.5,1)),
                (645.5, .6, (0.5,1), (0.8,1)),
                (657.5, 1,  (0.9,1), (1.3,1)),
                (658.9, .4, (0.3,1), (0.5,1)),
                (663.4, .6, (0.5,1), (0.8,1)),
                (667.6, .3, (0.2,1), (0.3,1)),
                (671.2, .8, (0.7,1), (0.9,1)),
                (671.9, .6, (0.5,1), (0.8,1)),
                (676.4, .4, (0.2,1), (0.4,1)),
                (678.5, .6, (0.4,1), (0.7,1)),
                (680.7, .8, (0.7,1), (0.9,1)),
                (683.7, 1,  (1.0,1), (1.3,1)),
                (685.0, .2, (0.6,1), (0.8,1)),
                (689.4, .5, (0.8,1), (1.0,1)),
                (692.4, 1, (0.2,1), (1.3,1)),
                (693.8, .1, (0.6,1), (0.7,1)),
                (694.8, 0, (0.6,1), (0.7,1)),
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
                        "ramp": ramp if timestamp < 694 else 8,
                    }
                ))
        


        elif event.type == EVENT_TYPES.SECOND_SYNTH_BANDS:
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime,
                params={
                    "brightness": 0.3,
                    "ratio": 0.3,
                    "ramp": 5,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime,
                params={
                    "speed": 3,
                    "ramp": 6,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 6,
                params={
                    "ratio": 0.6,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 10,
                params={
                    "speed": 3,
                    "ramp": 6,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 12,
                params={
                    "ratio": 0.2,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 17,
                params={
                    "speed": 30,
                    "ramp": 4,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 17,
                params={
                    "ratio": 0,
                    "width": 140,
                    "ramp": 10,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 28,
                params={
                    "ratio": 0.3,
                    "width": 70,
                    "ramp": 2,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 28,
                params={
                    "brightness": 0.05,
                    "ramp": 3,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 32,
                params={
                    "brightness": 0.4,
                    "ramp": 2,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 35.5,
                params={
                    "speed": 3000,
                    "ratio": 0,
                    "ramp": 1,
                }
            ))
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_HORIZONTAL_BANDS,
                atTime=event.atTime + 35.5,
                params={
                    "brightness": 0,
                    "ramp": 1,
                }
            ))
        
        elif event.type == EVENT_TYPES.PIANO:
            lowSpeed = 0.03
            highSpeed = 0.3
            startTime = 740
            startPhase = 2
            # max brightness with 0 band width (all dark)
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime,
                params={
                    "brightness": 1,
                    "hue": 0.2,
                    "saturation": 0.8,
                    "hueSecond": 0.8,
                    "saturationSecond": 0.8,
                    "min1": .3,
                    "max1": .3,
                    "min2": .7,
                    "max2": .7,
                    "phase": startPhase,
                }
            ))
            # Appear
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 1.5,
                params={
                    "min1": .4,
                    "max1": .5,
                    "min2": .7,
                    "max2": .8,
                    "ramp": 1,
                }
            ))
            # Slowly change colour
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 5,
                params={
                    "hue": .6,
                    "saturation": .8,
                    "hueSecond": .7,
                    "saturationSecond": .8,
                    "ramp": 15,
                }
            ))
            # Slow down
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 4,
                params={
                    "speed": lowSpeed,
                    "ramp": 4,
                }
            ))

            # (timestamp, movement 0-1, duration)
            steps = [
                (751.8, 0.7, 2),
                (757.8, 0.7, 1),
                (765.3, 0.4, 1),
                (771.5, 1, 4),
                (782.7, 1.3, 2),
                (792.8, 0.7, 2),
                (800.5, 0.4, 1),
                (802.5, 1, 4),
                (811.7, 0.4, 1),
                (812.8, 1, 4),
                (820.8, 0.4, 1),
                (821.9, 0.7, 3),
                (829.8, 0.4, 1),
                (830.5, 1, 4),
                (838.0, 1, 0.6),
                (839.7, 0.6, 3),
                (848.7, 0.6, 3),
                (857.0, 0.3, 3),
                (875.4, 0.3, 1),
                (883.3, 0.5, 1),
                (894.0, 0.5, 1),
            ]
            anticipationTime = 0
            for (timestamp, movement, duration) in steps:
                stepTime = event.atTime + timestamp - startTime - anticipationTime
                newEvents.append(Event(
                    type=EVENT_TYPES.PROG_ACCELERATE,
                    atTime=stepTime,
                    params={
                        "high": lowSpeed + (highSpeed - lowSpeed) * movement,
                        "low": lowSpeed,
                        "duration": duration,
                        "attack": .3,
                        "release": duration / 2,
                    }
                ))
            # Disappear
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_NOISE_THRESHOLD,
                atTime=event.atTime + 894 - startTime,
                params={
                    "min1": .5,
                    "max1": .5,
                    "min2": .5,
                    "max2": .5,
                    "ramp": 8,
                }
            ))


        elif event.type == EVENT_TYPES.WAVE:
            intensity = event.params["intensity"] if "intensity" in event.params else 1
            newEvents.append(Event(
                type=EVENT_TYPES.PROG_SCAN_LINE,
                atTime=event.atTime,
                params={
                    "colour": getRandomColour(intensity),
                    "axis": 1,
                    "direction": -1,
                }
            ))
        
        
        else:
            # Add event as is
            newEvents.append(event)
    
    return newEvents
