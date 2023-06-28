from programmes.programme import Programme

class HorizontalBandsProgramme(Programme):
    speed: float
    height: float
    ratio: float # 0 to 1 (fully black to fully white)
    phase: float

    def __init__(
            self,
            ledCount: int,
            speed=100,
            brightness=0,
            height=70,
            ratio=0
        ):
        super().__init__(ledCount)
        self.brightness = brightness
        self.speed = speed
        self.height = height
        self.ratio = ratio
        self.phase = 0
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        self.phase += frameTime * self.speed

        for i, led in enumerate(self.leds):
            yPos = ledCoords[i][1]
            positionInBand = (yPos + self.phase) % self.height
            if positionInBand < self.ratio * self.height:
                led[0] = self.brightness * 255
                led[1] = self.brightness * 255
                led[2] = self.brightness * 255
            else:
                led[0] = 0
                led[1] = 0
                led[2] = 0

