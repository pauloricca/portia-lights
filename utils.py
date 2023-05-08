import threading
import os

def _playAudioFileSync(file):
    os.system("aplay '" + file + "'")

def playAudio(file):
    t = threading.Thread(target=_playAudioFileSync, args=(file,))
    t.start()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)