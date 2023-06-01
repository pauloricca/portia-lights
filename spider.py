#!/usr/bin/env python3

# Based on https://docs.circuitpython.org/projects/neopixel/en/latest/index.html
# adafruit-circuitpython-pixelbuf https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf

import time
#import neopixel
#import adafruit_pixelbuf
from rpi_ws281x import PixelStrip
import keyboard

from constants import *
from config import config, loadConfig
from utils import getBlankLEDsBuffer
from render import render
from networking.slave import Slave
from networking.master import Master
from events import EventManager

from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme
from programmes.programme import Programme

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
try:
    ledCoords = loadConfig()
except:
    ledCoords = config(ledStrip)

eventManager = EventManager()
slave: Slave
master: Master

if MODE == 'SLAVE':
    slave = Slave(verbose=True)
else:
    master = Master()

lastFrameTime = time.time()
framecount = 0
totalFrameTime = 0

programmes: list[Programme] = [
    SparksProgramme(),
    ColourNoiseProgramme(),
    ColourNoiseProgramme(saturation=0.35, hueNoiseScale=.05, speed=.1, brightnessNoiseScale=.4),
    ColourNoiseProgramme(saturation=0, hueNoiseScale=.05, speed=10, brightnessNoiseScale=.4, brightness=0.004),
]

# Main loop
while True:
    thisFrameTime = time.time()
    frameTime = thisFrameTime - lastFrameTime
    lastFrameTime = thisFrameTime
    #print(str(int(1/frameTime)) + "fps")

    ## Average frame time
    # totalFrameTime += frameTime
    # framecount += 1
    # print(str(totalFrameTime/framecount))

    # Change mode to config
    if keyboard.is_pressed("enter"):
        ledCoords = config(ledStrip)

    # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
    leds: list[list] = getBlankLEDsBuffer()

    if MODE == 'MASTER':
        # Send events to slaves
        master.pushEvents(eventManager.popEvents(popFromSlaveQueue=True))
    else:
        # Add events received from master
        eventManager.pushEvents(slave.popEvents())
    
    events = eventManager.popEvents()

    # Run programme cycles and add their output to the main render buffer
    for programme in programmes:
        programme.step(ledCoords, frameTime, events)
        if programme.brightness > 0:
            for i, led in enumerate(leds):
                led[0] += programme.leds[i][0]
                led[1] += programme.leds[i][1]
                led[2] += programme.leds[i][2]

    render(leds, ledStrip)

    renderTime = time.time() - thisFrameTime

    # TODO: fix target fps sleep time
    # sleepTime = renderTime - (1 / TARGET_FPS)
    # print(sleepTime)
    # if sleepTime > 0: time.sleep(sleepTime)

    # time.sleep(0.01)