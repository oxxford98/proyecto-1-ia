"""Juego de tres en línea con búsqueda Minimax y poda alfa-beta.

La IA juega con X y maximiza la puntuación; el jugador humano usa O y la
minimiza. El tablero es una lista de nueve posiciones, numeradas de 0 a 8.
"""

import math


def imprimir_tablero(tablero):
    """Muestra las nueve casillas en una cuadrícula de tres por tres."""
    for i in range(0, 9, 3):
        print(f" {tablero[i]} | {tablero[i+1]} | {tablero[i+2]} ")
        if i < 6:
            print("---+---+---")
    print()


def verificar_ganador(tablero, jugador):
    """Indica si el jugador ocupa alguna fila, columna o diagonal completa."""
    lineas = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(tablero[i] == tablero[j] == tablero[k] == jugador for i, j, k in lineas)


def es_terminal(tablero):
    """Indica si hay un ganador o si ya no quedan casillas vacías."""
    return verificar_ganador(tablero, 'X') or verificar_ganador(tablero, 'O') or ' ' not in tablero


def funcion_evaluacion(tablero):
    """Asigna +10 a una victoria de X, -10 a una de O y 0 a lo demás."""
    if verificar_ganador(tablero, 'X'):
        return 10
    if verificar_ganador(tablero, 'O'):
        return -10
    return 0


def obtener_movimientos(tablero):
    """Devuelve los índices de las casillas que todavía están vacías."""
    return [i for i, casilla in enumerate(tablero) if casilla == ' ']


# Cada contador acumula las llamadas recursivas de una búsqueda completa.
nodos_sin_poda = 0
nodos_con_poda = 0


def minimax(tablero, profundidad, maximizando):
    """Busca la puntuación óptima explorando todas las jugadas hasta el límite.

    X maximiza la puntuación y O la minimiza. El tablero se modifica para
    simular cada jugada y se restaura antes de explorar la siguiente.
    """
    global nodos_sin_poda
    nodos_sin_poda += 1

    # Se detiene al terminar la partida o al alcanzar el límite de búsqueda.
    if profundidad == 0 or es_terminal(tablero):
        return funcion_evaluacion(tablero)

    if maximizando:
        max_eval = -math.inf
        for mov in obtener_movimientos(tablero):
            tablero[mov] = 'X'
            evaluacion = minimax(tablero, profundidad - 1, False)
            tablero[mov] = ' '
            max_eval = max(max_eval, evaluacion)
        return max_eval

    min_eval = math.inf
    for mov in obtener_movimientos(tablero):
        tablero[mov] = 'O'
        evaluacion = minimax(tablero, profundidad - 1, True)
        tablero[mov] = ' '
        min_eval = min(min_eval, evaluacion)
    return min_eval


def alfa_beta(tablero, profundidad, alfa, beta, maximizando):
    """Aplica Minimax y omite ramas que no pueden mejorar el resultado.

    ``alfa`` es la mejor puntuación conocida para X y ``beta`` la mejor para
    O. Cuando beta es menor o igual que alfa, el resto de esa rama no puede
    cambiar la decisión, así que se deja de explorarla.
    """
    global nodos_con_poda
    nodos_con_poda += 1

    if profundidad == 0 or es_terminal(tablero):
        return funcion_evaluacion(tablero)

    if maximizando:
        max_eval = -math.inf
        for mov in obtener_movimientos(tablero):
            tablero[mov] = 'X'
            evaluacion = alfa_beta(tablero, profundidad - 1, alfa, beta, False)
            tablero[mov] = ' '
            max_eval = max(max_eval, evaluacion)
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break
        return max_eval

    min_eval = math.inf
    for mov in obtener_movimientos(tablero):
        tablero[mov] = 'O'
        evaluacion = alfa_beta(tablero, profundidad - 1, alfa, beta, True)
        tablero[mov] = ' '
        min_eval = min(min_eval, evaluacion)
        beta = min(beta, evaluacion)
        if beta <= alfa:
            break
    return min_eval


def mejor_movimiento_ia(tablero, profundidad_limite=9):
    """Elige la jugada de X y devuelve también los nodos de ambas búsquedas.

    Minimax sin poda se ejecuta para medir su coste; su puntuación no se usa
    para elegir. La decisión se basa en la puntuación de alfa-beta.
    """
    global nodos_sin_poda, nodos_con_poda
    nodos_sin_poda = 0
    nodos_con_poda = 0

    mejor_puntaje = -math.inf
    movimiento_elegido = -1

    for mov in obtener_movimientos(tablero):
        tablero[mov] = 'X'
        # La jugada candidata ya ocupa un turno; las búsquedas reciben el resto.
        minimax(tablero, profundidad_limite - 1, False)
        puntaje = alfa_beta(tablero, profundidad_limite - 1, -math.inf, math.inf, False)
        tablero[mov] = ' '

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            movimiento_elegido = mov

    return movimiento_elegido, nodos_sin_poda, nodos_con_poda


def jugar_adversario():
    """Ejecuta una partida interactiva entre una persona y la IA."""
    tablero = [' '] * 9
    print("¡Bienvenido a 3 en Línea! Tú eres 'O', la IA es 'X'.")
    imprimir_tablero(tablero)

    while not es_terminal(tablero):
        # La persona elige el índice de una casilla libre (de 0 a 8).
        mov_humano = int(input("Tu turno (0-8): "))
        if tablero[mov_humano] != ' ':
            print("Movimiento inválido. Intenta de nuevo.")
            continue
        tablero[mov_humano] = 'O'
        imprimir_tablero(tablero)

        if es_terminal(tablero):
            break

        print("Turno de la IA (calculando...)")
        mov_ia, n_sin, n_con = mejor_movimiento_ia(tablero)
        tablero[mov_ia] = 'X'
        imprimir_tablero(tablero)
        print(f"Métricas de búsqueda: Nodos evaluados sin poda: {n_sin} | Con poda alfa-beta: {n_con}\n")

    if verificar_ganador(tablero, 'X'):
        print("¡La IA gana!")
    elif verificar_ganador(tablero, 'O'):
        print("¡Ganaste!")
    else:
        print("¡Empate!")