"""Dominio del módulo domain."""

import time
import random
from .pieza import Pieza
from ..views.pieza_animada import PiezaAnimada
from .tablero_logico import obtener_pieza_en


class Partida:
    """Gestiona el estado lógico de una sesión de ajedrez."""

    def __init__(self, minutos=10, bando_elegido="blanco", contra_ia=True):
        self.piezas = []  # Lista de objetos Pieza (lógicos)
        self.turno = "blanco"
        self.historial = []
        self.en_passant_target = None  # Almacena (f, c) de la captura al paso
        self.capturas_blancas = []  # Piezas negras capturadas por blancas
        self.capturas_negras = []  # Piezas blancas capturadas por negras
        self.pila_estados = []  # Para funcionalidad de deshacer

        self.resultado = None

        # Relojes
        self.tiempo_blanco = minutos * 60
        self.tiempo_negro = minutos * 60
        self.reloj_iniciado = False
        self.ultima_actualizacion = time.time()

        # Lógica de bando
        if bando_elegido == "aleatorio":
            color_usuario = random.choice(["blanco", "negro"])
        else:
            color_usuario = bando_elegido

        self.color_usuario = color_usuario
        self.color_ia = (
            ("negro" if color_usuario == "blanco" else "blanco") if contra_ia else None
        )

        self._colocar_piezas_iniciales()

    def _colocar_piezas_iniciales(self):
        """Configura la posición inicial estándar de las piezas."""
        self.piezas = []

        # Piezas Negras (Filas 0 y 1)
        for c in range(8):
            self.piezas.append(PiezaAnimada("peon", "negro", 1, c))

        orden_piezas = [
            "torre",
            "caballo",
            "alfil",
            "dama",
            "rey",
            "alfil",
            "caballo",
            "torre",
        ]
        for c, tipo in enumerate(orden_piezas):
            self.piezas.append(PiezaAnimada(tipo, "negro", 0, c))

        # Piezas Blancas (Filas 6 y 7)
        for c in range(8):
            self.piezas.append(PiezaAnimada("peon", "blanco", 6, c))

        for c, tipo in enumerate(orden_piezas):
            self.piezas.append(PiezaAnimada(tipo, "blanco", 7, c))

    def guardar_estado(self):
        """Guarda una copia del estado actual para permitir deshacer."""
        estado = {
            "piezas": [
                (p.tipo, p.color, p.fila, p.col, p.ha_movido) for p in self.piezas
            ],
            "turno": self.turno,
            "historial": list(self.historial),
            "capturas_blancas": list(self.capturas_blancas),
            "capturas_negras": list(self.capturas_negras),
            "en_passant": self.en_passant_target,
        }
        self.pila_estados.append(estado)

    def deshacer_movimiento(self):
        if not self.pila_estados:
            return
        estado = self.pila_estados.pop()
        self.turno = estado["turno"]
        self.historial = estado["historial"]
        self.capturas_blancas = estado["capturas_blancas"]
        self.capturas_negras = estado["capturas_negras"]
        self.en_passant_target = estado["en_passant"]
        self.piezas = [
            PiezaAnimada(t, c, f, col) for t, c, f, col, h in estado["piezas"]
        ]
        for i, p in enumerate(self.piezas):
            p.ha_movido = estado["piezas"][i][4]

    def actualizar_relojes(self):
        if not self.reloj_iniciado or self.resultado:
            return

        ahora = time.time()
        delta = ahora - self.ultima_actualizacion
        self.ultima_actualizacion = ahora

        if self.turno == "blanco":
            self.tiempo_blanco = max(0, self.tiempo_blanco - delta)
            if self.tiempo_blanco <= 0:
                self.resultado = "Ganan Negras por Tiempo"
        else:
            self.tiempo_negro = max(0, self.tiempo_negro - delta)
            if self.tiempo_negro <= 0:
                self.resultado = "Ganan Blancas por Tiempo"

    def obtener_fen(self):
        """Convierte el estado actual a formato FEN optimizado."""
        fen_rows = []
        tablero_matriz = [[None for _ in range(8)] for _ in range(8)]
        for p in self.piezas:
            tablero_matriz[p.fila][p.col] = p

        for fila in range(8):
            vacios = 0
            fen_row = ""
            for col in range(8):
                pieza = tablero_matriz[fila][col]
                if pieza is None:
                    vacios += 1
                else:
                    if vacios > 0:
                        fen_row += str(vacios)
                        vacios = 0
                    letras = {
                        "peon": "p",
                        "caballo": "n",
                        "alfil": "b",
                        "torre": "r",
                        "dama": "q",
                        "rey": "k",
                    }
                    letra = letras.get(pieza.tipo, "p")
                    if pieza.color == "blanco":
                        letra = letra.upper()
                    fen_row += letra
            if vacios > 0:
                fen_row += str(vacios)
            fen_rows.append(fen_row)

        turno_fen = "w" if self.turno == "blanco" else "b"
        return "/".join(fen_rows) + f" {turno_fen} KQkq - 0 1"

    def registrar_movimiento(self, p, f_dest, c_dest, uci_ia="", promocion="dama"):
        self.guardar_estado()
        f_ori, c_ori = p.fila, p.col
        coord_dest = f"{chr(97 + c_dest)}{8 - f_dest}"
        # 1. Manejo de capturas simplificado
        pieza_capturada = obtener_pieza_en(self.piezas, f_dest, c_dest)
        char_cap = ""
        if (
            p.tipo == "peon"
            and (f_dest, c_dest) == self.en_passant_target
            and c_ori != c_dest
        ):
            pieza_capturada = obtener_pieza_en(self.piezas, f_ori, c_dest)
            char_cap = "x"
        elif pieza_capturada:
            char_cap = "x"

        # Definir texto del movimiento antes de mover la pieza
        if p.tipo == "peon":
            mov_txt = (
                f"{chr(97+c_ori)}x{coord_dest}"
                if char_cap
                else f"{chr(97+c_dest)}{8-f_dest}"
            )
        elif p.tipo == "rey" and abs(c_dest - c_ori) == 2:
            mov_txt = "O-O" if c_dest > c_ori else "O-O-O"
        else:
            # Estilo Chess: Solo la casilla de llegada (el icono se pone en la vista)
            mov_txt = f"{char_cap}{coord_dest}"

        if pieza_capturada:
            # Guardar para el panel visual
            if hasattr(pieza_capturada, "tipo"):
                if pieza_capturada.color == "blanco":
                    self.capturas_negras.append(pieza_capturada.tipo)
                else:
                    self.capturas_blancas.append(pieza_capturada.tipo)
            self.piezas.remove(pieza_capturada)

        # 2. Manejo de Enroque (Mover la torre automáticamente)
        if p.tipo == "rey" and abs(c_dest - c_ori) == 2:
            c_t_ori = 7 if c_dest > c_ori else 0
            c_t_dest = 5 if c_dest > c_ori else 3
            torre = obtener_pieza_en(self.piezas, f_ori, c_t_ori)
            if torre:
                torre.fila, torre.col = f_ori, c_t_dest
                torre.ha_movido = True

        # 3. Peón al Paso
        self.en_passant_target = None
        if p.tipo == "peon" and abs(f_dest - f_ori) == 2:
            self.en_passant_target = ((f_ori + f_dest) // 2, c_ori)

        # 4. Promoción de Peón
        if p.tipo == "peon" and (f_dest == 0 or f_dest == 7):
            p.tipo = promocion
            # Actualizar imagen visual inmediatamente
            if hasattr(p, "_cargar_imagen"):
                p.imagen = p._cargar_imagen()
            p.ha_movido = True  # Promoted piece has moved

        # 5. Ejecutar movimiento físico/lógico
        p.fila, p.col = f_dest, c_dest
        p.ha_movido = True

        self.ultimo_movimiento = (f_ori, c_ori, f_dest, c_dest)
        self.historial.append({"tipo": p.tipo, "color": p.color, "txt": mov_txt})
        self.reloj_iniciado = True
        # El cambio de turno debe ser lo último para sincronizar con el bucle de Pygame
        self.turno = "negro" if self.turno == "blanco" else "blanco"