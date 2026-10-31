# Preguntas y respuestas para la presentación

Guía de preparación para explicar y defender el proyecto de búsqueda en el
8-Puzzle y el juego adversario de tres en línea. Las respuestas están basadas
en la implementación actual del repositorio. Se recomienda comprenderlas y
expresarlas con palabras propias, no memorizarlas literalmente.

## 1. Preguntas generales del proyecto

### 1. ¿Qué problema resuelve la aplicación?

La aplicación de consola reúne dos problemas de inteligencia artificial. En
el 8-Puzzle compara DFS, BFS, búsqueda de costo uniforme y A*. En tres en
línea, una persona juega contra una IA que decide con Minimax y poda
alfa-beta.

### 2. ¿Por qué eligieron estos problemas?

El 8-Puzzle permite comparar algoritmos de búsqueda sobre el mismo espacio de
estados y observar diferencias de optimalidad, costo y cantidad de nodos. Tres
en línea permite mostrar decisiones adversarias: cada jugador intenta
maximizar su propio resultado frente al otro.

### 3. ¿Cómo ejecuto el programa?

Desde una terminal abierta en la carpeta del proyecto, en Windows se ejecuta
`py interfaz.py` para la interfaz gráfica o `py main.py` para la consola.
También se puede usar `python` en lugar de `py`; en macOS/Linux, `python3`.
La interfaz requiere Tkinter y Python 3.10 o posterior. No se requieren
paquetes de `pip`. El paso a paso está en el [README](./README.md).

### 4. ¿Qué hace cada módulo principal?

- [main.py](./main.py): muestra los menús, llama al algoritmo seleccionado e
  imprime resultados.
- [interfaz.py](./interfaz.py): permite ingresar tableros, animar soluciones,
  comparar resultados y jugar con clics, reutilizando los mismos algoritmos.
- [estado.py](./estado.py): representa un estado del 8-Puzzle y genera los
  movimientos legales.
- [algoritmos_no_informados.py](./algoritmos_no_informados.py): implementa
  DFS y BFS.
- [algoritmos_informados.py](./algoritmos_informados.py): implementa UCS y A*.
- [minimax.py](./minimax.py): implementa el juego de tres en línea, Minimax y
  alfa-beta.

## 2. Preguntas sobre el 8-Puzzle

### 5. ¿Cómo se representa un estado del 8-Puzzle?

Se representa mediante una tupla de nueve enteros ordenados por filas. Los
números del 1 al 8 son las fichas y `0` representa el espacio vacío. La tupla
puede usarse para identificar un tablero en los conjuntos de estados
explorados.

### 6. ¿Qué significan las acciones “Arriba”, “Abajo”, “Izquierda” y “Derecha”?

Indican la dirección en que se mueve el espacio vacío, no la ficha. Por
ejemplo, si el vacío se mueve a la derecha, la ficha que estaba a su derecha
se desliza a la izquierda.

### 7. ¿Cuál es la condición de meta?

El tablero debe quedar como `(1, 2, 3, 4, 5, 6, 7, 8, 0)`: las fichas
ordenadas por filas y el espacio vacío en la última posición.

### 8. ¿Por qué algunos tableros no tienen solución?

Los movimientos legales conservan la paridad de las inversiones. En este
tablero de ancho impar, una configuración alcanza la meta estándar solo si el
número de inversiones entre fichas no vacías es par. Una inversión es un par
de fichas que aparece en el orden contrario al objetivo. El programa comprueba
esta condición antes de ejecutar la búsqueda.

### 9. ¿Qué significa el tablero inicial configurado actualmente?

En `main.py` el tablero inicial del menú es
`(6, 2, 4, 0, 3, 5, 7, 8, 1)`. Tiene 12 inversiones, por lo que supera la
comprobación de paridad y es resoluble. Para probarlo con otro estado se
modifica esa tupla; debe ser una permutación de `0` a `8`.

