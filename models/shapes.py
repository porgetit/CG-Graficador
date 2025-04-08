from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        self.points = points
        self.color = color
        self.lineWidth = lineWidth
        self.drawingAlgorithm = drawingAlgorithm

    @abstractmethod
    def draw(self, surface, canvas_rect):
        pass

    def updatePoints(self, newPoints):
        self.points = newPoints

class Line(Shape):
    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class Circle(Shape): # NOTE: Circle no imprime los puntos teniendo en cuenta el lineWidth si se usa el algoritmo básico. No es un bug, es una limitación del algoritmo.
    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class Rectangle(Shape):
    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class Polygon(Shape):
    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class Curve(Shape):
    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class EraseArea(Shape):
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        super().__init__(points, color, lineWidth, drawingAlgorithm)
        self.erase_color = color

    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class EraseFree(Shape):
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        super().__init__(points, color, lineWidth, drawingAlgorithm)
        self.erase_color = color

    def draw(self, surface, canvas_rect):
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

class ShapeFactory:
    @staticmethod
    def createShape(shapeType, points, color, lineWidth, algorithmType):
        if algorithmType == "PYGAME":
            from models.algorithms import PygameDrawingAlgorithm
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
            elif shapeType == "ERASE_AREA":
                return EraseArea(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        elif algorithmType == "BASIC":
            if shapeType == "LINE":
                from models.algorithms import DDADrawingAlgorithm
                algorithm = DDADrawingAlgorithm()
                return Line(points, color, lineWidth, algorithm)
            elif shapeType == "CIRCLE":
                from models.algorithms import MidpointCircleAlgorithm
                algorithm = MidpointCircleAlgorithm()
                return Circle(points, color, lineWidth, algorithm)
            elif shapeType == "RECTANGLE":
                from models.algorithms import BasicRectangleAlgorithm
                algorithm = BasicRectangleAlgorithm()
                return Rectangle(points, color, lineWidth, algorithm)
            elif shapeType == "POLYGON":
                from models.algorithms import BasicPolygonAlgorithm
                algorithm = BasicPolygonAlgorithm()
                return Polygon(points, color, lineWidth, algorithm)
            elif shapeType == "CURVE":
                from models.algorithms import BezierCurveAlgorithm
                algorithm = BezierCurveAlgorithm()
                return Curve(points, color, lineWidth, algorithm)
            elif shapeType == "ERASE_AREA":
                from models.algorithms import EraseAreaAlgorithm
                algorithm = EraseAreaAlgorithm()
                return EraseArea(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        else:
            raise ValueError("Tipo de algoritmo no reconocido")
