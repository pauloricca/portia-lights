#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html
# adafruit-circuitpython-pixelbuf https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf

from app import App

# Check for audio interface present. if so, this is master

app = App(isMaster=False, isLightController=True, isVerbose=False)