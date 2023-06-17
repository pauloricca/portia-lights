from dataclasses import dataclass
import time
from typing import Union

from constants import *

@dataclass
class AnimatorItem():
    object: any
    propertyName: str
    targetTime: float
    targetValues: tuple[float]
    steps: tuple[float] # amount to change per second, per value
    lastStepTimestamp: float

# Animates object numeric properties towards a target value, over a set of time
class Animator():
    animations: list[AnimatorItem]

    def __init__(self):
        self.animations = []
    
    def createAnimation(
        self,
        object: any,
        propertyName: str,
        targetValue: Union[float, int, tuple[float]],
        duration: float,
    ):
        # Remove previous animations on the same object and property
        existingAnimations = [
            animation
            for animation in self.animations 
            if animation.propertyName == propertyName 
            and animation.object == object
        ]
        for animation in existingAnimations:
            self.animations.remove(animation)

        targetValues = targetValue if hasattr(targetValue, '__iter__') else (targetValue,)
        
        def getCurrentValue(i):
            if len(targetValues) == 1:
                return getattr(object, propertyName)
            else:
                return getattr(object, propertyName)[i]

        self.animations.append(AnimatorItem(
            object=object,
            propertyName=propertyName,
            targetTime=time.time() + duration,
            targetValues=targetValues,
            steps=[
                ((value - getCurrentValue(i)) / duration) if duration > 0 else 0 for i, value in enumerate(targetValues)
            ],
            lastStepTimestamp=time.time()
        ))
    
    def animate(self):
        currentTime = time.time()
        for animation in [animation for animation in self.animations]:
            frameTime = currentTime - animation.lastStepTimestamp
            if animation.targetTime <= currentTime:
                self.__setValues(animation.targetValues, animation)
                self.animations.remove(animation)
            else:
                currentValues = getattr(animation.object, animation.propertyName)
                if len(animation.targetValues) == 1:
                    currentValues = (currentValues,)
                
                newValues = tuple([value + animation.steps[i] * frameTime for i, value in enumerate(currentValues)])
                self.__setValues(newValues, animation)
            animation.lastStepTimestamp = currentTime

    def __setValues(self, value: tuple[float], animation: AnimatorItem):
                if len(value) == 1:
                    setattr(animation.object, animation.propertyName, value[0])
                else:
                    setattr(animation.object, animation.propertyName, value)