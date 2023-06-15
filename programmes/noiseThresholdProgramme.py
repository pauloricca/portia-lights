from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import snoise3

class NoiseThresholdProgramme(Programme):
    saturation: float
    hue: float
    scale: float
    speed: float
    phase: float
    thresholdMin: float
    thresholdMax: float

    def __init__(
            self,
            brightness=1,
            saturation=1,
            hue=.5,
            scale=.002,
            speed=.15,
            thresholdMin=.3,
            thresholdMax=.6,
            phase=0
        ):
        super().__init__()
        self.brightness = brightness
        self.saturation = saturation
        self.hue = hue
        self.scale = scale
        self.speed = speed
        self.phase = phase
        self.thresholdMin = thresholdMin
        self.thresholdMax = thresholdMax
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phase += frameTime * self.speed
        
        for i, led in enumerate(self.leds):
            # noise gives values [-1, 1] adding 1 we get [0, 2],to get hues gradients red - violet - red
            noiseLevel = snoise3(
                (ledCoords[i][0] + ledCoords[i][1]) * self.scale, 
                (ledCoords[i][2] - ledCoords[i][1]) * self.scale, 
                self.phase
            )
            
            # brightness is max is noise level is between threshold limits
            ledBrightness = self.brightness if noiseLevel >= self.thresholdMin and noiseLevel <= self.thresholdMax else 0
            
            rgb = hsv_to_rgb(self.hue, self.saturation, ledBrightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
