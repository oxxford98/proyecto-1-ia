"""Interfaz de escritorio que reutiliza las búsquedas de la aplicación."""

from collections.abc import Callable
from dataclasses import dataclass
from queue import Empty, Queue
from threading import Thread
from time import perf_counter
import logging
import tkinter as tk
from tkinter import messagebox, ttk

from algoritmos_informados import ejecutar_a_star, ejecutar_ucs
from algoritmos_no_informados import ejecutar_bfs, ejecutar_dfs
from estado import EstadoPuzzle
from minimax import es_terminal, mejor_movimiento_ia, verificar_ganador


ALGORITMOS = {
    "DFS": ejecutar_dfs,
    "BFS": ejecutar_bfs,
    "UCS": ejecutar_ucs,
    "A*": ejecutar_a_star,
}
EJEMPLOS = {
    "1 movimiento": (1, 2, 3, 4, 5, 6, 7, 0, 8),
    "2 movimientos": (1, 2, 3, 4, 0, 6, 7, 5, 8),
    "3 movimientos": (1, 2, 3, 0, 4, 5, 7, 8, 6),
}
OPUESTAS = {
    "Arriba": "abajo",
    "Abajo": "arriba",
    "Izquierda": "a la derecha",
    "Derecha": "a la izquierda",
}


@dataclass
class ResultadoBusqueda:
    algoritmo: str
    camino: list[str]
    nodos: int
    segundos: float
    costo: int
    tablero_inicial: tuple[int, ...]
    tablero_final: tuple[int, ...]


def validar_tablero(valores: list[str]) -> tuple[int, ...]:
    try:
        tablero = tuple(int(valor) for valor in valores)
    except ValueError as error:
        raise ValueError("Ingresa un entero de 0 a 8 en cada casilla.") from error
    if len(tablero) != 9 or sorted(tablero) != list(range(9)):
        raise ValueError("El tablero debe contener los números de 0 a 8, sin repetir.")
    estado = EstadoPuzzle(tablero)
    if not estado.es_resoluble():
        raise ValueError(
            f"El tablero tiene {estado.contar_inversiones()} inversiones (impar). "
            "No puede alcanzar la meta estándar; usa un tablero con paridad par."
        )
    return tablero


def aplicar_movimiento(tablero: tuple[int, ...], accion: str) -> tuple[int, ...]:
    for sucesor in EstadoPuzzle(tablero).generar_sucesores():
        if sucesor.accion == accion:
            return sucesor.tablero
    raise ValueError(f"El movimiento {accion!r} no es legal en este tablero.")


def buscar(tablero: tuple[int, ...], algoritmo: str) -> ResultadoBusqueda:
    inicio = perf_counter()
    camino, nodos, _ = ALGORITMOS[algoritmo](EstadoPuzzle(tablero))
    segundos = perf_counter() - inicio
    if camino is None:
        raise ValueError(f"{algoritmo} no encontró una solución.")
    actual = tablero
    costo = 0
    for accion in camino:
        for sucesor in EstadoPuzzle(actual).generar_sucesores():
            if sucesor.accion == accion:
                costo += sucesor.costo_acumulado
                actual = sucesor.tablero
                break
        else:
            raise ValueError(f"{algoritmo} devolvió un movimiento ilegal: {accion}.")
    if not EstadoPuzzle(actual).es_meta():
        raise ValueError(f"La ruta de {algoritmo} no llega a la meta.")
    return ResultadoBusqueda(algoritmo, camino, nodos, segundos, costo, tablero, actual)


Respuesta = list[ResultadoBusqueda] | tuple[int, int, int]


