# Juego de Adivinanzas - "Adivinando" - Grupo 8

import random
import time
from adivinanzas import facil, medio, dificil 


categorias_disponibles = ["cultura general", "logica", "argentina"]

ranking = {}
aciertos = {}
fallos = {}
rachas = {}
normalizar = lambda s: s.strip().lower()


def mostrar_menu():
    print("🧩 Bienvenido a Adivinando! 🧩")
    print("----------------------")
    print("|MENÚ PRINCIPAL|")
    print("1) Jugar (todas las categorías)")
    print("2) Jugar eligiendo categorías")
    print("3) Jugar Modo Contrarreloj")
    print("4) Ranking Histórico")
    print("5) Instructivo del juego")
    print("6) Salir")
    print("----------------------")


def pedir_categorias():
    print("Elegí categoría de adivinanzas:")
    print("1) Cultura general / 2) Lógica / 3) Argentina")

    while True:
        try:
            num = int(input("Ingrese el número de la categoría: "))

            if 1 <= num <= len(categorias_disponibles):
                categoria = categorias_disponibles[num - 1]
                print("Categoría elegida:", categoria)
                return categoria
            else:
                print("Número fuera de rango. Probá de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingresá solo números.")


def elegir_adivinanza(nivel, usadas, categoria):
    dificultades = {
        "facil": facil,
        "media": medio,
        "dificil": dificil,
    }

    lista = dificultades[nivel]

    if categoria is None:
        # Modo sin filtro de categoría
        if len(usadas[nivel]) == len(lista):
            usadas[nivel].clear()

        restantes = [i for i in range(len(lista)) if i not in usadas[nivel]]
    else:
        # Modo con categoría elegida
        restantes = [
            i for i in range(len(lista))
            if i not in usadas[nivel] and lista[i][2] == categoria
        ]

        if len(restantes) == 0:
            usadas[nivel].clear()
            restantes = [
                i for i in range(len(lista))
                if lista[i][2] == categoria
            ]

    indice = random.choice(restantes)
    usadas[nivel].add(indice)

    pregunta, respuesta, categoria = lista[indice]
    return pregunta, respuesta


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
    """Cuenta regresiva para usar recursividad."""
    if n == 0:
        print("¡Comienza el juego!")
    else:
        print(n)
        time.sleep(1)
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
    """Muestra el historial completo y el Top 5 histórico, si existe."""
    try:
        with open("ranking.txt", "r", encoding="utf-8") as f:
            print("\n--HISTORIAL DE PARTIDAS--")
            print(f.read())
            print("-----------------------------")
    except FileNotFoundError:
        print("Aún no hay partidas guardadas.")
        return

    mostrar_top5_jugadores()


def mostrar_top5_jugadores():
    try:
        totales = {}
        with open("ranking.txt", "r", encoding="utf-8") as f:
            for line in f:
                linea = line.strip()
                
                if not linea or linea.startswith("--") or linea.startswith("="):
                    continue
                
                if ":" in linea and "puntos" in linea:
                    nombre_parte, resto = linea.split(":", 1)
                    nombre = nombre_parte.strip()
                    partes = resto.strip().split()
                    if partes:
                        try:
                            puntos = int(partes[0])
                        except ValueError:
                            continue
                        totales[nombre] = totales.get(nombre, 0) + puntos

        if not totales:
            print("No hay datos suficientes para calcular el Top 5.")
            return

        ordenados = sorted(totales.items(), key=lambda x: x[1], reverse=True)

        print("\n-- TOP 5 JUGADORES HISTÓRICOS --")
        for i, (nombre, puntos) in enumerate(ordenados[:5], start=1):
            print(f"{i}. {nombre}: {puntos} puntos")
        print("-----------------------------")

    except FileNotFoundError:
        print("Aún no hay ranking histórico guardado (archivo 'ranking.txt').")



def cargar_adivinanzas(nivel, usadas, categoria):
    pregunta, respuesta = elegir_adivinanza(nivel, usadas, categoria)
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
            nombre = input(
                f"'{nombre}' ya está usado, ingresá otro: "
            ).strip().capitalize() or f"Jugador{i}"
        jugadores.append(nombre)

    return jugadores


