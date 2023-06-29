from constants import *
from renderers.renderer import Renderer
from utils import getAbsolutePath
try:
    from rpi_ws281x import PixelStrip, Color
except:
    print("rpi_ws281x library not present (not required if app is not light controller)")

class LEDRenderer(Renderer):
    pinSplitIndex: int # Index that starts the LEDs connected to pin 18

    def __init__(self, ledCount: int):
        super().__init__()
        self.pinSplitIndex = -1

        # Try to load pin split index
        try:
            f = open(getAbsolutePath(PIN_SPLIT_INDEX_FILE), "r")
            self.pinSplitIndex = int(f.read())
        except Exception as e:
            pass

        self.ledStrip = PixelStrip(ledCount, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.ledStrip.begin()

        if self.pinSplitIndex >= 0:
            self.ledStrip2 = PixelStrip(ledCount, LED_PIN_2, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            self.ledStrip2.begin()
    
    def render(
            self,
            leds: list[tuple[float, float, float]],
            ledCoords: list[tuple[float, float, float]]
        ):
        for i in range(len(leds)):
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

            if self.pinSplitIndex == -1 or i < self.pinSplitIndex:
                self.ledStrip.setPixelColor(i, Color(int(r), int(g), int(b)))
            else:
                self.ledStrip2.setPixelColor(i - self.pinSplitIndex, Color(int(r), int(g), int(b)))
        self.ledStrip.show()
        if self.pinSplitIndex >= 0:
            self.ledStrip2.show()
