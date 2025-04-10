import pygame

class Cashier:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 0, 0)  # Red color for cashiers
        self.current_customer = None
        self.is_available = True
        
    def draw(self, surface):
        # Draw cashier
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Draw status indicator
        status_color = (0, 255, 0) if self.is_available else (255, 0, 0)
        pygame.draw.circle(surface, status_color, 
                         (self.x + self.width//2, self.y - 10), 5)
        
    def serve_customer(self, customer):
        if self.is_available and customer:
            self.current_customer = customer
            self.is_available = False
            customer.is_being_served = True
            return True
        return False
        
    def update(self, dt):
        if self.current_customer:
            if self.current_customer.update(dt):
                self.current_customer = None
                self.is_available = True 