### 10. ¿Qué diferencia hay entre un movimiento y su costo?

La longitud de una ruta cuenta cuántas acciones contiene. El costo suma el
valor asignado a cada acción. En el modelo actual, Arriba cuesta 1, Abajo 2,
Izquierda 3 y Derecha 4. Por ello, dos rutas con igual número de pasos pueden
tener costos diferentes.

### 11. ¿Qué guarda cada nodo del espacio de búsqueda?

`EstadoPuzzle` guarda el tablero, el estado padre, la acción que generó el
nodo y el costo acumulado desde el inicio. La referencia al padre permite
reconstruir el camino al encontrar la meta sin almacenar una copia completa
del camino en cada nodo.

## 3. Preguntas sobre los algoritmos de búsqueda

### 12. ¿Cómo funciona DFS?

DFS usa una pila LIFO: procesa primero el último estado insertado y continúa
profundizando en una rama antes de retroceder. En este espacio finito usa un
conjunto de estados expandidos para evitar volver a expandir tableros. Puede
encontrar una solución, pero no garantiza que sea corta ni de costo mínimo.

### 13. ¿Por qué DFS encontró una ruta de más de cien mil movimientos cuando el estado estaba a un paso?

DFS no sabe cuál estado está más cerca de la meta: su decisión depende del
orden de sucesores y de la pila. Esta implementación no mantiene un conjunto
de estados pendientes, así que puede poner tableros repetidos en la pila. En
la prueba del estado a un paso, encontró una ruta de 106 329 acciones antes de
encontrar la solución. Esto no es un error de que la meta sea inalcanzable;
es una consecuencia de la estrategia DFS y su orden de exploración.

### 14. ¿Cómo funciona BFS?

BFS usa una cola FIFO y explora primero todos los estados de una profundidad
antes de pasar a la siguiente. Por eso, cuando cada movimiento cuenta igual,
la primera solución hallada tiene el menor número de movimientos.

### 15. ¿BFS encuentra siempre la ruta de menor costo?

No con los costos direccionales de este proyecto. BFS minimiza el número de
acciones, no la suma de sus costos. Para costo mínimo se usan UCS o A*.

### 16. ¿Qué diferencia a UCS de BFS?

BFS prioriza por cantidad de pasos desde el inicio, mientras que UCS prioriza
por `g(n)`, el costo acumulado real. UCS es apropiado cuando los costos de
acción no son iguales y, con costos positivos, devuelve una ruta de costo
mínimo.

### 17. ¿Qué significa `g(n)` en UCS y A*?

`g(n)` es el costo real acumulado desde el estado inicial hasta el estado
actual. En el programa se guarda en `costo_acumulado`.

### 18. ¿Cómo funciona A*?

A* prioriza cada estado usando `f(n) = g(n) + h(n)`: el costo real ya pagado
más una estimación del costo que falta. Aquí `h(n)` es la distancia Manhattan.
Al devolver la solución, el algoritmo reporta el costo real `g`, no el valor
estimado `f`.

### 19. ¿Por qué A* expande menos nodos que UCS en los casos medidos?

UCS solo conoce el costo acumulado. A* también usa Manhattan para ordenar la
frontera hacia estados que parecen más próximos al objetivo. En los tres
casos probados, A* expandió menos nodos que UCS; esto es un resultado de esos
tableros y no una promesa de que siempre lo hará en cualquier instancia.

### 20. ¿Qué se considera un nodo expandido?

Es un estado extraído y procesado para generar sus sucesores. La meta se
comprueba antes del incremento del contador, así que el nodo meta no se cuenta
como expandido. En Minimax, el contador tiene una interpretación distinta:
cuenta llamadas recursivas de la búsqueda.

### 21. ¿Qué algoritmos son completos y óptimos?

