import pygame
import pygame_gui
import sys
from pygame.locals import *
from components.counter import Counter
from customer import Customer
from cashier import Cashier
from components.button import Button

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (157, 191, 255)

class Simulation:
    def __init__(self):
        # Create screen before initializing UIManager
        pygame.display.set_caption("Simulación de Supermercado")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background_image = pygame.image.load("assets/fondo-supermercado.jpg")
        self.background = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create the pygame_gui manager
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), "theme.json")

        # Initialize buttons after manager
        self.state = "welcome"
        self.start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 120, 250, 50, "INICIAR SIMULACIÓN", manager=self.manager, btn_type="#btn-init")
        
        self.clock = pygame.time.Clock()

        # ------------ Controls the Simulation -------------

        # Control panel height
        self.control_panel_height = 150

        # Control panel
        self.counters = [
            Counter(50, self.control_panel_height/2, 85, 40, 2, 8, 1, "Cajeros", self.manager),
            Counter(150, self.control_panel_height/2, 85, 40, 1, 20, 10, "# Productos", self.manager),
            Counter(250, self.control_panel_height/2, 85, 40, 1, 10, 5, "Frecuencia", self.manager),
            Counter(350, self.control_panel_height/2, 85, 40, 1, 5, 2, "Tiempo/prod", self.manager)
        ]
        
        # Control buttons
        button_width = 60
        button_height = 60
        button_spacing = 20
        total_width = 3 * button_width + 2 * button_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        y_position = 85

        self.control_buttons = [
            Button(start_x, y_position, button_width, button_height, "", color=(0, 150, 0), hover_color=(0, 200, 0), active_color=(0, 100, 0), manager=self.manager, btn_type="#btn-start"),
            Button(start_x + button_width + button_spacing, y_position, button_width, button_height, "", color=(150, 150, 0), hover_color=(200, 200, 0), active_color=(100, 100, 0), manager=self.manager, btn_type="#btn-pause"),
            Button(start_x + 2 * (button_width + button_spacing), y_position, button_width, button_height, "", color=(150, 0, 0), hover_color=(200, 0, 0), active_color=(100, 0, 0), manager=self.manager, btn_type="#btn-reset")
        ]
        
        # ------------  Simulation variables ------------------
        self.num_cashiers = 1
        self.max_products = 10
        self.arrival_frequency = 5  # seconds between arrivals
        self.time_since_last_customer = 0
        self.customers = []
        self.cashiers = []
        self.queues = []  # List of lists, one for each cashier
        self.is_running = False
        self.is_paused = False
        self.total_simulation_time = 0.0  # Para el tiempo total

        # Crear UILabel para mostrar el tiempo total
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WINDOW_WIDTH//2 - 62, 40, 125, 30)),
            text="00:00:0",
            manager=self.manager,
            visible=False,
            object_id="#time_label"
        )
        
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            running = self.handle_events()
            
            if self.state == "welcome":
                self.draw_welcome_screen()
            else:
                self.update_simulation(dt)
                self.draw_simulation_screen()
            
            # Draw pygame_gui elements
            self.manager.draw_ui(self.screen)
            self.manager.update(dt)  # Actualizar el gestor para que los botones se dibujen correctamente
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            # Pasar eventos a pygame_gui
            self.manager.process_events(event)  
            
            if self.state == "welcome":
                # Manejar clic en el botón de inicio
                if self.start_button.handle_event(event):
                    self.state = "simulation"
                    self.setup_simulation()
            else:
                # Manejar eventos de los contadores
                for counter in self.counters:
                    counter.handle_event(event)
                    
                # Manejar eventos de los botones de control
                for i, button in enumerate(self.control_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Button "Iniciar"
                            self.is_running = True
                            self.is_paused = False
                            self.control_buttons[0].set_active(True)
                            self.control_buttons[1].set_active(False)
                            # Deshabilitar el contador de cajeros
                            self.counters[0].set_enabled(False)
                        elif i == 1:  # Button "Pausar"
                            self.is_running = False
                            self.is_paused = True
                            self.control_buttons[0].set_active(False)
                            self.control_buttons[1].set_active(True)
                            # Mantener el contador de cajeros deshabilitado
                            self.counters[0].set_enabled(False)
                        elif i == 2:  # Button "Reset"
                            # Restablecer valores de los contadores
                            self.counters[0].set_value(1)  # Cajeros
                            self.counters[1].set_value(10)  # Productos
                            self.counters[2].set_value(5)   # Frecuencia
                            self.counters[3].set_value(2)   # Tiempo/prod
                            
                            self.setup_simulation()
                            self.is_running = False
                            self.is_paused = False
                            self.total_simulation_time = 0.0  # Reiniciar el tiempo
                            self.time_label.set_text("00:00:0")  # Actualizar el texto
                            self.control_buttons[0].set_active(False)
                            self.control_buttons[1].set_active(False)
                            # Habilitar el contador de cajeros
                            self.counters[0].set_enabled(True)
                            
            # Manejar hover del mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar hover sobre clientes en todas las colas
                for queue in self.queues:
                    for customer in queue:
                        customer.handle_mouse_hover(mouse_pos)
            
        return True

    def setup_simulation(self):
        self.customers = []
        self.cashiers = []
        self.queues = []
        self.time_since_last_customer = 0
        
        # Create cashiers at the top with proper spacing for images
        cashier_spacing = (WINDOW_WIDTH - 200) // self.num_cashiers  # Aumentamos el espaciado para las imágenes
        for i in range(self.num_cashiers):
            x = 100 + i * cashier_spacing  # Ajustamos la posición inicial
            self.cashiers.append(Cashier(x, self.control_panel_height + 50, i))
            self.queues.append([])  # Initialize empty queue for each cashier
            
    def draw_welcome_screen(self):
        self.screen.fill(WHITE)
        image_path = pygame.image.load("assets/logo-minerva.png")
        image_width, image_height = image_path.get_size()
        
        # Center the image horizontally and vertically
        x_position = (WINDOW_WIDTH - image_width) // 2
        y_position = (WINDOW_HEIGHT - image_height) // 2 - 100  # Adjust vertical position
        self.screen.blit(image_path, (x_position, y_position))

        # Initialize font here
        font = pygame.font.Font(None, 48)
        welcome_text = font.render("Simulación de Clientes en Supermercado", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(WINDOW_WIDTH//2, y_position + image_height + 50))  # Adjust vertical spacing
        self.screen.blit(welcome_text, welcome_rect)

        
        self.start_button.draw(self.screen)
        
    def draw_control_panel(self):
        # Draw control panel background
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.control_panel_height)
        pygame.draw.rect(self.screen, LIGHT_BLUE, panel_rect)
        pygame.draw.line(self.screen, BLACK, (0,self.control_panel_height), (WINDOW_WIDTH,self.control_panel_height), 1)
        
        # Hide the start button
        self.start_button.hide()

        # Draw title time label
        title_font = pygame.font.Font(None, 30)
        title_text = title_font.render("Tiempo Total", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 25))
        self.screen.blit(title_text, title_rect)

        # Draw time label
        self.time_label.show()

        # Convertir tiempo total a MM:SS:MS
        total_seconds = self.total_simulation_time
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)  # Parte decimal a milisegundos
        time_str = f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{milliseconds}"
        
        # Actualizar el texto del UILabel
        self.time_label.set_text(time_str)

        # Draw counters
        for counter in self.counters:
            counter.draw(self.screen)
            
        # Draw control buttons
        for button in self.control_buttons:
            button.draw(self.screen)
            
    def draw_simulation(self):
        # Draw cashiers
        for cashier in self.cashiers:
            cashier.draw(self.screen)
            
        # Draw queues
        for i, queue in enumerate(self.queues):
            cashier = self.cashiers[i]
            queue_start_y = cashier.rect.bottom + 20  # Start queue 20 pixels below cashier image
            
            for j, customer in enumerate(queue):
                # Calculate position for customer
                customer_x = cashier.rect.centerx - (customer.rect.width // 2)  # Center customer under cashier
                customer_y = queue_start_y + (j * (customer.rect.height + 30))  # Stack customers vertically with more spacing
                
                # Update customer position
                customer.update_position(customer_x, customer_y)
                customer.draw(self.screen)
            
    def draw_simulation_screen(self):
        self.screen.fill(WHITE)
        self.draw_control_panel()
        self.draw_simulation()
        
    def update_simulation(self, dt):
        if not self.is_running or self.is_paused:
            return

        # Actualizar el tiempo total
        self.total_simulation_time += dt
        
        # Convertir tiempo total a MM:SS:MS
        total_seconds = self.total_simulation_time
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 10)  # Parte decimal a milisegundos
        time_str = f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{milliseconds}"
        
        # Actualizar el texto del UILabel
        self.time_label.set_text(time_str)
            
        # Update simulation variables from counters
        new_num_cashiers = int(self.counters[0].get_value())
        if new_num_cashiers != self.num_cashiers:
            self.num_cashiers = new_num_cashiers
            print(f"Número de cajeros cambiado a: {self.num_cashiers}")
            self.setup_simulation()
            
        self.max_products = int(self.counters[1].get_value())
        self.arrival_frequency = int(self.counters[2].get_value())
        self.time_per_product = self.counters[3].get_value()
        
        # Generate new customers
        self.time_since_last_customer += dt
        if self.time_since_last_customer >= self.arrival_frequency:
            self.time_since_last_customer = 0
            # Find shortest queue
            shortest_queue = min(self.queues, key=len)
            shortest_queue_index = self.queues.index(shortest_queue)
            
            # Create new customer at the end of the shortest queue
            if len(shortest_queue) > 0:
                last_customer = shortest_queue[-1]
                new_x = last_customer.x
                new_y = last_customer.y + 60
            else:
                cashier = self.cashiers[shortest_queue_index]
                new_x = cashier.rect.centerx - 25  # Center under cashier
                new_y = cashier.rect.bottom + 20
                
            new_customer = Customer(new_x, new_y, self.max_products, self.time_per_product)
            shortest_queue.append(new_customer)
            print(f"Nuevo cliente añadido a la cola {shortest_queue_index + 1}")
            
        # Update customers in queues
        for i, queue in enumerate(self.queues):
            cashier = self.cashiers[i]
            if cashier.is_available and queue:  # Si el cajero está disponible y hay clientes en la cola
                customer = queue[0]
                customer.is_being_served = True
                cashier.is_available = False
                print(f"Cliente comenzando a ser atendido en cajero {i+1}. Tiempo de espera previo: {customer.waiting_time:.1f}s")
                
            # Actualizar estado del cliente actual
            if queue and queue[0].is_being_served:
                if queue[0].update(dt, True):  # Cliente ha terminado
                    queue.pop(0)  # Eliminar cliente de la cola
                    cashier.is_available = True
                    print(f"Cliente atendido en cajero {i+1}. Cola actual: {len(queue)} clientes")
            
            # Actualizar el resto de clientes en la cola
            for customer in queue[1:]:
                customer.update(dt, True)
            
        # Update pygame_gui manager
        self.manager.update(dt)
