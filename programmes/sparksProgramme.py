from constants import *
from random import random
from utils import getDistanceSquared, getRandomPointInSpace, getRandomColour

def sparksProgramme(
    leds: list[tuple[float, float, float]],
    pixelCoords: list[tuple[float, float, float]],
    frameTime: float
):
    # Init
    if "sparks" not in sparksProgramme.__dict__:
        sparksProgramme.pixelCoords = pixelCoords
        sparksProgramme.sparks = [] # list of dict with life, radius, lastRadius, colour and centre

    # Sparks life cycle
    sparksToRemove = []
    for spark in sparksProgramme.sparks:
        if spark["life"] < 0:
            sparksToRemove.append(spark)
        else:
            spark["life"] -= frameTime
            spark["lastRadius"] = spark["radius"]
            spark["radius"] += frameTime * 15
    
    # Remove dead sparks
    for spark in sparksToRemove:
        sparksProgramme.sparks.remove(spark)

    # Add new sparks
    if random() < frameTime * 0.5:
        sparksProgramme.sparks.append({
            "life": 2,
            "radius": 0,
            "lastRadius": 0,
            "centre": getRandomPointInSpace(),
            "colour": getRandomColour(brightness = 2)
        })

    for i in range(LED_COUNT):
        coords = pixelCoords[i]

        r = leds[i][0] * (1 - frameTime * 10)
        g = leds[i][1] * (1 - frameTime * 10)
        b = leds[i][2] * (1 - frameTime * 10)

        for spark in sparksProgramme.sparks:
            distanceSquared = getDistanceSquared(coords, spark["centre"])
            radiusSquared = spark["radius"] * spark["radius"]
            lastRadiusSquared = spark["lastRadius"] * spark["lastRadius"]
            if (distanceSquared < radiusSquared and distanceSquared > lastRadiusSquared):
                r = r + spark["colour"][0]
                g = g + spark["colour"][1]
                b = b + spark["colour"][2]

        leds[i] = (r, g, b)