En el espacio finito del 8-Puzzle, las implementaciones terminan si la
frontera se agota o se encuentra la meta. BFS es óptima en cantidad de pasos
cuando todos los pasos se consideran iguales; UCS es óptima en costo
acumulado con costos positivos; A* es óptima con una heurística admisible y
consistente como Manhattan. DFS no garantiza optimalidad.

### 22. ¿Qué significan las complejidades mencionadas en el informe?

Son cotas teóricas en función del factor de ramificación, la profundidad o el
costo de la solución. Describen cómo puede crecer el trabajo y la memoria al
aumentar el problema; no son los tiempos exactos de una ejecución concreta.
En un grafo con estados repetidos también influyen las estructuras de estados
explorados y pendientes.

## 4. Preguntas sobre Manhattan y A*

### 23. ¿Cómo se calcula la distancia Manhattan?

Para cada ficha distinta de cero, se compara su fila y columna actual con su
fila y columna objetivo. Se suma
`|fila_actual - fila_objetivo| + |columna_actual - columna_objetivo|`.
El espacio vacío no se incluye.

### 24. ¿Cuál es el valor de Manhattan para el caso P3?

P3 es:

```text
1 | 2 | 3
0 | 4 | 5
7 | 8 | 6
```

Las fichas 4, 5 y 6 están cada una a una posición de su lugar objetivo; las
demás están colocadas. Por eso `h(n) = 1 + 1 + 1 = 3`.

### 25. ¿Por qué Manhattan es admisible?

Porque no sobreestima el costo restante. Cada ficha necesita al menos tantos
desplazamientos como su distancia Manhattan y cada movimiento cuesta al
menos 1. Las interacciones entre fichas pueden exigir más movimientos, pero
no menos que esa suma.

### 26. ¿Qué significa que Manhattan sea consistente?

Para cada transición de un estado `n` a un sucesor `n'`, cumple
`h(n) <= costo(n,n') + h(n')`. En un movimiento solo una ficha cambia su
Manhattan en una unidad como máximo y cualquier acción cuesta al menos 1.
Esta propiedad respalda que A* no necesite reabrir estados ya expandidos en
esta implementación.

### 27. ¿Se probaron otras heurísticas?

No. El código utiliza únicamente Manhattan; la evaluación experimental compara
algoritmos de búsqueda, no varias heurísticas. Una mejora sería implementar
otra heurística admisible y comparar sus expansiones sobre los mismos
tableros.

## 5. Preguntas sobre Minimax y alfa-beta

### 28. ¿Quién maximiza y quién minimiza?

La IA es `X` y maximiza la utilidad. La persona es `O` y se modela como un
oponente que minimiza la utilidad de `X`.

### 29. ¿Cuál es la función de utilidad?

Devuelve `+10` si gana `X`, `-10` si gana `O` y `0` en los demás casos. No
pondera amenazas ni prefiere explícitamente victorias rápidas. Con profundidad
9, la búsqueda cubre las jugadas restantes de tres en línea desde la posición
de la IA.

### 30. ¿Qué son alfa y beta?

Alfa es el mejor valor que el jugador maximizador puede garantizar en el
camino actual; beta es el mejor valor que puede garantizar el minimizador. Si
`beta <= alfa`, explorar las alternativas restantes de ese nodo no puede
cambiar la decisión de un ancestro, así que se poda esa rama.

### 31. ¿La poda alfa-beta cambia la jugada óptima?

No, si la búsqueda explora el mismo árbol y usa la misma función de utilidad.
Alfa-beta omite ramas que no pueden afectar el valor de Minimax; el propósito
es reducir trabajo, no cambiar el resultado.

### 32. ¿Qué se midió en la comparación de Minimax?

`mejor_movimiento_ia()` ejecuta búsqueda sin poda y búsqueda alfa-beta para
cada posible movimiento de la IA. Los contadores son llamadas/nodos visitados
por las búsquedas, incluyendo nodos internos y llamadas de hojas; no solo
posiciones terminales. La decisión final usa la puntuación de alfa-beta.

