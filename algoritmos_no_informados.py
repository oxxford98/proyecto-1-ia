from collections import deque


def reconstruir_camino(nodo):
    """Reconstruye las acciones que llevan del estado inicial hasta ``nodo``.

    Los enlaces ``padre`` apuntan desde cada estado hacia su predecesor, así
    que las acciones se recopilan en orden inverso y se invierten al final.
    """
    camino = []
    while nodo.padre is not None:
        camino.append(nodo.accion)
        nodo = nodo.padre
    return camino[::-1]


def ejecutar_bfs(estado_inicial):
    """
    Busca por niveles y devuelve una ruta con el menor número de movimientos.

    El resultado es ``(acciones, nodos_expandidos, profundidad)``; si no hay
    solución, ``acciones`` es ``None`` y la profundidad devuelta es cero.
    """
    # La cola FIFO garantiza que se procesen primero los estados más cercanos
    # al inicio, es decir, los que tienen menor cantidad de movimientos.
    frontera = deque([estado_inicial])
    # Evita insertar repetidamente un estado que ya espera en la cola.
    frontera_estados = {estado_inicial.tablero}
    # Guarda estados ya extraídos y procesados.
    explorados = set()
    nodos_expandidos = 0

    while frontera:
        nodo = frontera.popleft()
        frontera_estados.remove(nodo.tablero)

        # Se comprueba la meta al extraer el estado; no se cuentan sus
        # sucesores porque no hace falta expandirlo.
        if nodo.es_meta():
            camino = reconstruir_camino(nodo)
            return camino, nodos_expandidos, len(camino)

        explorados.add(nodo.tablero)
        nodos_expandidos += 1

        for sucesor in nodo.generar_sucesores():
            # Un tablero se agrega una sola vez, ya sea que esté pendiente
            # o que haya sido procesado.
            if sucesor.tablero not in explorados and sucesor.tablero not in frontera_estados:
                frontera.append(sucesor)
                frontera_estados.add(sucesor.tablero)

    return None, nodos_expandidos, 0


def ejecutar_dfs(estado_inicial):
    """
    Explora una rama en profundidad antes de retroceder a otras alternativas.

    Devuelve ``(acciones, nodos_expandidos, profundidad)`` para la primera
    solución encontrada. DFS no garantiza que esa ruta tenga la menor cantidad
    de movimientos. Si no hay solución, devuelve ``(None, nodos_expandidos, 0)``.
    """
    # La lista se usa como pila LIFO: pop() toma el último sucesor agregado.
    frontera = [estado_inicial]
    # Controla los estados que ya fueron expandidos.
    explorados = set()
    nodos_expandidos = 0

    while frontera:
        nodo = frontera.pop()

        # Igual que en BFS, el estado meta no necesita generar sucesores ni se
        # incluye en el contador de nodos expandidos.
        if nodo.es_meta():
            camino = reconstruir_camino(nodo)
            return camino, nodos_expandidos, len(camino)

        if nodo.tablero not in explorados:
            explorados.add(nodo.tablero)
            nodos_expandidos += 1

            # Los sucesores se generan como Arriba, Abajo, Izquierda y Derecha.
            # Se insertan al revés para que la pila explore primero Arriba.
            for sucesor in reversed(nodo.generar_sucesores()):
                if sucesor.tablero not in explorados:
                    frontera.append(sucesor)

    return None, nodos_expandidos, 0