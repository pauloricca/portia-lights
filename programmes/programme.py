from abc import *

from constants import *
from utils import getBlankLEDsBuffer
from events import Event

class Programme(ABC):
    brightness: float

    def __init__(self):
        self.leds: list[list] = getBlankLEDsBuffer()

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
    
    # Darken all leds by amount (0 to 1)
    def fade(
        self,
        amount: float
    ):
        for led in self.leds:
            led[0] *= 1 - amount
            led[1] *= 1 - amount
            led[2] *= 1 - amount