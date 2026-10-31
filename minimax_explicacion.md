# Cómo funciona `minimax.py`

Este programa implementa el juego de tres en línea para una persona contra
una IA. La IA usa el algoritmo **Minimax** para evaluar sus jugadas y también
ejecuta una versión con **poda alfa-beta** para reducir la cantidad de
posiciones que necesita explorar.

## Reglas y representación del tablero

El tablero es una lista de nueve elementos:

```text
índice:   0 | 1 | 2
          3 | 4 | 5
          6 | 7 | 8
```

Cada elemento contiene `'X'`, `'O'` o `' '` (casilla vacía). La persona juega
con `O`; la IA juega con `X`. `imprimir_tablero` presenta esa lista en forma
de cuadrícula, y `obtener_movimientos` devuelve los índices de las casillas
que todavía pueden jugarse.

`verificar_ganador` comprueba las ocho combinaciones ganadoras: tres filas,
tres columnas y las dos diagonales. `es_terminal` considera que la partida
terminó si alguno de los jugadores ganó o si ya no quedan casillas vacías.

## Puntuación de las posiciones

`funcion_evaluacion` traduce el resultado del tablero a una puntuación:

| Resultado | Puntuación |
|---|---:|
| Victoria de `X` (IA) | `+10` |
| Victoria de `O` (persona) | `-10` |
| Sin ganador | `0` |

La IA maximiza esta puntuación y la persona se modela como un oponente que
intenta minimizarla. La función no pondera cuánto falta para ganar: cualquier
victoria de `X` vale `+10`, independientemente de su distancia.
También devuelve `0` para una posición sin ganador cuando la búsqueda alcanza
el límite de profundidad; el evaluador no estima amenazas o victorias futuras.

## Minimax sin poda

`minimax(tablero, profundidad, maximizando)` examina de forma recursiva los
movimientos posibles:

1. Cuenta la llamada actual en `nodos_sin_poda`.
2. Si la partida terminó o `profundidad` llegó a cero, devuelve la evaluación
   del tablero.
3. Si toca maximizar, simula cada movimiento de `X` y conserva la puntuación
   más alta.
4. Si toca minimizar, simula cada movimiento de `O` y conserva la puntuación
   más baja.
5. En cada rama, reduce la profundidad en uno y alterna entre maximizar y
   minimizar.

La función escribe temporalmente el símbolo en el tablero para explorar una
jugada y luego vuelve a dejar esa casilla vacía. Así, cada alternativa parte
del mismo estado y el tablero original queda restaurado al terminar la
búsqueda.

## Poda alfa-beta

`alfa_beta` devuelve la misma clase de puntuación que Minimax, pero mantiene
dos límites durante la exploración:

- **Alfa**: la mejor puntuación que `X` puede garantizar hasta el momento.
- **Beta**: la mejor puntuación que `O` puede garantizar hasta el momento.

En un turno de `X`, alfa se actualiza al encontrar puntuaciones mayores; en un
turno de `O`, beta se actualiza al encontrar puntuaciones menores. Cuando
`beta <= alfa`, continuar con los demás movimientos de esa rama no puede
cambiar la decisión de los niveles anteriores, por lo que la función los
omite. Cada llamada se cuenta en `nodos_con_poda`.

La poda cambia el trabajo realizado, no la puntuación óptima encontrada para
el mismo tablero, profundidad y orden de movimientos.

## Elección de la jugada y métricas

`mejor_movimiento_ia(tablero, profundidad_limite=9)`:

1. Reinicia ambos contadores.
2. Prueba cada casilla libre como candidata para `X`.
3. Ejecuta Minimax sin poda para contar sus nodos; su puntuación se descarta.
4. Ejecuta alfa-beta para obtener la puntuación de esa candidata.
5. Conserva la casilla con la mayor puntuación alfa-beta.
6. Devuelve una tupla `(índice, nodos_sin_poda, nodos_con_poda)`.

El límite predeterminado es nueve turnos de búsqueda contando la jugada
candidata: después de colocar `X`, ambas búsquedas reciben profundidad ocho.
En tres en línea, este límite permite explorar hasta el final desde una
partida nueva. Si dos movimientos tienen la misma puntuación, se conserva el
primero según el orden de índices de las casillas.

Los contadores acumulan las llamadas de todas las candidatas analizadas para
una decisión. Por eso las métricas que imprime el juego permiten comparar el
número de nodos explorados por ambos algoritmos en ese turno. Minimax se
ejecuta como referencia de coste, aunque la jugada se elige con el resultado
de alfa-beta.

## Flujo de la partida

`jugar_adversario` crea un tablero vacío y alterna turnos:

1. Solicita a la persona el índice de una casilla, entre `0` y `8`.
2. Si la casilla ya está ocupada, vuelve a solicitar un movimiento.
3. Actualiza y muestra el tablero después de cada jugada.
4. Si la partida no terminó tras el turno de la persona, calcula y coloca la
   jugada de la IA; muestra también las métricas de búsqueda.
5. Al terminar, anuncia la victoria de `X`, la victoria de `O` o el empate.

La entrada espera un entero dentro del rango `0`–`8`; el controlador solo
comprueba si la casilla elegida está libre.
