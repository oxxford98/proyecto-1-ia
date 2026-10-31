# Búsquedas informadas: UCS y A*

`algoritmos_informados.py` implementa dos búsquedas para resolver el 8-Puzzle:
**Búsqueda de Costo Uniforme (UCS)** y **A***. Ambas usan una cola de prioridad
y devuelven una secuencia de movimientos, la cantidad de nodos expandidos y el
costo acumulado de la solución.

## Modelo de estado y acciones

Las búsquedas reciben un `EstadoPuzzle`, definido en `estado.py`. Cada estado
contiene:

- `tablero`: una tupla de nueve números; `0` representa el espacio vacío.
- `padre`: el estado desde el que se llegó al actual.
- `accion`: el movimiento del espacio vacío que produjo este estado.
- `costo_acumulado`: suma de los costos de las acciones desde el estado inicial.

El estado meta es `(1, 2, 3, 4, 5, 6, 7, 8, 0)`. `generar_sucesores` crea un
estado por cada movimiento legal del espacio vacío. Los costos definidos allí
son:

| Acción del espacio vacío | Costo |
|---|---:|
| Arriba | 1 |
| Abajo | 2 |
| Izquierda | 3 |
| Derecha | 4 |

Estos costos importan para UCS y A*: no todos los caminos con el mismo número
de movimientos tienen necesariamente el mismo costo total. Las acciones
nombran el movimiento del **espacio vacío**, no la dirección en que se desplaza
la ficha que intercambia lugar con él.

## Reconstrucción del camino

`reconstruir_camino(nodo)` sigue las referencias `padre` desde un estado
encontrado hasta el inicial. Mientras retrocede, recopila la acción que llevó
a cada estado; luego invierte esa lista para devolver las acciones en orden
de ejecución. Si el nodo recibido es el estado inicial, devuelve una lista
vacía.

## Búsqueda de Costo Uniforme (UCS)

`ejecutar_ucs(estado_inicial)` elige siempre para expansión el estado pendiente
con menor costo acumulado `g(n)`:

1. Inicializa la frontera con el estado inicial y prioridad cero.
2. Extrae de la cola de prioridad la entrada de menor costo.
3. Si el estado extraído es la meta, reconstruye y devuelve el camino y el
   costo acumulado.
4. Si todavía no fue expandido, lo registra en `explorados` e incrementa
   `nodos_expandidos`.
5. Genera sus sucesores y agrega a la frontera los que aún no estén
   expandidos, con el costo acumulado del sucesor como prioridad.
6. Si la frontera se vacía, devuelve que no hubo solución.

Con costos de acción positivos, el primer estado meta extraído tiene el menor
costo total. En este problema UCS minimiza los costos de la tabla anterior,
no necesariamente la cantidad de movimientos.

## Heurística Manhattan

`calcular_heuristica_manhattan(tablero)` estima el costo que falta para llegar
a la meta. Para cada ficha distinta de cero, obtiene su posición actual y la
posición objetivo. Suma las diferencias absolutas de fila y columna:

```text
distancia = |fila_actual - fila_objetivo|
          + |columna_actual - columna_objetivo|
```

El espacio vacío se omite porque no es una ficha que deba colocarse. La suma
es una cota inferior del costo restante: cada movimiento desplaza una ficha
una casilla y el costo de cada acción es al menos uno. Esta heurística no
cuenta conflictos entre fichas ni intenta estimar más allá de esas distancias.

## Búsqueda A*

`ejecutar_a_star(estado_inicial)` ordena la frontera por:

```text
f(n) = g(n) + h(n)
```

- `g(n)` (`costo_acumulado`) es el costo real desde el inicio.
- `h(n)` es la distancia Manhattan estimada restante.
- `f(n)` combina lo ya pagado con una estimación del costo por pagar.

El procedimiento es similar a UCS: extrae un estado de la frontera, comprueba
si es meta, marca estados como explorados y agrega sucesores. La diferencia
es que A* calcula para cada sucesor `f = costo_acumulado + Manhattan` y usa
ese valor como prioridad. Al encontrar la meta, devuelve el costo real
acumulado, no el valor `f` estimado.

La heurística Manhattan es admisible y consistente con los costos de acciones
de este proyecto porque cada desplazamiento de ficha reduce su distancia
Manhattan a lo sumo en uno y el costo de la acción correspondiente es al menos
uno. Por ello, A* puede priorizar estados prometedores sin sobreestimar el
costo restante.

## Desempate y estados repetidos

Ambas búsquedas insertan tuplas con un contador creciente:

```text
(prioridad, orden_de_inserción, estado)
```

El contador resuelve empates sin que Python tenga que comparar objetos
`EstadoPuzzle`. Entre estados con la misma prioridad, se conserva el orden de
inserción.

`explorados` guarda las tuplas de tablero que ya fueron expandidas, evitando
expandirlas de nuevo. La frontera puede contener duplicados: si un estado
repetido se extrae después de haber sido explorado, no se vuelve a expandir.

## Valores devueltos y métricas

Tanto `ejecutar_ucs` como `ejecutar_a_star` devuelven una tupla:

```text
(camino, nodos_expandidos, costo)
```

- `camino`: lista ordenada de acciones, o `None` si no se encontró solución.
- `nodos_expandidos`: cantidad de estados no meta que se procesaron para
  generar sucesores. El estado meta se comprueba antes de incrementar el
  contador.
- `costo`: costo acumulado de la ruta encontrada; en caso de fallo, el código
  devuelve `0`.

La longitud de `camino` representa el número de movimientos. No debe
confundirse con `costo`: UCS y A* optimizan el costo ponderado, que puede ser
distinto de la longitud. El menú principal mide el tiempo de ejecución y
muestra estos valores junto con la ruta.
