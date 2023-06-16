from constants import EVENTS_BOUNDING_BOX
from events import EVENT_TYPES
from dataclasses import dataclass

from programmes.programme import Programme

@dataclass
class ScanLine:
    axis: int # 0 (sideways), 1 (vertical), 2 (frontwards)
    direction: int # 1 (positive), -1 (negative)
    life = 40
    lastPosition: float
    position: float
    colour: tuple[float, float, float]

class ScanLineProgramme(Programme):
    scanLines: list[ScanLine]
    fadeByTime: float
    speed: float

    def __init__(
        self,
        ledCount: int,
        speed=30,
        brightness=10,
        fadeByTime=2
    ):
        super().__init__(ledCount)
        self.speed = speed
        self.brightness = brightness
        self.fadeByTime = fadeByTime
        self.scanLines = []
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        super().fade(frameTime * self.fadeByTime)

        for event in events:
            if event.type == EVENT_TYPES.SCAN_LINE:
                pass
                self.scanLines.append(ScanLine(
                    axis = event.params["axis"],
                    direction = event.params["direction"],
                    position = EVENTS_BOUNDING_BOX[event.params["axis"]][0 if event.params["direction"] == 1 else 1],
                    lastPosition = EVENTS_BOUNDING_BOX[event.params["axis"]][0 if event.params["direction"] == 1 else 1],
                    colour = event.params["colour"]
                ))
    
        # Remove dead scanLines
        self.scanLines = [scanLine for scanLine in self.scanLines if scanLine.life > 0]

        # scanLines life cycle
        for scanLine in self.scanLines:
            scanLine.life -= frameTime
            scanLine.lastPosition = scanLine.position
            scanLine.position += frameTime * self.speed * scanLine.direction

        for i, led in enumerate(self.leds):
            for scanLine in self.scanLines:
                ledCoord = ledCoords[i][scanLine.axis]
                if (
                    (ledCoord <= scanLine.position and ledCoord >= scanLine.lastPosition) or
                    (ledCoord >= scanLine.position and ledCoord <= scanLine.lastPosition)
                ):
                    led[0] += scanLine.colour[0] * self.brightness
                    led[1] += scanLine.colour[1] * self.brightness
                    led[2] += scanLine.colour[2] * self.brightness
