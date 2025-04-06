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
    """Figura: Línea."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Circle(Shape):
    """Figura: Círculo."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Rectangle(Shape):
    """Figura: Rectángulo."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Polygon(Shape):
    """Figura: Polígono."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class Curve(Shape):
    """Figura: Curva."""
    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)
        

class EraseArea(Shape):
    """Figura: Borrado por área (rectángulo relleno con color fondo)."""
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        super().__init__(points, color, lineWidth, drawingAlgorithm)
        self.erase_color = color

    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)


class EraseFree(Shape):
    """Figura: Borrado a mano alzada (trazo libre con color fondo)."""
    def __init__(self, points, color, lineWidth, drawingAlgorithm):
        super().__init__(points, color, lineWidth, drawingAlgorithm)
        self.erase_color = color

    def draw(self, surface):
        self.drawingAlgorithm.draw(self, surface)
        

class DrawingAlgorithm(ABC):
    """
    Clase abstracta para algoritmos de dibujo.
    """
    @abstractmethod
    def draw(self, shape, surface):
        pass


class DDADrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            pygame.draw.circle(surface, shape.color, (round(x1), round(y1)), max(1, shape.lineWidth // 2))
            return
        xIncrement = dx / steps
        yIncrement = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            pygame.draw.circle(surface, shape.color, (round(x), round(y)), max(1, shape.lineWidth // 2))
            x += xIncrement
            y += yIncrement


class MidpointCircleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x_center, y_center = shape.points[0]
        # Calcula el radio como distancia euclidiana entre el centro y el punto de la circunferencia.
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
        steps = 100
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
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        thickness = shape.lineWidth
        pygame.draw.line(surface, shape.color, (rect.left, rect.top), (rect.right, rect.top), thickness)
        pygame.draw.line(surface, shape.color, (rect.right, rect.top), (rect.right, rect.bottom), thickness)
        pygame.draw.line(surface, shape.color, (rect.right, rect.bottom), (rect.left, rect.bottom), thickness)
        pygame.draw.line(surface, shape.color, (rect.left, rect.bottom), (rect.left, rect.top), thickness)


    # def draw_line(self, surface, start, end, color):
    #     x1, y1 = start
    #     x2, y2 = end
    #     dx = x2 - x1
    #     dy = y2 - y1
    #     steps = max(abs(dx), abs(dy))
    #     if steps == 0:
    #         surface.set_at((round(x1), round(y1)), color)
    #         return
    #     xIncrement = dx / steps
    #     yIncrement = dy / steps
    #     x, y = x1, y1
    #     for _ in range(steps + 1):
    #         surface.set_at((round(x), round(y)), color)
    #         x += xIncrement
    #         y += yIncrement


class BasicPolygonAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        points = shape.points
        if len(points) < 2:
            return
        thickness = shape.lineWidth
        for i in range(len(points) - 1):
            pygame.draw.line(surface, shape.color, points[i], points[i+1], thickness)

    # def draw_line(self, surface, start, end, color):
    #     x1, y1 = start
    #     x2, y2 = end
    #     dx = x2 - x1
    #     dy = y2 - y1
    #     steps = max(abs(dx), abs(dy))
    #     if steps == 0:
    #         surface.set_at((round(x1), round(y1)), color)
    #         return
    #     x_inc = dx / steps
    #     y_inc = dy / steps
    #     x, y = x1, y1
    #     for _ in range(steps + 1):
    #         surface.set_at((round(x), round(y)), color)
    #         x += x_inc
    #         y += y_inc


# Algoritmos para borrado (usando el color de fondo)

class EraseAreaAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        # Usa el color de borrado (color fondo) proporcionado en la figura
        pygame.draw.rect(surface, shape.erase_color, rect)


class FreehandEraseAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface):
        points = shape.points
        if len(points) < 2:
            return
        pygame.draw.lines(surface, shape.erase_color, False, points, shape.lineWidth)


# -------------------------------
# Factoría y Lienzo
# -------------------------------

class ShapeFactory:
    """
    Factoría para la creación de figuras según el tipo y algoritmo.
    """
    @staticmethod
    def createShape(shapeType, points, color, lineWidth, algorithmType):
        if algorithmType == "BASIC":
            if shapeType == "LINE":
                from model import DDADrawingAlgorithm
                algorithm = DDADrawingAlgorithm()
                return Line(points, color, lineWidth, algorithm)
            elif shapeType == "CIRCLE":
                from model import MidpointCircleAlgorithm
                algorithm = MidpointCircleAlgorithm()
                return Circle(points, color, lineWidth, algorithm)
            elif shapeType == "RECTANGLE":
                from model import BasicRectangleAlgorithm
                algorithm = BasicRectangleAlgorithm()
                return Rectangle(points, color, lineWidth, algorithm)
            elif shapeType == "POLYGON":
                from model import BasicPolygonAlgorithm
                algorithm = BasicPolygonAlgorithm()
                return Polygon(points, color, lineWidth, algorithm)
            elif shapeType == "CURVE":
                from model import BezierCurveAlgorithm
                algorithm = BezierCurveAlgorithm()
                return Curve(points, color, lineWidth, algorithm)
            elif shapeType == "ERASE_AREA":
                from model import EraseAreaAlgorithm
                algorithm = EraseAreaAlgorithm()
                return EraseArea(points, color, lineWidth, algorithm)
            # elif shapeType == "ERASE_FREE":
            #     from model import FreehandEraseAlgorithm
            #     algorithm = FreehandEraseAlgorithm()
            #     return EraseFree(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        elif algorithmType == "PYGAME":
            from model import PygameDrawingAlgorithm
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
                # Para borrado con PYGAME se dibuja un rectángulo relleno
                return EraseArea(points, color, lineWidth, algorithm)
            elif shapeType == "ERASE_FREE":
                return EraseFree(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
        else:
            raise ValueError("Tipo de algoritmo no reconocido")


class Canvas:
    """
    Clase que representa el lienzo de dibujo.
    """
    def __init__(self):
        self.shapes = []
        self.background_color = (255, 255, 255)  # Color de fondo por defecto

    def addShape(self, shape):
        """Agrega una figura al lienzo."""
        self.shapes.append(shape)

    def removeShape(self, shape):
        """Elimina una figura del lienzo."""
        self.shapes.remove(shape)

    def clear(self):
        """Limpia el lienzo (elimina todas las figuras)."""
        self.shapes.clear()

    def saveCanvasBinary(self, surface, filePath):
        """
        Guarda el arreglo de píxeles del lienzo en un archivo binario.
        (Método antiguo, se mantiene para compatibilidad)
        """
        import pickle
        import pygame.surfarray as surfarray
        arr = surfarray.array3d(surface)
        with open(filePath, "wb") as f:
            pickle.dump(arr, f)
            
    def to_json(self):
        """
        Serializa el canvas (la lista de figuras) a una cadena JSON.
        Se guarda el tipo, puntos, color, grosor y el algoritmo (se usa "BASIC" por defecto).
        """
        shapes_data = []
        for shape in self.shapes:
            shape_type = None
            if isinstance(shape, Line):
                shape_type = "LINE"
            elif isinstance(shape, Circle):
                shape_type = "CIRCLE"
            elif isinstance(shape, Rectangle):
                shape_type = "RECTANGLE"
            elif isinstance(shape, Polygon):
                shape_type = "POLYGON"
            elif isinstance(shape, Curve):
                shape_type = "CURVE"
            elif isinstance(shape, EraseArea):
                shape_type = "ERASE_AREA"
            # Se asume que para todas se usa "BASIC"
            shape_data = {
                "type": shape_type,
                "points": shape.points,
                "color": shape.color,
                "lineWidth": shape.lineWidth,
                "algorithmType": "BASIC"
            }
            shapes_data.append(shape_data)
        import json
        return json.dumps(shapes_data)

    def load_json(self, json_str):
        """
        Deserializa una cadena JSON y reconstruye las figuras del canvas.
        Se limpia el canvas actual y se recrean las figuras usando ShapeFactory.
        """
        import json
        shapes_data = json.loads(json_str)
        self.shapes.clear()
        for data in shapes_data:
            shape_type = data.get("type")
            points = data.get("points")
            color = tuple(data.get("color"))
            lineWidth = data.get("lineWidth")
            algorithmType = data.get("algorithmType", "BASIC")
            # Se usa ShapeFactory para recrear la figura
            shape = ShapeFactory.createShape(shape_type, points, color, lineWidth, algorithmType)
            self.shapes.append(shape)
