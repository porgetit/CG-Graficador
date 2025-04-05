# color_picker.py
import pygame

def color_picker(surface, initial_color=(255, 255, 255), prompt="Elija un color"):
    """
    Muestra un diálogo modal para seleccionar un color usando tres sliders (R, G, B).
    Retorna el color seleccionado (r, g, b).
    """
    clock = pygame.time.Clock()
    screen_width, screen_height = surface.get_size()
    picker_width, picker_height = 400, 300
    picker_rect = pygame.Rect((screen_width - picker_width) // 2,
                              (screen_height - picker_height) // 2,
                              picker_width, picker_height)
    
    slider_width, slider_height = 300, 20
    slider_x = picker_rect.x + 50
    slider_y_start = picker_rect.y + 80
    slider_gap = 40

    r_val, g_val, b_val = initial_color
    button_rect = pygame.Rect(picker_rect.centerx - 50, picker_rect.y + picker_height - 60, 100, 30)
    active_slider = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Verificar si se hace clic en alguno de los sliders:
                for color_name, slider_y in zip(['r', 'g', 'b'],
                                                  [slider_y_start, slider_y_start + slider_gap, slider_y_start + 2*slider_gap]):
                    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
                    if slider_rect.collidepoint(event.pos):
                        active_slider = color_name
                        relative = max(0, min(slider_width, mouse_x - slider_x))
                        val = int((relative / slider_width) * 255)
                        if color_name == 'r':
                            r_val = val
                        elif color_name == 'g':
                            g_val = val
                        elif color_name == 'b':
                            b_val = val
                # Verificar si se hace clic en el botón de confirmación:
                if button_rect.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                active_slider = None
            elif event.type == pygame.MOUSEMOTION:
                if active_slider:
                    mouse_x, _ = event.pos
                    relative = max(0, min(slider_width, mouse_x - slider_x))
                    val = int((relative / slider_width) * 255)
                    if active_slider == 'r':
                        r_val = val
                    elif active_slider == 'g':
                        g_val = val
                    elif active_slider == 'b':
                        b_val = val

        # Dibujar la interfaz del color picker sobre un overlay:
        overlay = pygame.Surface((picker_width, picker_height))
        overlay.fill((240, 240, 240))
        pygame.draw.rect(overlay, (0, 0, 0), overlay.get_rect(), 2)

        font = pygame.font.SysFont(None, 28)
        prompt_surf = font.render(prompt, True, (0, 0, 0))
        prompt_rect = prompt_surf.get_rect(center=(picker_width // 2, 30))
        overlay.blit(prompt_surf, prompt_rect)

        # Dibujar sliders para R, G y B:
        slider_labels = ['R', 'G', 'B']
        for i, label in enumerate(slider_labels):
            y_pos = slider_y_start + i * slider_gap
            slider_rect = pygame.Rect(slider_x, y_pos, slider_width, slider_height)
            pygame.draw.rect(overlay, (200, 200, 200), slider_rect)
            pygame.draw.rect(overlay, (0, 0, 0), slider_rect, 2)
            if label == 'R':
                val = r_val
            elif label == 'G':
                val = g_val
            else:
                val = b_val
            handle_x = slider_x + (val / 255) * slider_width
            handle_rect = pygame.Rect(handle_x - 5, y_pos - 5, 10, slider_height + 10)
            pygame.draw.rect(overlay, (50, 50, 50), handle_rect)
            label_surf = font.render(label, True, (0, 0, 0))
            overlay.blit(label_surf, (slider_x - 30, y_pos))

        # Vista previa del color seleccionado:
        preview_rect = pygame.Rect(picker_width - 70, 50, 50, 50)
        pygame.draw.rect(overlay, (r_val, g_val, b_val), preview_rect)
        pygame.draw.rect(overlay, (0, 0, 0), preview_rect, 2)

        # Botón de confirmación:
        pygame.draw.rect(overlay, (180, 180, 180),
                         (button_rect.x - picker_rect.x, button_rect.y - picker_rect.y,
                          button_rect.width, button_rect.height))
        pygame.draw.rect(overlay, (0, 0, 0),
                         (button_rect.x - picker_rect.x, button_rect.y - picker_rect.y,
                          button_rect.width, button_rect.height), 2)
        button_text = font.render("OK", True, (0, 0, 0))
        btn_text_rect = button_text.get_rect(center=(button_rect.x - picker_rect.x + button_rect.width // 2,
                                                       button_rect.y - picker_rect.y + button_rect.height // 2))
        overlay.blit(button_text, btn_text_rect)

        # Colocar el overlay en el centro de la pantalla:
        surface.blit(overlay, (picker_rect.x, picker_rect.y))
        pygame.display.flip()
        clock.tick(60)

    return (r_val, g_val, b_val)
