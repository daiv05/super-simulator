import pygame

class Tooltip:
    def __init__(self, x, y, text, font_size=20):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.visible = False
        self.padding = 10
        self.arrow_size = 0
        self.background_color = (100, 100, 100)  # Gris oscuro
        self.text_color = (255, 255, 255)  # Texto blanco
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        
    def set_text(self, text):
        self.text = text
        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        
    def draw(self, surface):
        if not self.visible:
            return
            
        # Renderizar el texto
        text_lines = self.text.split('\n')
        text_surfaces = [self.font.render(line, True, self.text_color) for line in text_lines]
        
        # Calcular el ancho y alto máximo del texto
        max_width = max(surface.get_width() for surface in text_surfaces)
        total_height = sum(surface.get_height() for surface in text_surfaces)
        line_spacing = 2
        total_height += (len(text_lines) - 1) * line_spacing
        
        # Crear el rectángulo del fondo con espacio para la flecha
        bg_width = max_width + 2 * self.padding
        bg_height = total_height + 2 * self.padding
        
        # Puntos para el polígono (incluyendo la flecha)
        points = [
            (self.x + self.arrow_size, self.y),  # Punta izquierda
            (self.x, self.y + bg_height//2),  # Punta de la flecha
            (self.x + self.arrow_size, self.y + bg_height),  # Esquina inferior izquierda
            (self.x + self.arrow_size + bg_width, self.y + bg_height),  # Esquina inferior derecha
            (self.x + self.arrow_size + bg_width, self.y)  # Esquina superior derecha
        ]
        
        # Dibujar el fondo con la flecha
        pygame.draw.polygon(surface, self.background_color, points)
        
        # Dibujar el texto
        y_offset = self.y + self.padding
        for text_surface in text_surfaces:
            x_pos = self.x + self.arrow_size + self.padding
            surface.blit(text_surface, (x_pos, y_offset))
            y_offset += text_surface.get_height() + line_spacing 