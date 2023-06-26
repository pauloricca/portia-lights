from colorsys import hsv_to_rgb
from constants import EVENTS_BOUNDING_BOX
from programmes.programme import Programme
from utils import mapToRange

class GradientProgramme(Programme):
    hue: float
    saturation: float
    hueBottom: float
    saturationBottom: float
    interpolateByHue: bool # If true the gradient will be interpolated by hue/frequency, otherwise by RBG interpolation


    def __init__(
            self,
            ledCount: int,
            hue=0,
            saturation=1,
            brightness=0,
            hueBottom=0,
            saturationBottom=1,
            interpolateByHue=False,
            shimmerAmount=0.5,
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
        self.hueBottom = hueBottom
        self.saturationBottom = saturationBottom
        self.interpolateByHue = interpolateByHue
        self.shimmerAmount = shimmerAmount
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        (bottom, top) = EVENTS_BOUNDING_BOX[1]
        if not self.interpolateByHue:
            topColour = hsv_to_rgb(self.hue%1, self.saturation, self.brightness)
            bottomColour = hsv_to_rgb(self.hueBottom%1, self.saturationBottom, self.brightness)
        for i, led in enumerate(self.leds):
            yPos = ledCoords[i][1]
            if self.interpolateByHue:
                hue = mapToRange(yPos, self.hue, self.hueBottom, top, bottom)%1
                saturation = mapToRange(yPos, self.saturation, self.saturationBottom, top, bottom)
                colour = hsv_to_rgb(hue, saturation, self.brightness)
            else:
                positionInGradient = mapToRange(yPos, 0, 1, top, bottom)
                colour = [
                    topColour[j] + (bottomColour[j] - topColour[j]) * positionInGradient for j in range(3)
                ]
            led[0] = colour[0] * 255
            led[1] = colour[1] * 255
            led[2] = colour[2] * 255

        self.shimmer(frameTime)
