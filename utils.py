import threading
import os
import subprocess
import math
from colorsys import hsv_to_rgb

from random import random
from constants import *

def _playAudioFileSync(file):
    #os.system("aplay '" + file + "'")
    #os.system("dd if='" + file + "' | aplay")
    #subprocess.run("dd if='" + file + "' | aplay", shell=True)
    os.system("su -c 'aplay temple.wav' admin")

def playAudio(file):
    t = threading.Thread(target=_playAudioFileSync, args=(file,))
    t.start()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def getEmptyPixelCoords():
    return [(math.inf, math.inf, math.inf) for _ in range(LED_COUNT)]

def getDistanceSquared(a: tuple[float, float, float], b: tuple[float, float, float]):
    return (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2])

def getDistance(a: tuple[float, float, float], b: tuple[float, float, float]):
    return math.sqrt(getDistanceSquared(a, b))

def getRandomBetween(a: float, b: float):
    return a + random() * (b - a)

def getRandomPointInSpace(): 
    return (
        getRandomBetween(SPACE_BOUNDING_BOX[0][0], SPACE_BOUNDING_BOX[0][1]),
        getRandomBetween(SPACE_BOUNDING_BOX[1][0], SPACE_BOUNDING_BOX[1][1]),
        getRandomBetween(SPACE_BOUNDING_BOX[2][0], SPACE_BOUNDING_BOX[2][1]),
    )

def getRandomColour(brightness = 0.5):
    rgbColour = hsv_to_rgb(random(), 1, brightness)
    return (rgbColour[0] * 255, rgbColour[1] * 255, rgbColour[2] * 255)
