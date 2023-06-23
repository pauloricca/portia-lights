from colorsys import hsv_to_rgb
from utils import clamp, getDistanceSquared, mapToRange
from math import sin, cos

from programmes.programme import Programme

class RotatingOrbProgramme(Programme):
    angle: float
    fadeByDistance: float
    speed: float
    orbRadius: float
    pathRadius: float
    centre: list[float, float, float]
    hue: float
    saturation: float

    def __init__(
        self,
        ledCount: int,
        speed=1,
        brightness=0,
        fadeByDistance=.002,
        orbRadius=15,
        pathRadius=65,
        centre=(20, 0, 0),
        hue=0.2,
        saturation=1,
        shimmerAmount=0,
    ):
        super().__init__(ledCount)
        self.speed = speed
        self.brightness = brightness
        self.fadeByDistance = fadeByDistance
        self.angle = 0
        self.orbRadius = orbRadius
        self.pathRadius = pathRadius
        self.centre = centre
        self.hue = hue
        self.saturation = saturation
        self.shimmerAmount = shimmerAmount
        self.shimmerScale = 0.2
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 4)

        self.angle += frameTime * self.speed

        orbX = self.centre[0] + self.pathRadius * sin(self.angle)
        orbY = self.centre[1] + self.pathRadius * cos(self.angle)
        orbZ = self.centre[2]

        radiusSquared = self.orbRadius**2

        orbColour = hsv_to_rgb(self.hue, self.saturation, 255)

        for i, led in enumerate(self.leds):
            distanceSquared = getDistanceSquared(ledCoords[i], (orbX, orbY, orbZ))
            if distanceSquared < radiusSquared:
                for i in range(0, 3):
                    led[i] = self.brightness * orbColour[i]
            else:
                radialBrightness = clamp(mapToRange(distanceSquared, 1, 0, radiusSquared, 2 * radiusSquared), 0, 1)
                for i in range(0, 3):
                    led[i] = clamp(led[i] + self.brightness * radialBrightness * orbColour[i], 0, 255)
        
        self.shimmer(frameTime)
                