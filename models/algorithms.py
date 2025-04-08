import pygame
import math
from models.shapes import Circle, Line, Rectangle, Polygon, Curve

class DrawingAlgorithm:
    def draw(self, shape, surface, canvas_rect):
        raise NotImplementedError

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
        if len(shape.points) < 3:
            print("Error: Se necesitan al menos 3 puntos para dibujar una curva Bézier.")
            return
        p0, p1, p2 = shape.points[0], shape.points[1], shape.points[2]
        curve_points = []
        steps = 100
        try:
            for i in range(steps + 1):
                t = i / steps
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                curve_points.append((int(x), int(y)))
            for i in range(len(curve_points) - 1):
                if canvas_rect.collidepoint(curve_points[i]) or canvas_rect.collidepoint(curve_points[i + 1]):
                    pygame.draw.line(surface, shape.color, curve_points[i], curve_points[i + 1], shape.lineWidth)
        except Exception as e:
            print(f"Error al dibujar la curva Bézier: {e}")

class PygameDrawingAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        if isinstance(shape, Circle):
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
        points = [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if canvas_rect.collidepoint(px, py):
                surface.set_at((px, py), color)

class BasicRectangleAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
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

class EraseAreaAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        x1, y1 = shape.points[0]
        x2, y2 = shape.points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        rect = rect.clip(canvas_rect)
        pygame.draw.rect(surface, shape.erase_color, rect)

class FreehandEraseAlgorithm(DrawingAlgorithm):
    def draw(self, shape, surface, canvas_rect):
        points = shape.points
        if len(points) < 2:
            return
        filtered_points = [p for p in points if canvas_rect.collidepoint(p)]
        if len(filtered_points) > 1:
            pygame.draw.lines(surface, shape.erase_color, False, filtered_points, shape.lineWidth)
