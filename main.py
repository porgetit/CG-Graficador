import sys
import pygame
from models.canvas import Canvas
from views.canvas_view import CanvasView
from views.toolbar_view import ToolbarView
from controllers.super_controller import SuperController

pygame.init()

window_width, window_height = 800, 600
toolbar_width = 100
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("Graficador")

# Modelo
canvas = Canvas()

# Vista
canvasView = CanvasView(canvas, screen, toolbar_width)

# Controlador
superController = SuperController(canvas, canvasView)

# Pasamos directamente el drawingController al constructor de ToolbarView
toolbarView = ToolbarView(
    superController.drawingController,
    screen,
    window_height,
    toolbar_width
)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Aquí podrías actualizar el layout si lo deseas
            pass
        else:
            # Procesar eventos de la toolbar
            if not toolbarView.handle_event(event):
                # Si la toolbar no consumió el evento, se pasa al controlador
                superController.eventHandler.processEvent(event)

    canvasView.render()
    toolbarView.draw()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
