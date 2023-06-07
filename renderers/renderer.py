from abc import *

from constants import *

class Renderer(ABC):
    @abstractmethod
    def render(
            self,
            leds: list[tuple[float, float, float]],
            ledCoords: list[tuple[float, float, float]]
        ):
        raise NotImplementedError("Please Implement this method")
