import math
from constants import *

def colourWave(leds: list[tuple[float, float, float]]):
    # Init vars
    if "phaser" not in colourWave.__dict__:
        colourWave.phaser = 0
        colourWave.phaseg = 0
        colourWave.phaseb = 0 

    colourWave.phaser += 0.2
    colourWave.phaseg += 0.1
    colourWave.phaseb += 0.05
    for i in range(LED_COUNT):
        valuer = 55 + 255 * math.sin(colourWave.phaser + i / 10)
        valueg = 55 + 255 * math.sin(colourWave.phaseg + i / 6)
        valueb = 55 + 255 * math.sin(colourWave.phaseb + i / 4)
        leds[i] = (valuer, valueg, valueb)
