from animator import Animator
from constants import *
from events import EVENT_TYPES, Event
from programmes.axisColourNoiseProgramme import AxisColourNoiseProgramme
from programmes.rotatingOrbProgramme import RotatingOrbProgramme
from utils import getBlankLEDsBuffer, mapToRange
from programmes.programme import Programme
from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme
from programmes.solidColourProgramme import SolidColourProgramme

# Schedules changes in the programmes in response to events
class ProgrammeManager():
    animator: Animator
    programmes: list[Programme]
    colourSparks: SparksProgramme
    fullColourNoise: ColourNoiseProgramme
    paleNoise: ColourNoiseProgramme
    edgeBlink: ColourNoiseProgramme
    axisNoise: AxisColourNoiseProgramme
    orb: RotatingOrbProgramme
    solidColour: SolidColourProgramme

    def __init__(self):
        self.animator = Animator()

        self.colourSparks = SparksProgramme()
        self.fullColourNoise = ColourNoiseProgramme(hueNoiseScale=0.0001, speed=0.03)
        self.paleNoise = ColourNoiseProgramme(saturation=0.35, hueNoiseScale=.05, speed=.1, brightnessNoiseScale=.4, brightness=0.01)
        self.edgeBlink = ColourNoiseProgramme(saturation=0.2, hueNoiseScale=.05, speed=10, brightnessNoiseScale=.4, brightness=0.01)
        self.axisNoise = AxisColourNoiseProgramme(hueNoiseScale=0.2, speedHue=.01, speedBrightness=0.3, brightnessNoiseScale=.01)
        self.solidColour = SolidColourProgramme()

        self.programmes = [
            self.colourSparks,
            # self.fullColourNoise,
            # self.paleNoise,
            # self.edgeBlink,
            # self.solidColour,
            # self.axisNoise,
            self.orb
        ]
    
    def renderProgrammes(self, events: list[Event], ledCoords: list[tuple[float, float, float]], frameTime: float):
        # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
        leds: list[list] = getBlankLEDsBuffer()

        for event in events:

            if event.type == EVENT_TYPES.GRITTINESS:
                level = event.params["level"]
                self.animator.createAnimation(self.fullColourNoise, "brightness", mapToRange(level, 0.15, 0.05), 1)
                self.animator.createAnimation(self.edgeBlink, "brightness", mapToRange(level, 0.004, 0.05), 1)
            
            if event.type == EVENT_TYPES.BACKGROUND_COLOUR:
                brightness = event.params["brightness"]
                transition = event.params["transition"]
                if "colour" in event.params:
                    self.solidColour.colour = event.params["colour"]
                self.animator.createAnimation(self.solidColour, "brightness", brightness, transition)
        
        self.animator.animate(frameTime)

        # Run programme cycles and add their output to the main render buffer
        for programme in self.programmes:
            programme.step(ledCoords, frameTime, events)
            if programme.brightness > 0:
                for i, led in enumerate(leds):
                    led[0] += programme.leds[i][0]
                    led[1] += programme.leds[i][1]
                    led[2] += programme.leds[i][2]
        
        return leds
