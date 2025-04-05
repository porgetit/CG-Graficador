# views.py
import pygame

class CanvasView:
    """
    Vista responsable de renderizar el lienzo y sus figuras.
    """
    def __init__(self, canvas, surface):
        self.canvas = canvas
        self.surface = surface

    def render(self):
        """Renderiza todas las figuras contenidas en el lienzo en la superficie."""
        self.surface.fill((255, 255, 255))
        for shape in self.canvas.shapes:
            shape.draw(self.surface)
        pygame.display.flip()

    def update(self):
        self.render()


class MenuView:
    """
    Vista encargada de la presentación de menús y opciones de herramientas.
    """
    def displayMenu(self):
        print("Menú de Herramientas:")
        print("1 - Línea")
        print("2 - Círculo")
        print("3 - Rectángulo")
        print("4 - Polígono")
        print("5 - Curva")
        print("b - Algoritmo BASIC")
        print("p - Algoritmo PYGAME")
        print("s - Guardar canvas (archivo binario)")
        print("e - Exportar canvas a imagen JPG")

    def updateMenuSelection(self, selection):
        print(f"Herramienta seleccionada: {selection}")
