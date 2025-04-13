import pygame
import random
import os

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
        
        print(f"Nuevo cliente creado: {self.num_products} productos, tiempo por producto: {self.time_per_product}s, tiempo total estimado: {self.serving_time:.1f}s")
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        # Dibujar la imagen del cliente
        screen.blit(self.image, self.rect)
        
        # Dibujar número de productos arriba
        products_text = self.font.render(f"{self.num_products}", True, (0, 0, 0))
        products_rect = products_text.get_rect(centerx=self.rect.centerx, bottom=self.rect.top - 5)
        screen.blit(products_text, products_rect)
        
        # Dibujar tiempo de espera a la derecha
        waiting_text = self.font.render(f"{self.waiting_time:.1f}s", True, (0, 0, 0))
        waiting_rect = waiting_text.get_rect(left=self.rect.right + 5, centery=self.rect.centery)
        screen.blit(waiting_text, waiting_rect)
        
        # Si está siendo atendido, mostrar tiempo de servicio abajo
        if self.is_being_served:
            serving_text = self.font.render(f"{self.time_served:.1f}/{self.serving_time:.1f}s", True, (0, 0, 0))
            serving_rect = serving_text.get_rect(centerx=self.rect.centerx, top=self.rect.bottom + 5)
            screen.blit(serving_text, serving_rect)
            
    def update(self, dt):
        if self.is_being_served:
            self.time_served += dt
            if self.time_served >= self.serving_time:
                print(f"Cliente atendido. Tiempo total: {self.time_served:.1f}s (espera: {self.waiting_time:.1f}s, servicio: {self.serving_time:.1f}s)")
                return True
        else:
            self.waiting_time += dt
            print(f"Cliente en cola. Tiempo de espera: {self.waiting_time:.1f}s")
        return False 