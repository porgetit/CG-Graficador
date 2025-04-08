# main.py
import sys
import pygame
from models.canvas import Canvas
from views.canvas_view import CanvasView
from views.toolbar_view import ToolbarView
from controllers.super_controller import SuperController

if __name__ == "__main__":
    pygame.init()
    window_width, window_height = 800, 600
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Graficador")

    canvas = Canvas()
    toolbar_width = 100
    canvasView = CanvasView(canvas, screen, toolbar_width)
    toolbarView = ToolbarView(None, screen, window_height, toolbar_width)
    superController = SuperController(canvas, canvasView)
    toolbarView.controller = superController.drawingController

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Actualizar el diseño
                pass
            else:
                superController.eventHandler.processEvent(event)

        toolbarView.draw()
        canvasView.render()
        clock.tick(60)

    pygame.quit()
    sys.exit()


"""
TODO: Mejorar la interfaz de la barra de herramientas para que sea más atractiva y fácil de usar.
TODO: Implementar la herramienta de dibujo a mano alzada. Teniendo en cuenta el grosor del pincel y el color.
TODO: Implementar la herramienta de borrado a mano alzada. Teniendo en cuenta el grosor.
TODO: Implementar la herramienta de relleno. Tener en cuenta algún algoritmo de distribución para relleno de áreas.
TODO: Implementar la herramienta de deshacer. Tener en cuenta el uso de una pila para almacenar los estados anteriores del canvas.
TODO: Implementar la herramienta de rehacer. Tener en cuenta el uso de una pila para almacenar los estados anteriores del canvas.
"""