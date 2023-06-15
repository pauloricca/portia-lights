from animator import Animator
from constants import *
from events import EVENT_TYPES, Event
from programmes.axisColourNoiseProgramme import AxisColourNoiseProgramme
from programmes.noiseThresholdProgramme import NoiseThresholdProgramme
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
    inverseColourSparks: SparksProgramme
    fullColourNoise: ColourNoiseProgramme
    paleNoise: ColourNoiseProgramme
    edgeBlink: ColourNoiseProgramme
    axisNoise: AxisColourNoiseProgramme
    leftFrontOrb: RotatingOrbProgramme
    leftBackOrb: RotatingOrbProgramme
    rightFrontOrb: RotatingOrbProgramme
    rightBackOrb: RotatingOrbProgramme
    solidColour: SolidColourProgramme
    redNoiseThreshold: NoiseThresholdProgramme
    blueNoiseThreshold: NoiseThresholdProgramme

    def __init__(self):
        self.animator = Animator()

        self.colourSparks = SparksProgramme()
        self.inverseColourSparks = SparksProgramme(propagationSpeed=-150)
        self.fullColourNoise = ColourNoiseProgramme(hueScale=0.0002, hueSpeed=0.02, brightnessScale=0.01, brightness=4)
        self.paleNoise = ColourNoiseProgramme(saturation=0.35, hueScale=.05, hueSpeed=.1, brightnessScale=.4, brightness=0.01)
        self.edgeBlink = ColourNoiseProgramme(saturation=0.2, hueScale=.05, hueSpeed=10, brightnessScale=.4, brightness=0.01)
        self.axisNoise = AxisColourNoiseProgramme(hueScale=0.2, hueSpeed=.01, brightnessSpeed=0.3, brightnessScale=.01, brightness=0.1)
        self.solidColour = SolidColourProgramme()
        self.leftFrontOrb = RotatingOrbProgramme(centre=(-100, 0, 25), pathRadius=65, hue=0.1, speed=1)
        self.leftBackOrb = RotatingOrbProgramme(centre=(-100, 0, 0), pathRadius=30, hue=0.6, speed=-2)
        self.rightFrontOrb = RotatingOrbProgramme(centre=(100, 0, 25), pathRadius=65, hue=0.1, speed=-1)
        self.rightBackOrb = RotatingOrbProgramme(centre=(100, 0, 0), pathRadius=30, hue=0.6, speed=2)
        self.redNoiseThreshold = NoiseThresholdProgramme(hue=1)
        self.blueNoiseThreshold = NoiseThresholdProgramme(hue=0.7, phase=30)

        self.programmes = [
            self.colourSparks,
            # self.inverseColourSparks,
            # self.fullColourNoise,
            self.redNoiseThreshold,
            self.blueNoiseThreshold,
            # self.paleNoise,
            # self.edgeBlink,
            # self.solidColour,
            # self.axisNoise,
            # self.leftFrontOrb,
            # self.leftBackOrb,
            # self.rightFrontOrb,
            # self.rightBackOrb,
        ]
    
    def renderProgrammes(
            self,
            events: list[Event],
            ledCoords: list[tuple[float, float, float]],
            frameTime: float
        ):
        # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
        leds: list[list] = getBlankLEDsBuffer()

        for event in events:

            if event.type == EVENT_TYPES.GRITTINESS:
                level = event.params["level"]
                # self.animator.createAnimation(self.fullColourNoise, "brightness", mapToRange(level, 0.15, 0.05), 1)
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
