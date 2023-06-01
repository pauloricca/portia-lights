from dataclasses import dataclass
import time

from constants import *

@dataclass
class AnimatorItem():
    object: any
    propertyName: str
    targetValue: float
    targetTime: float
    step: float # value change per second

# Animates object numeric properties towards a target value, over a set of time
class Animator():
    animations: list[AnimatorItem]

    def __init__(self):
        self.animations = []
    
    def createAnimation(
        self,
        object: any,
        propertyName: str,
        targetValue: float,
        duration: float
    ):
        self.animations.append(AnimatorItem(
            object=object,
            propertyName=propertyName,
            targetValue=targetValue,
            targetTime=time.time() + duration,
            step=((targetValue - getattr(object, propertyName)) / duration) if duration > 0 else 0
        ))
    
    def animate(self, frameTime: float):
        currentTime = time.time()
        for animation in [animation for animation in self.animations]:
            if animation.targetTime <= currentTime:
                setattr(animation.object, animation.propertyName, animation.targetValue)
                self.animations.remove(animation)
            else:
                currentValue = getattr(animation.object, animation.propertyName)
                setattr(animation.object, animation.propertyName, currentValue + animation.step * frameTime)
