import os
import pygame

class Button:
    """
    Clase que representa un botón en la interfaz gráfica.
    """
    def __init__(self, rect, callback, font, text=None, image=None, alt_image=None, bg_color=(200, 200, 200)):
        """
        Inicializa un botón con sus propiedades.

        Args:
            rect (tuple): Coordenadas y tamaño del botón (x, y, ancho, alto).
            callback (function): Función que se ejecutará al presionar el botón.
            font (pygame.font.Font): Fuente para el texto del botón.
            text (str, opcional): Texto que se mostrará en el botón.
            image (pygame.Surface, opcional): Imagen principal que se mostrará en el botón.
            alt_image (pygame.Surface, opcional): Imagen alternativa (por ejemplo, en blanco).
            bg_color (tuple, opcional): Color de fondo del botón (RGB). Por defecto es gris claro.
        """
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self.font = font
        self.text = text
        self.image = image
        self.alt_image = alt_image  # Imagen alternativa (en blanco)
        self.bg_color = bg_color

    def get_contrast_color(self):
        """
        Calcula un color de contraste (blanco o negro) basado en el brillo del color de fondo.

        Returns:
            tuple: Color de contraste en formato RGB.
        """
        r, g, b = self.bg_color
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        return (255, 255, 255) if brightness < 128 else (0, 0, 0)

    def draw(self, surface):
        """
        Dibuja el botón en la superficie proporcionada.

        Args:
            surface (pygame.Surface): Superficie donde se dibujará el botón.
        """
        # Dibujar sombra
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=10)

        # Dibujar fondo del botón
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=10)

        # Dibujar borde del botón
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        # Seleccionar imagen según el brillo del fondo
        if self.image and self.alt_image:
            img = self.alt_image if self.get_contrast_color() == (255, 255, 255) else self.image
            img_rect = img.get_rect(center=self.rect.center)
            surface.blit(img, img_rect)
        elif self.image:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        elif self.text:
            text_color = self.get_contrast_color()
            text_surf = self.font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        """
        Verifica si el botón fue presionado.

        Args:
            pos (tuple): Coordenadas del clic del mouse.

        Returns:
            bool: True si el clic ocurrió dentro del botón, False en caso contrario.
        """
        return self.rect.collidepoint(pos)


