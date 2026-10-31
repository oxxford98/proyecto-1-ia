# Búsquedas no informadas: BFS y DFS

`algoritmos_no_informados.py` implementa dos estrategias para recorrer los
estados del 8-Puzzle sin usar una estimación de qué tan cerca está cada uno de
la meta:

- **BFS** (Búsqueda en Amplitud) explora primero los estados con menos
  movimientos desde el inicio.
- **DFS** (Búsqueda en Profundidad) sigue una rama hasta donde puede antes de
  volver y explorar alternativas.

## Estados, transiciones y objetivo

Ambas funciones reciben un `EstadoPuzzle`, definido en `estado.py`. Su tablero
es una tupla de nueve posiciones y `0` representa el espacio vacío. El estado
meta es:

```text
(1, 2, 3,
 4, 5, 6,
 7, 8, 0)
```

`EstadoPuzzle.generar_sucesores()` crea un estado por cada movimiento legal
del espacio vacío y guarda en el sucesor:

- `padre`: el estado desde el que se hizo el movimiento;
- `accion`: la dirección en que se desplazó el espacio vacío;
- `costo_acumulado`: el costo ponderado acumulado de las acciones.

El orden en que se generan los sucesores es Arriba, Abajo, Izquierda y Derecha.
Ambos algoritmos evitan volver a expandir tableros ya explorados.

## Reconstrucción de la ruta

`reconstruir_camino(nodo)` sigue los enlaces `padre` desde el nodo encontrado
hasta el estado inicial. En cada enlace agrega la acción que produjo el nodo
actual. Como el recorrido va desde la meta hacia el inicio, invierte la lista
antes de devolverla.

Por ejemplo, una lista devuelta como `['Derecha', 'Abajo']` indica que el
espacio vacío se mueve primero a la derecha y luego hacia abajo. Para mostrar
qué ficha se desliza en sentido contrario, el menú principal interpreta esa
lista al imprimir cada tablero.

## Búsqueda en Amplitud (BFS)

`ejecutar_bfs(estado_inicial)` usa una cola FIFO (`collections.deque`):

1. Añade el estado inicial a la cola y a `frontera_estados`.
2. Extrae el estado más antiguo de la cola y lo retira del conjunto de estados
   pendientes.
3. Si es la meta, reconstruye la ruta y la devuelve.
4. Si no es la meta, lo marca como explorado y aumenta
   `nodos_expandidos`.
5. Añade al final de la cola los sucesores que no estén ni explorados ni ya
   pendientes.
6. Si la cola se vacía, devuelve que no se encontró una solución.

Como la cola procesa primero los estados con menor profundidad, BFS encuentra
una solución con la menor cantidad de movimientos cuando cada movimiento
cuenta como un paso. **No minimiza los costos ponderados** definidos para las
acciones en `estado.py`: por ejemplo, un camino más corto puede costar más que
uno más largo. El tercer valor que devuelve BFS es `len(camino)`, es decir, la
profundidad en movimientos, no el costo acumulado del estado.

`frontera_estados` evita encolar varias veces un mismo tablero mientras está
pendiente. `explorados` evita que un tablero ya procesado vuelva a agregarse
posteriormente. Ambos conjuntos se comparan por la tupla del tablero.

## Búsqueda en Profundidad (DFS)

`ejecutar_dfs(estado_inicial)` usa una lista como pila LIFO:

1. Añade el estado inicial a la pila.
2. Extrae el último estado insertado.
3. Si es la meta, reconstruye y devuelve la ruta.
4. Si no fue explorado antes, lo marca como explorado, incrementa el contador
   y agrega a la pila sus sucesores no explorados.
5. Si la pila se vacía, devuelve que no se encontró una solución.

La pila hace que DFS continúe por la rama más recientemente añadida. Para
conservar el orden de exploración Arriba, Abajo, Izquierda y Derecha, el
código agrega los sucesores en orden inverso: el primero que se extrae de la
pila es Arriba, cuando ese movimiento es legal.

DFS devuelve la **primera solución que encuentra**, no necesariamente una de
menor profundidad ni de menor costo. En espacios de búsqueda grandes, el orden
de generación de sucesores puede influir en cuál solución encuentra primero.
En esta implementación, los estados que ya están pendientes en la pila no se
registran en un conjunto separado: puede haber duplicados hasta que se extraen
y se descartan si ya fueron explorados. Además, la meta se comprueba antes de
esa verificación de repetidos. Por eso DFS puede recorrer y devolver una ruta
muy larga incluso si existe una solución cercana; por ejemplo, en una prueba
con un tablero a un movimiento de la meta, la ruta devuelta tuvo 106329 pasos.

## Valor devuelto y contador

Las dos funciones usan la misma forma de resultado:

```text
(camino, nodos_expandidos, profundidad)
```

- `camino`: lista de acciones desde el inicio hasta la meta, o `None` si no se
  encontró una solución.
- `nodos_expandidos`: cantidad de estados no meta para los que se generaron
  sucesores. La meta se comprueba antes de incrementar el contador.
- `profundidad`: número de acciones de la ruta encontrada; en caso de fallo,
  se devuelve `0`.

En BFS, la profundidad de la ruta hallada es mínima en número de movimientos.
En DFS, solo describe la ruta encontrada y no expresa una garantía de
optimalidad. Estos algoritmos no usan `costo_acumulado` para priorizar estados;
para optimizar costos ponderados, el proyecto ofrece UCS y A* en
`algoritmos_informados.py`.
