# views.py
import pygame

# --- Clases para la barra de herramientas ---

class Button:
    """
    Botón simple para la barra de herramientas.
    """
    def __init__(self, rect, text, callback, font, bg_color=(200, 200, 200), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 1)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class ToolbarView:
    """
    Barra de herramientas integrada en la parte superior de la ventana.
    Contiene botones para selección de herramienta, algoritmo, y selectores de color.
    """
    def __init__(self, controller, surface, width):
        self.controller = controller
        self.surface = surface
        self.width = width
        self.height = 50  # Altura fija de la barra
        self.font = pygame.font.SysFont(None, 20)
        self.buttons = []
        self.createButtons()

    def createButtons(self):
        margin = 5
        btn_width = 80
        btn_height = 30
        x = margin
        y = (self.height - btn_height) // 2

        # Botones para herramientas
        tools = [("LINE", "LINE"),
                 ("CIRCLE", "CIRCLE"),
                 ("RECT", "RECTANGLE"),
                 ("POLY", "POLYGON"),
                 ("CURVE", "CURVE"),
                 ("E.Area", "ERASE_AREA"),
                 ("E.Free", "ERASE_FREE")]
        for label, tool in tools:
            btn = Button((x, y, btn_width, btn_height), label, lambda t=tool: self.controller.setTool(t), self.font)
            self.buttons.append(btn)
            x += btn_width + margin

        # Botones para algoritmo
        algos = [("BASIC", "BASIC"), ("PYGAME", "PYGAME")]
        for label, algo in algos:
            btn = Button((x, y, btn_width, btn_height), label, lambda a=algo: self.controller.setAlgorithm(a), self.font)
            self.buttons.append(btn)
            x += btn_width + margin

        # Botones para color del pincel (ej.: negro, rojo, verde, azul)
        brush_colors = [((0,0,0), "Negro"), ((255,0,0), "Rojo"), ((0,255,0), "Verde"), ((0,0,255), "Azul")]
        for color, label in brush_colors:
            btn = Button((x, y, btn_width, btn_height), label, lambda c=color: self.controller.setBrushColor(c), self.font, bg_color=color, text_color=(255,255,255))
            self.buttons.append(btn)
            x += btn_width + margin

        # Botones para color del lienzo (fondo)
        canvas_colors = [((255,255,255), "Blanco"), ((220,220,220), "Gris")]
        for color, label in canvas_colors:
            btn = Button((x, y, btn_width, btn_height), label, lambda c=color: self.controller.setCanvasColor(c), self.font, bg_color=color, text_color=(0,0,0))
            self.buttons.append(btn)
            x += btn_width + margin

    def draw(self):
        # Dibuja el fondo de la barra
        pygame.draw.rect(self.surface, (180, 180, 180), (0, 0, self.width, self.height))
        for btn in self.buttons:
            btn.draw(self.surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Solo se consideran clics dentro del área de la barra
            if event.pos[1] <= self.height:
                for btn in self.buttons:
                    if btn.is_clicked(event.pos):
                        btn.callback()
                        return True
        return False


# --- Vista del lienzo ---

class CanvasView:
    """
    Vista encargada de renderizar el lienzo y sus figuras.
    """
    def __init__(self, canvas, surface, toolbar_height=50):
        self.canvas = canvas
        self.surface = surface
        self.toolbar_height = toolbar_height

    def render(self):
        # Rellena únicamente el área del canvas (dejando la barra de herramientas intacta)
        canvas_rect = pygame.Rect(0, self.toolbar_height, self.surface.get_width(), self.surface.get_height() - self.toolbar_height)
        pygame.draw.rect(self.surface, self.canvas.background_color, canvas_rect)
        # Dibuja las figuras en el área del canvas
        for shape in self.canvas.shapes:
            shape.draw(self.surface)
        pygame.display.flip()

    def update(self):
        self.render()


