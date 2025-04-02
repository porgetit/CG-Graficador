
# ============================================================
# SECCIÓN DE MODELADO (MODEL)
# ============================================================
from abc import ABC, abstractmethod

# -------------------------------
# Clases de Figuras y Estrategias
# -------------------------------

class Shape(ABC):
    """
    Clase abstracta que representa una figura drawable.
    
    Atributos:
        points (List): Lista de puntos que definen la figura.
        color (Any): Color de la figura.
        lineWidth (int): Grosor de la línea.
        drawingAlgorithm (DrawingAlgorithm): Algoritmo de dibujo asociado.
    """
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        self.points = points
        self.color = color
        self.lineWidth = lineWidth
        self.drawingAlgorithm = drawingAlgorithm

    @abstractmethod
    def draw(self, surface):
        """
        Dibuja la figura en la superficie especificada.
        """
        pass

    def updatePoints(self, newPoints):
        """
        Actualiza los puntos que definen la figura.
        """
        self.points = newPoints


class Line(Shape):
    """Clase que representa una línea."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Circle(Shape):
    """Clase que representa un círculo."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Rectangle(Shape):
    """Clase que representa un rectángulo."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Polygon(Shape):
    """Clase que representa un polígono."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Curve(Shape):
    """Clase que representa una curva."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class DrawingAlgorithm(ABC):
    """
    Clase abstracta para algoritmos de dibujo.
    
    Las clases concretas deben implementar el método draw.
    """
    @abstractmethod
    def draw(self, shape, surface):
        pass


# Implementaciones concretas de algoritmos de dibujo (sin implementaciones completas)

class DDADrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        pass


class BresenhamDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        pass


class MidpointCircleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        pass


class BezierCurveAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        pass


class PygameDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        pass


# -------------------------------
# Factoría y Lienzo
# -------------------------------

class ShapeFactory:
    """
    Factoría para la creación de figuras.
    
    Método:
        createShape: Crea una instancia de Shape según el tipo de figura y algoritmo.
    """
    @staticmethod
    def createShape(shapeType, points, color, lineWidth, algorithmType):
        if algorithmType == "BASIC":
            if shapeType == "LINE":
                algorithm = DDADrawingAlgorithm()
                return Line(points, color, lineWidth, algorithm)
            elif shapeType == "CIRCLE":
                algorithm = MidpointCircleAlgorithm()
                return Circle(points, color, lineWidth, algorithm)
            elif shapeType == "RECTANGLE":
                algorithm = BresenhamDrawingAlgorithm()
                return Rectangle(points, color, lineWidth, algorithm)
            elif shapeType == "POLYGON":
                algorithm = DDADrawingAlgorithm()  # O elegir otro algoritmo básico
                return Polygon(points, color, lineWidth, algorithm)
            elif shapeType == "CURVE":
                algorithm = BezierCurveAlgorithm()
                return Curve(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        elif algorithmType == "PYGAME":
            algorithm = PygameDrawingAlgorithm()
            if shapeType == "LINE":
                return Line(points, color, lineWidth, algorithm)
            elif shapeType == "CIRCLE":
                return Circle(points, color, lineWidth, algorithm)
            elif shapeType == "RECTANGLE":
                return Rectangle(points, color, lineWidth, algorithm)
            elif shapeType == "POLYGON":
                return Polygon(points, color, lineWidth, algorithm)
            elif shapeType == "CURVE":
                return Curve(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        else:
            raise ValueError("Tipo de algoritmo no reconocido")


class Canvas:
    """
    Clase que representa el lienzo de dibujo, conteniendo múltiples figuras.
    """
    def __init__(self):
        self.shapes = []

    def addShape(self, shape):
        """
        Agrega una figura al lienzo.
        """
        self.shapes.append(shape)

    def removeShape(self, shape):
        """
        Elimina una figura del lienzo.
        """
        self.shapes.remove(shape)

    def clear(self):
        """
        Limpia el lienzo, eliminando todas las figuras.
        """
        self.shapes.clear()

    def saveCanvas(self, filePath):
        """
        Guarda el lienzo en disco.
        """
        pass

    def exportCanvas(self, filePath, format):
        """
        Exporta el lienzo a un archivo en el formato especificado.
        """
        pass


# ============================================================
# SECCIÓN DE CONTROL (CONTROLLER)
# ============================================================

class DrawingController:
    """
    Controlador que gestiona la interacción del usuario y la coordinación
    entre el modelo y la vista.
    """
    def __init__(self, canvas, canvasView, menuView):
        self.canvas = canvas
        self.canvasView = canvasView
        self.menuView = menuView
        self.currentTool = None
        self.currentAlgorithm = "BASIC"  # Alternativamente "PYGAME"

    def handleEvent(self, event):
        """
        Procesa los eventos de entrada (por ejemplo, clics y teclas) y 
        delega acciones en el modelo y la vista.
        """
        pass

    def selectTool(self, tool):
        """
        Actualiza la herramienta actual para el dibujo.
        """
        self.currentTool = tool

    def setAlgorithm(self, algorithmType):
        """
        Establece el algoritmo de dibujo a utilizar.
        """
        self.currentAlgorithm = algorithmType

    def createShapeFromInput(self, points, color, lineWidth):
        """
        Crea una figura utilizando la ShapeFactory y la agrega al lienzo.
        """
        shape = ShapeFactory.createShape(self.currentTool, points, color, lineWidth, self.currentAlgorithm)
        self.canvas.addShape(shape)
        self.canvasView.render()


class EventHandler:
    """
    Clase para el manejo de eventos de bajo nivel.
    """
    def processEvent(self, event):
        """
        Procesa un evento y delega la acción correspondiente al controlador.
        """
        pass


# ============================================================
# SECCIÓN DE VISTA (VIEW)
# ============================================================

class CanvasView:
    """
    Vista responsable de renderizar el lienzo y sus figuras.
    """
    def __init__(self, canvas, surface):
        self.canvas = canvas
        self.surface = surface

    def render(self):
        """
        Renderiza todas las figuras contenidas en el lienzo en la superficie.
        """
        for shape in self.canvas.shapes:
            shape.draw(self.surface)
        # Actualizar la pantalla (por ejemplo, pygame.display.update())
        pass

    def update(self):
        """
        Actualiza la vista, refrescando la pantalla según sea necesario.
        """
        pass


class MenuView:
    """
    Vista encargada de la presentación de menús y opciones de herramientas.
    """
    def displayMenu(self):
        """
        Muestra el menú principal con las herramientas y opciones disponibles.
        """
        pass

    def updateMenuSelection(self, selection):
        """
        Actualiza el menú según la selección del usuario.
        """
        pass
