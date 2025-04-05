# views.py
import os
import pygame

# --- Clase Button modificada para soportar imágenes ---
class Button:
    def __init__(self, rect, callback, font, text=None, image=None, bg_color=(200, 200, 200)):
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self.font = font
        self.text = text
        self.image = image  # Debe ser un objeto pygame.Surface o None
        self.bg_color = bg_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
        if self.image:
            # Centra la imagen en el botón
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        elif self.text:
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# --- Barra de herramientas lateral con iconos ---
class ToolbarView:
    """
    Barra de herramientas ubicada en el lateral izquierdo.
    Se usan imágenes (PNG) para representar las herramientas, y se agregan
    botones para seleccionar el color del pincel y del fondo.
    """
    def __init__(self, controller, surface, height, toolbar_width=100):
        self.controller = controller
        self.surface = surface
        self.toolbar_width = toolbar_width  # Ancho fijo para la barra lateral
        self.height = height  # Altura total de la ventana
        self.font = pygame.font.SysFont(None, 24)
        # Ruta base para los iconos
        icons_path = os.path.join(os.path.dirname(__file__), "icons")
        # Cargamos los iconos para herramientas
        self.icons = {
            "LINE": pygame.image.load(os.path.join(icons_path, "line.png")),
            "CIRCLE": pygame.image.load(os.path.join(icons_path, "circle.png")),
            "RECTANGLE": pygame.image.load(os.path.join(icons_path, "rect.png")),
            "POLYGON": pygame.image.load(os.path.join(icons_path, "polygon.png")),
            "CURVE": pygame.image.load(os.path.join(icons_path, "curve.png")),
            "ERASE_AREA": pygame.image.load(os.path.join(icons_path, "erase.png"))
        }
        # Escalamos los iconos al tamaño deseado (por ejemplo, 24x24)
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (24, 24))
        self.buttons = []
        self.createButtons()

    def createButtons(self):
        self.buttons = []
        margin = 5
        btn_width = self.toolbar_width - 2 * margin
        btn_height = 30
        x = margin
        y = margin

        # Sección de herramientas: usamos iconos
        tools = ["LINE", "CIRCLE", "RECTANGLE", "POLYGON", "CURVE", "ERASE_AREA"]
        for tool in tools:
            img = self.icons.get(tool)
            btn = Button((x, y, btn_width, btn_height),
                         lambda t=tool: self.controller.setTool(t),
                         self.font, image=img)
            self.buttons.append(btn)
            y += btn_height + margin

        y += margin  # Espacio entre secciones

        # Sección de algoritmo: usamos botones con letras ("B" para BASIC, "P" para PYGAME)
        algos = [("BASIC", "B"), ("PYGAME", "P")]
        for algo, label in algos:
            btn = Button((x, y, btn_width, btn_height),
                         lambda a=algo: self.controller.setAlgorithm(a),
                         self.font, text=label)
            self.buttons.append(btn)
            y += btn_height + margin

        y += margin

        # Botón para color del pincel: el botón muestra el color actual del pincel.
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setBrushColor(),  # Se invoca sin color para abrir el modal
                     self.font, text="Pincel", bg_color=self.controller.current_color)
        self.brush_color_btn = btn  # Guardamos la referencia para actualizar su color
        self.buttons.append(btn)
        y += btn_height + margin

        # Botón para color del lienzo (fondo)
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setCanvasColor(),
                     self.font, text="Fondo", bg_color=self.controller.canvas.background_color)
        self.canvas_color_btn = btn  # Guardamos la referencia para actualizar su color
        self.buttons.append(btn)
        y += btn_height + margin

    def updateLayout(self, new_height):
        """
        Actualiza la altura de la barra según la nueva altura de la ventana.
        """
        self.height = new_height
        self.createButtons()

    def draw(self):
        # Dibuja el fondo de la barra lateral
        pygame.draw.rect(self.surface, (180, 180, 180), (0, 0, self.toolbar_width, self.height))
        for btn in self.buttons:
            btn.draw(self.surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] <= self.toolbar_width:
                for btn in self.buttons:
                    if btn.is_clicked(event.pos):
                        btn.callback()
                        return True
        return False


# --- Vista del lienzo ---
class CanvasView:
    """
    Vista encargada de renderizar el lienzo y sus figuras.
    Se ajusta automáticamente según el tamaño de la ventana y el área reservada para la barra lateral.
    """
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
            shape.draw(self.surface)
        pygame.display.flip()

    def update(self):
        self.render()


