from events import EVENT_TYPES
from utils import getDistanceSquared
from dataclasses import dataclass

from programmes.programme import Programme

@dataclass
class Spark:
    life = 4
    lastRadius: float
    radius: float
    centre: tuple[float, float, float]
    colour: tuple[float, float, float]

class SparksProgramme(Programme):
    sparks: list[Spark]
    fadeByDistance: float
    fadeByTime: float
    propagationSpeed: float

    def __init__(
        self,
        propagationSpeed=800,
        brightness=25,
        fadeByDistance=.002,
        fadeByTime=4
    ):
        super().__init__()
        self.propagationSpeed = propagationSpeed
        self.brightness = brightness
        self.fadeByDistance = fadeByDistance
        self.fadeByTime = fadeByTime
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
                radius = 100 if self.propagationSpeed < 0 else 0,
                lastRadius = 100 if self.propagationSpeed < 0 else 0
            ))
    
        # Remove dead sparks
        self.sparks = [spark for spark in self.sparks if spark.life > 0 and spark.radius >= 0]

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
                if (
                    (distanceSquared > radiusSquared and distanceSquared < lastRadiusSquared) or
                    (distanceSquared < radiusSquared and distanceSquared > lastRadiusSquared)
                ):
                    led[0] += spark.colour[0] / (distanceSquared * self.fadeByDistance)
                    led[1] += spark.colour[1] / (distanceSquared * self.fadeByDistance)
                    led[2] += spark.colour[2] / (distanceSquared * self.fadeByDistance)
