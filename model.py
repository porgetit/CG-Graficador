# model.py
from abc import ABC, abstractmethod
import pygame
import math

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
        """Dibuja la figura en la superficie especificada."""
        pass

    def updatePoints(self, newPoints):
        """Actualiza los puntos que definen la figura."""
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


# Implementaciones concretas de algoritmos de dibujo

class DDADrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            surface.set_at((round(x1), round(y1)), shape.color)
            return
        xIncrement = dx / steps
        yIncrement = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            surface.set_at((round(x), round(y)), shape.color)
            x += xIncrement
            y += yIncrement


class BresenhamDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        # Se podría actualizar de manera similar, pero se recomienda usar el algoritmo de Midpoint.
        x_center, y_center = shape.points[0]
        # Se calcula el radio usando la distancia entre el centro y el segundo punto
        radius = int(math.hypot(shape.points[1][0] - x_center, shape.points[1][1] - y_center))
        x = 0
        y = radius
        d = 3 - 2 * radius

        def draw_circle_points(x_center, y_center, x, y, color):
            surface.set_at((x_center + x, y_center + y), color)
            surface.set_at((x_center - x, y_center + y), color)
            surface.set_at((x_center + x, y_center - y), color)
            surface.set_at((x_center - x, y_center - y), color)
            surface.set_at((x_center + y, y_center + x), color)
            surface.set_at((x_center - y, y_center + x), color)
            surface.set_at((x_center + y, y_center - x), color)
            surface.set_at((x_center - y, y_center - x), color)

        draw_circle_points(x_center, y_center, x, y, shape.color)
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d += 4 * (x - y) + 10
            else:
                d += 4 * x + 6
            draw_circle_points(x_center, y_center, x, y, shape.color)


class MidpointCircleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x_center, y_center = shape.points[0]
        # Calcular el radio como la distancia euclidiana entre el centro y el punto en la circunferencia
        radius = int(math.hypot(shape.points[1][0] - x_center, shape.points[1][1] - y_center))
        x = 0
        y = radius
        d = 1 - radius
        self.draw_circle_points(surface, x_center, y_center, x, y, shape.color)
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            self.draw_circle_points(surface, x_center, y_center, x, y, shape.color)

    def draw_circle_points(self, surface, xc, yc, x, y, color):
        surface.set_at((xc + x, yc + y), color)
        surface.set_at((xc - x, yc + y), color)
        surface.set_at((xc + x, yc - y), color)
        surface.set_at((xc - x, yc - y), color)
        surface.set_at((xc + y, yc + x), color)
        surface.set_at((xc - y, yc + x), color)
        surface.set_at((xc + y, yc - x), color)
        surface.set_at((xc - y, yc - x), color)


class BezierCurveAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        if len(shape.points) < 3:
            return
        p0, p1, p2 = shape.points[0], shape.points[1], shape.points[2]
        points = []
        steps = 100  # Suavizado de la curva
        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            points.append((int(x), int(y)))
        for point in points:
            surface.set_at(point, shape.color)


class PygameDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        if isinstance(shape, Line):
            pygame.draw.line(surface, shape.color, shape.points[0], shape.points[1], shape.lineWidth)
        elif isinstance(shape, Circle):
            # Calcular el radio usando la distancia euclidiana
            x_center, y_center = shape.points[0]
            radius = int(math.hypot(shape.points[1][0] - x_center, shape.points[1][1] - y_center))
            pygame.draw.circle(surface, shape.color, shape.points[0], radius, shape.lineWidth)
        elif isinstance(shape, Rectangle):
            x1, y1 = shape.points[0]
            x2, y2 = shape.points[1]
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(surface, shape.color, rect, shape.lineWidth)
        elif isinstance(shape, Polygon):
            pygame.draw.polygon(surface, shape.color, shape.points, shape.lineWidth)
        elif isinstance(shape, Curve):
            if len(shape.points) >= 3:
                p0, p1, p2 = shape.points[0], shape.points[1], shape.points[2]
                curve_points = []
                steps = 100
                for i in range(steps + 1):
                    t = i / steps
                    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                    curve_points.append((int(x), int(y)))
                if len(curve_points) > 1:
                    pygame.draw.lines(surface, shape.color, False, curve_points, shape.lineWidth)


class BasicRectangleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        p1 = (x1, y1)
        p2 = (x2, y1)
        p3 = (x2, y2)
        p4 = (x1, y2)
        self.draw_line(surface, p1, p2, shape.color)
        self.draw_line(surface, p2, p3, shape.color)
        self.draw_line(surface, p3, p4, shape.color)
        self.draw_line(surface, p4, p1, shape.color)

    def draw_line(self, surface, start, end, color):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            surface.set_at((round(x1), round(y1)), color)
            return
        xInc = dx / steps
        yInc = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            surface.set_at((round(x), round(y)), color)
            x += xInc
            y += yInc


class BasicPolygonAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        points = shape.points
        n = len(points)
        if n < 2:
            return
        for i in range(n - 1):
            self.draw_line(surface, points[i], points[i + 1], shape.color)

    def draw_line(self, surface, start, end, color):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            surface.set_at((round(x1), round(y1)), color)
            return
        xInc = dx / steps
        yInc = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            surface.set_at((round(x), round(y)), color)
            x += xInc
            y += yInc


# -------------------------------
# Factoría y Lienzo
# -------------------------------

class ShapeFactory:
    """
    Factoría para la creación de figuras.
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
                algorithm = BasicRectangleAlgorithm()
                return Rectangle(points, color, lineWidth, algorithm)
            elif shapeType == "POLYGON":
                algorithm = BasicPolygonAlgorithm()
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
        """Agrega una figura al lienzo."""
        self.shapes.append(shape)

    def removeShape(self, shape):
        """Elimina una figura del lienzo."""
        self.shapes.remove(shape)

    def clear(self):
        """Limpia el lienzo, eliminando todas las figuras."""
        self.shapes.clear()

    # La funcionalidad de guardar se implementa como guardado binario del arreglo de píxeles
    def saveCanvasBinary(self, surface, filePath):
        import pickle
        import pygame.surfarray as surfarray
        arr = surfarray.array3d(surface)
        with open(filePath, "wb") as f:
            pickle.dump(arr, f)
