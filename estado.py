class EstadoPuzzle:
    def __init__(self, tablero, padre=None, accion=None, costo_acumulado=0):
        """Crea un nodo del espacio de búsqueda del 8-Puzzle.

        ``tablero`` es una tupla de nueve valores; el cero representa el
        espacio vacío. ``padre`` y ``accion`` enlazan este nodo con el camino
        que lo generó, y ``costo_acumulado`` suma los costos desde el inicio.
        """
        self.tablero = tablero
        self.padre = padre
        self.accion = accion
        self.costo_acumulado = costo_acumulado

    def es_meta(self):
        """Indica si el tablero está ordenado y el espacio vacío está al final."""
        return self.tablero == (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def contar_inversiones(self):
        """Cuenta los pares de fichas no vacías que aparecen fuera de orden."""
        fichas = [valor for valor in self.tablero if valor != 0]
        return sum(
            fichas[i] > fichas[j]
            for i in range(len(fichas))
            for j in range(i + 1, len(fichas))
        )

    def es_resoluble(self):
        """Indica si la paridad permite alcanzar la meta estándar del tablero 3x3.

        En un 8-Puzzle de ancho impar, el tablero es resoluble si el conteo de
        inversiones de sus fichas (sin incluir el espacio vacío) es par.
        """
        return self.contar_inversiones() % 2 == 0

    def generar_sucesores(self):
        """Genera los estados alcanzables con un movimiento legal del espacio vacío.

        Cada sucesor conserva este estado como padre, registra la acción
        realizada y acumula el costo correspondiente a esa dirección.
        """
        sucesores = []
        # La posición lineal del cero se convierte a coordenadas (fila, columna).
        indice_vacio = self.tablero.index(0)
        fila, col = divmod(indice_vacio, 3)

        # (cambio de fila, cambio de columna, dirección del vacío, costo)
        # Las acciones se nombran según el movimiento del espacio vacío.
        movimientos = [
            (-1, 0, 'Arriba', 1),
            (1, 0, 'Abajo', 2),
            (0, -1, 'Izquierda', 3),
            (0, 1, 'Derecha', 4)
        ]

        for df, dc, accion, costo in movimientos:
            nueva_fila, nueva_col = fila + df, col + dc

            # Descarta movimientos que saldrían de los límites del tablero.
            if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
                nuevo_indice = nueva_fila * 3 + nueva_col
                nuevo_tablero = list(self.tablero)

                # El cero intercambia posición con la ficha vecina.
                nuevo_tablero[indice_vacio], nuevo_tablero[nuevo_indice] = \
                    nuevo_tablero[nuevo_indice], nuevo_tablero[indice_vacio]

                nuevo_estado = EstadoPuzzle(
                    tablero=tuple(nuevo_tablero),
                    padre=self,
                    accion=accion,
                    costo_acumulado=self.costo_acumulado + costo
                )
                sucesores.append(nuevo_estado)

        return sucesores