#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html

import time
import board
import neopixel
import argparse
import math
import threading
import os

AUDIO_FILE = "temple.wav"

LED_COUNT = 300
LED_PIN = board.D10 # 10 uses SPI /dev/spidev0.0 (pin 19)
#LED_PIN = board.D18 # PWM (pin 12) - needs to be run with sudo

# 1 means overblowing is linear, less means it takes higher values to get to full white
# Different overblow ratios per channel so we can control how it per channel.
# When all ratios are the same, the overblow tends to be bluer
OVERBLOW_BLEED_RATIO_R = 1
OVERBLOW_BLEED_RATIO_G = .5
OVERBLOW_BLEED_RATIO_B = .2

pixels = neopixel.NeoPixel(LED_PIN, n=LED_COUNT, pixel_order=neopixel.GRB, auto_write=False)
leds = [[0, 0, 0] for i in range(LED_COUNT)]

def playAudioFileSync():
    os.system("aplay '" + AUDIO_FILE + "'")

def startAudio():
    t = threading.Thread(target=playAudioFileSync)
    t.start()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def render():
    for i in range(LED_COUNT):
        r = clamp(leds[i][0] + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R, 0, 255)
        g = clamp(leds[i][1] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G, 0, 255)
        b = clamp(leds[i][2] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B, 0, 255)
        pixels[i] = (r, g, b)
    print(pixels[0])
    pixels.show()

startAudio()

phaser = 0
phaseg = 0
phaseb = 0

# Main loop
while True:
    phaser += 0.2
    phaseg += 0.1
    phaseb += 0.05
    for i in range(LED_COUNT):
        valuer = 55 + 255 * math.sin(phaser + i / 10)
        valueg = 55 + 255 * math.sin(phaseg + i / 6)
        valueb = 55 + 255 * math.sin(phaseb + i / 4)
        leds[i] = (valuer, valueg, valueb)
    render()