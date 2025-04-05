# controllers.py
import pygame
from model import ShapeFactory, Canvas
# Ya no usamos el antiguo color_picker, ahora se usará el modal integrado en views.py

class DrawingController:
    """
    Controlador que coordina la interacción entre modelo y vista.
    """
    def __init__(self, canvas, canvasView):
        self.canvas = canvas
        self.canvasView = canvasView
        self.currentTool = "LINE"
        self.currentAlgorithm = "BASIC"
        self.current_color = (0, 0, 0)  # Negro por defecto
        self.currentLineWidth = 1
        self.tempPoints = []

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > self.canvasView.toolbar_width:
                if event.button == 1:
                    self.tempPoints.append(event.pos)
                elif event.button == 3:
                    self.processShape(event.pos)
        elif event.type == pygame.KEYDOWN:
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
        if self.currentTool in ["LINE", "CIRCLE", "RECTANGLE", "ERASE_AREA"]:
            if len(self.tempPoints) >= 1:
                points = [self.tempPoints[0], pos]
                color = self.canvas.background_color if self.currentTool == "ERASE_AREA" else self.current_color
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
        self.tempPoints = []

    def createShapeFromInput(self, points, color, lineWidth):
        shape = ShapeFactory.createShape(self.currentTool, points, color, lineWidth, self.currentAlgorithm)
        self.canvas.addShape(shape)
        self.canvasView.render()

    def setTool(self, tool):
        self.currentTool = tool
        print(f"Herramienta seleccionada: {tool}")

    def setAlgorithm(self, algorithm):
        self.currentAlgorithm = algorithm
        print(f"Algoritmo seleccionado: {algorithm}")

    def setBrushColor(self, color=None):
        # Si no se pasa un color, se abre el modal de color para el pincel
        if color is None:
            from views import ColorPickerModal  # Importación local para evitar dependencias circulares
            modal = ColorPickerModal(self.canvasView.surface, self.current_color, "Elija color de pincel")
            new_color = modal.run()
            if new_color is not None:
                self.current_color = new_color
        else:
            self.current_color = color
        print(f"Color del pincel seleccionado: {self.current_color}")
        # Actualizar el botón de color del pincel en la vista (si se tiene referencia)
        if hasattr(self.canvasView, 'toolbar'):
            self.canvasView.toolbar.brush_color_btn.bg_color = self.current_color

    def setCanvasColor(self, color=None):
        if color is None:
            from views import ColorPickerModal
            modal = ColorPickerModal(self.canvasView.surface, self.canvas.background_color, "Elija color de lienzo")
            new_color = modal.run()
            if new_color is not None:
                self.canvas.background_color = new_color
        else:
            self.canvas.background_color = color
        print(f"Color del lienzo seleccionado: {self.canvas.background_color}")
        if hasattr(self.canvasView, 'toolbar'):
            self.canvasView.toolbar.canvas_color_btn.bg_color = self.canvas.background_color
        self.canvasView.render()


class EventHandler:
    """
    Clase que delega la gestión de eventos al controlador.
    """
    def __init__(self, controller):
        self.controller = controller

    def processEvent(self, event):
        self.controller.handleEvent(event)
