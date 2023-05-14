#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html
# adafruit-circuitpython-pixelbuf https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf

import time
import argparse
#import neopixel
#import adafruit_pixelbuf
from rpi_ws281x import PixelStrip
import keyboard

from constants import *
from config import config, loadConfig, saveConfig
from utils import playAudio, getBlankLEDsBuffer
from render import render
from networking.slave import Slave
from networking.master import Master

from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme

# class TestBuf(adafruit_pixelbuf.PixelBuf):
#    called = False

#    def show(self):
#        self.called = True

# ledStrip = neopixel.NeoPixel(LED_PIN, n=LED_COUNT, pixel_order=neopixel.GRB, auto_write=False)
# ledStrip = TestBuf(byteorder="GRB", size=LED_COUNT, auto_write=False)

# Create NeoPixel object with appropriate configuration.
ledStrip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
ledStrip.begin()

# Holds the coordinates for each pixel
ledCoords = loadConfig()
playAudio(AUDIO_FILE)

def onMessageHandler(message):
    print(message)

slave = Slave(onMessage = onMessageHandler)
# master = Master()

lastFrameTime = time.time()

framecount = 0
totalFrameTime = 0

sparksProgramme = SparksProgramme()
colourNoiseProgramme = ColourNoiseProgramme()

if (LED_COUNT > len(ledCoords)): ledCoords = config(ledStrip)

# Main loop
while True:
    thisFrameTime = time.time()
    frameTime = thisFrameTime - lastFrameTime
    lastFrameTime = thisFrameTime
    print(str(int(1/frameTime)) + "fps")

    ## Average frame time
    # totalFrameTime += frameTime
    # framecount += 1
    # print(str(totalFrameTime/framecount))

    # Change mode to config
    if keyboard.is_pressed("enter"):
        ledCoords = config(ledStrip)

    # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
    leds: list[list] = getBlankLEDsBuffer()

    events = []
    
    sparksProgramme.render(ledCoords, frameTime, events)
    colourNoiseProgramme.render(ledCoords, frameTime, events)

    for i, led in enumerate(leds):
        led[0] += sparksProgramme.leds[i][0]
        led[1] += sparksProgramme.leds[i][1]
        led[2] += sparksProgramme.leds[i][1]
        led[0] += colourNoiseProgramme.leds[i][0]
        led[1] += colourNoiseProgramme.leds[i][1]
        led[2] += colourNoiseProgramme.leds[i][2]

    render(leds, ledStrip)

    renderTime = time.time() - thisFrameTime

    sleepTime = renderTime - (1 / TARGET_FPS)
    # print(sleepTime)
    # if sleepTime > 0: time.sleep(sleepTime)