import math
from constants import *

def coordsTest(leds: list[tuple[float, float, float]], pixelCoords: list[tuple[float, float, float]]):
    # Init vars
    if "position" not in coordsTest.__dict__:
        coordsTest.position = 0

    coordsTest.position += 0.2
    if coordsTest.position > 12:
        coordsTest.position = -2

    bandWidth = 0.3

    for i in range(LED_COUNT):
        coords = pixelCoords[i]
        if coords[1] > coordsTest.position - bandWidth / 2 and coords[1] < coordsTest.position + bandWidth / 2:
            leds[i] = (0, 100, 255)
        else:
            leds[i] = (leds[i][0] * 0.94,  leds[i][1] * 0.94, leds[i][2] * 0.94)
