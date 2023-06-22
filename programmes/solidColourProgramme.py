from colorsys import hsv_to_rgb
from programmes.programme import Programme

class SolidColourProgramme(Programme):
    hue: float
    saturation: float


    def __init__(
            self,
            ledCount: int,
            hue=0,
            saturation=1,
            brightness=0,
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        colour = hsv_to_rgb(self.hue, self.saturation, self.brightness)
        for led in self.leds:
            led[0] = colour[0] * 255
            led[1] = colour[1] * 255
            led[2] = colour[2] * 255
