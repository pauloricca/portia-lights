import threading
import os
import subprocess
import math
from colorsys import hsv_to_rgb

from random import random
from constants import *

def _playAudioFileSync(file):
    playCommand = 'aplay' if PLATFORM == 'Linux' else 'afplay'
    stopAudio()
    try: subprocess.call((playCommand, file), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except Exception as e: print('Error playing audio: ' + str(e))

def playAudio(variant = ''):
    filePath = getAbsolutePath(AUDIO_FILE if variant == '' else AUDIO_FILE.replace('.wav', '.' + variant + '.wav'))
    t = threading.Thread(target=_playAudioFileSync, args=(filePath,), daemon=True)
    t.start()

def stopAudio():
    playCommand = 'aplay' if PLATFORM == 'Linux' else 'afplay'
    try: subprocess.call(("killall", playCommand), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except: pass

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def getEmptyLedCoords(ledCount: int):
    return [(0, 0, 0) for _ in range(ledCount)]

def getDistanceSquared(a: tuple[float, float, float], b: tuple[float, float, float]):
    return (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2])

def getDistance(a: tuple[float, float, float], b: tuple[float, float, float]):
    return math.sqrt(getDistanceSquared(a, b))

def getRandomBetween(a: float, b: float):
    return a + random() * (b - a)

def getRandomPointInSpace(): 
    return (
        getRandomBetween(EVENTS_BOUNDING_BOX[0][0], EVENTS_BOUNDING_BOX[0][1]),
        getRandomBetween(EVENTS_BOUNDING_BOX[1][0], EVENTS_BOUNDING_BOX[1][1]),
        getRandomBetween(EVENTS_BOUNDING_BOX[2][0], EVENTS_BOUNDING_BOX[2][1]),
    )

def getRandomColour(brightness = 0.5):
    rgbColour = hsv_to_rgb(random(), 1, brightness)
    return (rgbColour[0] * 255, rgbColour[1] * 255, rgbColour[2] * 255)

def getBlankLEDsBuffer(ledCount: int):
    return [[0, 0, 0] for _ in range(ledCount)]

def getAbsolutePath(relativePath: str):
    return os.path.join(os.path.dirname(__file__), relativePath)

# Maps a value to a min-max range
def mapToRange(num, outMin, outMax, inMin = 0, inMax = 1):
  return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))

def oneOf(these: list[any]):
    return these[math.floor(getRandomBetween(0, len(these)))]