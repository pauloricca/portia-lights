from constants import *
from rpi_ws281x import PixelStrip, Color
# import neopixel
from utils import clamp

def render(leds: list[tuple[float, float, float]], ledStrip: PixelStrip):
    for i in range(LED_COUNT):
        r = leds[i][0]
        g = leds[i][1]
        b = leds[i][2]

        if r < 0: r = 0
        if g < 0: g = 0
        if b < 0: b = 0

        addToR = 0
        addToG = 0
        addToB = 0

        if r > 255:
            rOver = r - 255
            if rOver > 255: rOver = 255
            addToG = rOver * OVERBLOW_BLEED_RATIO_R
            addToB = rOver * OVERBLOW_BLEED_RATIO_R
        
        if g > 255:
            gOver = g - 255
            if gOver > 255: gOver = 255
            addToR = gOver * OVERBLOW_BLEED_RATIO_G
            addToB = gOver * OVERBLOW_BLEED_RATIO_G
        
        if b > 255:
            bOver = b - 255
            if bOver > 255: bOver = 255
            addToR = bOver * OVERBLOW_BLEED_RATIO_B
            addToG = bOver * OVERBLOW_BLEED_RATIO_B
        
        if addToR > 0: r += addToR
        if addToG > 0: g += addToG
        if addToB > 0: b += addToB

        if r > 255: r = 255
        if g > 255: g = 255
        if b > 255: b = 255

        # r = clamp(leds[i][0] + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_R, 0, 255)
        # g = clamp(leds[i][1] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G + clamp(leds[i][2] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_G, 0, 255)
        # b = clamp(leds[i][2] + clamp(leds[i][0] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B + clamp(leds[i][1] - 255, 0, 255) * OVERBLOW_BLEED_RATIO_B, 0, 255)
        # ledStrip[i] = (r, g, b)
        ledStrip.setPixelColor(i, Color(int(r), int(g), int(b)))
    ledStrip.show()