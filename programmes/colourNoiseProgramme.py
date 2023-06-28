from colorsys import hsv_to_rgb

from programmes.programme import Programme
from noise import pnoise3

class ColourNoiseProgramme(Programme):
    saturation: float
    hue: float # The hue around which the noise navigates
    hueRange: float
    hueScale: float
    hueSpeed: float
    huePhase: float
    brightnessScale: float
    brightnessSpeed: float
    brightnessPhase: float

    def __init__(
            self,
            ledCount: int,
            brightness=0,
            saturation=.7,
            hue=.5,
            hueRange=.2,
            hueScale=.02,
            hueSpeed=2,
            brightnessScale=.01,
            brightnessSpeed=.2,
            shimmerAmount=.3,
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.saturation = saturation
        self.hue = hue
        self.hueRange = hueRange
        self.hueScale = hueScale
        self.hueSpeed = hueSpeed
        self.brightnessScale = brightnessScale
        self.brightnessSpeed = brightnessSpeed
        self.huePhase = 0
        self.brightnessPhase = 0
        self.shimmerAmount = shimmerAmount
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):

        self.huePhase += frameTime * self.hueSpeed
        self.brightnessPhase += frameTime * self.brightnessSpeed

        # Paulo
        # print((self.huePhase, self.brightnessPhase, self.hueSpeed, self.brightnessSpeed))
        # print((self.brightness, self.brightnessPhase))
        
        for i, led in enumerate(self.leds):
            ledBrightness = self.brightness * pnoise3(
                (ledCoords[i][0] + ledCoords[i][1]) * self.brightnessScale, 
                (ledCoords[i][2] - ledCoords[i][1]) * self.brightnessScale, 
                self.brightnessPhase
            )

            # Only calculate hues for visible leds
            # noise gives values [-1, 1], but mostly around 0.5. By multiplying by 5 and mod 1 we force it to
            # go through all values and wrap around 1 to 0 (which works for hue as 0 is the same as 1)
            if ledBrightness > 0:
                hueNoise = pnoise3(
                    (ledCoords[i][0] + ledCoords[i][1]) * self.hueScale, 
                    (ledCoords[i][2] - ledCoords[i][1]) * self.hueScale, 
                    self.huePhase
                ) * self.hueRange / 2
                hue = (self.hue + hueNoise) % 1
            else:
                ledBrightness = 0
                hue = 0
            
            rgb = hsv_to_rgb(hue, self.saturation, ledBrightness)
            led[0] = rgb[0] * 255
            led[1] = rgb[1] * 255
            led[2] = rgb[2] * 255
        
        self.shimmer(frameTime)
