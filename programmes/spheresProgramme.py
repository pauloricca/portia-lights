from constants import EVENTS_BOUNDING_BOX
from events import EVENT_TYPES
from dataclasses import dataclass

from programmes.programme import Programme
from utils import getDistanceSquared, mapToRange

@dataclass
class Sphere:
    life: int
    radius: float
    centre: tuple[float, float, float]
    colour: tuple[float, float, float]

class SpheresProgramme(Programme):
    spheres: list[Sphere]

    def __init__(
        self,
        ledCount: int,
        brightness=1,
        shimmerAmount=0,
    ):
        super().__init__(ledCount)
        self.shimmerScale = .00001
        self.brightness = brightness
        self.shimmerAmount = shimmerAmount
        self.spheres = []
    
    def step(
            self,
            ledCoords,
            frameTime,
            events,
        ):
        self.clear()

        for event in events:
            if event.type == EVENT_TYPES.FLASH:
                pass
                self.spheres.append(Sphere(
                    centre = event.params["centre"],
                    radius = event.params["radius"],
                    colour = event.params["colour"],
                    life = event.params["life"],
                ))
    
        # Remove dead spheres
        self.spheres = [sphere for sphere in self.spheres if sphere.life > 0]

        # spheres life cycle
        for sphere in self.spheres:
            sphere.life -= frameTime
        
        for i, led in enumerate(self.leds):
            for sphere in self.spheres:
                distance = getDistanceSquared(ledCoords[i], sphere.centre)
                if distance < sphere.radius**2 :
                    led[0] = sphere.colour[0]
                    led[1] = sphere.colour[1]
                    led[2] = sphere.colour[2]
        
        self.shimmer(frameTime)
        
