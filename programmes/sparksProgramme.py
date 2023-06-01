from events import EVENT_TYPES
from utils import getDistanceSquared
from dataclasses import dataclass

from programmes.programme import Programme

@dataclass
class Spark:
    life = 4
    radius = 0
    lastRadius = 0
    centre: tuple[float, float, float]
    colour: tuple[float, float, float]

class SparksProgramme(Programme):
    sparks: list[Spark]
    fadeByDistance: float
    propagationSpeed: float

    def __init__(
        self,
        propagationSpeed=100,
        brightness=2,
        fadeByDistance=.02
    ):
        super().__init__()
        self.propagationSpeed = propagationSpeed
        self.brightness = brightness
        self.fadeByDistance = fadeByDistance
        self.sparks = []
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 10)

        for event in events:
            if event.type == EVENT_TYPES.SPARK:
                self.sparks.append(Spark(
                centre = event.params["centre"],
                colour = event.params["colour"],
            ))
    
        # Remove dead sparks
        self.sparks = [spark for spark in self.sparks if spark.life > 0]

        # Sparks life cycle
        for spark in self.sparks:
            spark.life -= frameTime
            spark.lastRadius = spark.radius
            spark.radius += frameTime * self.propagationSpeed

        for i, led in enumerate(self.leds):
            for spark in self.sparks:
                distanceSquared = getDistanceSquared(ledCoords[i], spark.centre)
                radiusSquared = spark.radius * spark.radius
                lastRadiusSquared = spark.lastRadius * spark.lastRadius
                if (distanceSquared < radiusSquared and distanceSquared > lastRadiusSquared):
                    led[0] += spark.colour[0] / (distanceSquared * self.fadeByDistance)
                    led[1] += spark.colour[1] / (distanceSquared * self.fadeByDistance)
                    led[2] += spark.colour[2] / (distanceSquared * self.fadeByDistance)
