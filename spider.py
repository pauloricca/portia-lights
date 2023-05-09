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

from config import config
from utils import playAudio, clamp
from constants import *

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

leds = [[0, 0, 0] for i in range(LED_COUNT)]

def render():
    for i in range(LED_COUNT):
        r = clamp(leds[i][0] + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R, 0, 255)
        g = clamp(leds[i][1] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G, 0, 255)
        b = clamp(leds[i][2] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B, 0, 255)
        # pixels[i] = (r, g, b)
        pixels.setPixelColor(i, Color(int(r), int(g), int(b)))
    print((int(r), int(g), int(b)))
    pixels.show()
    

playAudio(AUDIO_FILE)

phaser = 0
phaseg = 0
phaseb = 0

# Main loop
while True:
    # Change mode to config
    if keyboard.is_pressed("enter"):
        config(pixels)

    phaser += 0.2
    phaseg += 0.1
    phaseb += 0.05
    for i in range(LED_COUNT):
        valuer = 55 + 255 * math.sin(phaser + i / 10)
        valueg = 55 + 255 * math.sin(phaseg + i / 6)
        valueb = 55 + 255 * math.sin(phaseb + i / 4)
        leds[i] = (valuer, valueg, valueb)
    render()