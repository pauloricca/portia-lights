from utils import getDistanceSquared, mapToRange
from math import sin, cos

from programmes.programme import Programme

class RotatingOrbProgramme(Programme):
    angle: float
    fadeByDistance: float
    speed: float
    radius: float

    def __init__(
        self,
        speed=150,
        brightness=3,
        fadeByDistance=.01,
        radius=20
    ):
        super().__init__()
        self.speed = speed
        self.brightness = brightness
        self.fadeByDistance = fadeByDistance
        self.angle = 0
        self.radius = radius
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 10)

        self.angle += frameTime * self.speed

        orbX = 75 * sin(self.angle)
        orbY = 75 * cos(self.angle)

        radiusSquared = self.radius * self.radius

        for i, led in enumerate(self.leds):
            distanceSquared = getDistanceSquared(ledCoords[i], (orbX, orbY, 10))
            if distanceSquared < radiusSquared:
                led[0] = self.brightness * 255
            else:
                led[0] = self.brightness * mapToRange(distanceSquared, 255, 0, radiusSquared, 2 * radiusSquared)
                
            led[1] = led[1]
            led[2] = led[2]
