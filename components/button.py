from pygame_gui.core import ObjectID
import pygame
import pygame_gui

# Tipos de Botones con iconos (btn-type):
# Botón de inicio: #btn-start
# Botón de pausa: #btn-pause
# Botón de reinicio: #btn-restart

class Button:
    def __init__(self, x, y, width, height, text, color=(0, 0, 255), hover_color=(0, 0, 200), active_color=(0, 200, 0), manager=None, btn_type=""):
        self.text = text
        self.color = color #NOTA: innecesario por el momento
        self.hover_color = hover_color #NOTA: innecesario por el momento
        self.active_color = active_color
        self.is_active = False
        self.manager = manager
        self.was_pressed = False

        # Estilado del botón
        if btn_type != "":
            self.object_id = ObjectID(None, btn_type)
            self.text = ""
        else:
            self.object_id = ObjectID(None, None)

        # Crear el botón de pygame_gui
        self.ui_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(x, y, width, height),
            text=self.text,
            manager=self.manager,
            object_id=self.object_id,
            visible=False
        )

    def handle_event(self, event):
        # Verifica si el boton fue presionado usando eventos de pygame_gui
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_button:
                    self.was_pressed = True
                    return True
        return False

    def is_clicked(self, pos):
        # Devuelve True si el botón fue presionado en el frame actual, luego resetea el estado
        was_pressed = self.was_pressed
        self.was_pressed = False
        return was_pressed

    def set_active(self, active):
        # Establece el estado activo del botón
        self.is_active = active
    
    def draw(self, surface):
        self.ui_button.show()
    
    def hide(self):
        self.ui_button.hide()