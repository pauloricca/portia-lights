from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import snoise3

class NoiseBandsProgramme(Programme):
    hue: float
    saturation: float
    hueSecond: float
    saturationSecond: float
    firstBand: tuple[float, float]
    secondBand: tuple[float, float]
    scale: float
    speed: float
    phase: float
    fadeByTime: float

    def __init__(
            self,
            ledCount: int,
            brightness=0,
            hue=0,
            saturation=1,
            hueSecond=.7,
            saturationSecond=1,
            scale=.002,
            speed=.15,
            firstBand=(.2, .3),
            secondBand=(.5, .7),
            shimmerAmount=0.2
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
        self.hueSecond = hueSecond
        self.saturationSecond = saturationSecond
        self.scale = scale
        self.speed = speed
        self.phase = 0
        self.firstBand = firstBand
        self.secondBand = secondBand
        self.shimmerAmount = shimmerAmount
        self.fadeByTime = 1
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.phase += frameTime * self.speed

        self.fade(frameTime * self.fadeByTime)
        self.shimmer(frameTime)

        for i, led in enumerate(self.leds):
            # noise gives values [-1, 1] adding 1 we get [0, 2],to get hues gradients red - violet - red
            noiseLevel = .5 + snoise3(
                (ledCoords[i][0] + ledCoords[i][1]) * self.scale, 
                (ledCoords[i][2] - ledCoords[i][1]) * self.scale, 
                self.phase
            ) / 2
            
            if noiseLevel > self.firstBand[0] and noiseLevel < self.firstBand[1]:
                rgb = hsv_to_rgb(self.hue, self.saturation, self.brightness)
                led[0] = rgb[0] * 255
                led[1] = rgb[1] * 255
                led[2] = rgb[2] * 255
            elif noiseLevel > self.secondBand[0] and noiseLevel < self.secondBand[1]:
                rgb = hsv_to_rgb(self.hueSecond, self.saturationSecond, self.brightness)
                led[0] = rgb[0] * 255
                led[1] = rgb[1] * 255
                led[2] = rgb[2] * 255
            else:
                pass
                # led[0] = 0
                # led[1] = 0
                # led[2] = 0
    
        
