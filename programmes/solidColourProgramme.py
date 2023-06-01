from programmes.programme import Programme

class SolidColourProgramme(Programme):
    colour: tuple[float, float, float]

    def __init__(
            self,
            colour=[0, 0, 0],
            brightness=0,
        ):
        super().__init__()
        self.brightness = brightness
        self.colour = colour
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        for i, led in enumerate(self.leds):
            led[0] = self.colour[0] * self.brightness
            led[1] = self.colour[1] * self.brightness
            led[2] = self.colour[2] * self.brightness
