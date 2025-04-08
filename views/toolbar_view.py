import os
import pygame

class Button:
    def __init__(self, rect, callback, font, text=None, image=None, bg_color=(200,200,200)):
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self.font = font
        self.text = text
        self.image = image
        self.bg_color = bg_color

    def get_contrast_color(self):
        r, g, b = self.bg_color
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        return (255,255,255) if brightness < 128 else (0,0,0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 1)
        if self.image:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        elif self.text:
            text_color = self.get_contrast_color()
            text_surf = self.font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ToolbarView:
    def __init__(self, controller, surface, height, toolbar_width=100):
        self.controller = controller
        self.surface = surface
        self.toolbar_width = toolbar_width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)
        icons_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
        self.icons = {
            "LINE": pygame.image.load(os.path.join(icons_path, "line.png")),
            "CIRCLE": pygame.image.load(os.path.join(icons_path, "circle.png")),
            "RECTANGLE": pygame.image.load(os.path.join(icons_path, "rect.png")),
            "POLYGON": pygame.image.load(os.path.join(icons_path, "polygon.png")),
            "CURVE": pygame.image.load(os.path.join(icons_path, "curve.png")),
            "ERASE_AREA": pygame.image.load(os.path.join(icons_path, "erase.png"))
        }
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (24,24))
        self.buttons = []
        self.tool_buttons = {}
        self.algo_buttons = {}
        self.file_buttons = {}
        self.brush_color_btn = None
        self.canvas_color_btn = None
        self.createButtons()

    def createButtons(self):
        self.buttons = []
        self.tool_buttons = {}
        self.algo_buttons = {}
        self.file_buttons = {}
        margin = 5
        btn_width = self.toolbar_width - 2 * margin
        btn_height = 30
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
        # Sección de algoritmos
        algos = [("BASIC", "B"), ("PYGAME", "P")]
        for algo, label in algos:
            btn = Button((x, y, btn_width, btn_height),
                         lambda a=algo: self.controller.setAlgorithm(a),
                         self.font, text=label)
            self.buttons.append(btn)
            self.algo_buttons[algo] = btn
            y += btn_height + margin

        y += margin
        # Botón para color del pincel
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setBrushColor(),
                     self.font, text="Pincel", bg_color=self.controller.current_color)
        self.buttons.append(btn)
        self.brush_color_btn = btn
        y += btn_height + margin
        # Botón para color del lienzo
        btn = Button((x, y, btn_width, btn_height),
                     lambda: self.controller.setCanvasColor(),
                     self.font, text="Fondo", bg_color=self.controller.canvas.background_color)
        self.buttons.append(btn)
        self.canvas_color_btn = btn
        y += btn_height + margin

        y += margin
        # Sección de acciones de archivo
        file_actions = [("Guardar", "S"), ("Abrir", "O"), ("Exportar", "E")]
        for action, label in file_actions:
            btn = Button((x, y, btn_width, btn_height),
                         lambda act=action: self.controller.fileAction(act),
                         self.font, text=label)
            self.buttons.append(btn)
            self.file_buttons[action] = btn
            y += btn_height + margin

    def disableAlgorithmButton(self, algo):
        if algo in self.algo_buttons:
            self.algo_buttons[algo].bg_color = (150,150,150)
            self.algo_buttons[algo].callback = lambda: None

    def enableAlgorithmButton(self, algo):
        if algo in self.algo_buttons:
            self.algo_buttons[algo].bg_color = (200,200,200)
            self.algo_buttons[algo].callback = lambda a=algo: self.controller.setAlgorithm(a)

    def updateLayout(self, new_height):
        self.height = new_height
        self.createButtons()

    def draw(self):
        pygame.draw.rect(self.surface, (180,180,180), (0,0,self.toolbar_width,self.height))
        for btn in self.buttons:
            btn.draw(self.surface)
        for tool, btn in self.tool_buttons.items():
            if tool == self.controller.currentTool:
                pygame.draw.rect(self.surface, (255,0,0), btn.rect, 3)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] <= self.toolbar_width:
                for btn in self.buttons:
                    if btn.is_clicked(event.pos):
                        btn.callback()
                        return True
        return False
