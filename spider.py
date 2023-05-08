#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html

import time
import argparse
import neopixel
import math
import keyboard

from config import config
from utils import playAudio, clamp
from constants import *

pixels = neopixel.NeoPixel(LED_PIN, n=LED_COUNT, pixel_order=neopixel.GRB, auto_write=False)
leds = [[0, 0, 0] for i in range(LED_COUNT)]

def render():
    for i in range(LED_COUNT):
        r = clamp(leds[i][0] + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R, 0, 255)
        g = clamp(leds[i][1] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G, 0, 255)
        b = clamp(leds[i][2] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B, 0, 255)
        pixels[i] = (r, g, b)
    print(pixels[0])
    pixels.show()
    

playAudio(AUDIO_FILE)

phaser = 0
phaseg = 0
phaseb = 0

# Main loop
while True:
    # Change mode to config
    if keyboard.is_pressed("c"):
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