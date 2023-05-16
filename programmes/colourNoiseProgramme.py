from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import snoise3

class ColourNoiseProgramme(Programme):

    def __init__(self):
        super().__init__()
        self.brightness = 0.12
        self.saturation = 1
        self.phase = 0
        self.hueNoiseScale = 0.003
        self.brightnessNoiseScale = 0.02
        self.speed = 0.1
    
    def render(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phase += frameTime * self.speed
        
        for i, led in enumerate(self.leds):
            hue = snoise3(
                ledCoords[i][0] * self.hueNoiseScale, 
                ledCoords[i][1] * self.hueNoiseScale, 
                # ledCoords[i][2] * self.hueNoiseScale, 
                self.phase
            ) * .5 + .5
            brightness = self.brightness * snoise3(
                ledCoords[i][0] * self.brightnessNoiseScale, 
                ledCoords[i][1] * self.brightnessNoiseScale, 
                # ledCoords[i][2] * self.brightnessNoiseScale, 
                self.phase
            )
            rgb = hsv_to_rgb(hue, self.saturation, brightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
