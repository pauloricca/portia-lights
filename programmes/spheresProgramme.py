import time
from events import EVENT_TYPES
from dataclasses import dataclass

from programmes.programme import Programme
from utils import getDistanceSquared, getRandomPointInSpace

@dataclass
class Sphere:
    startTime: float
    life: float
    radius: float
    centre: tuple[float, float, float]
    colour: tuple[float, float, float]
    velocity: tuple[float, float, float]


class SpheresProgramme(Programme):
    spheres: list[Sphere]

    def __init__(
        self,
        ledCount: int,
        brightness=0,
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
        currentTime = time.time()

        for event in events:
            if event.type == EVENT_TYPES.FLASH:
                self.spheres.append(Sphere(
                    centre = event.params["centre"],
                    radius = event.params["radius"],
                    colour = event.params["colour"],
                    life = event.params["life"],
                    startTime = 0,
                    velocity = (0, 0, 0)
                ))

        # Remove dead spheres
        self.spheres = [sphere for sphere in self.spheres if sphere.life > 0]

        # spheres life cycle
        for sphere in self.spheres:
            if sphere.startTime >= currentTime:
                sphere.life -= frameTime
                for i, led in enumerate(self.leds):
                    distanceSquared = getDistanceSquared(ledCoords[i], sphere.centre)
                    if distanceSquared < sphere.radius**2 :
                        led[0] = sphere.colour[0]
                        led[1] = sphere.colour[1]
                        led[2] = sphere.colour[2]
        
        self.shimmer(frameTime)


    def startRain(self, duration: float):
        dropRadius = 100
        dropFrequency = 5 # Drops per second
        numberOfDrops = int(duration * dropFrequency)
        intervalBetweenDrops = duration / numberOfDrops
        currentTime = time.time()

        for _ in range(numberOfDrops):
            startTime = currentTime + intervalBetweenDrops
            self.spheres.append(Sphere(
                centre = getRandomPointInSpace(),
                radius = dropRadius,
                colour = (255, 255, 255),
                life = 5,
                startTime = 0, # startTime Paulo
                velocity = (0, -1, 0)
            ))

