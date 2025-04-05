# controllers.py
import pygame
from model import ShapeFactory
from model import Canvas

class DrawingController:
    """
    Controlador que gestiona la interacción del usuario y la coordinación
    entre el modelo y la vista.
    """
    def __init__(self, canvas, canvasView, menuView):
        self.canvas = canvas
        self.canvasView = canvasView
        self.menuView = menuView
        self.currentTool = "LINE"  # Herramienta inicial
        self.currentAlgorithm = "BASIC"  # Alternativamente "PYGAME"
        self.tempPoints = []

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo: registra punto
                self.tempPoints.append(event.pos)
            elif event.button == 3:  # Clic derecho: confirma figura
                if self.currentTool in ["LINE", "CIRCLE", "RECTANGLE"]:
                    if len(self.tempPoints) >= 1:
                        points = [self.tempPoints[0], event.pos]
                        self.createShapeFromInput(points, (255, 0, 0), 1)
                elif self.currentTool == "POLYGON":
                    if len(self.tempPoints) >= 2:
                        if self.tempPoints[0] != self.tempPoints[-1]:
                            self.tempPoints.append(self.tempPoints[0])
                        self.createShapeFromInput(self.tempPoints, (0, 255, 0), 1)
                elif self.currentTool == "CURVE":
                    if len(self.tempPoints) >= 2:
                        points = [self.tempPoints[0], self.tempPoints[1], event.pos]
                        self.createShapeFromInput(points, (0, 0, 255), 1)
                self.tempPoints = []
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selectTool("LINE")
                self.menuView.updateMenuSelection("LINE")
            elif event.key == pygame.K_2:
                self.selectTool("CIRCLE")
                self.menuView.updateMenuSelection("CIRCLE")
            elif event.key == pygame.K_3:
                self.selectTool("RECTANGLE")
                self.menuView.updateMenuSelection("RECTANGLE")
            elif event.key == pygame.K_4:
                self.selectTool("POLYGON")
                self.menuView.updateMenuSelection("POLYGON")
            elif event.key == pygame.K_5:
                self.selectTool("CURVE")
                self.menuView.updateMenuSelection("CURVE")
            elif event.key == pygame.K_b:
                self.setAlgorithm("BASIC")
                print("Algoritmo BASIC seleccionado")
            elif event.key == pygame.K_p:
                self.setAlgorithm("PYGAME")
                print("Algoritmo PYGAME seleccionado")
            elif event.key == pygame.K_s:
                # Guardar canvas como archivo binario
                self.canvas.saveCanvasBinary(self.canvasView.surface, "canvas.bin")
                print("Canvas guardado en 'canvas.bin' (archivo binario)")
            elif event.key == pygame.K_e:
                # Exportar canvas a imagen JPG
                try:
                    import matplotlib.pyplot as plt
                    import numpy as np
                    arr = pygame.surfarray.array3d(self.canvasView.surface)
                    arr = np.transpose(arr, (1, 0, 2))
                    plt.imsave("canvas.jpg", arr)
                    print("Canvas exportado a 'canvas.jpg' (imagen JPG)")
                except ImportError:
                    print("Matplotlib o Numpy no están instalados.")

    def selectTool(self, tool):
        self.currentTool = tool

    def setAlgorithm(self, algorithmType):
        self.currentAlgorithm = algorithmType

    def createShapeFromInput(self, points, color, lineWidth):
        shape = ShapeFactory.createShape(self.currentTool, points, color, lineWidth, self.currentAlgorithm)
        self.canvas.addShape(shape)
        self.canvasView.render()


class EventHandler:
    """
    Clase para el manejo de eventos de bajo nivel.
    """
    def __init__(self, controller):
        self.controller = controller

    def processEvent(self, event):
        self.controller.handleEvent(event)
