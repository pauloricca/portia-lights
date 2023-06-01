import time
import keyboard

from constants import *
from config import config, loadConfig
from programmes.programmeManager import ProgrammeManager
from renderer import Renderer
from networking.slave import Slave
from networking.master import Master
from events import EventManager

class App:
    renderer: Renderer
    eventManager: EventManager
    programmeManager: ProgrammeManager
    slave: Slave
    master: Master
    ledCoords: list[tuple[float, float, float]]
    isMaster: bool
    isLightController: bool

    lastFrameTime: float
    framecount: int
    totalFrameTime: float


    def __init__(self, isMaster: bool, isLightController=True, isVerbose=False):
        self.isMaster = isMaster
        self.isLightController = isLightController
        self.eventManager = EventManager(self.isMaster)
        self.programmeManager = ProgrammeManager()
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
            if keyboard.is_pressed("enter"): self.ledCoords = config(self.renderer)

            self.renderer.render(
                self.programmeManager.renderProgrammes(
                    self.eventManager.popEvents(),
                    self.ledCoords,
                    self.frameTime
                )
            )

            # TODO: fix target fps sleep time
            # renderTime = time.time() - self.thisFrameTime
            # sleepTime = renderTime - (1 / TARGET_FPS)
            # print(sleepTime)
            # if sleepTime > 0: time.sleep(sleepTime)

            # time.sleep(0.01)
        else:
            time.sleep(0.1)