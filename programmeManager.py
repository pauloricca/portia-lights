import time
from animator import Animator
from constants import *
from events import EVENT_TYPES, Event, EventManager
from programmes.axisColourNoiseProgramme import AxisColourNoiseProgramme
from programmes.noiseThresholdProgramme import NoiseThresholdProgramme
from programmes.rotatingOrbProgramme import RotatingOrbProgramme
from programmes.scanLineProgramme import ScanLineProgramme
from programmes.spheresProgramme import SpheresProgramme
from utils import getBlankLEDsBuffer, mapToRange
from programmes.programme import Programme
from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme
from programmes.solidColourProgramme import SolidColourProgramme

# Schedules changes in the programmes in response to events
class ProgrammeManager():
    animator: Animator
    programmes: list[Programme]
    isMaster: bool

    colourSparks: SparksProgramme
    flashes: SpheresProgramme
    inverseColourSparks: SparksProgramme
    fullColourNoise: ColourNoiseProgramme
    axisNoise: AxisColourNoiseProgramme
    leftFrontOrb: RotatingOrbProgramme
    leftBackOrb: RotatingOrbProgramme
    rightFrontOrb: RotatingOrbProgramme
    rightBackOrb: RotatingOrbProgramme
    solidColour: SolidColourProgramme
    firstNoiseThreshold: NoiseThresholdProgramme
    secondNoiseThreshold: NoiseThresholdProgramme
    scanLines: ScanLineProgramme

    def __init__(self, ledCount: int, isMaster: bool):
        self.animator = Animator()
        self.isMaster = isMaster

        self.colourSparks = SparksProgramme(ledCount)
        self.flashes = SpheresProgramme(ledCount, shimmerAmount=1)
        self.inverseColourSparks = SparksProgramme(ledCount, propagationSpeed=-150)
        self.fullColourNoise = ColourNoiseProgramme(ledCount, hueScale=0.0002, hueSpeed=0.02, brightnessScale=0.01, shimmerAmount=1)
        self.axisNoise = AxisColourNoiseProgramme(ledCount, hueScale=0.2, hueSpeed=.01, brightnessSpeed=0.3, brightnessScale=.01)
        self.solidColour = SolidColourProgramme(ledCount)
        self.leftFrontOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 25), pathRadius=65, hue=0.1, speed=1)
        self.leftBackOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 0), pathRadius=30, hue=0.6, speed=-2)
        self.rightFrontOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 25), pathRadius=65, hue=0.1, speed=-1)
        self.rightBackOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 0), pathRadius=30, hue=0.6, speed=2)
        self.firstNoiseThreshold = NoiseThresholdProgramme(ledCount, hue=1, shimmerAmount=0.5)
        self.secondNoiseThreshold = NoiseThresholdProgramme(ledCount, hue=0.6, phase=30, shimmerAmount=0.5)
        self.scanLines = ScanLineProgramme(ledCount, shimmerAmount=1.5)

        self.programmes = [
            # Background
            self.fullColourNoise,
            self.firstNoiseThreshold,
            self.secondNoiseThreshold,
            self.solidColour,
            # Effects
            self.colourSparks,
            self.inverseColourSparks,
            self.flashes,
            self.axisNoise,
            self.leftFrontOrb,
            self.leftBackOrb,
            self.rightFrontOrb,
            self.rightBackOrb,
            self.scanLines,
        ]
    
    def renderProgrammes(
            self,
            events: list[Event],
            ledCoords: list[tuple[float, float, float]],
            frameTime: float,
            eventManager: EventManager,
        ):
        # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
        leds: list[list] = getBlankLEDsBuffer(len(ledCoords))

        # Pre-Programme Events
        for event in events:

            if event.type == EVENT_TYPES.PROG_QUIET_CLOUDS:
                self.animator.createAnimation(self.fullColourNoise, "brightness", 0.3, 1)
                self.animator.createAnimation(self.fullColourNoise, "hueCentre", 0.3, 1)
                self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 0.3, 1)
                self.animator.createAnimation(self.solidColour, "brightness", 0, 1)
                self.animator.createAnimation(self.firstNoiseThreshold, "brightness", 0, 1)
                self.animator.createAnimation(self.secondNoiseThreshold, "brightness", 0, 1)
            
            if event.type == EVENT_TYPES.PROG_RUMBLE:
                self.animator.createAnimation(self.fullColourNoise, "brightness", 1.5, 0.2)
                self.animator.createAnimation(self.fullColourNoise, "hueCentre", 0.15, 1)
                self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 1, 1)
                self.animator.createAnimation(self.solidColour, "brightness", 0, 1)
                self.animator.createAnimation(self.firstNoiseThreshold, "brightness", 0, 1)
                self.animator.createAnimation(self.secondNoiseThreshold, "brightness", 0, 1)

            if event.type == EVENT_TYPES.GRITTINESS:
                level = event.params["level"]
                # self.animator.createAnimation(self.fullColourNoise, "brightness", mapToRange(level, 0.15, 0.05), 1)
                self.animator.createAnimation(self.edgeBlink, "brightness", mapToRange(level, 0.004, 0.05), 1)
            
            if event.type == EVENT_TYPES.BACKGROUND_COLOUR:
                brightness = event.params["brightness"]
                transition = event.params["transition"]
                if "colour" in event.params:
                    self.animator.createAnimation(self.solidColour, "colour", event.params["colour"], transition)
                self.animator.createAnimation(self.solidColour, "brightness", brightness, transition)
            
            if event.type == EVENT_TYPES.PHASES_SYNC and not self.isMaster:
                self.fullColourNoise.huePhase = event.params['fullColourNoise.huePhase']
                self.fullColourNoise.brightnessPhase = event.params['fullColourNoise.brightnessPhase']
                self.axisNoise.phaseHue = event.params['axisNoise.phaseHue']
                self.axisNoise.phaseBrightness = event.params['axisNoise.phaseBrightness']
                self.leftFrontOrb.pathRadius = event.params['leftFrontOrb.pathRadius']
                self.leftBackOrb.pathRadius = event.params['leftBackOrb.pathRadius']
                self.rightFrontOrb.pathRadius = event.params['rightFrontOrb.pathRadius']
                self.rightBackOrb.pathRadius = event.params['rightBackOrb.pathRadius']
                self.firstNoiseThreshold.phase = event.params['firstNoiseThreshold.phase']
                self.secondNoiseThreshold.phase = event.params['secondNoiseThreshold.phase']

        
        self.animator.animate()

        # Run programme cycles and add their output to the main render buffer
        for programme in self.programmes:
            programme.step(ledCoords, frameTime, events)
            if programme.brightness > 0:
                for i, led in enumerate(leds):
                    led[0] += programme.leds[i][0]
                    led[1] += programme.leds[i][1]
                    led[2] += programme.leds[i][2]
        
        # Post-programme Events
        for event in events:

            if event.type == EVENT_TYPES.SYNC_PHASES and self.isMaster:
                eventManager.pushEvents([Event(
                    type=EVENT_TYPES.PHASES_SYNC,
                    atTime=time.time(),
                    params={
                        'fullColourNoise.huePhase': self.fullColourNoise.huePhase,
                        'fullColourNoise.brightnessPhase': self.fullColourNoise.brightnessPhase,
                        'axisNoise.phaseHue': self.axisNoise.phaseHue,
                        'axisNoise.phaseBrightness': self.axisNoise.phaseBrightness,
                        'leftFrontOrb.pathRadius': self.leftFrontOrb.pathRadius,
                        'leftBackOrb.pathRadius': self.leftBackOrb.pathRadius,
                        'rightFrontOrb.pathRadius': self.rightFrontOrb.pathRadius,
                        'rightBackOrb.pathRadius': self.rightBackOrb.pathRadius,
                        'firstNoiseThreshold.phase': self.firstNoiseThreshold.phase,
                        'secondNoiseThreshold.phase': self.secondNoiseThreshold.phase,
                    },
                )])
        
        return leds