# --- Modal de selección de color (ColorPickerModal) ---
class ColorPickerModal:
    """
    Modal emergente para seleccionar un color mediante tres sliders (R, G, B).
    Muestra una vista previa del color actual, y botones Cancelar y Aceptar.
    """
    def __init__(self, surface, initial_color=(255, 255, 255), prompt="Elija un color"):
        self.surface = surface
        self.initial_color = initial_color
        self.current_color = list(initial_color)  # [r, g, b]
        self.prompt = prompt
        self.font = pygame.font.SysFont(None, 28)
        self.width = 400
        self.height = 300
        screen_width, screen_height = surface.get_size()
        self.rect = pygame.Rect((screen_width - self.width) // 2,
                                (screen_height - self.height) // 2,
                                self.width, self.height)
        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = self.rect.x + 50
        self.slider_y_start = self.rect.y + 80
        self.slider_gap = 40
        self.cancel_rect = pygame.Rect(self.rect.x + 50, self.rect.y + self.height - 60, 100, 30)
        self.accept_rect = pygame.Rect(self.rect.x + self.width - 150, self.rect.y + self.height - 60, 100, 30)
        self.active_slider = None
        self.running = True
        self.result = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verificar si se hace clic en alguno de los sliders:
            for color_name, slider_y in zip(['r', 'g', 'b'],
                                              [self.slider_y_start, self.slider_y_start + self.slider_gap, self.slider_y_start + 2 * self.slider_gap]):
                slider_rect = pygame.Rect(self.slider_x, slider_y, self.slider_width, self.slider_height)
                if slider_rect.collidepoint(event.pos):
                    self.active_slider = color_name
                    relative = max(0, min(self.slider_width, mouse_x - self.slider_x))
                    val = int((relative / self.slider_width) * 255)
                    if color_name == 'r':
                        self.current_color[0] = val
                    elif color_name == 'g':
                        self.current_color[1] = val
                    elif color_name == 'b':
                        self.current_color[2] = val
            # Verificar si se hace clic en el botón Cancelar:
            if self.cancel_rect.collidepoint(event.pos):
                self.result = None
                self.running = False
            # Verificar si se hace clic en el botón Aceptar:
            if self.accept_rect.collidepoint(event.pos):
                self.result = tuple(self.current_color)
                self.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active_slider = None
        elif event.type == pygame.MOUSEMOTION:
            if self.active_slider:
                mouse_x, _ = event.pos
                relative = max(0, min(self.slider_width, mouse_x - self.slider_x))
                val = int((relative / self.slider_width) * 255)
                if self.active_slider == 'r':
                    self.current_color[0] = val
                elif self.active_slider == 'g':
                    self.current_color[1] = val
                elif self.active_slider == 'b':
                    self.current_color[2] = val

    def draw(self):
        # Dibuja un overlay semi-transparente
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.surface.blit(overlay, (0, 0))
        # Modal
        modal_surface = pygame.Surface((self.width, self.height))
        modal_surface.fill((240, 240, 240))
        pygame.draw.rect(modal_surface, (0, 0, 0), modal_surface.get_rect(), 2)
        prompt_surf = self.font.render(self.prompt, True, (0, 0, 0))
        prompt_rect = prompt_surf.get_rect(center=(self.width // 2, 30))
        modal_surface.blit(prompt_surf, prompt_rect)
        # Dibujar sliders para R, G, B
        slider_labels = ['R', 'G', 'B']
        for i, label in enumerate(slider_labels):
            y_pos = 80 + i * self.slider_gap
            slider_rect = pygame.Rect(50, y_pos, self.slider_width, self.slider_height)
            pygame.draw.rect(modal_surface, (200, 200, 200), slider_rect)
            pygame.draw.rect(modal_surface, (0, 0, 0), slider_rect, 2)
            val = self.current_color[i]
            handle_x = 50 + (val / 255) * self.slider_width
            handle_rect = pygame.Rect(handle_x - 5, y_pos - 5, 10, self.slider_height + 10)
            pygame.draw.rect(modal_surface, (50, 50, 50), handle_rect)
            label_surf = self.font.render(label, True, (0, 0, 0))
            modal_surface.blit(label_surf, (10, y_pos))
        # Vista previa del color seleccionado
        preview_rect = pygame.Rect(self.width - 70, 50, 50, 50)
        pygame.draw.rect(modal_surface, tuple(self.current_color), preview_rect)
        pygame.draw.rect(modal_surface, (0, 0, 0), preview_rect, 2)
        # Botón Cancelar
        pygame.draw.rect(modal_surface, (180, 180, 180), (50, self.height - 60, 100, 30))
        pygame.draw.rect(modal_surface, (0, 0, 0), (50, self.height - 60, 100, 30), 2)
        cancel_text = self.font.render("Cancelar", True, (0, 0, 0))
        cancel_rect = cancel_text.get_rect(center=(50 + 50, self.height - 60 + 15))
        modal_surface.blit(cancel_text, cancel_rect)
        # Botón Aceptar
        pygame.draw.rect(modal_surface, (180, 180, 180), (self.width - 150, self.height - 60, 100, 30))
        pygame.draw.rect(modal_surface, (0, 0, 0), (self.width - 150, self.height - 60, 100, 30), 2)
        accept_text = self.font.render("Aceptar", True, (0, 0, 0))
        accept_rect = accept_text.get_rect(center=(self.width - 150 + 50, self.height - 60 + 15))
        modal_surface.blit(accept_text, accept_rect)
        # Colocar el modal en la superficie
        self.surface.blit(modal_surface, (self.rect.x, self.rect.y))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
        return self.result
