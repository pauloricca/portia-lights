from constants import *
from random import random
from utils import getDistanceSquared, getRandomPointInSpace, getRandomColour

from programmes.programme import Programme

class SparksProgramme(Programme):

    def __init__(self):
        super().__init__()
        self.sparks = [] # list of dict with life, radius, lastRadius, colour and centre
    
    def render(
            self,
            pixelCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * 10)

        # Sparks life cycle
        sparksToRemove = []
        for spark in self.sparks:
            if spark["life"] < 0:
                sparksToRemove.append(spark)
            else:
                spark["life"] -= frameTime
                spark["lastRadius"] = spark["radius"]
                spark["radius"] += frameTime * 15
    
        # Remove dead sparks
        for spark in sparksToRemove:
            self.sparks.remove(spark)

        # Add new sparks
        if random() < frameTime * 0.5:
            self.sparks.append({
                "life": 2,
                "radius": 0,
                "lastRadius": 0,
                "centre": getRandomPointInSpace(),
                "colour": getRandomColour(brightness = 2)
            })

        for i in range(LED_COUNT):
            coords = pixelCoords[i]

            r = self.leds[i][0]
            g = self.leds[i][1]
            b = self.leds[i][2]

            for spark in self.sparks:
                distanceSquared = getDistanceSquared(coords, spark["centre"])
                radiusSquared = spark["radius"] * spark["radius"]
                lastRadiusSquared = spark["lastRadius"] * spark["lastRadius"]
                if (distanceSquared < radiusSquared and distanceSquared > lastRadiusSquared):
                    self.leds[i][0] += spark["colour"][0]
                    self.leds[i][1] += spark["colour"][1]
                    self.leds[i][2] += spark["colour"][2]

        return self.leds
