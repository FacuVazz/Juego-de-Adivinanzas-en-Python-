#Juego de Adivinanzas - "Adivinando" - Grupo 8
from adivinanzas import facil, medio, dificil
import random
ranking = {}
aciertos = {}  
fallos = {}
rachas = {}
normalizar = lambda s: s.strip().lower()

def mostrar_menu():
    """Muestra menú principal."""
    print("🧩 Bienvenido a Adivinando! 🧩")
    print("----------------------")
    print("|MENÚ PRINCIPAL|")
    print("1) Jugar")
    print("2) Salir")
    print("----------------------")
    
    
def elegir_adivinanza(nivel,usadas):
    
    dificultades = {
        "facil" : facil,
        "media" : medio,
        "dificil" : dificil,
    }

    lista = dificultades[nivel]

    if len(usadas[nivel]) == len(lista):
        usadas[nivel].clear()

    restantes = [i for i in range(len(lista)) if i not in usadas[nivel]]

    indice = random.choice(restantes)
    usadas[nivel].add(indice)
    return lista[indice]
    

def dificultad_por_ronda(rondas_completas):
    if rondas_completas < 3:
        return "facil"
    if rondas_completas < 6:
        return "media"
    return "dificil"
    
def siguiente_nivel(nivel):
    if nivel == "facil":
        return "media"
    if nivel == "media":
        return "dificil"
    return "dificil"  

def cargar_adivinanzas(nivel, usadas):
    pregunta, respuesta = elegir_adivinanza(nivel, usadas)
    return {pregunta: respuesta}


def pedir_jugadores():
    """
    Pide cantidad de jugadores (2 a 4) y nombres.
    Devuelve la lista completa de jugadores en orden de turno.
    """
    while True:
        try:
            cant = input("¿Cuántos jugadores van a jugar? (2-4): ").strip()
            if not cant.isdigit():
                raise ValueError("Debe ser un número.")
            cant = int(cant)
            if not (2 <= cant <= 4):
                raise ValueError("Ingresá entre 2 y 4 jugadores.")
            break
        except ValueError as e:
            print("Entrada inválida:", e)

    jugadores = []
    for i in range(1, cant + 1):
        nombre = input(f"Nombre del Jugador {i}: ").strip().capitalize() or f"Jugador{i}"
        while nombre in jugadores:
            nombre = input(f"'{nombre}' ya está usado, ingresá otro: ").strip().capitalize() or f"Jugador{i}"
        jugadores.append(nombre)

    return jugadores



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
 
def preguntar(nombre, vidas, nivel, usadas):
    """
    Turno de un jugador: pregunta y valida.
    Devuelve (acerto: bool, eliminado_ahora: bool)
    (Actualizacion de Facu)
    """
    if vidas[nombre] <= 0:
        return False, False
    adiv = cargar_adivinanzas(nivel, usadas)
    pregunta, solucion = list(adiv.items())[0]
    print(f"\nTurno de {nombre} / Nivel: {nivel}")
    print("Pregunta:", pregunta)
    
    try:
        resp = normalizar(input("Tu respuesta: "))
        acerto = (resp == normalizar(solucion))
        if nombre not in rachas:
            rachas[nombre] = 0
        if acerto:
            rachas[nombre] += 1
            puntos = 10
            if rachas[nombre] % 3 == 0:
                puntos += 15
                print("¡Estas en racha de 3! Bono de +15 puntos.")
            ranking[nombre] = ranking.get(nombre, 0) + puntos
            aciertos[nombre] = aciertos.get(nombre, 0) + 1
        else:
            rachas[nombre] = 0
            ranking[nombre] = ranking.get(nombre, 0) - 5
            vidas[nombre] -= 1
            fallos[nombre] = fallos.get(nombre, 0) + 1
            if vidas[nombre] == 0:
                print(f" {nombre} se quedó sin vidas.")

        mostrar_resultado(acerto)
        return acerto, (vidas[nombre] == 0)
        
    except Exception as e:
        print("Ocurrió un error al ingresar la respuesta:", e)
        print("Perdés 1 vida por error de entrada")
        rachas[nombre] = 0
        vidas[nombre] -= 1
        fallos[nombre] = fallos.get(nombre, 0) + 1
        if vidas[nombre] == 0:
            print(f" {nombre} se quedó sin vidas.")
        return False, (vidas[nombre] == 0)

            
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


def jugar(nivel_actual):
    """Disparador principal del juego (2 a 4 jugadores, racha y bump de dificultad)."""
    try:
        jugadores = pedir_jugadores()
        vidas = {n: 3 for n in jugadores}
        for n in jugadores:
            rachas[n] = 0
        rondas_completas = 0

        usadas = {
            "facil": set(),
            "media": set(),
            "dificil": set()
        }

        while True:
            # jugadores activos al inicio de la ronda
            activos = [n for n in jugadores if vidas[n] > 0]

            # fin si queda 1 o ninguno
            if len(activos) <= 1:
                print("----------------------------")
                print("|Juego Finalizado|")
                imprimir_tablero_general(jugadores)
                if len(activos) == 1:
                    g = activos[0]
                    print(f"El GANADOR es: {g} (último con vidas). Puntos: {ranking.get(g,0)}")
                else:
                    resultado = determinar_ganador_por_puntos(jugadores)
                    print(f"El GANADOR es: {resultado['nombre']} con {resultado['puntos']} puntos (sumatoria total).")
                imprimir_resumen_general(jugadores, vidas)
                break

            # turnos de la ronda, en orden de 'activos'
            for nombre in list(activos):
                if vidas[nombre] <= 0:
                    continue

                # progresión por rondas (no bajar si ya subimos antes)
                nivel_round = dificultad_por_ronda(rondas_completas)
                orden = {"facil": 0, "media": 1, "dificil": 2}
                if orden[nivel_round] > orden[nivel_actual]:
                    nivel_actual = nivel_round

                acerto, eliminado = preguntar(nombre, vidas, nivel_actual, usadas)

                # bump inmediato de dificultad si alguien fue eliminado en este turno
                if eliminado:
                    previo = nivel_actual
                    nivel_actual = siguiente_nivel(nivel_actual)
                    if nivel_actual != previo:
                        print(f"⬆️ Dificultad aumenta por eliminación: {previo} → {nivel_actual}")

                # si tras este turno ya queda 1 o 0 vivos, cortamos para cerrar
                if sum(1 for n in jugadores if vidas[n] > 0) <= 1:
                    break

            # si aún hay más de 1 con vida, cierra la ronda
            if sum(1 for n in jugadores if vidas[n] > 0) > 1:
                rondas_completas += 1
                imprimir_ronda(vidas)

    except Exception as e:
        print("Error inesperado durante la partida:", e)
        print("Se interrumpe la ronda, volvé a intentar jugar.")
        return nivel_actual

    return nivel_actual


if __name__ == "__main__":
    menu = True
    nivel_actual = "facil"
    while menu:
        mostrar_menu()
        opcion = input("Elegí opción: ").strip()
        if opcion == "1":
            nivel_actual = jugar(nivel_actual)
        elif opcion == "2":
            print("Gracias totales por jugar maquina!")
            menu = False
        else:
            print("Opción inválida.")

































