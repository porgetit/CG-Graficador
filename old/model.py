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

    def draw(self, surface, canvas_rect):
        """Dibuja la figura en la superficie especificada respetando el área del canvas."""
        self.drawingAlgorithm.draw(self, surface, canvas_rect)

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
    def draw(self, shape, surface, canvas_rect):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            if canvas_rect.collidepoint(round(x1), round(y1)):
                pygame.draw.circle(surface, shape.color, (round(x1), round(y1)), max(1, shape.lineWidth // 2))
            return
        xIncrement = dx / steps
        yIncrement = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            if canvas_rect.collidepoint(round(x), round(y)):
                pygame.draw.circle(surface, shape.color, (round(x), round(y)), max(1, shape.lineWidth // 2))
            x += xIncrement
            y += yIncrement


class MidpointCircleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        x_center, y_center = shape.points[0]
        radius = int(math.hypot(shape.points[1][0] - x_center, shape.points[1][1] - y_center))
        x = 0
        y = radius
        d = 1 - radius
        self.draw_circle_points(surface, x_center, y_center, x, y, shape.color, canvas_rect)
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            self.draw_circle_points(surface, x_center, y_center, x, y, shape.color, canvas_rect)

    def draw_circle_points(self, surface, xc, yc, x, y, color, canvas_rect):
        points = [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if canvas_rect.collidepoint(px, py):
                surface.set_at((px, py), color)


class BezierCurveAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        # Verificar que haya al menos tres puntos de control
        if len(shape.points) < 3:
            print("Error: Se necesitan al menos 3 puntos para dibujar una curva Bézier.")
            return

        # Puntos de control
        p0, p1, p2 = shape.points[0], shape.points[1], shape.points[2]
        curve_points = []
        steps = 100  # Número de pasos para calcular los puntos de la curva

        try:
            # Calcular los puntos de la curva usando la fórmula de Bézier cuadrática
            for i in range(steps + 1):
                t = i / steps
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                curve_points.append((int(x), int(y)))

            # Dibujar la curva como una serie de líneas entre los puntos calculados
            for i in range(len(curve_points) - 1):
                if canvas_rect.collidepoint(curve_points[i]) or canvas_rect.collidepoint(curve_points[i + 1]):
                    pygame.draw.line(surface, shape.color, curve_points[i], curve_points[i + 1], shape.lineWidth)
        except Exception as e:
            print(f"Error al dibujar la curva Bézier: {e}")


class PygameDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        if isinstance(shape, Circle):
            # Implementar el algoritmo de punto medio para círculos (similar al BASIC)
            x_center, y_center = shape.points[0]
            radius = int(math.hypot(shape.points[1][0] - x_center, shape.points[1][1] - y_center))
            x = 0
            y = radius
            d = 1 - radius
            self.draw_circle_points(surface, x_center, y_center, x, y, shape.color, canvas_rect)
            while x < y:
                if d < 0:
                    d = d + 2 * x + 3
                else:
                    d = d + 2 * (x - y) + 5
                    y -= 1
                x += 1
                self.draw_circle_points(surface, x_center, y_center, x, y, shape.color, canvas_rect)
        else:
            # Mantener el comportamiento existente para otras figuras
            if isinstance(shape, Line):
                x1, y1 = shape.points[0]
                x2, y2 = shape.points[1]
                pygame.draw.line(surface, shape.color, (x1, y1), (x2, y2), shape.lineWidth)
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

    def draw_circle_points(self, surface, xc, yc, x, y, color, canvas_rect):
        # Dibujar los puntos del círculo respetando los límites del canvas
        points = [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if canvas_rect.collidepoint(px, py):  # Verificar si el punto está dentro del canvas
                surface.set_at((px, py), color)
                    
                    
class BasicRectangleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        # Recortar el rectángulo al área del canvas
        rect = rect.clip(canvas_rect)
        thickness = shape.lineWidth
        pygame.draw.line(surface, shape.color, (rect.left, rect.top), (rect.right, rect.top), thickness)
        pygame.draw.line(surface, shape.color, (rect.right, rect.top), (rect.right, rect.bottom), thickness)
        pygame.draw.line(surface, shape.color, (rect.right, rect.bottom), (rect.left, rect.bottom), thickness)
        pygame.draw.line(surface, shape.color, (rect.left, rect.bottom), (rect.left, rect.top), thickness)


class BasicPolygonAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        points = [p for p in shape.points if canvas_rect.collidepoint(p)]
        if len(points) < 2:
            return
        thickness = shape.lineWidth
        for i in range(len(points) - 1):
            pygame.draw.line(surface, shape.color, points[i], points[i + 1], thickness)

# Algoritmos para borrado (usando el color de fondo)

class EraseAreaAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        # Recortar el rectángulo al área del canvas
        rect = rect.clip(canvas_rect)
        # Usa el color de borrado (color fondo) proporcionado en la figura
        pygame.draw.rect(surface, shape.erase_color, rect)


class FreehandEraseAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        points = shape.points
        if len(points) < 2:
            return
        # Filtrar los puntos que están dentro del canvas
        filtered_points = [p for p in points if canvas_rect.collidepoint(p)]
        if len(filtered_points) > 1:
            pygame.draw.lines(surface, shape.erase_color, False, filtered_points, shape.lineWidth)


# -------------------------------
# Factoría y Lienzo
# -------------------------------

class ShapeFactory:
    """
    Factoría para la creación de figuras según el tipo y algoritmo.
    """
    @staticmethod
    def createShape(shapeType, points, color, lineWidth, algorithmType):
        if algorithmType == "PYGAME":
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
                return EraseArea(points, color, lineWidth, algorithm)
            else:
                raise ValueError("Tipo de figura no reconocido")
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

    def to_json(self):
        """
        Serializa el canvas (la lista de figuras y el color de fondo) a una cadena JSON.
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
        canvas_data = {
            "background_color": self.background_color,  # Guardar el color de fondo
            "shapes": shapes_data
        }
        import json
        return json.dumps(canvas_data)

    def load_json(self, json_str):
        """
        Deserializa una cadena JSON y reconstruye las figuras y el color de fondo del canvas.
        """
        import json
        canvas_data = json.loads(json_str)
        self.background_color = tuple(canvas_data.get("background_color", (255, 255, 255)))  # Cargar el color de fondo
        shapes_data = canvas_data.get("shapes", [])
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
