from abc import *

from constants import *
from utils import clamp, getBlankLEDsBuffer
from events import Event
from noise import snoise2

class Programme(ABC):
    brightness: float
    shimmerAmount: float
    shimmerSpeed: float
    shimmerScale: float
    shimmerPhase: float
    leds: list[list]

    def __init__(self, ledCount: int):
        self.leds = getBlankLEDsBuffer(ledCount)
        self.shimmerAmount = 0
        self.shimmerSpeed = 300
        self.shimmerPhase = 0
        self.shimmerScale = 1000

    # Step programme by frameTime.
    # If brightness is 0, programme may update state but shouldn't render or do expensive calculations.
    # Receives events that may affect the programme, and may return events to be broadcasted to other devices.
    @abstractmethod
    def step(
        self,
        ledCoords: list[list],
        frameTime: float,
        events: list[Event],
    ) -> list[Event]:
        raise NotImplementedError("Please Implement this method")
    
    def clear(self):
        self.leds = getBlankLEDsBuffer(len(self.leds))

    # Darken all leds by amount (0 to 1)
    def fade(
        self,
        amount: float
    ):
        clampedAmount = clamp(amount, 0, 1)
        for led in self.leds:
            led[0] *= 1 - clampedAmount
            led[1] *= 1 - clampedAmount
            led[2] *= 1 - clampedAmount

    # Shimmer all leds according to shimmerAmount
    def shimmer(self, frameTime: float):
        if self.shimmerAmount <= 0:
            return

        self.shimmerPhase += self.shimmerSpeed * frameTime
        for i, led in enumerate(self.leds):
            if led[0] > 0 or led[1] > 0 or led[2] > 0:
                shimmer = abs(self.shimmerAmount * snoise2(
                    i * self.shimmerScale, 
                    self.shimmerPhase
                ))
                led[0] -= led[0] * shimmer
                led[1] -= led[1] * shimmer
                led[2] -= led[2] * shimmer