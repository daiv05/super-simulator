import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
    def draw(self, surface):
        # Draw label
        font = pygame.font.Font(None, 24)
        label_surface = font.render(f"{self.label}: {int(self.value)}", True, (0, 0, 0))
        surface.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Draw slider track
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Calculate handle position
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        
        # Draw handle
        pygame.draw.rect(surface, (0, 0, 255), handle_rect)
        pygame.draw.rect(surface, (0, 0, 0), handle_rect, 2)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
            
    def update_value(self, mouse_x):
        # Calculate new value based on mouse position
        relative_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
        self.value = round(self.value) 