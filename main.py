import time
from estado import EstadoPuzzle
from algoritmos_no_informados import ejecutar_bfs, ejecutar_dfs
from algoritmos_informados import ejecutar_ucs, ejecutar_a_star
from minimax import jugar_adversario

def imprimir_tablero(tablero):
    """Muestra el estado del 8-Puzzle; 0 representa el espacio vacío."""
    for fila in range(0, 9, 3):
        print(f" {tablero[fila]} | {tablero[fila + 1]} | {tablero[fila + 2]} ")
        if fila < 6:
            print("---+---+---")


def imprimir_resultados(camino, nodos_expandidos, costo, tiempo_ejecucion,
                        estado_inicial, algoritmo):
    """Muestra las métricas y explica cada transición de la solución."""
    if camino is None:
        print("\nNo se encontró una solución.")
    else:
        print("\nResultados de la búsqueda:")
        print(f"Camino solución: {camino}")
        print(f"Valor reportado por el algoritmo: {costo}")
        print(f"Movimientos de la ruta: {len(camino)}")
        if algoritmo == "BFS":
            print("Justificación: BFS explora por niveles y encuentra una "
                  "solución con el menor número de movimientos; no minimiza "
                  "el costo ponderado de las acciones.")
        elif algoritmo == "DFS":
            print("Justificación: DFS devuelve la primera solución encontrada; "
                  "no garantiza que tenga el menor número de movimientos.")
        elif algoritmo == "UCS":
            print("Justificación: UCS prioriza el menor costo acumulado de las "
                  "acciones.")
        else:
            print("Justificación: A* prioriza el costo acumulado más la "
                  "heurística de distancia Manhattan.")

        print("\nTablero inicial (0 = espacio vacío):")
        estado_actual = estado_inicial
        costo_acciones = 0
        imprimir_tablero(estado_actual.tablero)

        direcciones_opuestas = {
            "Arriba": "abajo",
            "Abajo": "arriba",
            "Izquierda": "a la derecha",
            "Derecha": "a la izquierda",
        }
        for numero_paso, accion in enumerate(camino, start=1):
            siguiente = next(
                (estado for estado in estado_actual.generar_sucesores()
                 if estado.accion == accion),
                None,
            )
            if siguiente is None:
                raise ValueError(
                    f"La acción {accion!r} no es válida para el estado "
                    f"del paso {numero_paso}."
                )

            ficha_movida = siguiente.tablero[estado_actual.tablero.index(0)]
            costo_acciones += (
                siguiente.costo_acumulado - estado_actual.costo_acumulado
            )
            print(
                f"Paso {numero_paso}: el espacio vacío se mueve {accion.lower()}; "
                f"la ficha {ficha_movida} se desliza "
                f"{direcciones_opuestas[accion]}."
            )
            imprimir_tablero(siguiente.tablero)
            estado_actual = siguiente

        if estado_actual.es_meta():
            print("Meta alcanzada: las fichas quedan ordenadas y el espacio "
                  "vacío está en la última casilla.")
        print(f"Costo ponderado de las acciones: {costo_acciones}")

    print(f"Nodos expandidos: {nodos_expandidos}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")


def comparar_algoritmos(estado_inicial):
    """Compara las búsquedas sobre el mismo tablero sin imprimir sus rutas."""
    algoritmos = [
        ("DFS", ejecutar_dfs),
        ("BFS", ejecutar_bfs),
        ("UCS", ejecutar_ucs),
        ("A*", ejecutar_a_star),
    ]
    print("\nComparación de los cuatro algoritmos:")
    print(f"{'Algoritmo':<12} {'Nodos expandidos':>17} {'Tiempo (s)':>14} "
          f"{'Movimientos':>14} {'Costo ponderado':>17}")
    for nombre, ejecutar in algoritmos:
        inicio = time.perf_counter()
        camino, nodos, _ = ejecutar(EstadoPuzzle(estado_inicial.tablero))
        segundos = time.perf_counter() - inicio
        if camino is None:
            print(f"{nombre:<12} {nodos:>17} {segundos:>14.6f} "
                  f"{'Sin solución':>14} {'N/A':>17}")
            continue

        # Reproduce la ruta sin mostrarla para comparar también el costo de DFS/BFS.
        tablero = estado_inicial.tablero
        costo = 0
        for accion in camino:
            siguiente = next(
                (estado for estado in EstadoPuzzle(tablero).generar_sucesores()
                 if estado.accion == accion),
                None,
            )
            if siguiente is None:
                raise ValueError(f"{nombre} devolvió un movimiento ilegal: {accion!r}.")
            costo += siguiente.costo_acumulado
            tablero = siguiente.tablero
        if not EstadoPuzzle(tablero).es_meta():
            raise ValueError(f"La ruta devuelta por {nombre} no alcanza la meta.")
        print(f"{nombre:<12} {nodos:>17} {segundos:>14.6f} "
              f"{len(camino):>14} {costo:>17}")
    print("El tiempo mide solo la búsqueda; excluye la comprobación de la ruta.")


def menu_un_agente():
    print("\n--- MODO 8-PUZZLE ---")
    print("1. Búsqueda en Profundidad (DFS)")
    print("2. Búsqueda en Amplitud (BFS)")
    print("3. Búsqueda de Costo Uniforme (UCS)")
    print("4. Búsqueda A* (Informada)")
    print("5. Volver")
    print("6. Comparar los cuatro algoritmos (solo resultados)")
    
    opcion = input("Elige el algoritmo a ejecutar: ")
    
    if opcion in ["1", "2", "3", "4", "6"]:
        # Cambia esta tupla para probar otro tablero (0 representa el vacío).
        estado_inicial = EstadoPuzzle(tablero=(6, 2, 4, 0, 3, 5, 7, 8, 1))

        inversiones = estado_inicial.contar_inversiones()
        if not estado_inicial.es_resoluble():
            print(
                "\nEl tablero inicial no tiene solución para la meta estándar. "
                f"Tiene {inversiones} inversiones (impar); en un tablero 3x3, "
                "el conteo debe ser par. Cambia el tablero por otra "
                "configuración resoluble."
            )
            return

        if opcion == "6":
            comparar_algoritmos(estado_inicial)
            return
        
        print("\nCalculando solución...")
        inicio = time.time()
        
        if opcion == "1":
            algoritmo = "DFS"
            camino, nodos, costo = ejecutar_dfs(estado_inicial)
        elif opcion == "2":
            algoritmo = "BFS"
            camino, nodos, costo = ejecutar_bfs(estado_inicial)
        elif opcion == "3":
            algoritmo = "UCS"
            camino, nodos, costo = ejecutar_ucs(estado_inicial)
        elif opcion == "4":
            algoritmo = "A*"
            camino, nodos, costo = ejecutar_a_star(estado_inicial)
            
        fin = time.time()
        imprimir_resultados(
            camino, nodos, costo, fin - inicio, estado_inicial, algoritmo
        )

def main():
    while True:
        print("\n========================================")
        print(" PROYECTO 1: ALGORITMOS DE BÚSQUEDA ")
        print("========================================")
        print("1. Resolver 8-Puzzle (Un Agente)")
        print("2. Jugar contra la Máquina (Minimax Adversario)")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            menu_un_agente()
        elif opcion == "2":
            print("\n--- MODO ADVERSARIO ---")
            jugar_adversario()
        elif opcion == "3":
            print("Cerrando aplicación.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()