#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html
# adafruit-circuitpython-pixelbuf https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf

import time
import argparse
import neopixel
import adafruit_pixelbuf
from rpi_ws281x import PixelStrip, Color
import math
import keyboard

from constants import *
from config import config, loadConfig
from utils import playAudio
from render import render
from programmes.colourWave import colourWave
from programmes.coordsTest import coordsTest

# class TestBuf(adafruit_pixelbuf.PixelBuf):
#    called = False

#    def show(self):
#        self.called = True

# pixels = neopixel.NeoPixel(LED_PIN, n=LED_COUNT, pixel_order=neopixel.GRB, auto_write=False)
# pixels = TestBuf(byteorder="GRB", size=LED_COUNT, auto_write=False)

# Create NeoPixel object with appropriate configuration.
pixels = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
pixels.begin()

# Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
leds: list[tuple[float, float, float]] = [(0, 0, 0) for _ in range(LED_COUNT)]

# Holds the coordinates for each pixel
pixelCoords = loadConfig()

playAudio(AUDIO_FILE)

# Main loop
while True:
    # Change mode to config
    if keyboard.is_pressed("enter"):
        config(pixelCoords, pixels)

    colourWave(leds)
    #coordsTest(leds, pixelCoords)

    render(leds, pixels)
    time.sleep(0.02)