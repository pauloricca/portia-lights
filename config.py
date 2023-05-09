#import neopixel
import time
import json
from rpi_ws281x import PixelStrip, Color

from constants import *
from utils import getEmptyPixelCoords

def saveConfig(pixelCoords):
    configJson = json.dumps(pixelCoords)
    f = open(CONFIG_FILE, "w")
    f.write(configJson)

def loadConfig():
    try:
        f = open(CONFIG_FILE, "r")
        configJson = f.read()
        return json.loads(configJson)
    except:
        return getEmptyPixelCoords()

def interpolateCoords(pixelCoords: list[tuple[float, float, float]], fromIndex: int, toIndex: int):
    try:
        nSteps = toIndex - fromIndex
        xStep = (pixelCoords[toIndex][0] - pixelCoords[fromIndex][0]) / nSteps
        yStep = (pixelCoords[toIndex][1] - pixelCoords[fromIndex][1]) / nSteps
        zStep = (pixelCoords[toIndex][2] - pixelCoords[fromIndex][2]) / nSteps
        for step in range(1, nSteps):
            pixelCoords[fromIndex + step] = (
                pixelCoords[fromIndex][0] + step * xStep,
                pixelCoords[fromIndex][1] + step * yStep,
                pixelCoords[fromIndex][2] + step * zStep,
            )
    except Exception as e:
        print("Error interpolating.")
        print(e)

def config(pixelCoords: list[tuple[float, float, float]], pixels: PixelStrip):
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
    indexOfPreviousSetPoint = -1 # Used to interpolate between this point and next of set coords
    cancelled = False
    referential = (0, 0, 0)
    while currentIndex < LED_COUNT:
        pixels.setPixelColor(previousIndex, Color(0, 0, 0))
        pixels.setPixelColor(currentIndex, Color(0, 255, 0))
        # pixels[previousIndex] = (0, 0, 0)
        # pixels[currentIndex] = (0, 255, 0)
        pixels.show()

        userInput = input("Enter X Y Z for pixel " + str(currentIndex) + ", Enter to skip and interpolate, r X Y Z to set new referential coordinates, or 'c' to cancel config:\n")

        if userInput is "":
            previousIndex = currentIndex
            currentIndex += 1
        elif userInput == "c":
            currentIndex = LED_COUNT
            cancelled = True
            print("Cancelling...")
        else:
            try:
                coords = userInput.split(" ")

                # Setting new referential
                if coords[0] == "r":
                    print("New referential set")
                    referential = (float(coords[1]), float(coords[2]), float(coords[3]))
                else:
                    x = float(coords[0]) + referential[0]
                    y = float(coords[1]) + referential[1]
                    z = float(coords[2]) + referential[2]

                    pixelCoords[currentIndex] = (x, y, z)

                    # Do we need to interpolate?
                    if (indexOfPreviousSetPoint is not -1 and indexOfPreviousSetPoint < currentIndex - 1):
                        print("Interpolating from " + str(indexOfPreviousSetPoint) + " to " + str(currentIndex))
                        interpolateCoords(pixelCoords, indexOfPreviousSetPoint, currentIndex)

                    indexOfPreviousSetPoint = currentIndex
                    previousIndex = currentIndex
                    currentIndex += 1
            except Exception as e:
                print("Invalid coordinates.")
                print(e)
    
    if not cancelled:
        print("Config complete.")
        saveConfig(pixelCoords)
    else:
        print("Config cancelled.")
        pixelCoords = loadConfig()
    