class ToolbarView:
    """
    Clase que representa la barra de herramientas lateral.

    Atributos:
        controller (object): Controlador que maneja las acciones de la barra de herramientas.
        surface (pygame.Surface): Superficie donde se dibuja la barra de herramientas.
        toolbar_width (int): Ancho de la barra de herramientas.
        height (int): Altura de la barra de herramientas.
        font (pygame.font.Font): Fuente utilizada para los textos de los botones.
        icons (dict): Diccionario que contiene las imágenes de los botones.
        buttons (list): Lista de botones en la barra de herramientas.
        tool_buttons (dict): Diccionario de botones de herramientas.
        algo_buttons (dict): Diccionario de botones de algoritmos.
        file_buttons (dict): Diccionario de botones de acciones de archivo.
        brush_color_btn (Button): Botón para seleccionar el color del pincel.
        canvas_color_btn (Button): Botón para seleccionar el color del lienzo.
    """
    def __init__(self, controller, surface, height, toolbar_width=100):
        """
        Inicializa la barra de herramientas.

        Args:
            controller (object): Controlador que maneja las acciones de la barra de herramientas.
            surface (pygame.Surface): Superficie donde se dibuja la barra de herramientas.
            height (int): Altura de la barra de herramientas.
            toolbar_width (int, opcional): Ancho de la barra de herramientas. Por defecto es 100.
        """
        self.controller = controller
        self.surface = surface
        self.toolbar_width = toolbar_width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)
        # Cargar los íconos de las herramientas desde la carpeta "icons"
        icons_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
        self.icons = {
            "LINE": pygame.image.load(os.path.join(icons_path, "line.png")),
            "CIRCLE": pygame.image.load(os.path.join(icons_path, "circle.png")),
            "RECTANGLE": pygame.image.load(os.path.join(icons_path, "rect.png")),
            "POLYGON": pygame.image.load(os.path.join(icons_path, "polygon.png")),
            "CURVE": pygame.image.load(os.path.join(icons_path, "curve.png")),
            "ERASE_AREA": pygame.image.load(os.path.join(icons_path, "erase.png")),
            "BRUSH": pygame.image.load(os.path.join(icons_path, "brush.png")),
            "BRUSH_WHITE": pygame.image.load(os.path.join(icons_path, "brush_white.png")),
            "CANVAS": pygame.image.load(os.path.join(icons_path, "canvas.png")),
            "CANVAS_WHITE": pygame.image.load(os.path.join(icons_path, "canvas_white.png")),
            "SAVE": pygame.image.load(os.path.join(icons_path, "save.png")),
            "OPEN": pygame.image.load(os.path.join(icons_path, "open.png")),
            "EXPORT": pygame.image.load(os.path.join(icons_path, "export.png")),
        }
        # Escalar los íconos al tamaño adecuado
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (24, 24))
        self.buttons = []
        self.tool_buttons = {}
        self.algo_buttons = {}
        self.file_buttons = {}
        self.brush_color_btn = None
        self.canvas_color_btn = None
        self.createButtons()

    def createButtons(self):
        """
        Crea y organiza los botones de la barra de herramientas.
        """
        self.buttons = []
        self.tool_buttons = {}
        self.algo_buttons = {}
        self.file_buttons = {}
        margin = 5
        btn_width = self.toolbar_width - 2 * margin
        btn_height = 40
        x = margin
        y = margin

        # Sección de herramientas
        tools = ["LINE", "CIRCLE", "RECTANGLE", "POLYGON", "CURVE", "ERASE_AREA"]
        for tool in tools:
            img = self.icons.get(tool)
            btn = Button((x, y, btn_width, btn_height),
                         lambda t=tool: self.controller.setTool(t),
                         self.font, image=img)
            self.buttons.append(btn)
            self.tool_buttons[tool] = btn
            y += btn_height + margin

        y += margin
        # Sección de algoritmos (comentada)
        # algos = [("BASIC", "B"), ("PYGAME", "P")]
        # for algo, label in algos:
        #     btn = Button((x, y, btn_width, btn_height),
        #                  lambda a=algo: self.controller.setAlgorithm(a),
        #                  self.font, text=label)
        #     self.buttons.append(btn)
        #     self.algo_buttons[algo] = btn
        #     y += btn_height + margin

        y += margin
        # Botón para color del pincel
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setBrushColor(),
                     self.font,
                     image=self.icons["BRUSH"],
                     alt_image=self.icons["BRUSH_WHITE"],
                     bg_color=self.controller.current_color)
        self.buttons.append(btn)
        self.brush_color_btn = btn
        y += btn_height + margin
        # Botón para color del lienzo
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setCanvasColor(),
                     self.font,
                     image=self.icons["CANVAS"],
                     alt_image=self.icons["CANVAS_WHITE"],
                     bg_color=self.controller.canvas.background_color)
        self.buttons.append(btn)
        self.canvas_color_btn = btn
        y += btn_height + margin

        y += margin
        # Sección de acciones de archivo
        file_actions = [("Guardar", "SAVE"), ("Abrir", "OPEN"), ("Exportar", "EXPORT")]
        for action, icon_key in file_actions:
            btn = Button((x, y, btn_width, btn_height),
                         lambda act=action: self.controller.fileAction(act),
                         self.font, image=self.icons[icon_key])
            self.buttons.append(btn)
            self.file_buttons[action] = btn
            y += btn_height + margin

    def disableAlgorithmButton(self, algo):
        """
        Deshabilita un botón de algoritmo específico.

        Args:
            algo (str): Nombre del algoritmo a deshabilitar.
        """
        if algo in self.algo_buttons:
            self.algo_buttons[algo].bg_color = (150, 150, 150)
            self.algo_buttons[algo].callback = lambda: None

    def enableAlgorithmButton(self, algo):
        """
        Habilita un botón de algoritmo específico.

        Args:
            algo (str): Nombre del algoritmo a habilitar.
        """
        if algo in self.algo_buttons:
            self.algo_buttons[algo].bg_color = (200, 200, 200)
            self.algo_buttons[algo].callback = lambda a=algo: self.controller.setAlgorithm(a)

    def updateLayout(self, new_height):
        """
        Actualiza el diseño de la barra de herramientas cuando cambia la altura.

        Args:
            new_height (int): Nueva altura de la barra de herramientas.
        """
        self.height = new_height
        self.createButtons()

    def draw(self):
        """
        Dibuja la barra de herramientas y sus botones en la superficie.
        """
        pygame.draw.rect(self.surface, (180, 180, 180), (0, 0, self.toolbar_width, self.height))
        for btn in self.buttons:
            btn.draw(self.surface)
        for tool, btn in self.tool_buttons.items():
            if tool == self.controller.currentTool:
                pygame.draw.rect(self.surface, (255, 0, 0), btn.rect, 3, border_radius=10)

    def handle_event(self, event):
        """
        Maneja los eventos de la barra de herramientas.

        Args:
            event (pygame.event.Event): Evento de Pygame.

        Returns:
            bool: True si el evento fue manejado por la barra de herramientas, False en caso contrario.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] <= self.toolbar_width:
                for btn in self.buttons:
                    if btn.is_clicked(event.pos):
                        btn.callback()
                        return True
        return False
