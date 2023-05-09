import neopixel
import time
import json
from rpi_ws281x import PixelStrip, Color

from constants import *

def config(pixels: neopixel.NeoPixel):
    # Make all leds red for one second (to indicate config and to allow E key to be depressed)
    for i in range(LED_COUNT): pixels.setPixelColor(i, Color(255, 0, 0))
    # for i in range(LED_COUNT): pixels[i] = (0, 255, 0)
    pixels.show()

    time.sleep(1)

    # Clear all leds
    for i in range(LED_COUNT): pixels.setPixelColor(i, Color(0, 0, 0))
    # for i in range(LED_COUNT): pixels[i] = (0, 0, 0)
    pixels.show()

    # Start Config
    currentIndex = 0
    previousIndex = 0
    while True:
        pixels.setPixelColor(previousIndex, Color(0, 0, 0))
        pixels.setPixelColor(currentIndex, Color(0, 255, 0))
        # pixels[previousIndex] = (0, 0, 0)
        # pixels[currentIndex] = (0, 255, 0)
        pixels.show()
