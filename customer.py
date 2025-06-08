import pygame
import random
import os
from components.tooltip import Tooltip
from utils.name_generator import generar_nombre
class Customer:
    def __init__(self, x, y, max_products, time_per_product):
        self.x = x
        self.y = y
        self.num_products = random.randint(1, max_products)
        self.time_per_product = time_per_product
        self.serving_time = self.num_products * self.time_per_product
        self.time_served = 0
        self.waiting_time = 0
        self.is_being_served = False
        self.name = generar_nombre()
        
        # Cargar imágenes de clientes
        self.images = []
        customer_dir = "assets/customers"
        for filename in os.listdir(customer_dir):
            if filename.endswith(".png"):
                image_path = os.path.join(customer_dir, filename)
                image = pygame.image.load(image_path)
                # Escalar la imagen a un tamaño apropiado
                image = pygame.transform.scale(image, (50, 50))
                self.images.append(image)
        
        # Seleccionar una imagen aleatoria
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Crear fuente para los textos
        self.font = pygame.font.Font(None, 20)
        
        # Determinar si el cliente paga con tarjeta (probabilidad del 30%)
        self.uses_card_payment = random.random() < 0.3

        # Cargar ícono de pago con tarjeta si es necesario
        self.card_icon = None
        if self.uses_card_payment:
            self.card_icon = pygame.image.load("assets/atm-card.png")
            self.card_icon = pygame.transform.scale(self.card_icon, (30, 30))
        
        # Crear tooltip
        self.tooltip = Tooltip(0, 0, "")
        self.update_tooltip_text()
        
        print(f"Nuevo cliente: {self.num_products} productos, tiempo por producto: {self.time_per_product}s, tiempo total estimado: {self.serving_time:.1f}s")
        
    def update_tooltip_text(self):
        """Actualiza el texto del tooltip con la información actual del cliente"""
        text = f"{self.name}\n"
        text += f"Productos: {self.num_products}\n"
        text += f"Espera: {self.waiting_time:.1f}s"
        if self.is_being_served:
            text += f"\nServicio: {self.time_served:.1f}/{self.serving_time:.1f}s"
        self.tooltip.set_text(text)
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        # Actualizar posición del tooltip (al lado derecho del cliente)
        self.tooltip.update_position(self.rect.right - 80, self.rect.top - 90)
        
    def draw(self, screen):
        # Dibujar la imagen del cliente
        screen.blit(self.image, self.rect)
        
        # Dibujar ícono de pago con tarjeta si es necesario
        if self.uses_card_payment and self.card_icon:
            screen.blit(self.card_icon, (self.rect.right - 15, self.rect.top + 20))

        # Dibujar tooltip si está visible
        self.tooltip.draw(screen)
            
    def update(self, dt, simulation_running=True):
        #Actualiza el estado del cliente
        if not simulation_running:
            return False
            
        if self.is_being_served:
            self.time_served += dt
            if self.time_served >= self.serving_time:
                print(f"Cliente atendido. Tiempo total: {self.time_served:.1f}s (espera: {self.waiting_time:.1f}s, servicio: {self.serving_time:.1f}s)")
                return True
        else:
            self.waiting_time += dt
            #print(f"Cliente en cola. Tiempo de espera: {self.waiting_time:.1f}s")
            
        # Actualizar texto del tooltip
        self.update_tooltip_text()
        return False
        
    def handle_mouse_hover(self, mouse_pos):
        #Maneja el hover del mouse sobre el cliente
        if self.rect.collidepoint(mouse_pos):
            self.tooltip.show()
        else:
            self.tooltip.hide()