# main.py
import sys
import pygame
from model import Canvas
from views import CanvasView, ToolbarView
from controllers import DrawingController, EventHandler

if __name__ == "__main__":
    pygame.init()
    window_width = 800
    window_height = 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Graficador")

    # Inicialización del modelo y las vistas
    canvas = Canvas()
    # La vista del lienzo tiene en cuenta la altura de la barra de herramientas
    toolbar_height = 50
    canvasView = CanvasView(canvas, screen, toolbar_height)
    controller = DrawingController(canvas, canvasView)
    eventHandler = EventHandler(controller)
    toolbarView = ToolbarView(controller, screen, window_width)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Primero se verifica si el evento es para la barra de herramientas
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] <= toolbarView.height:
                toolbarView.handle_event(event)
            else:
                eventHandler.processEvent(event)
        # Redibuja primero la barra y luego el lienzo
        toolbarView.draw()
        canvasView.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
    