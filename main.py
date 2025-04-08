import sys
import pygame
from models.canvas import Canvas
from views.canvas_view import CanvasView
from views.toolbar_view import ToolbarView
from controllers.super_controller import SuperController

pygame.init()

window_width, window_height = 800, 620
toolbar_width = 80
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


"""
BUG: El sistema de borrado no funciona correctamente. El problema es que en lugar de eliminar las figuras, está pintando sobre ellas. Lo que ocasiona que el canvas internamente conserve información de las figuras que deberían ser borradas.
Posible solución: Cambiar el algoritmo de borrado para que elimine las figuras del canvas en lugar de pintarlas. Esto podría implicar modificar la forma en que se manejan los eventos de borrado y cómo se actualiza el canvas después de cada acción.
"""