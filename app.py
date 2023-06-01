import time
import keyboard

from constants import *
from config import config, loadConfig
from utils import getBlankLEDsBuffer
from renderer import Renderer
from networking.slave import Slave
from networking.master import Master
from events import EventManager
from programmes.programme import Programme
from programmes.sparksProgramme import SparksProgramme
from programmes.colourNoiseProgramme import ColourNoiseProgramme

class App:
    renderer: Renderer
    eventManager: EventManager
    programmes: list[Programme]
    slave: Slave
    master: Master
    ledStrip: list[tuple[float, float, float]]
    isMaster: bool
    isLightController: bool

    lastFrameTime: float
    framecount: int
    totalFrameTime: float


    def __init__(self, isMaster: bool, isLightController=True, isVerbose=False):
        self.isMaster = isMaster
        self.isLightController = isLightController
        self.eventManager = EventManager(self.isMaster)
        self.lastFrameTime = time.time()
        self.framecount = 0
        self.totalFrameTime = 0

        if self.isMaster:
            # Raspberry pis have mac addresses starting with b8
            self.master = Master(macAddressStartMask = 'b8', isVerbose=isVerbose)
        else:
            self.slave = Slave(isVerbose=isVerbose)

        if self.isLightController:
            self.renderer = Renderer()

            # Holds the coordinates for each pixel
            try:
                self.ledCoords = loadConfig()
            except:
                self.ledCoords = config(self.renderer)

            self.programmes = [
                SparksProgramme(),
                ColourNoiseProgramme(),
                ColourNoiseProgramme(saturation=0.35, hueNoiseScale=.05, speed=.1, brightnessNoiseScale=.4),
                ColourNoiseProgramme(saturation=0, hueNoiseScale=.05, speed=10, brightnessNoiseScale=.4, brightness=0.004),
            ]

        while True: self.mainLoop()
    
    def mainLoop(self):
        self.thisFrameTime = time.time()
        self.frameTime = self.thisFrameTime - self.lastFrameTime
        self.lastFrameTime = self.thisFrameTime
        #print(str(int(1/self.frameTime)) + "fps")

        ## Average frame time
        # self.totalFrameTime += self.frameTime
        # self.framecount += 1
        # print(str(self.totalFrameTime/self.framecount))

        if self.isMaster:
            # Send events to slaves
            self.master.pushEvents(self.eventManager.popEvents(popFromSlaveQueue=True))
        else:
            # Add events received from master
            self.eventManager.pushEvents(self.slave.popEvents())
        
        if self.isLightController:
            # Enter Config when pressing Enter key
            if keyboard.is_pressed("enter"): self.ledCoords = config(self.ledStrip)

            # Holds pre-rendered pixel rgb values, from 0 to 500 (0: black, 255: full saturation, 500: white)
            leds: list[list] = getBlankLEDsBuffer()

            events = self.eventManager.popEvents()

            # Run programme cycles and add their output to the main render buffer
            for programme in self.programmes:
                programme.step(self.ledCoords, self.frameTime, events)
                if programme.brightness > 0:
                    for i, led in enumerate(leds):
                        led[0] += programme.leds[i][0]
                        led[1] += programme.leds[i][1]
                        led[2] += programme.leds[i][2]

            self.renderer.render(leds)

            # TODO: fix target fps sleep time
            # renderTime = time.time() - self.thisFrameTime
            # sleepTime = renderTime - (1 / TARGET_FPS)
            # print(sleepTime)
            # if sleepTime > 0: time.sleep(sleepTime)

            # time.sleep(0.01)
        else:
            time.sleep(0.1)