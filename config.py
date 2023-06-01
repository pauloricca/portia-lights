import time
import json
from renderer import Renderer
try:
    from rpi_ws281x import Color
except:
    print("rpi_ws281x library not present (not required if app is not light controller)")

from constants import *
from utils import getEmptyledCoords, getAbsolutePath

def saveConfig(ledCoords):
    configJson = json.dumps(ledCoords)
    f = open(getAbsolutePath(CONFIG_FILE), "w")
    f.write(configJson)
    f.close()

# Will raise exception if config not found or of incorrect length
def loadConfig():
    f = open(getAbsolutePath(CONFIG_FILE), "r")
    configJson = f.read()
    f.close()
    loadedConfig = json.loads(configJson)
    if (LED_COUNT > len(loadedConfig)): raise Exception('Wrong config length')
    return loadedConfig

def interpolateCoords(ledCoords: list[tuple[float, float, float]], fromIndex: int, toIndex: int):
    try:
        nSteps = toIndex - fromIndex
        xStep = (ledCoords[toIndex][0] - ledCoords[fromIndex][0]) / nSteps
        yStep = (ledCoords[toIndex][1] - ledCoords[fromIndex][1]) / nSteps
        zStep = (ledCoords[toIndex][2] - ledCoords[fromIndex][2]) / nSteps
        for step in range(1, nSteps):
            ledCoords[fromIndex + step] = (
                ledCoords[fromIndex][0] + step * xStep,
                ledCoords[fromIndex][1] + step * yStep,
                ledCoords[fromIndex][2] + step * zStep,
            )
    except Exception as e:
        print("Error interpolating.")
        print(e)

def config(renderer: Renderer):
    ledCoords = getEmptyledCoords()

    # Make all leds red for one second (to indicate config and to allow E key to be depressed)
    for i in range(LED_COUNT): renderer.ledStrip.setPixelColor(i, Color(255, 0, 0))
    renderer.ledStrip.show()

    time.sleep(1)

    # Clear all leds
    for i in range(LED_COUNT): renderer.ledStrip.setPixelColor(i, Color(0, 0, 0))
    renderer.ledStrip.show()

    # Start Config
    currentIndex = 0
    previousIndex = 0
    indexOfPreviousSetPoint = -1 # Used to interpolate between this point and next of set coords
    cancelled = False
    referential = (0, 0, 0)
    while currentIndex < LED_COUNT:
        renderer.ledStrip.setPixelColor(previousIndex, Color(0, 0, 0))
        renderer.ledStrip.setPixelColor(currentIndex, Color(0, 255, 0))
        renderer.ledStrip.show()

        userInput = input("Enter X Y Z for pixel " + str(currentIndex) + ", Enter to skip and interpolate, r X Y Z to set new referential coordinates, or 'c' to cancel config:\n")

        if userInput == "":
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

                    ledCoords[currentIndex] = (x, y, z)

                    # Do we need to interpolate?
                    if (indexOfPreviousSetPoint != -1 and indexOfPreviousSetPoint < currentIndex - 1):
                        print("Interpolating from " + str(indexOfPreviousSetPoint) + " to " + str(currentIndex))
                        interpolateCoords(ledCoords, indexOfPreviousSetPoint, currentIndex)

                    indexOfPreviousSetPoint = currentIndex
                    previousIndex = currentIndex
                    currentIndex += 1
            except Exception as e:
                print("Invalid coordinates.")
                print(e)
    
    if not cancelled:
        print("Config complete.")
        saveConfig(ledCoords)
    else:
        print("Config cancelled.")
        ledCoords = loadConfig()
    
    return ledCoords
    
