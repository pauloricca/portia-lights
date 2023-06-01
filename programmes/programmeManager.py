from constants import *
from events import EVENT_TYPES, Event
from utils import getBlankLEDsBuffer, getRandomColour, getRandomPointInSpace
from programmes.programme import Programme
from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme

# Schedules changes in the programmes in response to events
class ProgrammeManager():
    programmes: list[Programme]

    def __init__(self):
        self.programmes = [
            SparksProgramme(),
            ColourNoiseProgramme(),
            ColourNoiseProgramme(saturation=0.35, hueNoiseScale=.05, speed=.1, brightnessNoiseScale=.4),
            ColourNoiseProgramme(saturation=0, hueNoiseScale=.05, speed=10, brightnessNoiseScale=.4, brightness=0.004),
        ]
    
    def renderProgrammes(self, events: list[Event], ledCoords: list[tuple[float, float, float]], frameTime: float):
        # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
        leds: list[list] = getBlankLEDsBuffer()

        # Run programme cycles and add their output to the main render buffer
        for programme in self.programmes:
            programme.step(ledCoords, frameTime, events)
            if programme.brightness > 0:
                for i, led in enumerate(leds):
                    led[0] += programme.leds[i][0]
                    led[1] += programme.leds[i][1]
                    led[2] += programme.leds[i][2]
        
        return leds
