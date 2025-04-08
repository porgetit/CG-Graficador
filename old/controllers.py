# controllers.py
import pygame
from model import ShapeFactory, Canvas
import tkinter as tk
from tkinter import filedialog
from tk_color_picker import tk_color_picker

class DrawingController:
    def __init__(self, canvas, canvasView):
        self.canvas = canvas
        self.canvasView = canvasView
        self.currentTool = "LINE"
        self.currentAlgorithm = "BASIC"
        self.current_color = (0, 0, 0)
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
                self.saveCanvas()
            elif event.key == pygame.K_e:
                self.exportCanvas()
        # Se pueden agregar otros atajos si se desea

    def processShape(self, pos):
        if self.currentTool in ["LINE", "CIRCLE", "RECTANGLE", "ERASE_AREA"]:
            if len(self.tempPoints) >= 1:
                points = [self.tempPoints[0], pos]
                color = self.canvas.background_color if self.currentTool.startswith("ERASE") else self.current_color
                self.createShapeFromInput(points, color, self.currentLineWidth)
        elif self.currentTool == "POLYGON":
            if len(self.tempPoints) >= 2:
                if self.tempPoints[0] != self.tempPoints[-1]:
                    self.tempPoints.append(self.tempPoints[0])
                self.createShapeFromInput(self.tempPoints, self.current_color, self.currentLineWidth)
        elif self.currentTool == "CURVE":
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
        # Si se selecciona borrado, forzamos BASIC y deshabilitamos PYGAME
        if tool == "ERASE_AREA":
            self.currentAlgorithm = "BASIC"
            if hasattr(self.canvasView, 'toolbar'):
                self.canvasView.toolbar.disableAlgorithmButton("PYGAME")
        else:
            if hasattr(self.canvasView, 'toolbar'):
                self.canvasView.toolbar.enableAlgorithmButton("PYGAME")

    def setAlgorithm(self, algorithm):
        # Si la herramienta es borrado, ignorar PYGAME
        if self.currentTool == "ERASE_AREA" and algorithm != "BASIC":
            print("Para borrado solo se permite el algoritmo BASIC")
            return
        self.currentAlgorithm = algorithm
        print(f"Algoritmo seleccionado: {algorithm}")

    def setBrushColor(self, color=None):
        if color is None:
            new_color, new_thickness = tk_color_picker(self.current_color, self.currentLineWidth, "Elija color de pincel y grosor", show_thickness=True)
            if new_color is not None:
                self.current_color = new_color
                self.currentLineWidth = new_thickness
        else:
            self.current_color = color
        print(f"Color del pincel seleccionado: {self.current_color}, grosor: {self.currentLineWidth}")
        if hasattr(self.canvasView, 'toolbar'):
            self.canvasView.toolbar.brush_color_btn.bg_color = self.current_color

    def setCanvasColor(self, color=None):
        if color is None:
            new_color, _ = tk_color_picker(self.canvas.background_color, self.currentLineWidth, "Elija color de lienzo", show_thickness=False)
            if new_color is not None:
                self.canvas.background_color = new_color
        else:
            self.canvas.background_color = color
        print(f"Color del lienzo seleccionado: {self.canvas.background_color}")
        if hasattr(self.canvasView, 'toolbar'):
            self.canvasView.toolbar.canvas_color_btn.bg_color = self.canvas.background_color
        self.canvasView.render()

    # Métodos para acciones de archivo
    def saveCanvas(self):
        # Abre un diálogo para elegir nombre y ubicación para guardar el canvas en JSON.
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Guardar Canvas",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")]
        )
        root.destroy()
        if file_path:
            json_data = self.canvas.to_json()
            with open(file_path, "w") as f:
                f.write(json_data)
            print(f"Canvas guardado en '{file_path}' (JSON)")

    def exportCanvas(self):
        # Exporta el área del canvas (excluyendo la barra lateral) usando un diálogo para elegir nombre.
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Exportar Canvas",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        root.destroy()
        if file_path:
            # Extrae únicamente el área del canvas definida en canvasView.canvas_rect
            rect = self.canvasView.canvas_rect
            canvas_surface = pygame.Surface((rect.width, rect.height))
            canvas_surface.blit(self.canvasView.surface, (0, 0), rect)
            try:
                import matplotlib.pyplot as plt
                import numpy as np
                arr = pygame.surfarray.array3d(canvas_surface)
                arr = np.transpose(arr, (1, 0, 2))
                plt.imsave(file_path, arr)
                print(f"Canvas exportado a '{file_path}' (imagen)")
            except ImportError:
                print("Matplotlib o Numpy no están instalados.")

    def openCanvas(self):
        # Abre un diálogo para que el usuario seleccione el archivo JSON a abrir.
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Abrir Canvas",
            filetypes=[("Archivos JSON", "*.json")]
        )
        root.destroy()
        if file_path:
            try:
                with open(file_path, "r") as f:
                    json_data = f.read()
                self.canvas.load_json(json_data)
                self.canvasView.render()
                print(f"Canvas abierto desde '{file_path}'")
            except Exception as e:
                print("Error al abrir el canvas:", e)

    def fileAction(self, action):
        if action == "Guardar":
            self.saveCanvas()
        elif action == "Abrir":
            self.openCanvas()
        elif action == "Exportar":
            self.exportCanvas()


class EventHandler:
    def __init__(self, controller):
        self.controller = controller

    def processEvent(self, event):
        self.controller.handleEvent(event)
