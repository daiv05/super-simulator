import pygame
import pygame_gui

class InputNumber:
    def __init__(self, x, y, width, height, title, subtitle, initial_value, min_value, max_value, manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.subtitle = subtitle
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.manager = manager
        self.enabled = True
        
        # Crear fuentes
        self.title_font = pygame.font.Font(None, 20)
        self.value_font = pygame.font.Font(None, 24)
        self.subtitle_font = pygame.font.Font(None, 15)
        
        # Crear el rectángulo de entrada
        self.input_rect = pygame.Rect(
            x + (width - 80) // 2,  # Centrar el rectángulo
            y + 20,  # Espacio para el título
            80,  # Ancho fijo del rectángulo
            35   # Alto fijo del rectángulo
        )
        
        # Variable para controlar si el input está activo
        self.active = False
        self.text_input = str(initial_value)
        
    def draw(self, surface):
        # Dibujar título
        title_surface = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.x + self.width//2, y=self.y)
        surface.blit(title_surface, title_rect)
        
        # Dibujar rectángulo blanco para el valor
        pygame.draw.rect(surface, (255, 255, 255), self.input_rect)
        
        # Cambiar color del borde si está activo
        border_color = (0, 150, 255) if self.active else (0, 0, 0) # Azul claro si activo, negro si no
        pygame.draw.rect(surface, border_color, self.input_rect, 2)  # Borde con grosor 2
        
        # Dibujar valor o texto de entrada
        text_to_render = self.text_input if self.active else str(self.value)
        value_surface = self.value_font.render(text_to_render, True, (0, 0, 0))
        value_rect = value_surface.get_rect(center=self.input_rect.center)
        surface.blit(value_surface, value_rect)
        
        # Dibujar subtítulo
        subtitle_surface = self.subtitle_font.render(self.subtitle, True, (0, 0, 0))
        subtitle_rect = subtitle_surface.get_rect(
            centerx=self.x + self.width//2,
            top=self.input_rect.bottom + 5
        )
        surface.blit(subtitle_surface, subtitle_rect)
        
    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
                return True
            else:
                self.active = False
                
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                # Validar y actualizar el valor
                try:
                    new_value = int(self.text_input)
                    if self.min_value <= new_value <= self.max_value:
                        self.value = new_value
                    self.text_input = str(self.value)
                except ValueError:
                    self.text_input = str(self.value)
            elif event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.unicode.isnumeric():
                self.text_input += event.unicode
                # Validar longitud máxima
                if len(self.text_input) > 3:  # Limitar a 3 dígitos
                    self.text_input = self.text_input[:3]
            return True
        return False
        
    def get_value(self):
        return self.value
        
    def set_value(self, value):
        if self.min_value <= value <= self.max_value:
            self.value = value
            self.text_input = str(value)
            
    def set_enabled(self, enabled):
        self.enabled = enabled
