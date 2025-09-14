import random
ranking = {}



def mostrar_menu():
    print("=== MENÚ PRINCIPAL ===")
    print("1. Jugar")
    print("2. Ver ranking de puntos")
    print("3. Salir")

def cargar_adivinanzas(): 
    """
    Devuelve una adivinanza elegida al azar en forma de tupla (pregunta, respuesta).
    Se usan tuplas porque cada adivinanza es inmutable.
    """
    adivinanzas = [
        ("Me como con cuchara, soy nacional y vengo con dulce de leche. ¿Qué soy?", "flan"),
        ("Me prendés un domingo, me das carbón y chorizo, y hago felices a todos. ¿Qué soy?", "parrilla"),
        ("Soy larga, marrón y amarga, pero sin mí no arrancás la mañana. ¿Qué soy?", "cafe"),
        ("Parezco italiano pero soy argento: tengo jamón, queso y salsa. ¿Quién soy?", "fugazzeta"),
        ("No soy Messi ni Maradona, pero si me pateás bien, entro en el arco. ¿Qué soy?", "penal"),
        ("Soy redonda, salada y vengo en paquete. Me como en el bondi o mirando tele. ¿Qué soy?", "papas fritas"),
        ("Si me tomás, te mareás. Si me invitás, soy amigo. ¿Qué soy?", "fernet"),
        ("Cuando llueve en verano y hace calor, me decís…", "llovizna"),
        ("Me gritás en la calle si soy barato y de oferta. ¿Qué soy?", "liquidacion"),
        ("Tengo medialuna, cuernitos y azúcar arriba. ¿Qué soy?", "factura"),
        ("En la cancha me insultan todos, pero sin mí no hay partido. ¿Quién soy?", "arbitro"),
        ("Me decís cuando estoy muy caro: '¡está por las…!' ¿Por las qué?", "nubes"),
        ("Si digo 'soy una remera de piqué con cuellito', ¿qué soy?", "chomba"),
        ("Soy verde, me ponés en la pizza o en el mate. ¿Qué soy?", "menta"),
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

def mostrar_tablero():
    """ Muestra el puntaje de cada jugador al finalizar una ronda """
    print("TABLERO DE PUNTOS")
    if len(ranking) == 0:
        print("Todavía no hay jugadores registrados.")
    else:
        for jugador, puntos in ranking.items():
            print(jugador, "tiene", puntos, "puntos")



def jugar():
    nombre = input("Ingresa tu nombre: ")
    print("Bienvenido,", nombre, "¡vamos a jugar!")

   
    puntos = 10

    
    ranking[nombre] = puntos
    print("Juego terminado,", nombre, "obtuvo", puntos, "puntos.")


def ver_ranking():
    print("=== RANKING DE PUNTOS ===")
    if len(ranking) == 0:
        print("Todavía no hay jugadores registrados.")
    else:
        for jugador in ranking:
            print(jugador, ":", ranking[jugador], "puntos")


opcion = 0
while opcion != 3:
    mostrar_menu()
    eleccion = input("Elige una opción: ")

  
    if len(eleccion) > 0 and all(c >= '0' and c <= '9' for c in eleccion):
        opcion = int(eleccion)
    else:
        print("Entrada inválida")
        continue

    if opcion == 1:
        jugar()
    elif opcion == 2:
        ver_ranking()
    elif opcion == 3:
        print("Saliendo del programa...")
    else:
        print("Opción no válida")

#Posibles funciones a utilizar en este 40%
#mostrar_menu(): Primera imagen en consola con opciones para el jugador
#generar_adivinanza() : Selecciona aleatoriamente una adivinanza de la lista.
#mostrar_adivinanza(adivinanza) : Muestra el enunciado de la adivinanza en consola.
#recibir_respuesta() : Toma y valida la respuesta del jugador.
#verificar_respuesta(respuesta, solucion) : Compara la respuesta del jugador con la solución correcta.
#mostrar_resultado(es_correcta) : Informa si el jugador acertó o no.
#main() : Controla el flujo general del juego (mostrar adivinanza, leer respuesta, verificar, mostrar resultado).




