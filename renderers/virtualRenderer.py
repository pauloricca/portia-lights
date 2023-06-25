from constants import *
from renderers.renderer import Renderer
from utils import stopAudio
try:
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("pygame and/or opengl library not present (only required when using VirtualRenderer)")

class VirtualRenderer(Renderer):
    xCamRotation: float
    zCamRotation: float
    pointRadius: float
    isRotating: bool

    def __init__(self):
        self.xCamRotation = 0
        self.zCamRotation = 0
        self.pointRadius = 2
        self.isRotating = False

        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        glEnable(GL_DEPTH_TEST)

        gluPerspective(45, self.display[0] / self.display[1], 0.1, 50000.0)

        glTranslatef(VIRTUAL_CAMERA[0], VIRTUAL_CAMERA[1], VIRTUAL_CAMERA[2])
    
    def render(
            self,
            leds: list[tuple[float, float, float]],
            ledCoords: list[tuple[float, float, float]]
        ):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION and self.isRotating:
                self.xCamRotation += event.dict["rel"][0]
                self.zCamRotation += event.dict["rel"][1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.isRotating = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.isRotating = False
            elif event.type == pygame.QUIT:
                stopAudio()
                pygame.quit()
                quit()
        
        glClearDepth(1)

        glPushMatrix()

        glRotatef(self.zCamRotation, 1, 0, 0)
        glRotatef(self.xCamRotation, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        for i in range(len(ledCoords)):
            r = leds[i][0]
            g = leds[i][1]
            b = leds[i][2]

            if r < 0: r = 0
            if g < 0: g = 0
            if b < 0: b = 0

            addToR = 0
            addToG = 0
            addToB = 0

            if r > 255:
                rOver = r - 255
                if rOver > 255: rOver = 255
                addToG = rOver
                addToB = rOver
            
            if g > 255:
                gOver = g - 255
                if gOver > 255: gOver = 255
                addToR = gOver
                addToB = gOver
            
            if b > 255:
                bOver = b - 255
                if bOver > 255: bOver = 255
                addToR = bOver
                addToG = bOver
            
            if addToR > 0: r += addToR
            if addToG > 0: g += addToG
            if addToB > 0: b += addToB

            if r > 255: r = 255
            if g > 255: g = 255
            if b > 255: b = 255

            # Apply 0.5 exponent to get a brightness curve closer to the LEDs (as it's not linear like computer screens)
            r = (r / 255) ** 0.4
            g = (g / 255) ** 0.3
            b = (b / 255) ** 0.2

            glPushMatrix()
            glTranslatef(ledCoords[i][0], ledCoords[i][1], ledCoords[i][2])
            glColor3f(r, g, b)
            gluSphere(gluNewQuadric(), self.pointRadius, 3, 3)
            glPopMatrix()
        
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)