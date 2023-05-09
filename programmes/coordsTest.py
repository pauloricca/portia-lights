from constants import *

def coordsTest(
    leds: list[tuple[float, float, float]],
    pixelCoords: list[tuple[float, float, float]],
    frameTime: float
):
    # Init vars
    if "positionX" not in coordsTest.__dict__:
        coordsTest.positionX = 0
        coordsTest.lastPositionX = 0
        coordsTest.positionY = 0
        coordsTest.lastPositionY = 0

    coordsTest.positionX += frameTime * 3
    if coordsTest.positionX > 6:
        coordsTest.positionX = -1

    coordsTest.positionY +=  frameTime * 10
    if coordsTest.positionY > 11:
        coordsTest.positionY = -4

    for i in range(LED_COUNT):
        coords = pixelCoords[i]
        r = leds[i][0] * (1 - frameTime * 6)
        g = leds[i][1] * (1 - frameTime * 6)
        b = leds[i][2] * (1 - frameTime * 6)
        
        if coords[0] < coordsTest.positionX and coords[0] > coordsTest.lastPositionX:
            r = 500
        
        if coords[1] < coordsTest.positionY and coords[1] > coordsTest.lastPositionY:
            b = 500
        
        leds[i] = (r, g, b)
    
    coordsTest.lastPositionX = coordsTest.positionX
    coordsTest.lastPositionY = coordsTest.positionY
