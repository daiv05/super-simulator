from pygame_gui.core import ObjectID
import pygame
import pygame_gui

class Counter:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, label, manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.manager = manager
        self.enabled = True
        
        # Crear botones para incrementar y decrementar
        self.increment_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y + 5), (height, height)),
            text="+",
            manager=self.manager,
            object_id=ObjectID(None,"#btn-rounded-primary"),
            visible=False
        )
        self.decrement_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x + width - height, y + 5), (height, height)),
            text="-",
            manager=self.manager,
            object_id=ObjectID(None,"#btn-rounded-danger"),
            visible=False,
        )
        
        # Posición de la etiqueta
        self.label_x = x + height + 10
        self.label_y = y
        self.label_width = width - (2 * height) - 20
        
        # Crear fuente para el valor
        self.font = pygame.font.Font(None, 24)

    def set_enabled(self, enabled):
        #Habilita o deshabilita el control y actualiza su apariencia
        self.enabled = enabled
        self.increment_button.enable() if enabled else self.increment_button.disable()
        self.decrement_button.enable() if enabled else self.decrement_button.disable()
        
        # Actualizar el color de los botones para indicar el estado
        color = (0, 0, 0) if enabled else (150, 150, 150)
        self.increment_button.set_text_colour(color)
        self.decrement_button.set_text_colour(color)
        
    def draw(self, surface):
        # Dibujar etiqueta
        font = pygame.font.Font(None, 20)
        label_surface = font.render(self.label, True, (0, 0, 0) if self.enabled else (150, 150, 150))
        label_rect = label_surface.get_rect(center=(self.label_x + self.label_width // 2, self.label_y - 30))
        surface.blit(label_surface, label_rect.topleft)

        # Dibujar botones
        self.increment_button.show()
        self.decrement_button.show()
        
        # Dibujar rectángulo blanco para el valor
        value_rect = pygame.Rect(
            self.label_x + (self.label_width - 40) // 2,  # Centrar horizontalmente
            self.label_y - 20,  # Posicionar justo debajo de la etiqueta
            40,  # Ancho fijo para el rectángulo
            22   # Alto fijo para el rectángulo
        )
        pygame.draw.rect(surface, (255, 255, 255), value_rect)
        # pygame.draw.rect(surface, (0, 0, 0), value_rect, 1)  # Borde negro
        
        # Dibujar el valor centrado en el rectángulo
        value_surface = self.font.render(str(self.value), True, (0, 0, 0) if self.enabled else (150, 150, 150))
        value_text_rect = value_surface.get_rect(center=value_rect.center)
        surface.blit(value_surface, value_text_rect)

    def handle_event(self, event):
        if not self.enabled:
            return False
            
        # Manejar eventos de los botones
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.decrement_button and self.value > self.min_value:
                    self.value -= 1
                    return True
                elif event.ui_element == self.increment_button and self.value < self.max_value:
                    self.value += 1
                    return True
        return False

    def update(self, time_delta):
        # Actualizar el gestor de pygame_gui
        self.manager.update(time_delta)
        
    def get_value(self):
        return self.value
        
    def set_value(self, value):
        self.value = value