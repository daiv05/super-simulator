import pygame
import random

class Customer:
    def __init__(self, x, y, max_products, time_per_product):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 50
        self.products = random.randint(1, max_products)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.time_per_product = time_per_product
        self.serving_time = self.products * self.time_per_product
        self.time_served = 0
        self.is_being_served = False
        self.waiting_time = 0  # Tiempo que ha estado esperando en la cola
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, surface):
        # Draw customer body
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Draw products indicator
        font = pygame.font.Font(None, 20)
        products_text = font.render(str(self.products), True, (0, 0, 0))
        text_rect = products_text.get_rect(center=(self.x + self.width//2, self.y - 10))
        surface.blit(products_text, text_rect)
        
        # Draw waiting time on the right side
        waiting_text = font.render(f"{self.waiting_time:.1f}s", True, (0, 0, 0))
        waiting_rect = waiting_text.get_rect(midleft=(self.x + self.width + 5, self.y + self.height//2))
        surface.blit(waiting_text, waiting_rect)
        
        # Draw serving time if being served
        if self.is_being_served:
            time_text = font.render(f"{self.time_served:.1f}s", True, (0, 0, 0))
            time_rect = time_text.get_rect(center=(self.x + self.width//2, self.y + self.height + 10))
            surface.blit(time_text, time_rect)
        
    def update(self, dt):
        if self.is_being_served:
            self.time_served += dt
            if self.time_served >= self.serving_time:
                return True  # Customer is done being served
        else:
            self.waiting_time += dt
        return False 