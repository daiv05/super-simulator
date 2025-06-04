import pygame
import random
import os

class Cashier:
    def __init__(self, x, y, index, accepts_card_payment=False):
        self.x = x
        self.y = y
        self.index = index
        self.name = f"CAJA {index + 1}"
        self.is_available = True
        self.current_customer = None
        self.time_serving = 0
        self.accepts_card_payment = True
        
        # Cargar imágenes de cajeros
        self.images = []
        cashier_dir = "assets/cashiers"
        for filename in os.listdir(cashier_dir):
            if filename.endswith(".png"):
                image_path = os.path.join(cashier_dir, filename)
                image = pygame.image.load(image_path)
                # Escalar la imagen a un tamaño apropiado
                image = pygame.transform.scale(image, (100, 100))
                self.images.append(image)
        
        # Seleccionar una imagen aleatoria
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Crear fuente para el nombre
        self.font = pygame.font.Font(None, 24)
        
        # Cargar ícono de pago con tarjeta si es necesario
        self.card_icon = None
        if self.accepts_card_payment:
            self.card_icon = pygame.image.load("assets/atm-card.png")
            self.card_icon = pygame.transform.scale(self.card_icon, (30, 30))
        
    def draw(self, screen):
        # Dibujar el nombre del cajero
        name_text = self.font.render(self.name, True, (0, 0, 0))
        name_rect = name_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 5)
        screen.blit(name_text, name_rect)
        
        # Dibujar la imagen del cajero
        screen.blit(self.image, self.rect)
        
        # Dibujar ícono de pago con tarjeta si es necesario
        if self.accepts_card_payment and self.card_icon:
            screen.blit(self.card_icon, (self.rect.right - 35, self.rect.top - 35))
        
    def update(self, dt):
        if self.current_customer:
            self.time_serving += dt
            if self.time_serving >= self.current_customer.serving_time:
                self.current_customer = None
                self.is_available = True
                self.time_serving = 0
                
    def serve_customer(self, customer):
        if self.is_available:
            self.current_customer = customer
            self.is_available = False
            self.time_serving = 0
            return True
        return False