### 33. ¿Qué significan los 55 504 y 6 138 nodos?

Son los totales medidos al recomendar el movimiento de la IA cuando la persona
había jugado en el centro (`O` en índice 4): 55 504 llamadas sin poda y 6 138
con alfa-beta. La reducción en esa posición fue aproximadamente 88,94 %. Es
un ejemplo observado; depende del tablero y del orden de movimientos.

### 34. ¿Por qué el tablero de tres en línea usa una lista mutable?

Durante cada rama Minimax coloca temporalmente una ficha, evalúa el estado
resultante y restaura la casilla a `' '`. Así explora alternativas sobre el
mismo tablero sin crear una copia completa por cada llamada.

## 6. Preguntas sobre las pruebas y resultados

### 35. ¿Cuáles fueron los casos comparados?

Se probaron tres estados resolubles:

- P1: `(1, 2, 3, 4, 5, 6, 7, 0, 8)`, a un movimiento.
- P2: `(1, 2, 3, 4, 0, 6, 7, 5, 8)`, a dos movimientos mínimos.
- P3: `(1, 2, 3, 0, 4, 5, 7, 8, 6)`, a tres movimientos mínimos.

Los cuatro algoritmos se ejecutaron sobre el mismo tablero dentro de cada
caso.

### 36. ¿Cuál fue el resultado más importante?

A* expandió 2, 4 y 8 nodos en P1, P2 y P3; BFS expandió 3, 8 y 18; UCS, 4,
11 y 22. DFS devolvió rutas no óptimas de 106 329, 30 y 13 443 movimientos,
respectivamente. Los datos muestran especialmente la falta de optimalidad de
DFS y la utilidad de la heurística en estos casos cercanos a la meta.

### 37. ¿Por qué BFS y UCS reportan números diferentes para la misma ruta?

El tercer valor que devuelve BFS/DFS es la longitud de la ruta. El tercer
valor de UCS/A* es el costo ponderado acumulado. Por ejemplo, P3 tiene tres
movimientos y un costo de 10 (`Derecha` cuesta 4, otra `Derecha` cuesta 4 y
`Abajo` cuesta 2).

### 38. ¿Cómo se midieron tiempo y memoria?

El tiempo se midió con `time.perf_counter()`. El pico de asignaciones Python
se midió con `tracemalloc`, reiniciándolo por algoritmo. `tracemalloc` no es
la memoria residente total del proceso y su instrumentación puede afectar los
tiempos, especialmente en ejecuciones muy cortas. Por eso las cifras sirven
para comparar estas pruebas, no como valores universales de rendimiento.

### 39. ¿Por qué los resultados pueden cambiar en otra computadora?

El tiempo depende del procesador, del intérprete, de la carga del sistema y de
si se activa la instrumentación de memoria. El número de nodos y la ruta
dependen del tablero y del orden de sucesores; para el mismo código y tablero
determinista, normalmente se mantienen iguales.

### 40. ¿Qué evidencia falta para entregar?

El informe contiene resultados ejecutados y una lista de capturas
recomendadas, pero las capturas deben obtenerse desde la consola y añadirse al
documento. También deben completarse los nombres de integrantes y docente en
la portada.

## 7. Preguntas críticas y mejoras futuras

### 41. ¿Cuál es la principal limitación de DFS en esta implementación?

No evita duplicados mientras los estados esperan en la pila y no prioriza
estados cercanos a la meta. Esto puede causar muchas inserciones repetidas y
rutas enormes. Un conjunto de estados pendientes podría reducir duplicados,
pero DFS seguiría sin garantizar una solución óptima.

### 42. ¿Por qué el menú comprueba inversiones?

La búsqueda solo puede recorrer estados alcanzables mediante movimientos
legales. Si el tablero tiene paridad incompatible con la meta, la frontera
podría recorrer los 181 440 estados alcanzables y aun así no encontrarla. La
comprobación previa informa el problema de inmediato.

