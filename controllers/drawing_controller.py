import pygame
import tkinter as tk
from tkinter import filedialog
from models.shapes import ShapeFactory
from views.color_picker_modal import tk_color_picker

class DrawingController:
    def __init__(self, canvas, canvasView, toolbarView=None):
        """
        Inicializa el controlador de dibujo.

        Args:
            canvas (Canvas): Instancia del modelo Canvas.
            canvasView (CanvasView): Instancia de la vista del canvas.
            toolbarView (ToolbarView, opcional): Instancia de la barra de herramientas.
        """
        self.canvas = canvas
        self.canvasView = canvasView
        self.toolbarView = toolbarView  # Referencia a ToolbarView
        self.currentTool = "LINE"
        self.currentAlgorithm = "BASIC"  # Forzar el uso de algoritmos básicos
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
        """
        Procesa la acción de la herramienta seleccionada en función de la posición dada.

        Args:
            pos (tuple): Coordenadas del punto donde se realiza la acción.
        """
        if self.currentTool == "POLYGON":
            if pygame.mouse.get_pressed()[0]:  # Clic izquierdo
                self.tempPoints.append(pos)
                if len(self.tempPoints) > 1:
                    # Dibuja una línea entre el último punto y el anterior
                    shape = ShapeFactory.createShape(
                        "LINE",
                        self.tempPoints[-2:],
                        self.current_color,
                        self.currentLineWidth,
                        self.currentAlgorithm
                    )
                    self.canvas.addShape(shape)
                    self.canvasView.render()
            elif pygame.mouse.get_pressed()[2]:  # Clic derecho
                if len(self.tempPoints) > 2:
                    # Cierra el polígono uniendo el último punto con el primero
                    self.tempPoints.append(self.tempPoints[0])
                    polygon = ShapeFactory.createShape(
                        "POLYGON",
                        self.tempPoints,
                        self.current_color,
                        self.currentLineWidth,
                        self.currentAlgorithm
                    )
                    self.canvas.addShape(polygon)
                    self.canvasView.render()
                self.tempPoints = []  # Reinicia los puntos temporales
        elif self.currentTool == "ERASE_AREA":
            if len(self.tempPoints) >= 1:
                points = [self.tempPoints[0], pos]
                self.eraseShapesInArea(points)
                self.tempPoints = []  # Reinicia los puntos temporales después de borrar
        else:
            # Mantiene la lógica existente para otras herramientas
            shape = ShapeFactory.createShape(
                self.currentTool,
                self.tempPoints + [pos],
                self.current_color,
                self.currentLineWidth,
                self.currentAlgorithm
            )
            self.canvas.addShape(shape)
            self.canvasView.render()
            self.tempPoints = []  # Reinicia los puntos temporales después de dibujar

    def createShapeFromInput(self, points, color, lineWidth):
        shape = ShapeFactory.createShape(self.currentTool, points, color, lineWidth, self.currentAlgorithm)
        self.canvas.addShape(shape)
        self.canvasView.render()

    def setTool(self, tool):
        self.currentTool = tool
        print(f"Herramienta seleccionada: {tool}")
        if tool == "ERASE_AREA":
            self.currentAlgorithm = "BASIC"
            if hasattr(self.canvasView, 'toolbar'):
                self.canvasView.toolbar.disableAlgorithmButton("PYGAME")
        else:
            if hasattr(self.canvasView, 'toolbar'):
                self.canvasView.toolbar.enableAlgorithmButton("PYGAME")

    def setAlgorithm(self, algorithm):
        if self.currentTool == "ERASE_AREA" and algorithm != "BASIC":
            print("Para borrado solo se permite el algoritmo BASIC")
            return
        self.currentAlgorithm = algorithm
        print(f"Algoritmo seleccionado: {algorithm}")

    def setBrushColor(self):
        """
        Abre el selector de color para el pincel y actualiza el color seleccionado.
        """
        new_color = self.openColorPicker(self.current_color)
        if new_color:
            self.current_color = new_color
            # Actualizar el color de fondo del botón de pincel
            self.toolbarView.brush_color_btn.bg_color = new_color

    def setCanvasColor(self):
        """
        Abre el selector de color para el lienzo y actualiza el color seleccionado.
        """
        new_color = self.openColorPicker(self.canvas.background_color)
        if new_color:
            self.canvas.background_color = new_color
            # Actualizar el color de fondo del botón de lienzo
            self.toolbarView.canvas_color_btn.bg_color = new_color
            self.canvasView.render()

    def saveCanvas(self):
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
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Exportar Canvas",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        root.destroy()
        if file_path:
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

    def openColorPicker(self, initial_color):
        """
        Abre un selector de color y devuelve el color seleccionado.

        Args:
            initial_color (tuple): Color inicial que se mostrará en el selector.

        Returns:
            tuple: Color seleccionado en formato RGB, o None si se cancela.
        """
        new_color, _ = tk_color_picker(initial_color, self.currentLineWidth, "Seleccione un color", show_thickness=False)
        return new_color

    def eraseShapesInArea(self, points):
        """
        Identifica y elimina las figuras que intersectan con el área de borrado.

        Args:
            points (list): Dos puntos que definen el área rectangular de borrado.
        """
        x1, y1 = points[0]
        x2, y2 = points[1]
        erase_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        self.canvas.removeShapesInArea(erase_rect)
        self.canvasView.render()
