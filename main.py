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
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Graficador")

    canvas = Canvas()
    toolbar_width = 100
    canvasView = CanvasView(canvas, screen, toolbar_width)
    controller = DrawingController(canvas, canvasView)
    eventHandler = EventHandler(controller)
    toolbarView = ToolbarView(controller, screen, window_height, toolbar_width)
    canvasView.toolbar = toolbarView  # Para que el controlador actualice botones de color

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                toolbarView.updateLayout(window_height)
                canvasView.updateLayout(window_width, window_height, toolbar_width)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] <= toolbarView.toolbar_width:
                toolbarView.handle_event(event)
            else:
                eventHandler.processEvent(event)

        toolbarView.draw()
        canvasView.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


"""
BUG: El color del fondo no se tiene en cuenta al guardar la imagen.
BUG: El trazado sobrepasa el área del lienza y termina pintando sobre la barra de herramientas.
TODO: Mejorar la interfaz de la barra de herramientas para que sea más atractiva y fácil de usar.
TODO: Implementar la herramienta de dibujo a mano alzada. Teniendo en cuenta el grosor del pincel y el color.
TODO: Implementar la herramienta de borrado a mano alzada. Teniendo en cuenta el grosor.
TODO: Implementar la herramienta de relleno. Tener en cuenta algún algoritmo de distribución para relleno de áreas.
TODO: Implementar la herramienta de deshacer. Tener en cuenta el uso de una pila para almacenar los estados anteriores del canvas.
TODO: Implementar la herramienta de rehacer. Tener en cuenta el uso de una pila para almacenar los estados anteriores del canvas.
"""