### 43. ¿Qué mejorarían si continuaran el proyecto?

La interfaz gráfica ya permite ingresar el tablero con validación. Como
mejoras futuras proponemos mejorar el control de estados
pendientes y costos en las búsquedas; evaluar heurísticas adicionales; dar
preferencia en Minimax a victorias rápidas y derrotas tardías; y ampliar las
pruebas a tableros de mayor dificultad con más repeticiones de tiempo y
mediciones de memoria del proceso.

### 44. ¿Qué aprendieron del proyecto?

Que elegir la frontera cambia qué solución se encuentra y cuánto cuesta
encontrarla; que una heurística útil debe justificarse, no solo parecer
intuitiva; y que la poda alfa-beta puede conservar la decisión de Minimax
reduciendo las ramas exploradas. También aprendimos a separar métricas como
profundidad, costo, expansiones y memoria, porque no significan lo mismo.

## Recomendación para la defensa

- Explique primero el problema y la representación del estado.
- Use P3 para comparar BFS, UCS y A*: es pequeño y permite calcular
  manualmente Manhattan y el costo de la ruta.
- Use P1 para explicar por qué DFS no es óptimo.
- Use la posición con `O` en el centro para explicar la poda alfa-beta y sus
  contadores.
- Si una pregunta se refiere a tiempos o memoria, aclare que son mediciones
  de una ejecución instrumentada y dependientes del entorno.
- Si no conoce un dato, distinga entre lo que garantiza la teoría y lo que se
  midió en los casos del proyecto.

## 8. Guion de exposición según los bloques de la rúbrica

Esta sección responde a los puntos de la tabla compartida: qué explicar y
qué mostrar durante la presentación. Los bloques 2 a 6 suman **13 minutos**;
el tiempo del primer bloque no se distingue en el recorte de la imagen.
Asigna a ese bloque el tiempo que indique la rúbrica completa.

### Bloque 1. Presentación de la aplicación y modelado del problema

**Qué decir:**

> Nuestro proyecto compara búsquedas de un agente y búsqueda adversaria.
> En el 8-Puzzle representamos el estado con nueve números en una tupla.
> El cero es el espacio vacío y las acciones mueven ese espacio arriba,
> abajo, a la izquierda o a la derecha, intercambiándolo con una ficha
> vecina. La meta es ordenar las fichas del 1 al 8 y dejar el cero al final.
> En tres en línea participan una persona, con O, y una máquina, con X.
> Cada acción ocupa una casilla libre. La partida termina cuando hay tres
> símbolos iguales alineados o cuando el tablero está lleno.

**Qué mostrar:** abre [interfaz.py](./interfaz.py) con `py interfaz.py`,
señala las dos pestañas y carga el ejemplo **3 movimientos**:

```text
Inicial                 Meta
1 | 2 | 3               1 | 2 | 3
0 | 4 | 5               4 | 5 | 6
7 | 8 | 6               7 | 8 | 0
```

Aclara que una entrada debe contener todos los números de 0 a 8 sin repetir.
Además, se verifica la paridad de las inversiones para rechazar tableros que
no pueden alcanzar la meta estándar.

### Bloque 2. Demostración en vivo — 4 minutos

**Qué hacer y explicar:**

1. **Entrada y selección:** en la pestaña 8-Puzzle, carga **3 movimientos**,
   selecciona **BFS** y pulsa **Resolver**.
2. **Resultados:** señala la fila de BFS: 18 nodos expandidos, 3 movimientos
   y costo ponderado 10. El tiempo corresponde a la búsqueda, no a la
   animación ni a la comprobación posterior de la ruta.
3. **Solución visual:** selecciona la fila y pulsa **Paso** tres veces o
   **Reproducir**. Explica que el vacío se mueve Derecha, Derecha y Abajo;
   las fichas 4, 5 y 6 se deslizan en sentido contrario.
