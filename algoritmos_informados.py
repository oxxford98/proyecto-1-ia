import heapq
import itertools


def reconstruir_camino(nodo):
    """Devuelve las acciones desde el estado inicial hasta ``nodo``.

    Cada estado conserva una referencia a su padre y la acción que lo produjo.
    Como esos enlaces apuntan de la meta hacia el inicio, se invierte la lista
    al final para devolverla en el orden en que se ejecuta.
    """
    camino = []
    while nodo.padre is not None:
        camino.append(nodo.accion)
        nodo = nodo.padre
    return camino[::-1]


def calcular_heuristica_manhattan(tablero):
    """
    Estima los movimientos restantes sumando la distancia Manhattan de las fichas.

    Para cada ficha distinta de cero, suma cuántas filas y columnas la separan
    de su posición en el tablero meta. El espacio vacío no aporta distancia.
    Con los costos de movimiento del puzzle (todos de al menos 1), esta suma
    es una cota inferior del costo restante y es consistente para A*.
    """
    distancia = 0
    # Debe coincidir con la condición de meta de EstadoPuzzle.es_meta().
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    for i in range(9):
        valor = tablero[i]
        if valor != 0:
            fila_actual, col_actual = divmod(i, 3)
            indice_objetivo = objetivo.index(valor)
            fila_objetivo, col_objetivo = divmod(indice_objetivo, 3)
            distancia += abs(fila_actual - fila_objetivo) + abs(col_actual - col_objetivo)

    return distancia


def ejecutar_ucs(estado_inicial):
    """
    Encuentra una solución de costo acumulado mínimo con Búsqueda de Costo Uniforme.

    La cola de prioridad ordena los estados por g(n), el costo de las acciones
    desde el inicio. Devuelve ``(acciones, nodos_expandidos, costo)`` o
    ``(None, nodos_expandidos, 0)`` si se agota la frontera.
    """
    # El contador desempata prioridades iguales sin intentar comparar nodos.
    contador = itertools.count()
    # Cada entrada es (costo acumulado g(n), orden de inserción, estado).
    frontera = [(0, next(contador), estado_inicial)]
    explorados = set()
    nodos_expandidos = 0

    while frontera:
        costo_actual, _, nodo = heapq.heappop(frontera)

        # UCS extrae primero el estado pendiente de menor costo acumulado.
        if nodo.es_meta():
            camino = reconstruir_camino(nodo)
            return camino, nodos_expandidos, nodo.costo_acumulado

        # Un estado puede haberse agregado más de una vez antes de expandirse.
        if nodo.tablero not in explorados:
            explorados.add(nodo.tablero)
            nodos_expandidos += 1

            for sucesor in nodo.generar_sucesores():
                if sucesor.tablero not in explorados:
                    # El sucesor ya lleva el costo del camino desde el inicio.
                    heapq.heappush(frontera, (sucesor.costo_acumulado, next(contador), sucesor))

    return None, nodos_expandidos, 0


def ejecutar_a_star(estado_inicial):
    """
    Busca una solución con A*, priorizando el menor valor estimado f(n).

    ``g(n)`` es el costo acumulado real y ``h(n)`` la distancia Manhattan
    restante. La prioridad es ``f(n) = g(n) + h(n)``. Devuelve
    ``(acciones, nodos_expandidos, costo_real)`` o
    ``(None, nodos_expandidos, 0)`` si no encuentra una solución.
    """
    contador = itertools.count()
    h_inicial = calcular_heuristica_manhattan(estado_inicial.tablero)

    # Cada entrada es (f(n), orden de inserción, estado).
    frontera = [(h_inicial, next(contador), estado_inicial)]
    explorados = set()
    nodos_expandidos = 0

    while frontera:
        costo_f, _, nodo = heapq.heappop(frontera)

        # La meta se acepta al extraerla de la frontera, no al generarla.
        if nodo.es_meta():
            camino = reconstruir_camino(nodo)
            return camino, nodos_expandidos, nodo.costo_acumulado

        # Cada tablero se expande como máximo una vez.
        if nodo.tablero not in explorados:
            explorados.add(nodo.tablero)
            nodos_expandidos += 1

            for sucesor in nodo.generar_sucesores():
                if sucesor.tablero not in explorados:
                    h = calcular_heuristica_manhattan(sucesor.tablero)
                    # Combina el costo ya pagado y la estimación que falta.
                    f = sucesor.costo_acumulado + h
                    heapq.heappush(frontera, (f, next(contador), sucesor))

    return None, nodos_expandidos, 0