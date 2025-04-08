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

    def render(self):
        pygame.draw.rect(self.surface, self.canvas.background_color, self.canvas_rect)
        for shape in self.canvas.shapes:
            shape.drawingAlgorithm.draw(shape, self.surface, self.canvas_rect)
        pygame.display.flip()

    def update(self):
        self.render()
