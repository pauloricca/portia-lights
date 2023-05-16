from random import random
from utils import getDistanceSquared, getRandomPointInSpace, getRandomColour
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

    def __init__(self):
        super().__init__()
        self.sparks = []
        self.propagationSpeed = 100
        self.sparkProbability = 0.3
        self.brightness = 2
        self.fadeByDistance = 0.02
    
    def render(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 10)

        # Sparks life cycle
        sparksToRemove = []
        for spark in self.sparks:
            if spark.life < 0:
                sparksToRemove.append(spark)
            else:
                spark.life -= frameTime
                spark.lastRadius = spark.radius
                spark.radius += frameTime * self.propagationSpeed
    
        # Remove dead sparks
        for spark in sparksToRemove:
            self.sparks.remove(spark)

        # Add new sparks
        if random() < frameTime * self.sparkProbability:
            self.sparks.append(Spark(
                centre = getRandomPointInSpace(),
                colour = getRandomColour(brightness = self.brightness),
            ))

        for i, led in enumerate(self.leds):
            for spark in self.sparks:
                distanceSquared = getDistanceSquared(ledCoords[i], spark.centre)
                radiusSquared = spark.radius * spark.radius
                lastRadiusSquared = spark.lastRadius * spark.lastRadius
                if (distanceSquared < radiusSquared and distanceSquared > lastRadiusSquared):
                    led[0] += spark.colour[0] / (distanceSquared * self.fadeByDistance)
                    led[1] += spark.colour[1] / (distanceSquared * self.fadeByDistance)
                    led[2] += spark.colour[2] / (distanceSquared * self.fadeByDistance)
