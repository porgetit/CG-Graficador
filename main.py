import sys
from models.canvas import Canvas
from views.canvas_view import CanvasView
from views.toolbar_view import ToolbarView
from controllers.super_controller import SuperController


window_width, window_height = 800, 640
toolbar_width = 60


# Modelo
canvas = Canvas()
import pygame
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

# Asegúrate de pasar toolbarView al DrawingController
superController.drawingController.toolbarView = toolbarView

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Procesar eventos de la toolbar
            if not toolbarView.handle_event(event):
                # Si la toolbar no consumió el evento, se pasa al controlador
                superController.eventHandler.processEvent(event)
    
    canvasView.render()
    toolbarView.draw()
    

pygame.quit()
sys.exit()


"""
BUG: El sistema de borrado no funciona correctamente. El problema es que en lugar de eliminar las figuras, está pintando sobre ellas. Lo que ocasiona que el canvas internamente conserve información de las figuras que deberían ser borradas.
Posible solución: Cambiar el algoritmo de borrado para que elimine las figuras del canvas en lugar de pintarlas. Esto podría implicar modificar la forma en que se manejan los eventos de borrado y cómo se actualiza el canvas después de cada acción.
"""