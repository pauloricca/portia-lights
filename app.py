import time

from constants import *
from config import config, loadConfig
from eventProgrammer import eventProgrammer
from networking.slave import Slave
from networking.master import Master
from events import EventManager
from programmeManager import ProgrammeManager
from renderers.renderer import Renderer
from renderers.ledRenderer import LEDRenderer
from renderers.virtualRenderer import VirtualRenderer

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
        self.lastFrameTime = time.time()
        self.framecount = 0
        self.totalFrameTime = 0

        if self.isMaster:
            # Raspberry pis have mac addresses starting with b8
            self.master = Master(macAddressStartMask = RASPI_MAC_ADDRESS_START, isVerbose=isVerbose)
        else:
            self.slave = Slave(isVerbose=isVerbose)
        
        # Holds the coordinates for each pixel
        isConfigInvalid = False
        try:
            self.ledCoords = loadConfig()
            ledCount = len(self.ledCoords)
        except:
            isConfigInvalid = True
            ledCount = int(input("LED count:\n"))

        self.renderer = LEDRenderer(ledCount) if self.isLightController else VirtualRenderer()

        if (isConfigInvalid):
            self.ledCoords = config(self.renderer, ledCount)

        self.printConfigInfo()

        self.programmeManager = ProgrammeManager(ledCount, self.isMaster)
        self.eventManager = EventManager(self.isMaster, eventProgrammer)

        if self.isMaster:
            self.eventManager.startSequence()

        while True: self.mainLoop()


    def mainLoop(self):
        self.thisFrameTime = time.time()
        self.frameTime = self.thisFrameTime - self.lastFrameTime
        self.lastFrameTime = self.thisFrameTime

        # Print FPS
        # print(str(int(1/self.frameTime)) + "fps")

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

        self.renderer.render(
            self.programmeManager.renderProgrammes(
                self.eventManager.popEvents(),
                self.ledCoords,
                self.frameTime,
                self.eventManager
            ),
            self.ledCoords
        )
            
        # TODO: fix target fps sleep time
        # renderTime = time.time() - self.thisFrameTime
        # sleepTime = renderTime - (1 / TARGET_FPS)
        # print(sleepTime)
        # if sleepTime > 0: time.sleep(sleepTime)

        # Paulo comment sleep
        # time.sleep(0.01)

    
    def printConfigInfo(self):
        print("LED count: " + str(len(self.ledCoords)))
        range = [
            [float("inf"), float("-inf")],
            [float("inf"), float("-inf")],
            [float("inf"), float("-inf")],
        ]
        for ledPos in self.ledCoords:
            for i in [0, 1, 2]:
                if ledPos[i] < range[i][0]:
                    range[i][0] = ledPos[i]
                if ledPos[i] > range[i][1]:
                    range[i][1] = ledPos[i]
        for i, a in enumerate(['X', 'Y', 'Z']):
            print("Config " + a + " range: " + str(range[i][0]) + " to " + str(range[i][1]))
