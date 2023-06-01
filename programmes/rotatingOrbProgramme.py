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
    zPosition: float
    hue: float

    def __init__(
        self,
        speed=1,
        brightness=1,
        fadeByDistance=.01,
        orbRadius=15,
        pathRadius=65,
        zPosition=20,
        hue=0.2
    ):
        super().__init__()
        self.speed = speed
        self.brightness = brightness
        self.fadeByDistance = fadeByDistance
        self.angle = 0
        self.orbRadius = orbRadius
        self.pathRadius = pathRadius
        self.zPosition = zPosition
        self.hue = hue
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 4)

        self.angle += frameTime * self.speed

        orbX = self.pathRadius * sin(self.angle)
        orbY = self.pathRadius * cos(self.angle)

        radiusSquared = self.orbRadius * self.orbRadius

        orbColour = hsv_to_rgb(self.hue, 1, 255)

        for i, led in enumerate(self.leds):
            distanceSquared = getDistanceSquared(ledCoords[i], (orbX, orbY, self.zPosition))
            if distanceSquared < radiusSquared:
                for i in range(0, 3):
                    led[i] = self.brightness * orbColour[i]
            else:
                radialBrightness = clamp(mapToRange(distanceSquared, 1, 0, radiusSquared, 2 * radiusSquared), 0, 1)
                for i in range(0, 3):
                    led[i] = clamp(led[i] + self.brightness * radialBrightness * orbColour[i], 0, 255)
                