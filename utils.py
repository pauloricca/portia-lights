import threading
import os
import subprocess
import math
from colorsys import hsv_to_rgb

from random import random
from constants import *

def _playAudioFileSync(file):
    playCommand = 'aplay' if PLATFORM == 'Linux' else 'afplay'
    try: subprocess.call(("killall", playCommand), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except: pass
    try: subprocess.call((playCommand, file), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except: pass

def playAudio():
    t = threading.Thread(target=_playAudioFileSync, args=(getAbsolutePath(AUDIO_FILE),), daemon=True)
    t.start()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def getEmptyledCoords():
    return [(0, 0, 0) for _ in range(LED_COUNT)]

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

def getBlankLEDsBuffer():
    return [[0, 0, 0] for _ in range(LED_COUNT)]

def getAbsolutePath(relativePath: str):
    return os.path.join(os.path.dirname(__file__), relativePath)

# Maps a value to a min-max range
def mapToRange(num, outMin, outMax, inMin = 0, inMax = 1):
  return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))