4. **Comparación:** carga **2 movimientos** y pulsa **Comparar los cuatro**.
   Deja esta tabla disponible para los siguientes bloques. Todos los
   algoritmos reciben exactamente el mismo tablero.
5. **Modo adversario:** abre Tres en línea y juega O en el centro.
   La IA responde con X en la esquina de índice 0. Señala las métricas
   de búsqueda con y sin poda.

**Frase para acompañar la demostración:**

> La interfaz no reemplaza los algoritmos: reutiliza las funciones del
> proyecto de consola. Podemos observar tanto la solución como el trabajo
> necesario para encontrarla. La búsqueda se ejecuta en un hilo de trabajo
> y el hilo principal actualiza la ventana y la animación.

No reproduzcas rutas DFS enormes durante la exposición. Para mostrar el
resultado sin recorrer cada paso, selecciona su fila y pulsa **Ver meta**.

### Bloque 3. DFS y BFS — 2 minutos

**Cómo recorren el espacio y qué estructura usan:**

> DFS usa una pila: procesa el último estado agregado y sigue una rama antes
> de volver a otras alternativas. BFS usa una cola: procesa los estados por
> niveles de profundidad. Ambos evitan volver a expandir tableros ya
> explorados, pero BFS también evita duplicados pendientes en la frontera.

**En qué se diferencian sus soluciones:**

> BFS encuentra una solución con el menor número de movimientos. DFS
> devuelve la primera solución encontrada y no garantiza longitud ni costo
> mínimos. En el ejemplo de dos movimientos, DFS devuelve 30 movimientos
> con costo 68; BFS devuelve 2 movimientos con costo 6.

**Qué mostrar:** en la tabla del ejemplo **2 movimientos**, compara:

| Algoritmo | Frontera | Nodos expandidos | Movimientos | Costo ponderado |
|---|---|---:|---:|---:|
| DFS | Pila LIFO | 30 | 30 | 68 |
| BFS | Cola FIFO | 8 | 2 | 6 |

Precisión importante: **encontrar una solución no significa que sea óptima**.
Tampoco debe confundirse el número de nodos expandidos con la longitud de la
solución: BFS puede explorar estados que no forman parte del camino final.

### Bloque 4. Costo uniforme y A* — 3 minutos

**Cómo se definieron los costos:**

> Asignamos costos diferentes por dirección: Arriba 1, Abajo 2,
> Izquierda 3 y Derecha 4. Es una decisión del modelo para distinguir
> minimizar pasos de minimizar costo. UCS usa una cola de prioridad que
> selecciona el menor costo acumulado g(n). A* usa una cola de prioridad
> ordenada por f(n) = g(n) + h(n).

**Qué heurística se utilizó y cómo justificarla:**

> Usamos la distancia Manhattan: sumamos para cada ficha la diferencia
> de filas y columnas respecto a su posición objetivo, sin contar el cero.
> En el ejemplo de tres movimientos, las fichas 4, 5 y 6 están cada una
> a una casilla de su destino, así que h vale 3. La heurística es
> admisible porque cada desplazamiento cuesta al menos uno y las fichas
> no pueden llegar con menos desplazamientos que su distancia Manhattan.
> Es consistente porque una transición cambia esa suma como máximo en
> una unidad y su costo es al menos uno.

**Por qué A* expande menos nodos en las pruebas:**

> UCS solo considera el costo pagado. A* añade una estimación de lo que
> falta, por lo que orienta la exploración hacia la meta. En el ejemplo de
> dos movimientos, UCS expande 11 nodos y A* expande 4; ambos obtienen una
> ruta de dos movimientos y costo 6. En estos casos A* reduce las
> expansiones; no afirmamos que siempre sea más rápido en cualquier problema.

**Qué mostrar:** las filas UCS y A* del mismo ejemplo **2 movimientos**.
Si usas el ejemplo de Manhattan de tres pasos, muéstralo en una diapositiva
para no reemplazar accidentalmente la tabla del caso de dos pasos.

