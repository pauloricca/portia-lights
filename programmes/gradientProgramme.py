from colorsys import hsv_to_rgb
from constants import EVENTS_BOUNDING_BOX
from programmes.programme import Programme
from utils import mapToRange

class GradientProgramme(Programme):
    hue: float
    saturation: float
    hueBottom: float
    saturationBottom: float


    def __init__(
            self,
            ledCount: int,
            hue=0,
            saturation=1,
            brightness=0,
            hueBottom=0,
            saturationBottom=1,
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
        self.hueBottom = hueBottom
        self.saturationBottom = saturationBottom
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        (bottom, top) = EVENTS_BOUNDING_BOX[1]
        for i, led in enumerate(self.leds):
            yPos = ledCoords[i][1]
            hue = mapToRange(yPos, self.hue, self.hueBottom, top, bottom)%1
            saturation = mapToRange(yPos, self.saturation, self.saturationBottom, top, bottom)
            colour = hsv_to_rgb(hue, saturation, self.brightness)
            led[0] = colour[0] * 255
            led[1] = colour[1] * 255
            led[2] = colour[2] * 255
