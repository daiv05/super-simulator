import pygame
import pygame_gui

class Select:
    def __init__(self, x, y, width, height, title, options, manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.options = options
        self.selected_option = options[0] if options else ""
        self.manager = manager
        self.enabled = True
        self.is_open = False
        
        # Crear fuentes
        self.title_font = pygame.font.Font(None, 24)
        self.option_font = pygame.font.Font(None, 24)
        
        # Crear el rectángulo principal
        self.select_rect = pygame.Rect(
            x + (width - 150) // 2,  # Centrar el rectángulo
            y + 20,  # Espacio para el título
            150,  # Ancho fijo del rectángulo
            36   # Alto fijo del rectángulo
        )
        
        # Crear el rectángulo para las opciones desplegables
        self.dropdown_rect = pygame.Rect(
            self.select_rect.x,
            self.select_rect.bottom,
            self.select_rect.width,
            len(options) * 36  # Alto basado en número de opciones
        )
        
        # Crear el triángulo para la flecha
        self.arrow_points = [
            (self.select_rect.right - 30, self.select_rect.centery - 5),
            (self.select_rect.right - 20, self.select_rect.centery + 5),
            (self.select_rect.right - 10, self.select_rect.centery - 5)
        ]
        
    def draw(self, surface):
        # Dibujar título
        title_surface = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.x + self.width//2, y=self.y)
        surface.blit(title_surface, title_rect)
        
        # Dibujar rectángulo principal con esquinas redondeadas
        pygame.draw.rect(surface, (255, 255, 255), self.select_rect, border_radius=20)
        pygame.draw.rect(surface, (200, 200, 200), self.select_rect, 1, border_radius=20)
        
        # Dibujar opción seleccionada
        text_surface = self.option_font.render(self.selected_option, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            midleft=(self.select_rect.left + 15, self.select_rect.centery)
        )
        surface.blit(text_surface, text_rect)
        
        # Dibujar flecha
        pygame.draw.polygon(surface, (0, 0, 0), self.arrow_points)
        
        # Si está abierto, dibujar opciones
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + i * 40,
                    self.dropdown_rect.width,
                    40
                )
                # Dibujar fondo de la opción
                pygame.draw.rect(surface, (255, 255, 255), option_rect)
                pygame.draw.rect(surface, (200, 200, 200), option_rect, 1)
                
                # Dibujar texto de la opción
                text_surface = self.option_font.render(option, True, (0, 0, 0))
                text_rect = text_surface.get_rect(
                    midleft=(option_rect.left + 15, option_rect.centery)
                )
                surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se hace clic en el rectángulo principal
            if self.select_rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return True
                
            # Si está abierto y se hace clic en una opción
            if self.is_open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.dropdown_rect.x,
                        self.dropdown_rect.y + i * 40,
                        self.dropdown_rect.width,
                        40
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.is_open = False
                        return True
                        
            # Si se hace clic fuera, cerrar el dropdown
            self.is_open = False
            
        return False
        
    def get_value(self):
        return self.selected_option
        
    def set_value(self, value):
        if value in self.options:
            self.selected_option = value
            
    def set_enabled(self, enabled):
        self.enabled = enabled 