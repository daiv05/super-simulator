from pygame_gui.core import ObjectID
import pygame
import pygame_gui

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label, manager):
        self.label = label
        self.manager = manager
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

        # Crear botones para incrementar y decrementar
        self.increment_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (height, height)),
            text="+",
            manager=self.manager,
            object_id=ObjectID(None,"#btn-rounded-primary"),
            visible=False
        )
        self.decrement_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x + width - height, y), (height, height)),
            text="-",
            manager=self.manager,
            object_id=ObjectID(None,"#btn-rounded-danger"),
            visible=False
        )

        # Posición de la etiqueta
        self.label_x = x + height + 10
        self.label_y = y
        self.label_width = width - (2 * height) - 20

    def draw(self, surface):
        # Dibujar etiqueta
        font = pygame.font.Font(None, 20)
        label_surface = font.render(self.label, True, (0, 0, 0))
        value_surface = font.render(str(self.value), True, (0, 0, 0))
        
        label_rect = label_surface.get_rect(center=(self.label_x + self.label_width // 2, self.label_y - 30))
        value_rect = value_surface.get_rect(center=(self.label_x + self.label_width // 2, self.label_y - 10))
        
        surface.blit(label_surface, label_rect.topleft)
        surface.blit(value_surface, value_rect.topleft)

        # Dibujar botones
        self.increment_button.show()
        self.decrement_button.show()


    def handle_event(self, event):
        # Manejar eventos de los botones
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.decrement_button and self.value > self.min_val:
                    self.value -= 1
                elif event.ui_element == self.increment_button and self.value < self.max_val:
                    self.value += 1

    def update(self, time_delta):
        # Actualizar el gestor de pygame_gui
        self.manager.update(time_delta)

    def get_value(self):
        # Obtener el valor actual
        return self.value
    
    def set_value(self, value):
        # Establecer el valor actual
        self.value = value