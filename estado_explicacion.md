# Modelo de estado del 8-Puzzle

`estado.py` define la clase `EstadoPuzzle`, que representa tanto la disposición
actual de las fichas como un nodo dentro del árbol o grafo de búsqueda. Los
algoritmos BFS, DFS, UCS y A* usan sus métodos para comprobar la meta y generar
los tableros vecinos.

## Representación del tablero

El atributo `tablero` guarda nueve valores en una tupla, en orden por filas:

```text
índice:   0 | 1 | 2
          3 | 4 | 5
          6 | 7 | 8
```

Los valores `1` a `8` representan las fichas y `0` representa el espacio vacío.
Por ejemplo, `(1, 2, 3, 0, 4, 5, 7, 8, 6)` corresponde a:

```text
1 | 2 | 3
0 | 4 | 5
7 | 8 | 6
```

El constructor recibe además tres datos de búsqueda:

- `padre`: el estado anterior del camino; es `None` para el estado inicial.
- `accion`: el movimiento del espacio vacío que produjo este estado; es
  `None` para el inicial.
- `costo_acumulado`: la suma de costos de las acciones desde el inicio; parte
  de cero salvo que se indique otro valor.

El constructor almacena los argumentos tal como se reciben. No valida que el
tablero tenga nueve posiciones, que sus valores sean una permutación de `0` a
`8` ni que el costo sea válido; el resto del programa proporciona estados con
el formato esperado.

## Comprobación de la meta

`es_meta()` compara el tablero con la tupla objetivo:

```text
(1, 2, 3, 4, 5, 6, 7, 8, 0)
```

Devuelve `True` solo si todas las fichas están en ese orden y el espacio vacío
ocupa la última posición; para cualquier otra tupla devuelve `False`.

## Inversiones y posibilidad de solución

`contar_inversiones()` ignora el cero y cuenta cuántos pares de fichas están
en el orden contrario al objetivo. Una inversión es un par en que una ficha
mayor aparece antes que una menor al leer las fichas de izquierda a derecha y
de arriba hacia abajo. Por ejemplo, en `(2, 1, 3, 4, 5, 6, 7, 8, 0)`, el `2`
está antes que el `1`, así que hay una inversión.

`es_resoluble()` aplica la regla de paridad del 8-Puzzle estándar de ancho
impar: una configuración puede alcanzar la meta `(1, 2, 3, 4, 5, 6, 7, 8, 0)`
si y solo si su número de inversiones es par. El método permite al menú
detectar configuraciones imposibles antes de ejecutar BFS, DFS, UCS o A*.

## Generación de sucesores

`generar_sucesores()` devuelve una lista nueva de estados que se alcanzan con
un movimiento legal:

1. Busca el índice del espacio vacío con `tablero.index(0)`.
2. Convierte el índice lineal a `(fila, columna)` mediante `divmod(indice, 3)`.
3. Prueba los desplazamientos Arriba, Abajo, Izquierda y Derecha.
4. Descarta los que dejarían el espacio vacío fuera de las filas `0`–`2` o
   columnas `0`–`2`.
5. Para cada desplazamiento permitido, calcula el índice vecino, intercambia
   allí el cero con la ficha y crea un sucesor.

El nombre de la acción indica hacia dónde se mueve el **espacio vacío**. La
ficha vecina se desliza en sentido contrario. Por ejemplo, si el espacio vacío
se mueve a la derecha, la ficha situada a su derecha se desliza a la izquierda.

## Costos de movimiento

Cada posible transición define un costo:

| Dirección del espacio vacío | Cambio de fila | Cambio de columna | Costo |
|---|---:|---:|---:|
| Arriba | -1 | 0 | 1 |
| Abajo | +1 | 0 | 2 |
| Izquierda | 0 | -1 | 3 |
| Derecha | 0 | +1 | 4 |

El costo del sucesor se calcula como:

```text
costo_acumulado_del_sucesor =
    costo_acumulado_actual + costo_de_la_accion
```

BFS y DFS reportan la cantidad de movimientos y no usan estos costos para
ordenar su búsqueda. UCS usa el costo acumulado como prioridad; A* lo combina
con la heurística Manhattan.

## Relación padre-hijo

Cada sucesor establece `padre=self` y guarda la acción y el costo acumulado
actualizado. De esta manera, los algoritmos pueden guardar el estado encontrado
sin copiar explícitamente toda la ruta en cada nodo. Al llegar a la meta,
`reconstruir_camino` recorre los padres y recoge las acciones para producir el
camino en orden de ejecución.

Para no modificar el tablero del estado actual, el método lo convierte
temporalmente en una lista, realiza el intercambio y guarda el tablero
resultante del nuevo estado como una tupla.