No digas que se compararon varias heurísticas: el proyecto implementa
únicamente Manhattan.

### Bloque 5. Minimax con poda alfa-beta — 2 minutos

**Cómo decide la máquina y qué función evalúa:**

> La IA simula sus movimientos y las respuestas del rival. X maximiza la
> utilidad y O la minimiza. La evaluación vale +10 si gana X, -10 si gana O
> y 0 para empate o un estado sin ganador al límite de búsqueda. El límite
> predeterminado de nueve turnos permite alcanzar los estados terminales
> del juego. No se premian victorias más rápidas.

**Cómo funciona la poda:**

> Alfa guarda un límite para el maximizador y beta para el minimizador.
> Cuando beta es menor o igual que alfa, las alternativas restantes del
> nodo no pueden mejorar la decisión de los ancestros y se dejan de
> explorar. La poda ahorra trabajo sin cambiar el valor de Minimax.

Ejemplo conceptual: si X ya tiene una alternativa con valor 0, y al explorar
otra alternativa O encuentra una respuesta con valor -10, ese nodo
minimizador puede valer como máximo -10. X no preferirá esa alternativa sobre
su 0, así que pueden omitirse las otras respuestas de O en ese nodo.

**Qué mostrar y cuánto se ahorró:** con una partida nueva, coloca O en el
centro y señala los contadores:

| Sin poda | Con alfa-beta | Nodos evitados | Reducción |
|---:|---:|---:|---:|
| 55 504 | 6 138 | 49 366 | Aproximadamente 88,94 % |

Los contadores suman las llamadas recursivas de todas las candidatas de esa
decisión. La aplicación ejecuta **ambas búsquedas** para comparar nodos;
por tanto, el ahorro de nodos de alfa-beta no equivale a una reducción del
88,94 % del tiempo total de la aplicación.

### Bloque 6. Comparación y conclusiones — 2 minutos

**Qué mostrar:** la tabla del ejemplo **2 movimientos**, que resume:

| Algoritmo | Nodos expandidos | Movimientos | Costo ponderado |
|---|---:|---:|---:|
| DFS | 30 | 30 | 68 |
| BFS | 8 | 2 | 6 |
| UCS | 11 | 2 | 6 |
| A* | 4 | 2 | 6 |

Señala también la columna de tiempo de la ventana. Es una medición en vivo,
por lo que no tiene que coincidir con los tiempos del informe.
La ventana **no mide memoria**; las cifras de memoria del informe se
obtuvieron separadamente con `tracemalloc` y sus tiempos incluyen la
sobrecarga de esa instrumentación.

**Conclusión que puedes decir:**

> Aprendimos que la estructura de la frontera cambia el orden de búsqueda
> y la calidad de la solución. BFS minimiza movimientos; UCS minimiza
> costos; A* incorpora una heurística justificada para orientar la búsqueda.
> DFS es útil para ilustrar la exploración en profundidad, pero puede hallar
> rutas muy largas. En el juego adversario, alfa-beta conserva la decisión
> de Minimax evitando ramas innecesarias.
>
> Probamos tres casos y no generalizamos los tiempos a todas las entradas.
> Como mejoras proponemos ampliar las pruebas a tableros difíciles, controlar
> mejor los estados pendientes y comparar heurísticas adicionales.

### Lista breve para preparar la presentación

- Comprueba antes de clase que `py interfaz.py` abre la ventana.
- Ensaya la secuencia: BFS con **3 movimientos**, comparación con
  **2 movimientos**, y O en el centro de una partida nueva.
- Conserva capturas y la tabla del [informe](./informe_proyecto_1.md) como
  respaldo si falla la demostración.
- Distingue siempre **nodos**, **movimientos**, **costo** y **tiempo**.
- No atribuyas a la interfaz mediciones de memoria ni optimizaciones que
  todavía no están implementadas.
