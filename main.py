# main.py
import sys
import pygame
from model import Canvas
from views import CanvasView, MenuView
from controllers import DrawingController, EventHandler

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Graficador")

    # Inicialización de los componentes
    canvas = Canvas()
    canvasView = CanvasView(canvas, screen)
    menuView = MenuView()
    controller = DrawingController(canvas, canvasView, menuView)
    eventHandler = EventHandler(controller)

    menuView.displayMenu()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                eventHandler.processEvent(event)
        canvasView.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
