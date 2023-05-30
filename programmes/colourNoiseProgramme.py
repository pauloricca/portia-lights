from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import snoise3

class ColourNoiseProgramme(Programme):
    saturation: float
    hueNoiseScale: float
    brightnessNoiseScale: float
    speed: float

    def __init__(
            self,
            brightness=.12,
            saturation=1,
            hueNoiseScale=.0015,
            brightnessNoiseScale=.02,
            speed=.1
        ):
        super().__init__()
        self.brightness = brightness
        self.saturation = saturation
        self.hueNoiseScale = hueNoiseScale
        self.brightnessNoiseScale = brightnessNoiseScale
        self.speed = speed
        self.phase = 0
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phase += frameTime * self.speed
        
        for i, led in enumerate(self.leds):
            # noise gives values [-1, 1] adding 1 we get [0, 2],to get hues gradients red - violet - red
            ledBrightness = self.brightness * snoise3(
                ledCoords[i][0] * self.brightnessNoiseScale, 
                ledCoords[i][1] * self.brightnessNoiseScale, 
                # ledCoords[i][2] * self.brightnessNoiseScale, 
                self.phase
            )

            # Only calculate hues for visible leds
            if ledBrightness > 0:
                hue = snoise3(
                    ledCoords[i][0] * self.hueNoiseScale, 
                    ledCoords[i][1] * self.hueNoiseScale, 
                    # ledCoords[i][2] * self.hueNoiseScale, 
                    self.phase
                ) + 1
            else:
                hue = 0
            
            rgb = hsv_to_rgb(hue, self.saturation, ledBrightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
