#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html
# adafruit-circuitpython-pixelbuf https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf

from app import App
from constants import *
import subprocess

# Check for audio interface present. if so, this is master
isMaster = False
if PLATFORM == 'Linux':
    audioCardsOutput = subprocess.check_output(("cat", "/proc/asound/cards")).decode("ascii")
    audioCardsOutputLines = audioCardsOutput.split('\n')
    for line in audioCardsOutputLines:
        if "USB-Audio" in line:
            isMaster = True

if isMaster: print("Starting as Master")
else: print("Starting as Slave")

app = App(isMaster=isMaster, isLightController=True, isVerbose=False)