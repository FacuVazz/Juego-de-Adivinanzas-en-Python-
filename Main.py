#Juego de Adivinanzas - "Adivinando" - Grupo 8
from adivinanzas import facil, medio, dificil
import random
ranking = {}
aciertos = {}  
fallos = {}
rachas = {}
normalizar = lambda s: s.strip().lower()


    
    
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


def cuenta_regresiva(n):
    """Cuenta regresiva para usar recursividad"""
    if n == 0:
        print("¡Comienza el juego!")
    else:
        print(n)
        cuenta_regresiva(n - 1)


def guardar_ranking_txt(jugadores, ranking_sesion):
    """
    Guarda los puntajes finales de la partida en un archivo ranking.txt
    """
    try:
        with open("ranking.txt", "a", encoding="utf-8") as f:
            f.write("\n--NUEVA PARTIDA--\n")
            for nombre in jugadores:
                puntos = ranking_sesion.get(nombre, 0)
                f.write(f"{nombre}: {puntos} puntos\n")
            f.write("======================\n")
        print("\nRanking guardado en 'ranking.txt'")
    except Exception as e:
        print("Error al guardar el ranking:", e)


def mostrar_ranking_guardado():
    """Muestra el contenido del archivo ranking.txt, si existe."""
    try:
        with open("ranking.txt", "r", encoding="utf-8") as f:
            print("\n--HISTORIAL DE PARTIDAS--")
            print(f.read())
            print("-----------------------------")
    except FileNotFoundError:
        print("Aún no hay partidas guardadas.")


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


def imprimir_ronda(vidas):  
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
            ranking[nombre] = max(0, ranking.get(nombre, 0) - 5)
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


def determinar_ganador_por_puntos(jugadores):
    """
    Determina el ganador exclusivamente por puntaje total acumulado.
    """
    tabla = [(n, ranking.get(n, 0)) for n in jugadores]
    tabla.sort(key=lambda t: t[1], reverse=True)
    return {"nombre": tabla[0][0], "puntos": tabla[0][1]}


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
            usadas = 0  
        print(f"{nombre} -> Aciertos: {a} | Fallos: {f} | Vidas utilizadas: {usadas}")


def jugar(nivel_actual):
    """Disparador principal del juego (2 a 4 jugadores, racha y bump de dificultad)."""
    try:
        print("\nPreparando la partida...")
        cuenta_regresiva(3)
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
            activos = [n for n in jugadores if vidas[n] > 0]

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
                guardar_ranking_txt(jugadores, ranking)
                break

            for nombre in list(activos):
                if vidas[nombre] <= 0:
                    continue

                nivel_round = dificultad_por_ronda(rondas_completas)
                orden = {"facil": 0, "media": 1, "dificil": 2}
                if orden[nivel_round] > orden[nivel_actual]:
                    nivel_actual = nivel_round

                acerto, eliminado = preguntar(nombre, vidas, nivel_actual, usadas)
               
                if eliminado:
                    previo = nivel_actual
                    nivel_actual = siguiente_nivel(nivel_actual)
                    if nivel_actual != previo:
                        print(f"La Dificultad aumenta por cada eliminacion: {previo} → {nivel_actual}")

                if sum(1 for n in jugadores if vidas[n] > 0) <= 1:
                    break

            if sum(1 for n in jugadores if vidas[n] > 0) > 1:
                rondas_completas += 1
                imprimir_ronda(vidas)

    except Exception as e:
        print("Error inesperado durante la partida:", e)
        print("Se interrumpe la ronda, volvé a intentar jugar.")
        return nivel_actual

    return nivel_actual

def mostrar_instructivo():
    print("\n📘 INSTRUCTIVO DEL JUEGO - ADIVINANDO 📘")
    print("--------------------------------------------")

    print("\n🎯 OBJETIVO")
    print("Acertar la mayor cantidad posible de adivinanzas, sumar puntos y mantener tus vidas.")
    print("El último jugador con vidas o el que más puntos acumule será el ganador.")

    print("\n❤️ VIDAS")
    print("• Cada jugador comienza con 3 vidas.")
    print("• Cada respuesta incorrecta resta 1 vida.")
    print("• Los errores de entrada (excepciones) también restan 1 vida.")
    print("• Cuando un jugador llega a 0 vidas queda eliminado y no vuelve a jugar.")

    print("\n🔥 DIFICULTAD")
    print("El juego avanza en niveles según las rondas:")
    print("• Fácil: rondas 1 a 3.")
    print("• Media: rondas 4 a 6.")
    print("• Difícil: ronda 7 en adelante.")
    print("\nAdemás:")
    print("• Si un jugador es eliminado, la dificultad sube automáticamente para todos.")
    print("• Si ya están en Difícil, la dificultad no cambia.")
    print("• Todos los jugadores responden preguntas del mismo nivel actual.")

    print("\n🏆 SISTEMA DE PUNTOS")
    print("• Respuesta correcta: +10 puntos.")
    print("• Respuesta incorrecta: -5 puntos.")
    print("• Error de entrada: perdés 1 vida, sin pérdida de puntos.")

    print("\n💥 BONIFICACIÓN POR RACHA")
    print("• Cada 3 respuestas correctas consecutivas, sumás +15 puntos extra.")
    print("  (es decir, ese turno sumás 25 puntos en total).")

    print("\n📊 AL FINAL DEL JUEGO SE MUESTRA:")
    print("• El ganador.")
    print("• El ranking general de puntajes.")
    print("• Aciertos, fallos y vidas utilizadas por cada jugador.")

    print("--------------------------------------------\n")



if __name__ == "__main__":
    menu = True
    nivel_actual = "facil"
    while menu:
        mostrar_menu()
        opcion = input("Elegí opción: ").strip()
        if opcion == "1":
            nivel_actual = jugar(nivel_actual)
        elif opcion == "2":
            mostrar_ranking_guardado()
        elif opcion == "3":
            print("Gracias totales por jugar maquina!")
            menu = False
        else:
            print("Opción inválida.")







































