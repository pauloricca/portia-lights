from abc import *

from constants import *
from utils import getBlankLEDsBuffer

class Programme(ABC):

    def __init__(self):
        self.leds: list[list] = getBlankLEDsBuffer()

    @abstractmethod
    def render(
        self,
        ledCoords: list[list],
        frameTime: float,
        events: list,
    ):
        raise NotImplementedError("Please Implement this method")
    
    # darken all leds by amount (0 to 1)
    def fade(
        self,
        amount: float
    ):
        for led in self.leds:
            led[0] *= 1 - amount
            led[1] *= 1 - amount
            led[2] *= 1 - amount