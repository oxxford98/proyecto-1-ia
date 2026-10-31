# Proyecto 1 - Algoritmos de búsqueda

Aplicación de consola en Python con dos modos:

1. **8-Puzzle:** resuelve el tablero de prueba usando DFS, BFS, UCS o A*.
2. **Tres en línea:** permite jugar como `O` contra la IA, que juega como `X`
   usando Minimax y poda alfa-beta.

## Requisitos

- Python 3 instalado y disponible como `py`, `python` o `python3`, según el
  sistema operativo.
- No se necesitan paquetes externos. El proyecto utiliza únicamente módulos
  incluidos en la biblioteca estándar de Python.

## Abrir el proyecto

Descarga o clona el proyecto desde la plataforma donde te lo compartieron.
Abre una terminal en la carpeta del proyecto, es decir, en la carpeta que
contiene `main.py`, `estado.py` y los demás archivos `.py`. No hace falta crear
un entorno virtual ni instalar paquetes.

## Ejecutar

En Windows, abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py main.py
```

Si el comando `py` no está disponible, prueba:

```powershell
python main.py
```

En macOS o Linux, ejecuta:

```bash
python3 main.py
```

Al iniciar se muestra el menú principal:

```text
1. Resolver 8-Puzzle (Un Agente)
2. Jugar contra la Máquina (Minimax Adversario)
3. Salir
```

Escribe el número de la opción y presiona **Enter**.

### Resolver el 8-Puzzle

1. En el menú principal, escribe `1`.
2. Elige un algoritmo:
   - `1`: DFS
   - `2`: BFS
   - `3`: UCS
   - `4`: A*
   - `5`: volver al menú principal
3. La aplicación muestra el camino, el tablero inicial y cada tablero
   resultante de los movimientos, además de las métricas de búsqueda.

El tablero inicial de prueba se define en `main.py`, en la línea que crea
`EstadoPuzzle`. Puedes cambiar esa tupla por cualquier permutación válida de
los números `0` a `8`. Para que el tablero estándar 3x3 tenga solución, al
contar los pares de fichas fuera de orden (sin contar el `0`) debe haber un
número par de inversiones. Si la paridad es impar, el programa avisa y no
ejecuta una búsqueda que no puede encontrar la meta.

### Jugar tres en línea

1. En el menú principal, escribe `2`.
2. Eres `O` y la IA es `X`.
3. Escribe el índice de una casilla vacía cuando se solicite. Las posiciones
   van de `0` a `8`:

   ```text
   0 | 1 | 2
   ---+---+---
   3 | 4 | 5
   ---+---+---
   6 | 7 | 8
   ```

4. La aplicación muestra el tablero después de cada turno y las métricas de
   búsqueda de la IA.

Para cerrar una partida y terminar la aplicación, vuelve al menú principal y
elige `3`.

## Archivos principales

- `main.py`: menú e interacción por consola.
- `estado.py`: estado, movimientos y costos del 8-Puzzle.
- `algoritmos_no_informados.py`: DFS y BFS.
- `algoritmos_informados.py`: UCS y A*.
- `minimax.py`: juego de tres en línea y búsqueda Minimax.
