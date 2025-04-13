import random

# Lista de nombres comunes en español
nombres = [
    "Juan", "María", "José", "Ana", "Carlos", "Laura", "Pedro", "Carmen", "Luis",
    "Isabel", "Miguel", "Rosa", "Francisco", "Patricia", "Antonio", "Teresa",
    "Manuel", "Sofía", "David", "Lucía", "Fernando", "Elena", "Pablo", "Marta",
    "Jorge", "Cristina", "Alberto", "Paula", "Daniel", "Beatriz"
]

# Lista de apellidos comunes en español
apellidos = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez",
    "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno",
    "Muñoz", "Álvarez", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres",
    "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina"
]

def generar_nombre():
    """
    Genera un nombre aleatorio combinando un nombre y un apellido
    """
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    return f"{nombre} {apellido}"
