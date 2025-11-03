#Juego de Adivinanzas - "Adivinando" - Grupo 8
import random
ranking = {}
aciertos = {}  
fallos = {}    

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
    Devuelve una adivinanza elegida al azar en forma de diccionario {pregunta: respuesta}.
    """
    adivinanzas = {
        "Me como con cuchara, soy nacional y vengo con dulce de leche. ¿Qué soy?": "flan",
        "Me prendés un domingo, me das carbón, carne y hago felices a todos. ¿Qué soy?": "parrilla",
        "Soy oscuro y amargo, pero sin mí no arrancás la mañana. ¿Qué soy?": "cafe",
        "Parezco italiano pero soy argentino: tengo cebolla y estoy rellena de queso. ¿Quién soy?": "fugazzeta",
        "No soy Messi ni Maradona, pero si me pateás bien, entro en el arco. ¿Qué soy?": "pelota",
        "Soy redonda, salada y vengo en paquete. Me como en el bondi o mirando tele. ¿Qué soy?": "papas fritas",
        "Si me tomás, te mareás. Si me invitás, soy amigo. Soy dorada y testigo ¿Qué soy?": "cerveza",
        "Cuando llueve en verano hay mucha...": "humedad",
        "Caigo de un arbol, soy verde y bastante caro. ¿Qué soy?": "palta",
        "Puedo ser una medialuna, un cañoncito o un vigilante. ¿Qué soy?": "factura",
        "En la cancha me insultan todos, pero sin mí no hay partido. ¿Quién soy?": "arbitro",
        "Me decís cuando estoy muy caro: '¡está por las…!' ¿Por las qué?": "nubes",
        "Si digo 'soy una remera de piqué con cuellito', ¿qué soy?": "chomba",
        "Soy verde, me ponés en la pizza. ¿Qué soy?": "aceituna",
        "Me usás para cebar, soy de calabaza o de acero, y sin mí no hay ronda. ¿Qué soy?": "mate",
    }

    pregunta = random.choice(list(adivinanzas.keys()))
    return {pregunta: adivinanzas[pregunta]}

def pedir_jugadores():
    """
    Pide cantidad de jugadores (1 a 4) y nombres.
    Si hay más de 2 jugadores, devuelve los dos primeros para mantener compatibilidad por ahora.
    Los demás los guardo para expandir despues.
    """
    while True:
        try:
            cant = input("¿Cuántos jugadores van a jugar? (1-4): ").strip()
            if not cant.isdigit():
                raise ValueError("Debe ser un número.")
            cant = int(cant)
            if not (1 <= cant <= 4):
                raise ValueError("Ingresá entre 1 y 4 jugadores.")
            break
        except Exception as e:
            print("Entrada inválida:", e)

    jugadores = []
    for i in range(1, cant + 1):
        nombre = input(f"Nombre del Jugador {i}: ").strip().capitalize() or f"Jugador{i}"
        while nombre in jugadores:
            nombre = input(f"'{nombre}' ya está usado, ingresá otro: ").strip().capitalize() or f"Jugador{i}"
        jugadores.append(nombre)

    if len(jugadores) > 2:
        print(f"(Modo ampliado pronto disponible. Jugando con {jugadores[0]} y {jugadores[1]} por ahora.)")
    return jugadores[0], jugadores[1]


   

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

def imprimir_ronda(vidas):   # FELI REVISAR
    """
    Muestra por ronda: puntos y vidas por usuario.
    Ademas, notifica si algún jugador fue eliminado.
    """
    print("Resumen de la ronda")
    resumen = []
    for nombre in vidas:
        puntos = ranking.get(nombre, 0)
        resumen.append((nombre, puntos, vidas[nombre]))
    resumen.sort(key=lambda t: t[1], reverse=True)

    for nombre, puntos, v in resumen:
        print(f"{nombre} -> Puntos: {puntos} | Vidas: {v}")

    for nombre in vidas:
        if vidas[nombre] <= 0:
            print(f" {nombre} fue eliminado de la partida (sin vidas).")
 
def preguntar(nombre, vidas):
    """Turno de un jugador: pregunta y valida."""
    if vidas[nombre] <= 0:
        return
    adiv = cargar_adivinanzas()
    pregunta, solucion = list(adiv.items())[0]
    print(f"\nTurno de {nombre}")
    print("Pregunta:", pregunta)

    try:
        resp = normalizar(input("Tu respuesta: "))
        acerto = (resp == normalizar(solucion))
        if acerto:
            ranking[nombre] = ranking.get(nombre, 0) + 10
            aciertos[nombre] = aciertos.get(nombre, 0) + 1   #feli revisar
        else:
            ranking[nombre] = ranking.get(nombre, 0) - 5
            vidas[nombre] -= 1
            fallos[nombre] = fallos.get(nombre, 0) + 1       # feli revisar
            if vidas[nombre] == 0:  # ya lo tenías como nuevo
                print(f" {nombre} se quedó sin vidas.")
        mostrar_resultado(acerto)
    except Exception as e:
        print("Ocurrio un error al ingresar la respuesta:", e)
        print("Perdes 1 vida por error de entrada")
        vidas[nombre] -= 1
        fallos[nombre] = fallos.get(nombre, 0) + 1           # feli revisar
        if vidas[nombre] == 0:
            print(f" {nombre} se quedó sin vidas.")

            
def ganador(j1, j2, vidas):
    """Devuelve un diccionario con el ganador, sus puntos y vidas."""
    v1, v2 = vidas[j1], vidas[j2]
    p1, p2 = ranking.get(j1, 0), ranking.get(j2, 0)
    if v1 > 0 and v2 <= 0:
        return {"nombre": j1, "puntos": p1, "vidas": v1}
    if v2 > 0 and v1 <= 0:
        return {"nombre": j2, "puntos": p2, "vidas": v2}
    if p1 >= p2:
        return {"nombre": j1, "puntos": p1, "vidas": v1}
    return {"nombre": j2, "puntos": p2, "vidas": v2}


def jugar_1v1():
    """Juego 1 vs 1 con manejo de errores."""
    try:
        j1, j2 = pedir_jugadores()
        vidas = {j1: 3, j2: 3}
        jugadores = [j1, j2]
        while True:
            for j in jugadores:
                if not (vidas[j1] > 0 and vidas[j2] > 0):
                    break
                preguntar(j, vidas)

            imprimir_ronda(vidas)  # FELI REVISAR: resumen de la ronda (puntos, vidas, eliminados)

            if not (vidas[j1] > 0 and vidas[j2] > 0):
                print("----------------------------")
                print("|Juego Finalizado|")
                imprimir_tablero_general(jugadores)  # FELI REVISAR
                resultado = determinar_ganador_por_puntos(jugadores)  # FELI REVISAR
                print(f"El GANADOR es: {resultado['nombre']} con {resultado['puntos']} puntos (sumatoria total).")
                imprimir_resumen_general(jugadores, vidas)  # FELI REVISAR
                break

    except Exception as e:
        print("Error inesperado durante la partida:", e)
        print("Se interrumpe la ronda, volve a intentar jugar.")

       
        if not (vidas[j1] > 0 and vidas[j2] > 0):
            resultado = ganador(j1, j2, vidas)
            print("----------------------------")
            print("|Juego Finalizado|")
            print(f"El GANADOR es: {resultado['nombre']} con {resultado['puntos']} puntos (vidas {resultado['vidas']}).")
            imprimir_tablero(vidas)
            imprimir_resumen_general(jugadores, vidas)  # FELI REVISAR


menu = True
while menu:
    mostrar_menu()
    opcion = input("Elegí opción: ").strip()
    if opcion == "1":
        jugar_1v1()
    elif opcion == "2":
        print("Gracias totales por jugar maquina!")
        menu = False
    else:
        print("Opción inválida.")

# NUEVA FUNCION FELI
def imprimir_tablero_general(jugadores):
    """
    Muestra el tablero general de puntos (sumatoria total de todas las rondas).
    Ordenado de mayor a menor puntaje.
    """
    print("\n=== Tablero general de puntos ===")
    tabla = [(n, ranking.get(n, 0)) for n in jugadores]
    tabla.sort(key=lambda t: t[1], reverse=True)
    for i, (n, p) in enumerate(tabla, start=1):
        print(f"{i}. {n}: {p} puntos")

# NUEVA FUNCION FELI
def determinar_ganador_por_puntos(jugadores):
    """
    Determina el ganador exclusivamente por puntaje total acumulado.
    """
    tabla = [(n, ranking.get(n, 0)) for n in jugadores]
    tabla.sort(key=lambda t: t[1], reverse=True)
    return {"nombre": tabla[0][0], "puntos": tabla[0][1]}


# NUEVA FUNCION FELI
def imprimir_resumen_general(jugadores, vidas, vidas_iniciales=3):
    """
    Muestra resumen de desempeño general:
    Por jugador: aciertos, fallos y vidas utilizadas.
    """
    print("\n=== Resumen de desempeño general ===")
    for nombre in jugadores:
        a = aciertos.get(nombre, 0)
        f = fallos.get(nombre, 0)
        usadas = vidas_iniciales - vidas.get(nombre, 0)
        if usadas < 0:
            usadas = 0  # por seguridad, por si se modifica lógica de vidas
        print(f"{nombre} -> Aciertos: {a} | Fallos: {f} | Vidas utilizadas: {usadas}")

























