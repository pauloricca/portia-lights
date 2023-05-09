import threading
import os
import math
from constants import *

def _playAudioFileSync(file):
    os.system("aplay '" + file + "'")

def playAudio(file):
    t = threading.Thread(target=_playAudioFileSync, args=(file,))
    t.start()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def getEmptyPixelCoords():
    return [(math.inf, math.inf, math.inf) for _ in range(LED_COUNT)]