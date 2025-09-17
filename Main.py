#Juego de Adivinanzas - "Adivinando" - Grupo 8
import random
ranking = {}

normalizar = lambda s: s.strip().lower()

def mostrar_menu():
    """Muestra menú principal."""
    print("Bienvenido a Adivinando!")
    print("\n|MENÚ PRINCIPAL|")
    print("1) Jugar")
    print("2) Salir")
    print("\n(Proximamente juego de a mas jugadores)")
    
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

def mostrar_resultado(acerto):
    """ Informa si el jugador acertó o no la pregunta """
    if acerto:
        print("¡Respuesta correcta! Sumás 10 puntos.")
    else:
        print("Respuesta incorrecta. Perdés 5 puntos.")


def imprimir_tablero(vidas):
    """
    Muestra el tablero con jugadores, puntos y vidas.
    """
    matriz = [[n, ranking.get(n, 0), vidas[n]] for n in vidas]  
    matriz.sort(key=lambda fila: fila[1], reverse=True)
    for n, p, v in matriz:
        print(f"{n}: {p} puntos - {v} vidas")
 
 
def preguntar(nombre, vidas):
    """Turno de un jugador: pregunta, valida y actualiza su estado."""
    if vidas[nombre] <= 0:
        return
    pregunta, solucion = cargar_adivinanzas()
    print(f"\nTurno de {nombre}")
    print("Pregunta:", pregunta)
    resp = normalizar(input("Tu respuesta: "))
    acerto = (resp == normalizar(solucion))
    if acerto:
        ranking[nombre] = ranking.get(nombre, 0) + 10
    else:
        ranking[nombre] = ranking.get(nombre, 0) - 5
        vidas[nombre] -= 1
    mostrar_resultado(acerto)


def ganador(j1, j2, vidas):
    """Devuelve una tupla (nombre, puntos, vidas) con el ganador."""
    v1, v2 = vidas[j1], vidas[j2]
    p1, p2 = ranking.get(j1, 0), ranking.get(j2, 0)
    if v1 > 0 and v2 <= 0:
        return (j1, p1, v1)
    if v2 > 0 and v1 <= 0:
        return (j2, p2, v2)
    if p1 >= p2:
        return (j1, p1, v1)
    return (j2, p2, v2)


def jugar_1v1():
    """
    Juego de dos jugadores:
    - 3 vidas por jugador.
    - Tablero al final de cada ronda y al final del juego.
    """
    j1, j2 = pedir_jugadores()
    ranking[j1] = 0
    ranking[j2] = 0
    vidas = {j1: 3, j2: 3}

    jugadores = [j1, j2]
    while True:
        for j in jugadores:
            if not (vidas[j1] > 0 and vidas[j2] > 0):
                break
            preguntar(j, vidas)
        imprimir_tablero(vidas)  

        if not (vidas[j1] > 0 and vidas[j2] > 0):
            g, p, v = ganador(j1, j2, vidas)
            print("----------------------------")
            print("|Juego Finalizado|")
            print(f"El GANADOR es: {g} con {p} puntos (vidas {v}).")
            imprimir_tablero(vidas)  
            break