def pedir_parametros_partida():
    """
    Pide cuántas vidas tendrá cada jugador y cuántas rondas máximas se van a jugar.
    Para usarlo en el modo contrarreloj.
    """
    while True:
        try:
            vidas = int(input("¿Cuántas vidas quiere cada jugador? (1-10): ").strip())
            if not (1 <= vidas <= 10):
                raise ValueError("Las vidas deben estar entre 1 y 10.")
            break
        except ValueError as e:
            print("Entrada inválida:", e)

    while True:
        try:
            rondas = int(
                input("¿Cuántas rondas máximas querés jugar? (1-50): ").strip()
            )
            if not (1 <= rondas <= 50):
                raise ValueError("Las rondas deben estar entre 1 y 50.")
            break
        except ValueError as e:
            print("Entrada inválida:", e)

    return vidas, rondas


def mostrar_resultado(acerto):
    """Informa si el jugador acertó o no la pregunta."""
    if acerto:
        print("¡Respuesta correcta! Sumás 10 puntos.")
    else:
        print("Respuesta incorrecta. Perdés 5 puntos.")


def imprimir_ronda(vidas):
    """
    Muestra por ronda: puntos y vidas por usuario.
    Además, notifica si algún jugador fue eliminado.
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
            print(f"{nombre} fue eliminado de la partida (sin vidas).")


def preguntar(nombre, vidas, nivel, usadas, categoria):
    """
    Turno de un jugador: pregunta y valida.
    Devuelve (acerto: bool, eliminado_ahora: bool)
    """
    if vidas[nombre] <= 0:
        return False, False

    adiv = cargar_adivinanzas(nivel, usadas, categoria)
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
                print("¡Estás en racha de 3! Bono de +15 puntos.")
            ranking[nombre] = ranking.get(nombre, 0) + puntos
            aciertos[nombre] = aciertos.get(nombre, 0) + 1
        else:
            rachas[nombre] = 0
            ranking[nombre] = max(0, ranking.get(nombre, 0) - 5)
            vidas[nombre] -= 1
            fallos[nombre] = fallos.get(nombre, 0) + 1
            if vidas[nombre] == 0:
                print(f"{nombre} se quedó sin vidas.")

        mostrar_resultado(acerto)
        return acerto, (vidas[nombre] == 0)

    except Exception as e:
        print("Ocurrió un error al ingresar la respuesta:", e)
        print("Perdés 1 vida por error de entrada")
        rachas[nombre] = 0
        vidas[nombre] -= 1
        fallos[nombre] = fallos.get(nombre, 0) + 1
        if vidas[nombre] == 0:
            print(f"{nombre} se quedó sin vidas.")
        return False, (vidas[nombre] == 0)


def preguntar_contrareloj(nombre, vidas, nivel, usadas, categoria, limite_segundos):
    """
    Versión contrarreloj de preguntar:
    - El jugador tiene 'limite_segundos' para responder.
    - Si se pasa del tiempo, cuenta como incorrecta.
    """
    if vidas[nombre] <= 0:
        return False, False

    adiv = cargar_adivinanzas(nivel, usadas, categoria)
    pregunta, solucion = list(adiv.items())[0]
    print(f"\nTurno de {nombre} / Nivel: {nivel}")
    print("Pregunta:", pregunta)
    print(f"(Tenés {limite_segundos} segundos para responder)")

    try:
        inicio = time.time()
        resp = normalizar(input("Tu respuesta: "))
        duracion = time.time() - inicio

        if duracion > limite_segundos:
            print(
                f"Se terminó el tiempo ({duracion:.1f} segundos). "
                "La respuesta cuenta como incorrecta."
            )
            acerto = False
        else:
            acerto = (resp == normalizar(solucion))

        if nombre not in rachas:
            rachas[nombre] = 0

        if acerto:
            rachas[nombre] += 1
            puntos = 10
            if rachas[nombre] % 3 == 0:
                puntos += 15
                print("¡Estás en racha de 3! Bono de +15 puntos.")
            ranking[nombre] = ranking.get(nombre, 0) + puntos
            aciertos[nombre] = aciertos.get(nombre, 0) + 1
        else:
            rachas[nombre] = 0
            ranking[nombre] = max(0, ranking.get(nombre, 0) - 5)
            vidas[nombre] -= 1
            fallos[nombre] = fallos.get(nombre, 0) + 1
            if vidas[nombre] == 0:
                print(f"{nombre} se quedó sin vidas.")

        mostrar_resultado(acerto)
        return acerto, (vidas[nombre] == 0)

    except Exception as e:
        print("Ocurrió un error al ingresar la respuesta:", e)
        print("Perdés 1 vida por error de entrada")
        rachas[nombre] = 0
        vidas[nombre] -= 1
        fallos[nombre] = fallos.get(nombre, 0) + 1
        if vidas[nombre] == 0:
            print(f"{nombre} se quedó sin vidas.")
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


def aplicar_bonus_racha_perfecta(jugadores, bonus=50):
    """
    Aplica un bonus de puntos a quienes terminaron la partida
    sin ningún fallo (racha perfecta).
    """
    print("\nChequeando rachas perfectas...")
    for nombre in jugadores:
        if fallos.get(nombre, 0) == 0 and aciertos.get(nombre, 0) > 0:
            ranking[nombre] = ranking.get(nombre, 0) + bonus
            print(f"{nombre} tuvo una racha PERFECTA. Bonus de +{bonus} puntos!")


def jugar(nivel_actual, categoria):
    """Disparador principal del juego (2 a 4 jugadores, racha y bump de dificultad)."""
    try:
        print("\nPreparando la partida...")
        cuenta_regresiva(3)
        jugadores = pedir_jugadores()
        vidas = {n: 3 for n in jugadores}
        for n in jugadores:
            rachas[n] = 0
            aciertos[n] = 0
            fallos[n] = 0
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

                # Bonus por racha perfecta antes de mostrar ranking
                aplicar_bonus_racha_perfecta(jugadores)

                imprimir_tablero_general(jugadores)
                if len(activos) == 1:
                    g = activos[0]
                    print(
                        f"El GANADOR es: {g} (último con vidas). "
                        f"Puntos: {ranking.get(g, 0)}"
                    )
                else:
                    resultado = determinar_ganador_por_puntos(jugadores)
                    print(
                        f"El GANADOR es: {resultado['nombre']} "
                        f"con {resultado['puntos']} puntos (sumatoria total)."
                    )
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

                acerto, eliminado = preguntar(
                    nombre, vidas, nivel_actual, usadas, categoria
                )

                if eliminado:
                    previo = nivel_actual
                    nivel_actual = siguiente_nivel(nivel_actual)
                    if nivel_actual != previo:
                        print(
                            f"La Dificultad aumenta por cada eliminación: "
                            f"{previo} → {nivel_actual}"
                        )

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


def jugar_contrareloj(nivel_actual, categoria):
    """
    Modo contrarreloj:
    - 2 a 4 jugadores
    - Vidas y rondas elegidas al inicio
    - Límite de tiempo por pregunta
    """
    try:
        print("\nPreparando la partida Contrarreloj...")
        cuenta_regresiva(3)
        jugadores = pedir_jugadores()
        vidas_iniciales, rondas_maximas = pedir_parametros_partida()
        vidas = {n: vidas_iniciales for n in jugadores}

        for n in jugadores:
            rachas[n] = 0
            aciertos[n] = 0
            fallos[n] = 0

        while True:
            try:
                limite_segundos = int(
                    input("¿Cuántos segundos máximo por pregunta? (5-60): ").strip()
                )
                if not (5 <= limite_segundos <= 60):
                    raise ValueError("El tiempo debe estar entre 5 y 60 segundos.")
                break
            except ValueError as e:
                print("Entrada inválida:", e)

        rondas_completas = 0

        usadas = {
            "facil": set(),
            "media": set(),
            "dificil": set()
        }

        while True:
            activos = [n for n in jugadores if vidas[n] > 0]
            if len(activos) <= 1 or rondas_completas >= rondas_maximas:
                print("----------------------------")
                print("|Juego Finalizado (Contrarreloj)|")

                # Bonus por racha perfecta también en contrarreloj
                aplicar_bonus_racha_perfecta(jugadores)

                imprimir_tablero_general(jugadores)
                if len(activos) == 1:
                    g = activos[0]
                    print(
                        f"El GANADOR es: {g} (último con vidas). "
                        f"Puntos: {ranking.get(g, 0)}"
                    )
                else:
                    resultado = determinar_ganador_por_puntos(jugadores)
                    print(
                        f"El GANADOR es: {resultado['nombre']} "
                        f"con {resultado['puntos']} puntos (sumatoria total)."
                    )
                imprimir_resumen_general(jugadores, vidas, vidas_iniciales)
                guardar_ranking_txt(jugadores, ranking)
                break

            for nombre in list(activos):
                if vidas[nombre] <= 0:
                    continue

                nivel_round = dificultad_por_ronda(rondas_completas)
                orden = {"facil": 0, "media": 1, "dificil": 2}
                if orden[nivel_round] > orden[nivel_actual]:
                    nivel_actual = nivel_round

                acerto, eliminado = preguntar_contrareloj(
                    nombre, vidas, nivel_actual, usadas, categoria, limite_segundos
                )

                if eliminado:
                    previo = nivel_actual
                    nivel_actual = siguiente_nivel(nivel_actual)
                    if nivel_actual != previo:
                        print(
                            f"La Dificultad aumenta por cada eliminación: "
                            f"{previo} → {nivel_actual}"
                        )

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

    print("\nOBJETIVO")
    print("Acertar la mayor cantidad posible de adivinanzas, sumar puntos y mantener tus vidas.")
    print("El último jugador con vidas o el que más puntos acumule será el ganador.")

    print("\nVIDAS")
    print("• Cada jugador comienza con 3 vidas (o las que se definan en Contrarreloj).")
    print("• Cada respuesta incorrecta resta 1 vida.")
    print("• Los errores de entrada (excepciones) también restan 1 vida.")
    print("• Cuando un jugador llega a 0 vidas queda eliminado y no vuelve a jugar.")

    print("\nDIFICULTAD")
    print("El juego avanza en niveles según las rondas:")
    print("• Fácil: rondas 1 a 3.")
    print("• Media: rondas 4 a 6.")
    print("• Difícil: ronda 7 en adelante.")
    print("\nAdemás:")
    print("• Si un jugador es eliminado, la dificultad sube automáticamente para todos.")
    print("• Si ya están en Difícil, la dificultad no cambia.")
    print("• Todos los jugadores responden preguntas del mismo nivel actual.")

    print("\nMODOS DE JUEGO Y CATEGORÍAS")
    print("• Opción 1: Jugar (todas las categorías).")
    print("  - Usa todas las adivinanzas disponibles por nivel.")
    print("• Opción 2: Jugar eligiendo categorías.")
    print("  - Antes de empezar se elige una categoría:")
    print("    · Cultura general")
    print("    · Lógica")
    print("    · Argentina")
    print("• Opción 3: Modo Contrarreloj.")
    print("  - Podés definir vidas, rondas y tiempo máximo por pregunta.")

    print("\nSISTEMA DE PUNTOS")
    print("• Respuesta correcta: +10 puntos.")
    print("• Respuesta incorrecta: -5 puntos.")
    print("• Error de entrada: perdés 1 vida, sin pérdida de puntos.")

    print("\nBONIFICACIÓN POR RACHA")
    print("• Cada 3 respuestas correctas consecutivas, sumás +15 puntos extra.")
    print("  (es decir, ese turno sumás 25 puntos en total).")
    print("• Racha perfecta (sin fallos en toda la partida): bonus adicional al final.")

    print("\nAL FINAL DEL JUEGO SE MUESTRA:")
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
            # Todas las categorías
            nivel_actual = jugar(nivel_actual, None)

        elif opcion == "2":
            categoria = pedir_categorias()
            nivel_actual = jugar(nivel_actual, categoria)

        elif opcion == "3":
            print("\n1) Contrarreloj con todas las categorías")
            print("2) Contrarreloj eligiendo categoría")
            sub = input("Elegí opción: ").strip()
            if sub == "1":
                nivel_actual = jugar_contrareloj(nivel_actual, None)
            elif sub == "2":
                categoria = pedir_categorias()
                nivel_actual = jugar_contrareloj(nivel_actual, categoria)
            else:
                print("Opción inválida, volviendo al menú principal.")

        elif opcion == "4":
            mostrar_ranking_guardado()

        elif opcion == "5":
            mostrar_instructivo()

        elif opcion == "6":
            print("Gracias totales por jugar máquina!")
            menu = False

        else:
            print("Opción inválida.")





















































