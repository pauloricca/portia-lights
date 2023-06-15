from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import snoise3, snoise2

class AxisColourNoiseProgramme(Programme):
    saturation: float
    hueScale: float
    brightnessScale: float
    hueSpeed: float
    brightnessSpeed: float

    def __init__(
            self,
            brightness=.12,
            saturation=1,
            hueScale=.0015,
            brightnessScale=.02,
            hueSpeed=.1,
            brightnessSpeed=.1
        ):
        super().__init__()
        self.brightness = brightness
        self.saturation = saturation
        self.hueScale = hueScale
        self.brightnessScale = brightnessScale
        self.hueSpeed = hueSpeed
        self.brightnessSpeed = brightnessSpeed
        self.phaseHue = 0
        self.phaseBrightness = 0
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phaseHue += frameTime * self.hueSpeed
        self.phaseBrightness += frameTime * self.brightnessSpeed
        
        for i, led in enumerate(self.leds):
            # noise gives values [-1, 1] adding 1 we get [0, 2],to get hues gradients red - violet - red
            ledBrightness = self.brightness * snoise3(
                ledCoords[i][0] * self.brightnessScale, 
                ledCoords[i][1] * self.brightnessScale, 
                # ledCoords[i][2] * self.brightnessScale, 
                self.phaseBrightness
            )

            # Only calculate hues for visible leds
            if ledBrightness > 0:
                hue = snoise2(
                #     ledCoords[i][0] * self.hueScale, 
                #     ledCoords[i][1] * self.hueScale, 
                    ledCoords[i][2] * self.hueScale, 
                    self.phaseHue
                ) + 1
            else:
                hue = 0
            
            rgb = hsv_to_rgb(hue, self.saturation, ledBrightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
