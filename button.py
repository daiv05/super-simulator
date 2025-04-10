import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(0, 0, 255), hover_color=(0, 0, 200), active_color=(0, 200, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.is_active = False
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine which color to use
        if self.is_active:
            current_color = self.active_color
        else:
            current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Initialize font here
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
    def set_active(self, active):
        self.is_active = active 