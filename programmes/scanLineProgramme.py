from constants import EVENTS_BOUNDING_BOX
from events import EVENT_TYPES
from dataclasses import dataclass

from programmes.programme import Programme
from utils import mapToRange

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
    trailLength: float
    trailFalloff: float # 1 is linear
    speed: float
    scanLineIntensity: float

    def __init__(
        self,
        ledCount: int,
        speed=20,
        brightness=0,
        trailLength=170,
        shimmerAmount=0,
        trailFalloff=0.7,
        scanLineIntensity=3
    ):
        super().__init__(ledCount)
        self.speed = speed
        self.brightness = brightness
        self.trailLength = trailLength
        self.scanLines = []
        self.shimmerAmount = shimmerAmount
        self.trailFalloff = trailFalloff
        self.scanLineIntensity = scanLineIntensity
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        self.clear()

        for event in events:
            if event.type == EVENT_TYPES.PROG_SCAN_LINE:
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
        
        # draw trail before shimmering is applied
        for i, led in enumerate(self.leds):
            for scanLine in self.scanLines:
                ledCoord = ledCoords[i][scanLine.axis]
                distanceToScanLine = scanLine.position - ledCoord
                # is this led in the trail?
                if (
                    scanLine.direction < 0 and distanceToScanLine < 0 
                    or scanLine.direction > 0 and distanceToScanLine > 0
                ):
                    intensity = mapToRange(abs(distanceToScanLine)**self.trailFalloff, self.brightness, 0, 0, self.trailLength**self.trailFalloff)
                    if (intensity) > 0:
                        led[0] += scanLine.colour[0] * intensity
                        led[1] += scanLine.colour[1] * intensity
                        led[2] += scanLine.colour[2] * intensity
        
        self.shimmer(frameTime)

        for i, led in enumerate(self.leds):
            for scanLine in self.scanLines:
                ledCoord = ledCoords[i][scanLine.axis]
                if (
                    (ledCoord <= scanLine.position and ledCoord >= scanLine.lastPosition) or
                    (ledCoord >= scanLine.position and ledCoord <= scanLine.lastPosition)
                ):
                    led[0] = scanLine.colour[0] * self.scanLineIntensity
                    led[1] = scanLine.colour[1] * self.scanLineIntensity
                    led[2] = scanLine.colour[2] * self.scanLineIntensity
        
