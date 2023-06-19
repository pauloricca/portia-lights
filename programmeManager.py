import time
import traceback
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
    backgroundProgrammes: list[Programme]
    isMaster: bool

    colourSparks: SparksProgramme
    flashes: SpheresProgramme
    rain: SpheresProgramme
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

        # Backgrounds
        self.fullColourNoise = ColourNoiseProgramme(ledCount, hueScale=0.0002, hueSpeed=0.02, brightnessScale=0.01, shimmerAmount=1)
        self.firstNoiseThreshold = NoiseThresholdProgramme(ledCount, hue=1, shimmerAmount=0.5)
        self.secondNoiseThreshold = NoiseThresholdProgramme(ledCount, hue=0.6, phase=30, shimmerAmount=0.5)
        self.solidColour = SolidColourProgramme(ledCount)
        # Effects
        self.colourSparks = SparksProgramme(ledCount)
        self.inverseColourSparks = SparksProgramme(ledCount, propagationSpeed=-150)
        self.flashes = SpheresProgramme(ledCount, shimmerAmount=1)
        self.axisNoise = AxisColourNoiseProgramme(ledCount, hueScale=0.2, hueSpeed=.01, brightnessSpeed=0.3, brightnessScale=.01)
        self.leftFrontOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 25), pathRadius=65, hue=0.1, speed=1)
        self.leftBackOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 0), pathRadius=30, hue=0.6, speed=-2)
        self.rightFrontOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 25), pathRadius=65, hue=0.1, speed=-1)
        self.rightBackOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 0), pathRadius=30, hue=0.6, speed=2)
        self.scanLines = ScanLineProgramme(ledCount, shimmerAmount=1.5)
        self.rain = SpheresProgramme(ledCount, shimmerAmount=0.5)

        self.backgroundProgrammes = [
            self.fullColourNoise,
            self.firstNoiseThreshold,
            self.secondNoiseThreshold,
            self.solidColour,
        ]

        self.programmes = [
            *self.backgroundProgrammes,
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
            self.rain,
        ]
    
    def getBackgroundProgrammesOtherThan(self, programme: Programme):
        return [otherProgramme for otherProgramme in self.backgroundProgrammes if otherProgramme != programme]

    def getActiveBackgroundProgrammes(self):
        return [programme for programme in self.backgroundProgrammes if programme.brightness > 0]
    
    def renderProgrammes(
            self,
            events: list[Event],
            ledCoords: list[tuple[float, float, float]],
            frameTime: float,
            eventManager: EventManager,
        ):
        # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
        leds: list[list] = getBlankLEDsBuffer(len(ledCoords))

        # Process programme events
        for event in events:
            print('Will process programme event: ' + event.type)

            try:

                if event.type == EVENT_TYPES.PROG_QUIET_CLOUDS:
                    self.animator.createAnimation(self.fullColourNoise, "brightness", 0.3, 1)
                    self.animator.createAnimation(self.fullColourNoise, "hueCentre", 0.6, 1)
                    self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 0.3, 1)
                    for programme in self.getBackgroundProgrammesOtherThan(self.fullColourNoise):
                        self.animator.createAnimation(programme, "brightness", 0, 1)
                
                if event.type == EVENT_TYPES.PROG_BREATHING:
                    breathingStart =  event.atTime
                    breathingEvery = event.params["every"]
                    breathingCount = event.params["count"]
                    breathLength = event.params["length"]
                    activeBackgroundProgrammes = self.getActiveBackgroundProgrammes()
                    for i in range(int(breathingCount)):
                        for programme in activeBackgroundProgrammes:
                            self.animator.createAnimation(programme, "brightness", 0.8, 0.5, breathingStart + i * breathingEvery, 0.3)
                            self.animator.createAnimation(programme, "brightness", 0.3, 1, breathLength + breathingStart + i * breathingEvery, 0.8)
                
                if event.type == EVENT_TYPES.PROG_RUMBLE:
                    self.animator.createAnimation(self.fullColourNoise, "brightness", 1.5, 0.2)
                    self.animator.createAnimation(self.fullColourNoise, "hueCentre", 0.15, 1)
                    self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 1, 1)
                    for programme in self.getBackgroundProgrammesOtherThan(self.fullColourNoise):
                        self.animator.createAnimation(programme, "brightness", 0, 1)
                
                if event.type == EVENT_TYPES.PROG_SPEED_CHANGE:
                    targetSpeed = self.fullColourNoise.brightnessSpeed * event.params["factor"]
                    self.animator.createAnimation(self.fullColourNoise, "brightnessSpeed", targetSpeed, event.params["duration"])
                
                if event.type == EVENT_TYPES.PROG_RAIN:
                    duration = event.params["duration"]
                    attack = event.params["attack"]
                    release = event.params["release"]
                    self.rain.brightness = 0
                    self.rain.startRain(duration)
                    self.animator.createAnimation(self.rain, "brightness", 1, attack)
                    self.animator.createAnimation(self.rain, "brightness", 0, release, event.atTime+duration-release, 1)

                if event.type == EVENT_TYPES.GRITTINESS:
                    level = event.params["level"]
                    # self.animator.createAnimation(self.fullColourNoise, "brightness", mapToRange(level, 0.15, 0.05), 1)
                    self.animator.createAnimation(self.edgeBlink, "brightness", mapToRange(level, 0.004, 0.05), 1)
                
                if event.type == EVENT_TYPES.PROG_BACKGROUND_COLOUR:
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

            except:
                print("Error Processing Programme Event " + event.type +".")
                traceback.print_exc()
            
        self.animator.animate()

        # Run programme cycles and add their output to the main render buffer
        for programme in self.programmes:
            try:
                programme.step(ledCoords, frameTime, events)
                if programme.brightness > 0:
                    for i, led in enumerate(leds):
                        led[0] += programme.leds[i][0]
                        led[1] += programme.leds[i][1]
                        led[2] += programme.leds[i][2]
            except:
                print("Error Rendering.")
                traceback.print_exc()
        
        try:
            # Raise phase sync event
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
        except:
            print("Error Processing Post-Programme Events.")
            traceback.print_exc()

        return leds
