# Proyecto 1 - Algoritmos de búsqueda

Aplicación en Python con versiones de consola y escritorio, y dos modos:

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

### Interfaz gráfica (recomendada para presentar)

Abre una terminal en la carpeta del proyecto y ejecuta en Windows:

```powershell
py interfaz.py
```

También puedes usar `python interfaz.py`; en macOS/Linux,
`python3 interfaz.py`. Se recomienda Python 3.10 o posterior para la interfaz.
La ventana utiliza Tkinter, incluido normalmente con Python; no requiere
paquetes de `pip`. Puedes comprobar su disponibilidad con `py -m tkinter`
(o `python3 -m tkinter`). Si no está instalado, agrega el componente Tcl/Tk
desde el instalador de Python; en Linux instala el paquete de Tkinter de tu
distribución.

**Pestaña 8-Puzzle y comparación:**

1. Ingresa los números del `0` al `8`, sin repetir, o carga un ejemplo.
   El `0` representa el espacio vacío; los tableros imposibles se rechazan.
2. Elige DFS, BFS, UCS o A* y pulsa **Resolver**.
3. Pulsa **Comparar los cuatro** para ejecutar todos sobre la misma entrada.
   La tabla muestra nodos expandidos, tiempo de búsqueda, movimientos y costo
   ponderado. El tiempo excluye la animación y la comprobación posterior de
   la ruta. No se mide memoria en la ventana.
4. Selecciona una fila y pulsa **Paso** o **Reproducir** para observar
   los movimientos. **Pausar** detiene la animación; **Ver meta** muestra
   directamente el tablero final verificado.
5. Las rutas de DFS pueden ser muy largas: no se limita la búsqueda ni se
   ocultan sus métricas, pero la animación se inicia manualmente.

Si editas la entrada después de resolver, pulsa nuevamente **Resolver** para
calcular la nueva ruta; cada fila mantiene el tablero original que se evaluó.
Las búsquedas se realizan en un hilo de trabajo y la ventana sigue atendiendo
eventos. Los controles de cálculo y juego se bloquean durante cada operación
para evitar búsquedas simultáneas. No hay cancelación individual de búsquedas;
puedes cerrar la ventana para terminar la aplicación.

**Pestaña Tres en línea:**

1. Haz clic en una casilla libre para jugar como `O`.
2. La IA responde como `X`; se muestran los nodos con y sin poda y su reducción.
3. Al finalizar se muestra victoria o empate. **Nueva partida** reinicia
   el tablero y las métricas.

### Versión de consola

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
- `interfaz.py`: ventana Tkinter, animación, comparación y juego con clics.
- `estado.py`: estado, movimientos y costos del 8-Puzzle.
- `algoritmos_no_informados.py`: DFS y BFS.
- `algoritmos_informados.py`: UCS y A*.
- `minimax.py`: juego de tres en línea y búsqueda Minimax.
