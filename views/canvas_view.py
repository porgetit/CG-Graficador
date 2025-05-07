import pygame

class CanvasView:
    def __init__(self, canvas, surface, toolbar_width):
        self.canvas = canvas
        self.surface = surface
        self.toolbar_width = toolbar_width
        self.canvas_rect = pygame.Rect(self.toolbar_width, 0,
                                       self.surface.get_width() - self.toolbar_width,
                                       self.surface.get_height())

    def updateLayout(self, new_width, new_height, toolbar_width):
        self.toolbar_width = toolbar_width
        self.canvas_rect = pygame.Rect(toolbar_width, 0, new_width - toolbar_width, new_height)

    def render(self, preview_rect=None):
        """
        Renderiza el lienzo y opcionalmente un rectángulo de previsualización.

        Args:
            preview_rect (pygame.Rect, opcional): Rectángulo de previsualización.
        """
        # Dibuja el fondo del lienzo
        pygame.draw.rect(self.surface, self.canvas.background_color, self.canvas_rect)

        # Dibuja todas las figuras en el lienzo
        for shape in self.canvas.shapes:
            shape.drawingAlgorithm.draw(shape, self.surface, self.canvas_rect)

        # Dibuja el rectángulo de previsualización si se proporciona
        if preview_rect:
            pygame.draw.rect(self.surface, (200, 200, 200), preview_rect, 2)  # Gris claro con borde

        # Actualiza la pantalla
        pygame.display.flip()

    def update(self):
        self.render()
