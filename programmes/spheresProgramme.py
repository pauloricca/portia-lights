import time
from constants import EVENTS_BOUNDING_BOX
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
            if event.type == EVENT_TYPES.PROG_FLASH:
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
            if sphere.startTime <= currentTime:
                sphere.life -= frameTime
                sphere.centre = [sphere.centre[i] + pos * frameTime for i, pos in enumerate(sphere.velocity)]
                for i, led in enumerate(self.leds):
                    ## Optimised collision detection
                    if (
                        ledCoords[i][0] >= sphere.centre[0] - sphere.radius and 
                        ledCoords[i][0] <= sphere.centre[0] + sphere.radius and
                        ledCoords[i][1] >= sphere.centre[1] - sphere.radius and 
                        ledCoords[i][1] <= sphere.centre[1] + sphere.radius and
                        ledCoords[i][2] >= sphere.centre[2] - sphere.radius and 
                        ledCoords[i][2] <= sphere.centre[2] + sphere.radius
                    ):
                        distanceSquared = getDistanceSquared(ledCoords[i], sphere.centre)
                        if distanceSquared < sphere.radius**2 :
                            led[0] = sphere.colour[0] * self.brightness
                            led[1] = sphere.colour[1] * self.brightness
                            led[2] = sphere.colour[2] * self.brightness
        
        self.shimmer(frameTime)


    def startRain(self, duration: float):
        dropRadius = 10
        dropFrequency = 20 # Drops per second
        numberOfDrops = int(duration * dropFrequency)
        intervalBetweenDrops = duration / numberOfDrops
        currentTime = time.time()

        for i in range(numberOfDrops):
            startTime = currentTime + intervalBetweenDrops * i
            randomPoint = getRandomPointInSpace()
            startPoint = (randomPoint[0], EVENTS_BOUNDING_BOX[1][1], randomPoint[2])
            self.spheres.append(Sphere(
                centre = startPoint,
                radius = dropRadius,
                colour = (255, 255, 255),
                life = 5,
                startTime = startTime,
                velocity = (0, -140, 0)
            ))