class Aplicacion:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana
        ventana.title("Proyecto IA · Búsquedas y juego adversario")
        ventana.geometry("1020x780")
        ventana.minsize(960, 740)
        estilo = ttk.Style(ventana)
        estilo.theme_use("clam")
        estilo.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        estilo.configure("TButton", padding=8)

        self.ocupada = False
        self.respuestas: Queue[Respuesta | Exception] = Queue()
        self.operacion = ""
        self.controles: list[ttk.Button | ttk.Entry] = []
        self.resultado: ResultadoBusqueda | None = None
        self.tablero_puzzle = EJEMPLOS["3 movimientos"]
        self.paso = 0
        self.animacion: str | None = None
        self.tablero_juego = [" "] * 9
        self.ultimo_humano = -1
        self.estado_general = tk.StringVar(value="Listo para comenzar.")

        ttk.Label(ventana, text="Laboratorio de búsqueda", style="Title.TLabel").pack(
            anchor="w", padx=24, pady=(18, 4)
        )
        pestañas = ttk.Notebook(ventana)
        pestañas.pack(fill="both", expand=True, padx=20)
        puzzle = ttk.Frame(pestañas, padding=16)
        juego = ttk.Frame(pestañas, padding=16)
        pestañas.add(puzzle, text="  8-Puzzle y comparación  ")
        pestañas.add(juego, text="  Tres en línea  ")
        self.crear_puzzle(puzzle)
        self.crear_juego(juego)
        ttk.Label(ventana, textvariable=self.estado_general).pack(
            anchor="w", padx=24, pady=12
        )
        self.sondeo = ventana.after(50, self.recibir_respuesta)
        ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

    def boton(self, padre, texto, comando):
        boton = ttk.Button(padre, text=texto, command=comando)
        self.controles.append(boton)
        return boton

    def crear_puzzle(self, marco):
        superior = ttk.Frame(marco)
        superior.pack(fill="x")
        entrada = ttk.LabelFrame(superior, text="Tablero inicial · 0 = vacío", padding=10)
        entrada.pack(side="left", padx=(0, 20))
        self.entradas: list[ttk.Entry] = []
        for indice, numero in enumerate(self.tablero_puzzle):
            casilla = ttk.Entry(entrada, width=4, justify="center", font=("Segoe UI", 18))
            casilla.insert(0, str(numero))
            casilla.grid(row=indice // 3, column=indice % 3, padx=3, pady=3)
            self.entradas.append(casilla)
            self.controles.append(casilla)
        opciones = ttk.Frame(superior)
        opciones.pack(side="left", fill="both", expand=True)
        ttk.Label(opciones, text="Ejemplos para la presentación").pack(anchor="w")
        fila = ttk.Frame(opciones)
        fila.pack(anchor="w", pady=4)
        for nombre in EJEMPLOS:
            self.boton(
                fila, nombre, lambda nombre=nombre: self.cargar_ejemplo(nombre)
            ).pack(side="left", padx=(0, 5))
        ttk.Label(opciones, text="Algoritmo").pack(anchor="w", pady=(6, 0))
        self.algoritmo = ttk.Combobox(
            opciones, values=list(ALGORITMOS), state="readonly", width=12
        )
        self.algoritmo.set("BFS")
        self.algoritmo.pack(anchor="w", pady=4)
        acciones = ttk.Frame(opciones)
        acciones.pack(anchor="w")
        self.boton(acciones, "Resolver", self.resolver).pack(side="left", padx=(0, 5))
        self.boton(acciones, "Comparar los cuatro", self.comparar).pack(side="left")

        visual = ttk.Frame(marco)
        visual.pack(fill="x", pady=12)
        tablero = ttk.Frame(visual)
        tablero.pack(side="left", padx=(0, 20))
        self.casillas_puzzle: list[tk.Label] = []
        for indice in range(9):
            casilla = tk.Label(
                tablero, width=4, height=1, font=("Segoe UI", 24, "bold"),
                relief="flat", padx=8, pady=5,
            )
            casilla.grid(row=indice // 3, column=indice % 3, padx=3, pady=3)
            self.casillas_puzzle.append(casilla)
        detalle = ttk.Frame(visual)
        detalle.pack(side="left", fill="both", expand=True)
        self.detalle_puzzle = tk.StringVar(value="Ingresa un tablero y pulsa Resolver.")
        ttk.Label(
            detalle, textvariable=self.detalle_puzzle, wraplength=560
        ).pack(anchor="w", pady=8)
        reproduccion = ttk.Frame(detalle)
        reproduccion.pack(anchor="w")
        ttk.Button(reproduccion, text="Paso", command=self.avanzar).pack(side="left")
        ttk.Button(reproduccion, text="Reproducir", command=self.reproducir).pack(side="left")
        ttk.Button(reproduccion, text="Pausar", command=self.pausar).pack(side="left")
        ttk.Button(reproduccion, text="Ver meta", command=self.ver_meta).pack(side="left")
        ttk.Label(
            detalle,
            text="Animación: Muestra los movimientos seleccionados por el alforitmo.",
            wraplength=560,
        ).pack(anchor="w", pady=8)
        self.dibujar_puzzle()

        ttk.Label(
            marco,
            text="Resultados · mismo tablero, costo ponderado: ↑1 · ↓2 · ←3 · →4",
        ).pack(anchor="w")
        columnas = ("algoritmo", "nodos", "tiempo", "pasos", "costo")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=4)
        for columna, titulo in zip(
            columnas, ("Algoritmo", "Nodos expandidos", "Tiempo (s)", "Movimientos", "Costo")
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=130, anchor="center")
        self.tabla.pack(fill="x", pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_resultado)
        self.resultados: dict[str, ResultadoBusqueda] = {}
        ttk.Label(
            marco,
            text="Selecciona una fila para ver su solución y pulsa Reproducir. "
            "DFS puede producir rutas muy largas; Ver meta evita animar todos los pasos.",
            wraplength=880,
        ).pack(anchor="w", pady=4)

    def cargar_ejemplo(self, nombre):
        if self.ocupada:
            return
        self.pausar()
        self.resultado = None
        self.resultados.clear()
        self.tabla.delete(*self.tabla.get_children())
        self.tablero_puzzle = EJEMPLOS[nombre]
        for entrada, numero in zip(self.entradas, self.tablero_puzzle):
            entrada.delete(0, "end")
            entrada.insert(0, str(numero))
        self.dibujar_puzzle()
        self.detalle_puzzle.set("Ejemplo cargado. Pulsa Resolver o Comparar.")

    def leer_tablero(self):
        try:
            return validar_tablero([entrada.get() for entrada in self.entradas])
        except ValueError as error:
            messagebox.showerror("Tablero inválido", str(error), parent=self.ventana)
            return None

    def preparar_busqueda(self, comparar):
        if self.ocupada:
            return
        tablero = self.leer_tablero()
        if tablero is None:
            return
        self.pausar()
        self.resultado = None
        self.resultados.clear()
        self.tabla.delete(*self.tabla.get_children())
        self.tablero_puzzle = tablero
        self.paso = 0
        self.dibujar_puzzle()
        self.detalle_puzzle.set("Calculando; la ventana permanece disponible.")
        nombres = list(ALGORITMOS) if comparar else [self.algoritmo.get()]
        self.iniciar_trabajo(
            "puzzle", lambda: [buscar(tablero, nombre) for nombre in nombres]
        )

    def resolver(self):
        self.preparar_busqueda(False)

    def comparar(self):
        self.preparar_busqueda(True)

    def iniciar_trabajo(self, operacion: str, trabajo: Callable[[], Respuesta]):
        self.ocupada = True
        self.operacion = operacion
        for control in self.controles:
            control.configure(state="disabled")
        self.algoritmo.configure(state="disabled")
        self.actualizar_juego()
        self.estado_general.set("Calculando... Puedes mover la ventana o cambiar de pestaña.")

        # Solo el hilo principal toca widgets; el trabajador devuelve datos por la cola.
        def ejecutar():
            try:
                self.respuestas.put(trabajo())
            except Exception as error:
                logging.exception("Error durante la búsqueda gráfica")
                self.respuestas.put(error)

        Thread(target=ejecutar, daemon=True).start()

    def recibir_respuesta(self):
        try:
            respuesta = self.respuestas.get_nowait()
        except Empty:
            self.sondeo = self.ventana.after(50, self.recibir_respuesta)
            return
        self.ocupada = False
        for control in self.controles:
            control.configure(state="normal")
        self.algoritmo.configure(state="readonly")
        if isinstance(respuesta, Exception):
            self.estado_general.set("La operación falló. Revisa el mensaje de error.")
            if self.operacion == "juego":
                self.tablero_juego[self.ultimo_humano] = " "
            else:
                self.detalle_puzzle.set("No se pudo completar la búsqueda.")
            messagebox.showerror("Error de búsqueda", str(respuesta), parent=self.ventana)
        elif isinstance(respuesta, list):
            for resultado in respuesta:
                self.resultados[resultado.algoritmo] = resultado
                self.tabla.insert(
                    "", "end", iid=resultado.algoritmo,
                    values=(resultado.algoritmo, resultado.nodos,
                            f"{resultado.segundos:.6f}", len(resultado.camino), resultado.costo),
                )
            self.estado_general.set("Búsqueda terminada. Selecciona una fila para animar.")
            if respuesta:
                self.tabla.selection_set(respuesta[0].algoritmo)
        else:
            movimiento, sin_poda, con_poda = respuesta
            self.tablero_juego[movimiento] = "X"
            reduccion = (1 - con_poda / sin_poda) * 100 if sin_poda else 0
            self.metricas_juego.set(
                f"Nodos sin poda: {sin_poda:,}\nNodos alfa-beta: {con_poda:,}\n"
                f"Reducción de nodos: {reduccion:.2f}%"
            )
            self.estado_general.set("La IA jugó. Tu turno.")
        self.actualizar_juego()
        self.sondeo = self.ventana.after(50, self.recibir_respuesta)

    def seleccionar_resultado(self, _evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.pausar()
        self.resultado = self.resultados[seleccion[0]]
        self.tablero_puzzle = self.resultado.tablero_inicial
        self.paso = 0
        self.dibujar_puzzle()
        longitud = len(self.resultado.camino)
        self.detalle_puzzle.set(
            f"{self.resultado.algoritmo}: {longitud} movimientos, costo {self.resultado.costo}.\n"
            "Tablero inicial. Usa Paso o Reproducir."
        )
        if longitud == 0:
            self.detalle_puzzle.set("El tablero inicial ya es la meta (0 movimientos).")
        elif longitud > 100:
            self.detalle_puzzle.set(
                f"Ruta larga: {longitud:,} movimientos, costo {self.resultado.costo:,}. "
                "Animación manual disponible; Ver meta permite ir directamente al resultado."
            )

    def dibujar_puzzle(self):
        for casilla, numero in zip(self.casillas_puzzle, self.tablero_puzzle):
            casilla.configure(
                text=str(numero) if numero else "",
                bg="#2563eb" if numero else "#e2e8f0", fg="white",
            )

    def avanzar(self):
        if self.ocupada or self.resultado is None:
            return
        if self.paso >= len(self.resultado.camino):
            return
        accion = self.resultado.camino[self.paso]
        indice_vacio = self.tablero_puzzle.index(0)
        self.tablero_puzzle = aplicar_movimiento(self.tablero_puzzle, accion)
        ficha = self.tablero_puzzle[indice_vacio]
        self.paso += 1
        self.dibujar_puzzle()
        texto = (
            f"Paso {self.paso}/{len(self.resultado.camino)}: el vacío se mueve "
            f"{accion.lower()}; la ficha {ficha} se desliza {OPUESTAS[accion]}."
        )
        if self.paso == len(self.resultado.camino):
            texto += "\n¡Solucionado!"
        self.detalle_puzzle.set(texto)

    def reproducir(self):
        self.pausar()
        if self.ocupada or self.resultado is None:
            return
        self.avanzar()
        if self.paso < len(self.resultado.camino):
            self.animacion = self.ventana.after(400, self.reproducir)

    def pausar(self):
        if self.animacion is not None:
            self.ventana.after_cancel(self.animacion)
            self.animacion = None

    def ver_meta(self):
        if self.ocupada or self.resultado is None:
            return
        self.pausar()
        self.tablero_puzzle = self.resultado.tablero_final
        self.paso = len(self.resultado.camino)
        self.dibujar_puzzle()
        self.detalle_puzzle.set(
            f"Meta alcanzada · {self.paso:,} movimientos · costo {self.resultado.costo:,}."
        )

    def crear_juego(self, marco):
        ttk.Label(marco, text="Tú juegas con O; la IA juega con X.").pack(anchor="w")
        ttk.Label(
            marco, text="Haz clic en una casilla libre. La persona comienza."
        ).pack(anchor="w", pady=8)
        espacio_juego = ttk.Frame(marco)
        espacio_juego.pack(pady=12)
        lateral = ttk.Frame(espacio_juego, width=260)
        lateral.pack(side="left", fill="y", padx=(0, 20))
        lateral.pack_propagate(False)
        self.boton(lateral, "Nueva partida", self.nueva_partida).pack(
            anchor="w", pady=8
        )
        tablero = ttk.Frame(espacio_juego)
        tablero.pack(side="left")
        self.casillas_juego: list[tk.Button] = []
        for indice in range(9):
            boton = tk.Button(
                tablero, width=4, height=2, font=("Segoe UI", 32, "bold"),
                bg="#e2e8f0", disabledforeground="#1e293b",
                command=lambda indice=indice: self.jugar(indice),
            )
            boton.grid(row=indice // 3, column=indice % 3, padx=4, pady=4)
            self.casillas_juego.append(boton)
        self.detalle_juego = tk.StringVar(value="Tu turno.")
        self.metricas_juego = tk.StringVar(value="Las métricas aparecerán después del turno de la IA.")
        ttk.Label(
            lateral, textvariable=self.detalle_juego, wraplength=250
        ).pack(anchor="w", pady=8)
        ttk.Label(
            lateral, textvariable=self.metricas_juego, justify="left", wraplength=250
        ).pack(anchor="w", pady=8)

    def jugar(self, indice):
        if self.ocupada or es_terminal(self.tablero_juego) or self.tablero_juego[indice] != " ":
            return
        self.pausar()
        self.tablero_juego[indice] = "O"
        self.ultimo_humano = indice
        self.actualizar_juego()
        if es_terminal(self.tablero_juego):
            return
        tablero = self.tablero_juego.copy()
        self.iniciar_trabajo("juego", lambda: mejor_movimiento_ia(tablero))

    def actualizar_juego(self):
        terminal = es_terminal(self.tablero_juego)
        for boton, simbolo in zip(self.casillas_juego, self.tablero_juego):
            boton.configure(
                text=simbolo,
                state="disabled" if self.ocupada or terminal or simbolo != " " else "normal",
            )
        if verificar_ganador(self.tablero_juego, "X"):
            self.detalle_juego.set("La IA gana. Pulsa Nueva partida para volver a jugar.")
        elif verificar_ganador(self.tablero_juego, "O"):
            self.detalle_juego.set("¡Ganaste! Pulsa Nueva partida para volver a jugar.")
        elif terminal:
            self.detalle_juego.set("¡Empate! Pulsa Nueva partida para volver a jugar.")
        else:
            self.detalle_juego.set("Calculando..." if self.ocupada else "Tu turno.")

    def nueva_partida(self):
        if self.ocupada:
            return
        self.tablero_juego = [" "] * 9
        self.metricas_juego.set("Las métricas aparecerán después del turno de la IA.")
        self.actualizar_juego()

    def cerrar(self):
        self.pausar()
        self.ventana.after_cancel(self.sondeo)
        self.ventana.destroy()


if __name__ == "__main__":
    Aplicacion(tk.Tk()).ventana.mainloop()
