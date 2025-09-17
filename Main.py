#Juego de Adivinanzas - "Adivinando" - Grupo 8
import random
ranking = {}

normalizar = lambda s: s.strip().lower()

def mostrar_menu():
    """Muestra menú principal."""
    print("\n|MENÚ PRINCIPAL|")
    print("1) Jugar")
    print("2) Salir")
    print()
    print("(Proximamente juego de a mas jugadores)")
    
def cargar_adivinanzas(): 
    """
    Devuelve una adivinanza elegida al azar en forma de tupla (pregunta, respuesta).
    Se usan tuplas porque cada adivinanza es inmutable.
    """
    adivinanzas = [
        ("Me como con cuchara, soy nacional y vengo con dulce de leche. ¿Qué soy?", "flan"),
        ("Me prendés un domingo, me das carbón, carne y hago felices a todos. ¿Qué soy?", "parrilla"),
        ("Soy oscuro y amargo, pero sin mí no arrancás la mañana. ¿Qué soy?", "cafe"),
        ("Parezco italiano pero soy argentino: tengo cebolla y estoy rellena de queso. ¿Quién soy?", "fugazzeta"),
        ("No soy Messi ni Maradona, pero si me pateás bien, entro en el arco. ¿Qué soy?", "pelota"),
        ("Soy redonda, salada y vengo en paquete. Me como en el bondi o mirando tele. ¿Qué soy?", "papas fritas"),
        ("Si me tomás, te mareás. Si me invitás, soy amigo. Soy dorada y testigo ¿Qué soy?", "cerveza"),
        ("Cuando llueve en verano hay mucha...", "humedad"),
        ("Caigo de un arbol, soy verde y bastante caro. ¿Qué soy?", "palta"),
        ("Puedo ser una medialuna, un cañoncito o un vigilante. ¿Qué soy?", "factura"),
        ("En la cancha me insultan todos, pero sin mí no hay partido. ¿Quién soy?", "arbitro"),
        ("Me decís cuando estoy muy caro: '¡está por las…!' ¿Por las qué?", "nubes"),
        ("Si digo 'soy una remera de piqué con cuellito', ¿qué soy?", "chomba"),
        ("Soy verde, me ponés en la pizza. ¿Qué soy?", "aceituna"),
        ("Me usás para cebar, soy de calabaza o de acero, y sin mí no hay ronda. ¿Qué soy?", "mate"),
    ]
    return random.choice(adivinanzas)

def pedir_jugadores(): 
    """
    Pide los nombres de los dos jugadores.
    Usa cadenas de texto y funciones de cadenas (strip, capitalize).
    """
    j1 = input("Nombre del Jugador 1: ").strip().capitalize() or "Jugador1"
    j2 = input("Nombre del Jugador 2: ").strip().capitalize() or "Jugador2"
    return j1, j2

def mostrar_resultado(es_correcta):
    """ Informa si el jugador acertó o no la pregunta """
    if es_correcta:
        print("¡Respuesta correcta! Sumás 10 puntos.")
    else:
        print("Respuesta incorrecta. Perdés 5 puntos.")











