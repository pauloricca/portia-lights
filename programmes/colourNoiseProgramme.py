from perlin_noise import PerlinNoise
from colorsys import hsv_to_rgb

from programmes.programme import Programme

class ColourNoiseProgramme(Programme):

    def __init__(self):
        super().__init__()
        self.noise = PerlinNoise(octaves = 1)
        self.brightness = 0.2
        self.saturation = 0.8
        self.phase = 0
        self.scale = 0.03
        self.speed = 0.4
    
    def render(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phase += frameTime * self.speed
        
        for i, led in enumerate(self.leds):
            hue = self.noise([
                ledCoords[i][0] * self.scale + self.phase, 
                ledCoords[i][1] * self.scale + self.phase, 
                # ledCoords[i][2] * self.scale, 
                # self.phase
            ])
            brightness = self.brightness * self.noise([
                ledCoords[i][0] * self.scale + self.phase + 100, 
                ledCoords[i][1] * self.scale + self.phase + 100, 
                # ledCoords[i][2] * self.scale, 
                # self.phase + 100
            ])
            rgb = hsv_to_rgb(hue, self.saturation, brightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
