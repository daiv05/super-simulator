import pygame
import pygame_gui
import sys
import random
from pygame.locals import *
from components.counter import Counter
from components.radio_button import RadioButton
from customer import Customer
from cashier import Cashier
from components.button import Button

from components.input_number import InputNumber
from components.select import Select

# Inicializar pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (157, 191, 255)

class Simulation:
    def __init__(self):
        # Crear la pantalla antes de inicializar UIManager
        pygame.display.set_caption("Simulación de Supermercado")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Cargar icono
        icon = pygame.image.load("assets/favicon.png")
        icon = pygame.transform.scale(icon, (32, 32))  # Redimensionar icono
        pygame.display.set_icon(icon)

        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background_image = pygame.image.load("assets/fondo-supermercado.jpg")
        self.background = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Crear el gestor de pygame_gui
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), "theme.json")

        # Inicializar botones después del gestor
        self.state = "welcome"
        self.start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 120, 250, 50, "INICIAR SIMULACIÓN", manager=self.manager, btn_type="#btn-init")
        
        self.clock = pygame.time.Clock()

        self.speed_multiplier = 1.0  # Multiplicador de velocidad de la simulación
        
        # ------------ Controles de la Simulación -------------

        # Altura del panel de control
        self.control_panel_height = 150

        # Layout dinámico horizontal para controles
        x_inicio = 50
        espacio_horizontal = 100
        y_control = self.control_panel_height / 2 - 5

        #Contadores de configuración
        self.counters = [
            Counter(x_inicio + i * espacio_horizontal, y_control, 85, 40, min_val, max_val, valor_inicial, label, self.manager)
            for i, (min_val, max_val, valor_inicial, label) in enumerate([
                (1, 8, 1, "Cajeros"),
                (1, 20, 10, "# Productos"),
                (1, 10, 5, "Frecuencia"),
                (1, 5, 2, "Tiempo/prod")
            ])
        ]

        # Input dinámico para tiempo máximo de espera
        x_input = x_inicio + len(self.counters) * espacio_horizontal
        self.max_wait_input = InputNumber(
            480, 40, 85, 40,
            "T/Max. de espera", "Segundos",
            10, 1, 60, self.manager
        )

        # Botones de control
        button_width = 60
        button_height = 60
        button_spacing = 20
        total_width = 3 * button_width + 2 * button_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        y_position = 85

        self.control_buttons = [
            Button(start_x, y_position, button_width, button_height, "", color=(0, 150, 0), hover_color=(0, 200, 0), active_color=(0, 100, 0), manager=self.manager, btn_type="#btn-start", enabled=True),
            Button(start_x + button_width + button_spacing, y_position, button_width, button_height, "", color=(150, 150, 0), hover_color=(200, 200, 0), active_color=(100, 100, 0), manager=self.manager, btn_type="#btn-pause", enabled=False),
            Button(start_x + 2 * (button_width + button_spacing), y_position, button_width, button_height, "", color=(150, 0, 0), hover_color=(200, 0, 0), active_color=(100, 0, 0), manager=self.manager, btn_type="#btn-reset", enabled=True)
        ]
        
        # Botones de velocidad
        self.speed_buttons = [
            Button(WINDOW_WIDTH - 220, 20, 40, 40, "x0.5", color=(157, 191, 255), hover_color=(0, 200, 0), active_color=(0, 100, 0), btn_type="#btn-x0.5"),
            Button(WINDOW_WIDTH - 150, 20, 40, 40, "x1", color=(150, 150, 0), hover_color=(200, 200, 0), active_color=(100, 100, 0), btn_type="#btn-x1"),
            Button(WINDOW_WIDTH - 80, 20, 40, 40, "x2", color=(150, 0, 0), hover_color=(200, 0, 0), active_color=(100, 0, 0), btn_type="#btn-x2")
        ]

        # Distribución de clientes (usando RadioButton)
        self.distribution_radio = RadioButton(
            920, 
            self.control_panel_height/2 - 40,  # Ajustar Y para alinear con otros controles
            200, 
            100, 
            "Distribución de llegada",
            "Aleatoria",
            "Fila mas corta",
            self.manager
        )
        # Establecer valor inicial a "Fila mas corta"
        self.distribution_radio.set_value(1)

        # ------------ Variables de la Simulación ------------------
        self.num_cashiers = 1
        self.max_products = 10
        self.arrival_frequency = 5  # segundos entre llegadas
        self.time_since_last_customer = 0
        self.customers = []
        self.cashiers = []
        self.queues = []  # Lista de listas, una para cada cajero
        self.is_running = False
        self.is_paused = False
        self.total_simulation_time = 0.0  # Para el tiempo total
        self.maximum_queue_capacity = 5  # Capacidad máxima de la cola

        # Crear UILabel para mostrar el tiempo total
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WINDOW_WIDTH//2 - 62, 40, 125, 30)),
            text="00:00:0",
            manager=self.manager,
            visible=False,
            object_id="#time_label"
        )
        
        self.card_payment_cashier = None

        # Pago con tarjeta (usando Select)
        self.payment_select = Select(
            1110, 
            self.control_panel_height/2,  # Ajustar Y para alinear con otros controles
            200, 
            100, 
            "Pago con tarjeta",
            [f"CAJA {i + 1}" for i in range(self.num_cashiers)],  # Generar opciones dinámicamente
            self.manager
        )

        # Capacidad máxima de la cola
        self.maximum_queue_capacity_input = InputNumber(
            1330, 
            self.control_panel_height/2,
            100, 
            40, 
            "Capacidad max. de cola", 
            "Clientes", 
            initial_value=5, 
            min_value=1, 
            max_value=10, 
            manager=self.manager
        )
        

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  * self.speed_multiplier # Convertir a segundos y aplicar el multiplicador de velocidad
            
            running = self.handle_events()
            
            if self.state == "welcome":
                self.draw_welcome_screen()
            else:
                self.update_simulation(dt)
                self.draw_simulation_screen()
            
            # Dibujar elementos de pygame_gui
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
                # Manejar eventos de los botones de velocidad
                for i, button in enumerate(self.speed_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Botón "x0.5"
                            self.speed_multiplier = 0.5
                            print("Velocidad ajustada a x0.5")
                        elif i == 1:  # Botón "x1"
                            self.speed_multiplier = 1
                            print("Velocidad ajustada a x1")
                        elif i == 2:  # Botón "x2"
                            self.speed_multiplier = 2
                            print("Velocidad ajustada a x2")
                
                # Manejar eventos de los contadores
                # for counter in self.counters:
                #     counter.handle_event(event)

                # Manejar evento de edición del input
                self.max_wait_input.handle_event(event)
                    
                # Manejar eventos de los botones de control
                for i, button in enumerate(self.control_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Botón "Iniciar"
                            self.is_running = True
                            self.is_paused = False
                            self.control_buttons[0].set_active(True)
                            self.control_buttons[1].set_active(False)
                            self.control_buttons[0].set_enabled(False)
                            self.control_buttons[1].set_enabled(True)
                            # Desactivar counter de cajeros
                            self.counters[0].set_enabled(False)
                        elif i == 1:  # Botón "Pausar"
                            self.is_running = False
                            self.is_paused = True
                            self.control_buttons[0].set_active(False)
                            self.control_buttons[1].set_active(True)
                            self.control_buttons[0].set_enabled(True)
                            self.control_buttons[1].set_enabled(False)
                            # Desactivar counter de cajeros
                            self.counters[0].set_enabled(False)

                        elif i == 2:  # Botón "Reset"
                            # Restablecer valores de los contadores
                            self.counters[0].set_value(1)  # Cajeros
                            self.counters[1].set_value(10)  # Productos
                            self.counters[2].set_value(3)   # Frecuencia
                            self.counters[3].set_value(5)   # Tiempo/prod
                            # Actualizar número de cajeros y opciones del select
                            self.num_cashiers = 1
                            self.setup_simulation()
                            self.is_running = False
                            self.is_paused = False
                            self.total_simulation_time = 0.0  # Reiniciar el tiempo
                            self.time_label.set_text("00:00:0")  # Actualizar el texto
                            self.control_buttons[0].set_active(False)
                            self.control_buttons[1].set_active(False)
                            self.control_buttons[0].set_enabled(True)
                            self.control_buttons[1].set_enabled(False)
                            # Activar counter de cajeros
                            self.counters[0].set_enabled(True)
                for i, counter in enumerate(self.counters):
                    if counter.handle_event(event):
                        # Si es el contador de cajeros (índice 0)
                        if i == 0:
                            new_num_cashiers = counter.get_value()
                            if new_num_cashiers != self.num_cashiers:
                                self.num_cashiers = new_num_cashiers
                                print(f"Número de cajeros cambiado a: {self.num_cashiers}")
                                # Actualizar las opciones del select
                                self.payment_select.options = [f"CAJA {i + 1}" for i in range(self.num_cashiers)]
                                if not self.is_running:
                                    self.setup_simulation()

                # Manejar eventos del radio button de distribución
                self.distribution_radio.handle_event(event)

                # Manejar eventos del select de método de pago
                if self.payment_select.handle_event(event):
                    selected_value = self.payment_select.get_value()
                    # Actualizar el cajero que acepta pago con tarjeta
                    for cashier in self.cashiers:
                        if cashier.name == selected_value:
                            self.card_payment_cashier = cashier
                            print(f"Cajero seleccionado para pago con tarjeta: {cashier.name}")
                            break
                
                # Manejar eventos del input de capacidad máxima de cola
                if self.maximum_queue_capacity_input.handle_event(event):
                    self.maximum_queue_capacity = self.maximum_queue_capacity_input.get_value()
                    print(f"Capacidad máxima de cola actualizada a: {self.maximum_queue_capacity}")
            
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
        
        # Crear cajeros en la parte superior con el espaciado adecuado para las imágenes
        cashier_spacing = (WINDOW_WIDTH - 200) // self.num_cashiers  # Aumentamos el espaciado para las imágenes
        for i in range(self.num_cashiers):
            x = 100 + i * cashier_spacing  # Ajustamos la posición inicial
            self.cashiers.append(Cashier(x, self.control_panel_height + 50, i))
            self.queues.append([])  # Inicializar cola vacía para cada cajero
        
        # Actualizar opciones del select de método de pago
        self.payment_select.options = [f"CAJA {i + 1}" for i in range(self.num_cashiers)]
        # Reiniciar el cajero que acepta pago con tarjeta
        self.payment_select.set_value("CAJA 1")  # Por defecto, el primer cajero acepta pago con tarjeta
        self.card_payment_cashier = self.cashiers[0]  # Por defecto, el primer cajero acepta pago con tarjeta

    def draw_welcome_screen(self):
        self.screen.fill(WHITE)
        image_path = pygame.image.load("assets/logo-minerva.png")
        image_width, image_height = image_path.get_size()
        
        # Centrar la imagen horizontal y verticalmente
        x_position = (WINDOW_WIDTH - image_width) // 2
        y_position = (WINDOW_HEIGHT - image_height) // 2 - 100  # Ajustar posición vertical
        self.screen.blit(image_path, (x_position, y_position))

        # Inicializar fuente aquí
        font = pygame.font.Font(None, 48)
        welcome_text = font.render("Simulación de Clientes en Supermercado", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(WINDOW_WIDTH//2, y_position + image_height + 50))  # Ajustar espaciado vertical
        self.screen.blit(welcome_text, welcome_rect)

        
        self.start_button.draw(self.screen)
        
    def draw_control_panel(self):
        # Dibujar fondo del panel de control
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.control_panel_height)
        pygame.draw.rect(self.screen, LIGHT_BLUE, panel_rect)
        pygame.draw.line(self.screen, BLACK, (0,self.control_panel_height), (WINDOW_WIDTH,self.control_panel_height), 1)
        
        # Ocultar el botón de inicio
        self.start_button.hide()

        # Dibujar título de la etiqueta de tiempo
        title_font = pygame.font.Font(None, 30)
        title_text = title_font.render("Tiempo Total", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 25))
        self.screen.blit(title_text, title_rect)

        # Dibujar etiqueta de tiempo
        self.time_label.show()

        # Convertir tiempo total a MM:SS:MS
        total_seconds = self.total_simulation_time
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 100)  
        time_str = f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{str(milliseconds).zfill(2)}"
        
        # Actualizar el texto del UILabel
        self.time_label.set_text(time_str)

        # Dibujar contadores
        for counter in self.counters:
            counter.draw(self.screen)
            
        # Dibujar botones de control
        for button in self.control_buttons:
            button.draw(self.screen)

        # Dibujar botones de velocidad
        for button in self.speed_buttons:
            button.draw(self.screen)    

        # Draw distribution radio button
        self.distribution_radio.draw(self.screen)

        # Draw payment select dropdown
        self.payment_select.draw(self.screen)

        # Draw maximum queue capacity input
        self.maximum_queue_capacity_input.draw(self.screen)

        # Dibujar input de tiempo máximo de espera
        self.max_wait_input.draw(self.screen)

            
    def draw_simulation(self):
        # Dibujar cajeros
        for cashier in self.cashiers:
            cashier.draw(self.screen)
            
        # Dibujar colas
        for i, queue in enumerate(self.queues):
            cashier = self.cashiers[i]
            queue_start_y = cashier.rect.bottom + 20  # Iniciar cola 20 píxeles debajo de la imagen del cajero
            
            for j, customer in enumerate(queue):
                # Calcular posición para el cliente
                customer_x = cashier.rect.centerx - (customer.rect.width // 2)  # Centrar cliente debajo del cajero
                customer_y = queue_start_y + (j * (customer.rect.height + 30))  # Apilar clientes verticalmente con más espaciado
                
                # Actualizar posición del cliente
                customer.update_position(customer_x, customer_y)
                customer.draw(self.screen)
            
    def draw_simulation_screen(self):
        self.screen.fill(WHITE)
        self.draw_control_panel()
        self.draw_simulation()
        # Mostrar velocidad actual
        font = pygame.font.SysFont(None, 24)
        speed_text = font.render(f"Velocidad: x{self.speed_multiplier}", True, (0, 0, 0))
        self.screen.blit(speed_text, (10, self.control_panel_height + 10))
                        
    def update_simulation(self, dt):
        if not self.is_running or self.is_paused:
            return

        # Actualizar el tiempo total
        self.total_simulation_time += dt  # Actualizar opciones dinámicamente

        self.max_products = int(self.counters[1].get_value())
        self.arrival_frequency = int(self.counters[2].get_value())
        self.time_per_product = self.counters[3].get_value()
        
        selected_cashier_name = self.payment_select.get_value()
        for cashier in self.cashiers:
            if cashier.name == selected_cashier_name:
                cashier.accepts_card_payment = True
                self.card_payment_cashier = cashier
            else:
                cashier.accepts_card_payment = False
            cashier.update(dt, self.screen)  # Actualizar el estado del cajero
        
        # Convertir tiempo total a MM:SS:MS
        total_seconds = self.total_simulation_time
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 100)
        time_str = f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{str(milliseconds).zfill(2)}"
        
        ## TEST
        # Actualizar variables de simulación desde los contadores
        # new_num_cashiers = int(self.counters[0].get_value())
        # if new_num_cashiers != self.num_cashiers:
        #     self.num_cashiers = new_num_cashiers
        #     print(f"Número de cajeros cambiado a: {self.num_cashiers}")
        #     self.setup_simulation()
            
        # self.max_products = int(self.counters[1].get_value())
        # self.arrival_frequency = int(self.counters[2].get_value())
        # self.time_per_product = self.counters[3].get_value()
        ## TEST
        # Actualizar el texto del UILabel
        self.time_label.set_text(time_str)
            
        # Generate new customers
        self.time_since_last_customer += dt
        if self.time_since_last_customer >= self.arrival_frequency:
            self.time_since_last_customer = 0

            selected_queue = None
            new_customer = Customer(0, 0, self.max_products, self.time_per_product)

            if (new_customer.uses_card_payment and self.card_payment_cashier):
                # Buscar el índice del cajero que acepta pago con tarjeta
                for idx, cashier in enumerate(self.cashiers):
                    if cashier.accepts_card_payment == self.card_payment_cashier.accepts_card_payment:
                        queue_index = idx
                        print(f"Cliente asignado a la caja {idx +1 } (pago con tarjeta)")
                        break
                selected_queue = self.queues[queue_index]
            else:
                if self.distribution_radio.get_value() == 0:  # Distribución aleatoria
                    # Asignar a una cola aleatoria
                    queue_index = random.randint(0, len(self.queues) - 1)
                    selected_queue = self.queues[queue_index]
                else:  # Distribución por cola más corta
                    # Asignar a la cola más corta
                    selected_queue = min(self.queues, key=len)
                    queue_index = self.queues.index(selected_queue)

            # Verificar si la cola seleccionada ha alcanzado su capacidad máxima
            if len(selected_queue) >= self.maximum_queue_capacity:
                print(f"Cola {queue_index + 1} ha alcanzado su capacidad máxima ({self.maximum_queue_capacity}). No se puede añadir un nuevo cliente.")
            else:
                # Añadir el nuevo cliente a la cola seleccionada
                if len(selected_queue) > 0:
                    last_customer = selected_queue[-1]
                    new_customer.update_position(last_customer.x, last_customer.y + 60)  # Colocar debajo del último cliente
                else:
                    cashier = self.cashiers[queue_index]
                    new_customer.update_position(cashier.rect.centerx - 25, cashier.rect.bottom + 20)  # Colocar debajo del cajero
                selected_queue.append(new_customer)
                print(f"Nuevo cliente añadido a la cola {queue_index + 1} ({'que acepta tarjeta' if new_customer.uses_card_payment else 'aleatoria' if self.distribution_radio.get_value() == 0 else 'cola más corta'})")
                self.customers.append(new_customer)  # Añadir cliente a la lista de clientes
        # Actualizar clientes en las colas
        for i, queue in enumerate(self.queues):
            cashier = self.cashiers[i]
            # Verificar si algún cliente excede el tiempo de espera
            for customer in list(queue):  # se hace copia para evitar errores al eliminar
                if not customer.is_being_served and customer.waiting_time >= self.max_wait_input.get_value():
                    print(f"[ABANDONO] Cliente {customer.name} abandonó la cola {i+1} tras {customer.waiting_time:.1f}s")
                    queue.remove(customer)

            if cashier.is_available and queue:  # Si el cajero está disponible y hay clientes en la cola
                customer = queue[0]
                customer.is_being_served = True
                cashier.is_available = False
                print(f"Cliente comenzando a ser atendido en {cashier.name}. Tiempo de espera previo: {customer.waiting_time:.1f}s")

            # Actualizar estado del cliente actual
            if queue and queue[0].is_being_served:
                if queue[0].update(dt, True):  # Cliente ha terminado
                    queue.pop(0)  # Eliminar cliente de la cola
                    cashier.is_available = True
                    print(f"Cliente atendido en {cashier.name}. Cola actual: {len(queue)} clientes")

            # Actualizar el resto de clientes en la cola
            for customer in queue[1:]:
                customer.update(dt, True)
            
        # Actualizar el gestor de pygame_gui
        self.manager.update(dt)
