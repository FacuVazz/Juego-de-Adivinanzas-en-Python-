
ranking = {}


def mostrar_menu():
    print("=== MENÚ PRINCIPAL ===")
    print("1. Jugar")
    print("2. Ver ranking de puntos")
    print("3. Salir")


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
