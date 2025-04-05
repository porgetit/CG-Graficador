# controllers.py
import pygame
from model import ShapeFactory, Canvas

class DrawingController:
    """
    Controlador que coordina la interacción entre modelo y vista.
    """
    def __init__(self, canvas, canvasView):
        self.canvas = canvas
        self.canvasView = canvasView
        # Herramienta actual (por defecto: línea)
        self.currentTool = "LINE"
        # Algoritmo actual ("BASIC" o "PYGAME")
        self.currentAlgorithm = "BASIC"
        # Color del pincel (usado en figuras)
        self.current_color = (0, 0, 0)  # Negro por defecto
        # Grosor del trazo
        self.currentLineWidth = 1
        # Lista temporal de puntos capturados con el mouse
        self.tempPoints = []

    def handleEvent(self, event):
        # Primero se procesa la interacción sobre el lienzo (fuera de la barra de herramientas)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el clic es en el área de dibujo (por ejemplo, y > 50)
            if event.pos[1] > self.canvasView.toolbar_height:
                if event.button == 1:
                    self.tempPoints.append(event.pos)
                elif event.button == 3:
                    self.processShape(event.pos)
        elif event.type == pygame.KEYDOWN:
            # Opciones de teclas que no sean de la barra de herramientas
            if event.key == pygame.K_s:
                self.canvas.saveCanvasBinary(self.canvasView.surface, "canvas.bin")
                print("Canvas guardado en 'canvas.bin' (archivo binario)")
            elif event.key == pygame.K_e:
                try:
                    import matplotlib.pyplot as plt
                    import numpy as np
                    arr = pygame.surfarray.array3d(self.canvasView.surface)
                    arr = np.transpose(arr, (1, 0, 2))
                    plt.imsave("canvas.jpg", arr)
                    print("Canvas exportado a 'canvas.jpg' (imagen JPG)")
                except ImportError:
                    print("Matplotlib o Numpy no están instalados.")

    def processShape(self, pos):
        # Dependiendo de la herramienta, se procesan los puntos capturados
        if self.currentTool in ["LINE", "CIRCLE", "RECTANGLE", "ERASE_AREA"]:
            if len(self.tempPoints) >= 1:
                points = [self.tempPoints[0], pos]
                # Para herramientas de borrado, se usa el color de fondo del lienzo.
                if self.currentTool in ["ERASE_AREA"]:
                    color = self.canvas.background_color
                else:
                    color = self.current_color
                self.createShapeFromInput(points, color, self.currentLineWidth)
        elif self.currentTool in ["POLYGON"]:
            if len(self.tempPoints) >= 2:
                if self.tempPoints[0] != self.tempPoints[-1]:
                    self.tempPoints.append(self.tempPoints[0])
                self.createShapeFromInput(self.tempPoints, self.current_color, self.currentLineWidth)
        elif self.currentTool in ["CURVE"]:
            if len(self.tempPoints) >= 2:
                points = [self.tempPoints[0], self.tempPoints[1], pos]
                self.createShapeFromInput(points, self.current_color, self.currentLineWidth)
        elif self.currentTool in ["ERASE_FREE"]:
            # En borrado libre se consideran todos los puntos
            self.tempPoints.append(pos)
            self.createShapeFromInput(self.tempPoints, self.canvas.background_color, self.currentLineWidth)
        self.tempPoints = []

    def createShapeFromInput(self, points, color, lineWidth):
        shape = ShapeFactory.createShape(self.currentTool, points, color, lineWidth, self.currentAlgorithm)
        self.canvas.addShape(shape)
        self.canvasView.render()

    # Métodos para cambiar herramientas, algoritmo, colores, etc.
    def setTool(self, tool):
        self.currentTool = tool
        print(f"Herramienta seleccionada: {tool}")

    def setAlgorithm(self, algorithm):
        self.currentAlgorithm = algorithm
        print(f"Algoritmo seleccionado: {algorithm}")

    def setBrushColor(self, color):
        self.current_color = color
        print(f"Color del pincel seleccionado: {color}")

    def setCanvasColor(self, color):
        self.canvas.background_color = color
        print(f"Color del lienzo seleccionado: {color}")
        self.canvasView.render()


class EventHandler:
    """
    Clase que delega la gestión de eventos al controlador.
    """
    def __init__(self, controller):
        self.controller = controller

    def processEvent(self, event):
        self.controller.handleEvent(event)
