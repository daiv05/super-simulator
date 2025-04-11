import pygame
import pygame_gui
import sys
from pygame.locals import *
from slider import Slider
from customer import Customer
from cashier import Cashier
from button import Button

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (157, 191, 255)

class Simulation:
    def __init__(self):
        # Create screen after pygame is initialized
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simulación de Supermercado")
        self.clock = pygame.time.Clock()
        self.state = "welcome"
        self.start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50, 200, 50, "Comenzar")
        
        # Create the pygame_gui manager
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), "theme.json")

        # Simulation variables
        self.num_cashiers = 1
        self.max_products = 10
        self.arrival_frequency = 5  # seconds between arrivals
        self.time_since_last_customer = 0
        self.customers = []
        self.cashiers = []
        self.queues = []  # List of lists, one for each cashier
        self.is_running = False
        self.is_paused = False
        
        # Control panel
        self.control_panel_height = 150
        self.sliders = [
            Slider(50, 35, 85, 40, 2, 8, 1, "Cajeros", self.manager),
            Slider(300, 35, 85, 40, 1, 20, 10, "Productos máx", self.manager),
            Slider(550, 35, 85, 40, 1, 10, 5, "Frecuencia", self.manager),
            Slider(50, 100, 85, 40, 1, 5, 2, "Tiempo/prod", self.manager)
        ]
        
        # Control buttons
        self.control_buttons = [
            Button(300, 100, 100, 40, "Iniciar", color=(0, 150, 0), hover_color=(0, 200, 0), active_color=(0, 100, 0)),
            Button(420, 100, 100, 40, "Pausar", color=(150, 150, 0), hover_color=(200, 200, 0), active_color=(100, 100, 0)),
            Button(540, 100, 100, 40, "Reset", color=(150, 0, 0), hover_color=(200, 0, 0))
        ]
        
    def setup_simulation(self):
        self.customers = []
        self.cashiers = []
        self.queues = []
        self.time_since_last_customer = 0
        
        # Create cashiers at the top
        cashier_spacing = (WINDOW_WIDTH - 100) // self.num_cashiers
        for i in range(self.num_cashiers):
            x = 50 + i * cashier_spacing
            self.cashiers.append(Cashier(x, self.control_panel_height + 50))
            self.queues.append([])  # Initialize empty queue for each cashier
            
    def draw_welcome_screen(self):
        self.screen.fill(WHITE)
        
        # Initialize font here
        font = pygame.font.Font(None, 48)
        welcome_text = font.render("Simulación de Colas en Supermercado", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(welcome_text, welcome_rect)
        
        self.start_button.draw(self.screen)
        
    def draw_control_panel(self):
        # Draw control panel background
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.control_panel_height)
        pygame.draw.rect(self.screen, LIGHT_BLUE, panel_rect)
        pygame.draw.line(self.screen, BLACK, (0,self.control_panel_height), (WINDOW_WIDTH,self.control_panel_height), 1)
        
        # Draw sliders
        for slider in self.sliders:
            slider.draw(self.screen)
            
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
            queue_start_y = cashier.y + cashier.height + 20  # Start queue 20 pixels below cashier
            
            for j, customer in enumerate(queue):
                # Calculate position for customer
                customer_x = cashier.x + (cashier.width - customer.width) // 2  # Center customer under cashier
                customer_y = queue_start_y + (j * (customer.height + 10))  # Stack customers vertically
                
                # Update customer position
                customer.update_position(customer_x, customer_y)
                customer.draw(self.screen)
            
    def draw_simulation_screen(self):
        self.screen.fill(WHITE)
        self.draw_control_panel()
        self.draw_simulation()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
                
            if self.state == "welcome":
                if event.type == MOUSEBUTTONDOWN and self.start_button.is_clicked(event.pos):
                    self.state = "simulation"
                    self.setup_simulation()
            else:
                # Handle slider events
                for slider in self.sliders:
                    slider.handle_event(event)
                    
                # Handle control button events
                if event.type == MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.control_buttons):
                        if button.is_clicked(event.pos):
                            if i == 0:  # Start
                                self.is_running = True
                                self.is_paused = False
                                self.control_buttons[0].set_active(True)
                                self.control_buttons[1].set_active(False)
                            elif i == 1:  # Pause
                                self.is_paused = not self.is_paused
                                self.control_buttons[1].set_active(self.is_paused)
                            elif i == 2:  # Reset
                                self.setup_simulation()
                                self.is_running = False
                                self.is_paused = False
                                self.control_buttons[0].set_active(False)
                                self.control_buttons[1].set_active(False)
                                
            # Pass events to pygame_gui manager
            self.manager.process_events(event)
                                
        return True
        
    def update_simulation(self, dt):
        if not self.is_running or self.is_paused:
            return
            
        # Update simulation variables from sliders
        new_num_cashiers = int(self.sliders[0].get_value())
        if new_num_cashiers != self.num_cashiers:
            self.num_cashiers = new_num_cashiers
            print(f"Número de cajeros cambiado a: {self.num_cashiers}")
            self.setup_simulation()
            
        self.max_products = int(self.sliders[1].get_value())
        self.arrival_frequency = int(self.sliders[2].get_value())
        self.time_per_product = self.sliders[3].get_value()
        
        # Generate new customers
        self.time_since_last_customer += dt
        if self.time_since_last_customer >= self.arrival_frequency:
            self.time_since_last_customer = 0
            new_customer = Customer(0, 0, self.max_products, self.time_per_product)
            self.customers.append(new_customer)
            
            # Find shortest queue
            shortest_queue = min(self.queues, key=len)
            shortest_queue.append(new_customer)
            print(f"Nuevo cliente asignado a la cola más corta. Longitud de colas: {[len(q) for q in self.queues]}")
            
        # Update cashiers and serve customers
        for i, queue in enumerate(self.queues):
            cashier = self.cashiers[i]
            if cashier.is_available and queue:  # Si el cajero está disponible y hay clientes en la cola
                customer = queue[0]
                customer.is_being_served = True
                cashier.is_available = False
                print(f"Cliente comenzando a ser atendido en cajero {i+1}. Tiempo de espera previo: {customer.waiting_time:.1f}s")
                
            # Actualizar estado del cliente actual
            if queue and queue[0].is_being_served:
                if queue[0].update(dt):  # Si el cliente ha terminado de ser atendido
                    queue.pop(0)  # Eliminar cliente de la cola
                    cashier.is_available = True
                    print(f"Cliente atendido en cajero {i+1}. Cola actual: {len(queue)} clientes")
            
            cashier.update(dt)
            
        # Update pygame_gui manager
        self.manager.update(dt)
            
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
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()