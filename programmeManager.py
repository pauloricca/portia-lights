import time
import traceback
from animator import Animator
from constants import *
from events import EVENT_TYPES, Event, EventManager
from programmes.axisColourNoiseProgramme import AxisColourNoiseProgramme
from programmes.gradientProgramme import GradientProgramme
from programmes.noiseBandsProgramme import NoiseBandsProgramme
from programmes.rotatingOrbProgramme import RotatingOrbProgramme
from programmes.scanLineProgramme import ScanLineProgramme
from programmes.spheresProgramme import SpheresProgramme
from utils import getBlankLEDsBuffer, getCentrePointInSpace, getRandomPointInSpace, mapToRange
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
    # Backgrounds
    fullColourNoise: ColourNoiseProgramme
    noiseBands: NoiseBandsProgramme
    solidColour: SolidColourProgramme
    hueGradient: GradientProgramme
    rgbGradient: GradientProgramme
    # Effects
    colourSparks: SparksProgramme
    flashes: SpheresProgramme
    rain: SpheresProgramme
    inverseColourSparks: SparksProgramme
    axisNoise: AxisColourNoiseProgramme
    leftNearOrb: RotatingOrbProgramme
    leftFarOrb: RotatingOrbProgramme
    rightNearOrb: RotatingOrbProgramme
    rightFarOrb: RotatingOrbProgramme
    whistleGhost: RotatingOrbProgramme
    scanLines: ScanLineProgramme

    def __init__(self, ledCount: int, isMaster: bool):
        self.animator = Animator()
        self.isMaster = isMaster

        # Backgrounds
        self.fullColourNoise = ColourNoiseProgramme(ledCount, hueScale=0.002, hueSpeed=0.02, brightnessScale=0.01, shimmerAmount=1)
        self.noiseBands = NoiseBandsProgramme(ledCount, shimmerAmount=1)
        self.solidColour = SolidColourProgramme(ledCount)
        self.hueGradient = GradientProgramme(ledCount, hue=0.5, hueBottom=0.5, interpolateByHue=True)
        self.rgbGradient = GradientProgramme(ledCount, hue=0.5, hueBottom=0.5)
        # Effects
        self.colourSparks = SparksProgramme(ledCount, brightness=1)
        self.inverseColourSparks = SparksProgramme(ledCount, propagationSpeed=-150)
        self.flashes = SpheresProgramme(ledCount, shimmerAmount=1, brightness=1)
        self.axisNoise = AxisColourNoiseProgramme(ledCount, hueScale=0.2, hueSpeed=.01, brightnessSpeed=0.3, brightnessScale=.01)
        self.leftNearOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 25), pathRadius=65, hue=0.1, speed=1)
        self.leftFarOrb = RotatingOrbProgramme(ledCount, centre=(-100, 0, 0), pathRadius=30, hue=0.6, speed=-2)
        self.rightNearOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 25), pathRadius=65, hue=0.1, speed=-1)
        self.rightFarOrb = RotatingOrbProgramme(ledCount, centre=(100, 0, 0), pathRadius=30, hue=0.6, speed=2)
        self.whistleGhost = RotatingOrbProgramme(ledCount, centre=getCentrePointInSpace(), pathRadius=10, orbRadius=30, hue=0.5, saturation=1, speed=4, shimmerAmount=1)
        self.scanLines = ScanLineProgramme(ledCount, shimmerAmount=1, brightness=1)
        self.rain = SpheresProgramme(ledCount, shimmerAmount=0.5)

        self.backgroundProgrammes = [
            self.fullColourNoise,
            self.noiseBands,
            self.solidColour,
            self.hueGradient,
            self.rgbGradient,
        ]

        self.programmes = [
            *self.backgroundProgrammes,
            # Other Effects
            self.colourSparks,
            self.inverseColourSparks,
            self.flashes,
            self.axisNoise,
            self.leftNearOrb,
            self.leftFarOrb,
            self.rightNearOrb,
            self.rightFarOrb,
            self.whistleGhost,
            self.scanLines,
            self.rain,
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

        # Process programme events
        for event in events:
            print('Will process programme event: ' + event.type + ' at ' + str(event.atTime))

            try:

                if event.type == EVENT_TYPES.PROG_QUIET_CLOUDS:
                    self.animator.createAnimation(self.fullColourNoise, "brightness", 0.3, 1)
                    self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 0.3, 1)
                    for programme in self.getBackgroundProgrammesOtherThan(self.fullColourNoise):
                        self.animator.createAnimation(programme, "brightness", 0, 1)
                
                elif event.type == EVENT_TYPES.PROG_HUE_BREATHING:
                    self.generateBreathing(
                        attributes=["hue"],
                        start=event.atTime,
                        length=event.params["length"],
                        count=event.params["count"] if "count" in event.params else 1,
                        every=event.params["every"] if event.params["count"] > 1 else 0,
                        factor=event.params["factor"],
                        attack=0.5,
                        release=1,
                    )
                
                elif event.type == EVENT_TYPES.PROG_BREATHING:
                    self.generateBreathing(
                        attributes=["brightness"],
                        start=event.atTime,
                        length=event.params["length"],
                        count=event.params["count"] if "count" in event.params else 1,
                        every=event.params["every"] if event.params["count"] > 1 else 0,
                        factor=event.params["factor"],
                        attack=0.5,
                        release=1,
                    )
                
                elif event.type == EVENT_TYPES.PROG_SPEED_BREATHING:
                    self.generateBreathing(
                        attributes=["brightnessSpeed", "hueSpeed", "speed"],
                        start=event.atTime,
                        length=event.params["length"],
                        count=event.params["count"] if "count" in event.params else 1,
                        every=event.params["every"] if event.params["count"] > 1 else 0,
                        factor=event.params["factor"],
                        attack=0.5,
                        release=1,
                    )

                elif event.type == EVENT_TYPES.PROG_RUMBLE:
                    self.animator.createAnimation(self.fullColourNoise, "brightness", 1.5, 0.2)
                    self.animator.createAnimation(self.fullColourNoise, "shimmerAmount", 1, 1)
                    for programme in self.getBackgroundProgrammesOtherThan(self.fullColourNoise):
                        self.animator.createAnimation(programme, "brightness", 0, 1)
                
                elif event.type == EVENT_TYPES.PROG_SPEED_CHANGE:
                    targetSpeed = self.fullColourNoise.brightnessSpeed * event.params["factor"]
                    self.animator.createAnimation(self.fullColourNoise, "brightnessSpeed", targetSpeed, event.params["ramp"])
                
                elif event.type == EVENT_TYPES.PROG_SCALE_CHANGE:
                    targetBrightnessScale = self.fullColourNoise.brightnessScale * event.params["factor"]
                    self.animator.createAnimation(self.fullColourNoise, "brightnessScale", targetBrightnessScale, event.params["ramp"])
                    targetHueScale = self.fullColourNoise.hueScale * event.params["factor"]
                    self.animator.createAnimation(self.fullColourNoise, "hueScale", targetHueScale, event.params["ramp"])
                
                elif event.type == EVENT_TYPES.PROG_RAIN:
                    duration = event.params["duration"]
                    attack = event.params["attack"]
                    release = event.params["release"]
                    self.rain.brightness = 0
                    self.rain.startRain(duration)
                    self.animator.createAnimation(self.rain, "brightness", 1, attack)
                    self.animator.createAnimation(self.rain, "brightness", 0, release, event.atTime+duration-release, 1)
                
                elif event.type == EVENT_TYPES.PROG_NEAR_ORBS or event.type == EVENT_TYPES.PROG_FAR_ORBS:
                    programmes = [self.leftFarOrb, self.rightFarOrb] if event.type == EVENT_TYPES.PROG_FAR_ORBS else [self.leftNearOrb, self.rightNearOrb]
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    for programme in programmes:
                        if "hue" in event.params:
                            self.animator.createAnimation(programme, "hue", event.params["hue"], ramp)
                        if "brightness" in event.params:
                            self.animator.createAnimation(programme, "brightness", event.params["brightness"], ramp)
                        if "saturation" in event.params:
                            self.animator.createAnimation(programme, "saturation", event.params["saturation"], ramp)

                elif event.type ==EVENT_TYPES.PROG_HIDE_ORBS:
                    programmes = [self.leftFarOrb, self.rightFarOrb, self.leftNearOrb, self.rightNearOrb]
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    for programme in programmes:
                        self.animator.createAnimation(programme, "brightness", 0, ramp)

                elif event.type == EVENT_TYPES.PROG_BACKGROUND_COLOUR:
                    activeProgrammes = self.getActiveBackgroundProgrammes()
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    for programme in self.backgroundProgrammes:
                        if "hue" in event.params:
                            self.animator.createAnimation(programme, "hue", event.params["hue"], ramp)
                        # Only change brightness on active programmes, otherwise all of them would be visible
                        if "brightness" in event.params and programme in activeProgrammes:
                            self.animator.createAnimation(programme, "brightness", event.params["brightness"], ramp)
                        if "saturation" in event.params:
                            self.animator.createAnimation(programme, "saturation", event.params["saturation"], ramp)

                elif event.type == EVENT_TYPES.PROG_HUE_GRADIENT:
                    otherBackgrounds = self.getBackgroundProgrammesOtherThan(self.hueGradient)
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    for programme in otherBackgrounds:
                        self.animator.createAnimation(programme, "brightness", 0, ramp)
                    for attr in ["hue", "brightness", "saturation", "hueBottom", "saturationBottom"]:
                        self.animator.createAnimation(self.hueGradient, attr, event.params[attr], ramp)
                
                elif event.type == EVENT_TYPES.PROG_RGB_GRADIENT:
                    otherBackgrounds = self.getBackgroundProgrammesOtherThan(self.rgbGradient)
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    for programme in otherBackgrounds:
                        self.animator.createAnimation(programme, "brightness", 0, ramp)
                    for attr in ["hue", "brightness", "saturation", "hueBottom", "saturationBottom"]:
                        self.animator.createAnimation(self.rgbGradient, attr, event.params[attr], ramp)

                elif event.type == EVENT_TYPES.PROG_WHISTLE_GHOST_BRIGHTNESS:
                    brightness = event.params["brightness"]
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    self.animator.createAnimation(self.whistleGhost, "brightness", brightness, ramp)

                elif event.type == EVENT_TYPES.PROG_WHISTLE_GHOST_POSITION:
                    randomPoint = getRandomPointInSpace()
                    newPosition = (
                        randomPoint[0],
                        mapToRange(event.params["position"], EVENTS_BOUNDING_BOX[1][0], EVENTS_BOUNDING_BOX[1][1]),
                        20,
                    )
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    self.animator.createAnimation(self.whistleGhost, "centre", newPosition, ramp)

                elif event.type == EVENT_TYPES.PROG_NOISE_THRESHOLD:
                    ramp = event.params["ramp"] if "ramp" in event.params else 0
                    attributes = ["brightness", "hue", "saturation", "hueSecond", "saturationSecond"]
                    for attr in [attr for attr in attributes if attr in event.params]:
                        self.animator.createAnimation(self.noiseBands, attr, event.params[attr], ramp)
                    if "min1" in event.params and "max1" in event.params:
                        self.animator.createAnimation(self.noiseBands, "firstBand", (event.params["min1"], event.params["max1"]), ramp)
                    if "min2" in event.params and "max2" in event.params:
                        self.animator.createAnimation(self.noiseBands, "secondBand", (event.params["min2"], event.params["max2"]), ramp)




                elif event.type == EVENT_TYPES.PHASES_SYNC and not self.isMaster:
                    self.fullColourNoise.huePhase = event.params['fullColourNoise.huePhase']
                    self.fullColourNoise.brightnessPhase = event.params['fullColourNoise.brightnessPhase']
                    self.axisNoise.phaseHue = event.params['axisNoise.phaseHue']
                    self.axisNoise.phaseBrightness = event.params['axisNoise.phaseBrightness']
                    self.leftNearOrb.pathRadius = event.params['leftNearOrb.pathRadius']
                    self.leftFarOrb.pathRadius = event.params['leftFarOrb.pathRadius']
                    self.rightNearOrb.pathRadius = event.params['rightNearOrb.pathRadius']
                    self.rightFarOrb.pathRadius = event.params['rightFarOrb.pathRadius']
                    self.noiseBands.phase = event.params['noiseBands.phase']

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
                            'leftNearOrb.pathRadius': self.leftNearOrb.pathRadius,
                            'leftFarOrb.pathRadius': self.leftFarOrb.pathRadius,
                            'rightNearOrb.pathRadius': self.rightNearOrb.pathRadius,
                            'rightFarOrb.pathRadius': self.rightFarOrb.pathRadius,
                            'noiseBands.phase': self.noiseBands.phase,
                        },
                    )])
        except:
            print("Error Processing Post-Programme Events.")
            traceback.print_exc()

        return leds

    def generateBreathing(
            self,
            start: float,
            length: float,
            count: float,
            every: float,
            factor: float,
            attack: float,
            release: float,
            attributes: list[str],
            onlyActiveProgrammes=True
            ):
        programmes = self.getActiveBackgroundProgrammes() if onlyActiveProgrammes else self.backgroundProgrammes
        for i in range(int(count)):
            attackStart = start + i * every
            releaseStart = attackStart + length - release
            for programme in programmes:
                for attr in [attr for attr in attributes if hasattr(programme, attr)]:
                    currentValue = getattr(programme, attr)
                    targetValue = currentValue * factor
                    # Paulo
                    if programme == self.noiseBands:
                        print(('BREATH', currentValue, targetValue, factor))
                    self.animator.createAnimation(programme, attr, targetValue, attack, attackStart, currentValue)
                    self.animator.createAnimation(programme, attr, currentValue, release, releaseStart, targetValue)

    
    def getBackgroundProgrammesOtherThan(self, programme: Programme):
        return [otherProgramme for otherProgramme in self.backgroundProgrammes if otherProgramme != programme]

    def getActiveBackgroundProgrammes(self):
        return [programme for programme in self.backgroundProgrammes if programme.brightness > 0]