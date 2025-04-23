import pygame
import pygame_gui

class RadioButton:
    def __init__(self, x, y, width, height, title, option1_label, option2_label, manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.option1_label = option1_label
        self.option2_label = option2_label
        self.manager = manager
        self.enabled = True
        self.selected_option = 0  # 0 para primera opción, 1 para segunda opción
        
        # Crear fuentes
        self.title_font = pygame.font.Font(None, 24)
        self.option_font = pygame.font.Font(None, 20)
        
        # Radio button properties
        self.radio_radius = 10
        self.radio_spacing = 40
        
        # Calcular posiciones de los radio buttons
        title_height = 30
        self.radio1_pos = (x + 20, y + title_height + 20)
        self.radio2_pos = (x + 20, y + title_height + 20 + self.radio_spacing)
        
        # Calcular rectángulos para detección de clics
        self.radio1_rect = pygame.Rect(
            self.radio1_pos[0] - self.radio_radius,
            self.radio1_pos[1] - self.radio_radius,
            self.radio_radius * 2,
            self.radio_radius * 2
        )
        self.radio2_rect = pygame.Rect(
            self.radio2_pos[0] - self.radio_radius,
            self.radio2_pos[1] - self.radio_radius,
            self.radio_radius * 2,
            self.radio_radius * 2
        )
        
    def draw(self, surface):
        # Dibujar título
        title_surface = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.x + self.width//2, y=self.y)
        surface.blit(title_surface, title_rect)
        
        # Dibujar primer radio button
        pygame.draw.circle(surface, (255, 255, 255), self.radio1_pos, self.radio_radius)
        pygame.draw.circle(surface, (0, 0, 0), self.radio1_pos, self.radio_radius, 1)
        if self.selected_option == 0:
            pygame.draw.circle(surface, (0, 0, 0), self.radio1_pos, self.radio_radius - 4)
            
        # Dibujar segundo radio button
        pygame.draw.circle(surface, (255, 255, 255), self.radio2_pos, self.radio_radius)
        pygame.draw.circle(surface, (0, 0, 0), self.radio2_pos, self.radio_radius, 1)
        if self.selected_option == 1:
            pygame.draw.circle(surface, (0, 0, 0), self.radio2_pos, self.radio_radius - 4)
            
        # Dibujar labels
        option1_surface = self.option_font.render(self.option1_label, True, (0, 0, 0))
        option2_surface = self.option_font.render(self.option2_label, True, (0, 0, 0))
        
        surface.blit(option1_surface, (self.radio1_pos[0] + 20, self.radio1_pos[1] - 10))
        surface.blit(option2_surface, (self.radio2_pos[0] + 20, self.radio2_pos[1] - 10))
        
    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.radio1_rect.collidepoint(event.pos):
                self.selected_option = 0
                return True
            elif self.radio2_rect.collidepoint(event.pos):
                self.selected_option = 1
                return True
                
        return False
        
    def get_value(self):
        return self.selected_option
        
    def set_value(self, value):
        if value in [0, 1]:
            self.selected_option = value
            
    def set_enabled(self, enabled):
        self.enabled = enabled 