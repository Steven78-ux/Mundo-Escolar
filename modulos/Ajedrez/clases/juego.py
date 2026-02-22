import pygame
import copy
import os
import time
import threading
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEWHEEL,
    KEYDOWN,
    K_1,
    K_2,
    K_3,
    K_4,
)
from .TableroInteractivo import TableroInteractivo
from .PiezaAnimada import PiezaAnimada
from .Flecha import Flecha
from .ia import BotAjedrez


# --- CONSTANTES DE COLORES PARA FLECHES ---
COLORES_FLECHAS = {
    "1": (0, 255, 0, 160),  # Verde
    "2": (255, 0, 0, 160),  # Rojo
    "3": (0, 0, 255, 160),  # Azul
    "4": (255, 165, 0, 160),  # Naranja
}


class Juego:
    def __init__(self, minutos=10):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.tablero = TableroInteractivo()
        self.ancho_total = self.tablero.ancho_total
        self.alto_total = self.tablero.alto_total
        self.pantalla = pygame.display.set_mode((self.ancho_total, self.alto_total))
        self.partida_activa = True
        self.reloj_fps = pygame.time.Clock()
        self.piezas = []
        self.flechas = []
        self.circulos = []
        self.seleccionada = None
        self.movs_legales = []
        self.turno = "blanco"
        self.ultimo_movimiento = None
        self.resultado = None
        self.tiempo_inicial = 5
        self.tiempo_blanco = minutos * 60
        self.tiempo_negro = minutos * 60
        self.reloj_iniciado = False
        self.ultima_actualizacion_tiempo = pygame.time.get_ticks()

        # --- INTEGRACIÓN DE IA ---
        # 1. Definimos la ruta (usa la 'r' al principio para evitar errores de Windows)
        ruta_stockfish = r"C:\Users\Kirito\Downloads\stockfish\stockfish-windows-x86-64"
        # 2. Se la pasamos al Bot (quitamos el argumento 'color')
        self.bot = BotAjedrez(
            ruta_stockfish, color="negro"
        )  # Ahora sí le pasamos el color
        self.espera_bot = 0
        self.bot_pensando = False

        # --- SISTEMA DE HISTORIAL Y SCROLL ---
        self.historial = []
        self.scroll_historial = 0
        self.max_lineas_visibles = 18
        self.capturadas_blancas = []
        self.capturadas_negras = []
        self.historial_estados = []
        self.dibujando_flecha = False
        self.inicio_flecha = None
        self.color_flecha_actual = COLORES_FLECHAS["1"]

        self.ruta_sonidos = os.path.join(
            os.path.dirname(__file__), "..", "assets", "sonidos"
        )
        try:
            self.sonido_mover = pygame.mixer.Sound(
                os.path.join(self.ruta_sonidos, "Movimiento.wav")
            )
            self.sonido_captura = pygame.mixer.Sound(
                os.path.join(self.ruta_sonidos, "Captura.wav")
            )
            self.sonido_jaque = pygame.mixer.Sound(
                os.path.join(self.ruta_sonidos, "Jaque.wav")
            )
            self.sonido_fin = pygame.mixer.Sound(
                os.path.join(self.ruta_sonidos, "FinJuego.wav")
            )
        except:
            self.sonido_mover = self.sonido_captura = self.sonido_jaque = (
                self.sonido_fin
            ) = None

        self.crear_piezas_iniciales()
        self.guardar_estado()
        pygame.display.set_caption(f"Ajedrez - Turno: {self.turno.upper()}")

    def actualizar_scroll_automatico(self):
        """Mueve el foco del historial hacia el final si hay nuevos movimientos."""
        if len(self.historial) > self.max_lineas_visibles:
            self.scroll_historial = len(self.historial) - self.max_lineas_visibles
        else:
            self.scroll_historial = 0

    def obtener_notacion_corta(self, f_orig, c_orig, f_dest, c_dest, pieza, es_captura):
        """Convierte a notación corta en español: Inicial + destino (ej: Ce4, Dxf7)"""
        letras = "abcdefgh"
        iniciales = {
            "rey": "R",
            "dama": "D",
            "torre": "T",
            "alfil": "A",
            "caballo": "C",
            "peon": "",
        }
        prefijo = iniciales.get(pieza.nombre, "")
        if pieza.nombre == "peon" and es_captura:
            prefijo = letras[c_orig]
        conector = "x" if es_captura else ""
        destino = f"{letras[c_dest]}{8-f_dest}"
        if pieza.nombre == "rey" and abs(c_dest - c_orig) == 2:
            return "O-O" if c_dest > c_orig else "O-O-O"
        return f"{prefijo}{conector}{destino}"

    def guardar_estado(self):
        estado = {
            "piezas": copy.deepcopy(self.piezas),
            "turno": self.turno,
            "ultimo_movimiento": self.ultimo_movimiento,
            "historial_txt": list(self.historial),
            "cap_b": list(self.capturadas_blancas),
            "cap_n": list(self.capturadas_negras),
            "t_blanco": self.tiempo_blanco,
            "t_negro": self.tiempo_negro,
            "reloj_iniciado": self.reloj_iniciado,
            "resultado": self.resultado,
        }
        self.historial_estados.append(estado)

    def deshacer_movimiento(self):
        if len(self.historial_estados) > 1:
            self.historial_estados.pop()
            previo = self.historial_estados[-1]
            self.piezas = copy.deepcopy(previo["piezas"])
            self.turno = previo["turno"]
            self.ultimo_movimiento = previo["ultimo_movimiento"]
            self.historial = list(previo["historial_txt"])
            self.capturadas_blancas = list(previo["cap_b"])
            self.capturadas_negras = list(previo["cap_n"])
            self.tiempo_blanco = previo["t_blanco"]
            self.tiempo_negro = previo["t_negro"]
            self.reloj_iniciado = previo.get("reloj_iniciado", False)
            self.resultado = previo.get("resultado", None)
            for p in self.piezas:
                p.x, p.y = (
                    p.col * self.tablero.tam_cuadro,
                    p.fila * self.tablero.tam_cuadro,
                )
            self.seleccionada = None
            self.movs_legales = []
            self.flechas = []
            self.actualizar_scroll_automatico()
            pygame.display.set_caption(f"Ajedrez - Turno: {self.turno.upper()}")

    def crear_piezas_iniciales(self):
        tam = self.tablero.tam_cuadro
        orden = [
            "torre",
            "caballo",
            "alfil",
            "dama",
            "rey",
            "alfil",
            "caballo",
            "torre",
        ]
        for col, nombre in enumerate(orden):
            self.piezas.append(PiezaAnimada(nombre, "negro", 0, col, tam))
            self.piezas.append(PiezaAnimada("peon", "negro", 1, col, tam))
            self.piezas.append(PiezaAnimada("peon", "blanco", 6, col, tam))
            self.piezas.append(PiezaAnimada(nombre, "blanco", 7, col, tam))

    def reproducir_sonido(self, tipo):
        sonidos = {
            "Movimiento": self.sonido_mover,
            "Captura": self.sonido_captura,
            "Jaque": self.sonido_jaque,
            "Fin": self.sonido_fin,
        }
        if tipo in sonidos and sonidos[tipo]:
            sonidos[tipo].play()

    def obtener_rey(self, color):
        return next(
            (p for p in self.piezas if p.nombre == "rey" and p.color == color), None
        )

    def esta_atacada(self, fila, col, color_defensor):
        color_enemigo = "negro" if color_defensor == "blanco" else "blanco"
        for p in self.piezas:
            if p.color != color_enemigo:
                continue
            df, dc = fila - p.fila, col - p.col
            if p.nombre == "peon":
                dir_p = 1 if p.color == "negro" else -1
                if df == dir_p and abs(dc) == 1:
                    return True
            elif p.nombre == "caballo":
                if abs(df) * abs(dc) == 2:
                    return True
            elif p.nombre == "rey":
                if abs(df) <= 1 and abs(dc) <= 1:
                    return True
            elif p.nombre in ["dama", "torre", "alfil"]:
                if (
                    (p.nombre == "torre" and (df != 0 and dc != 0))
                    or (p.nombre == "alfil" and abs(df) != abs(dc))
                    or (
                        p.nombre == "dama"
                        and (df != 0 and dc != 0 and abs(df) != abs(dc))
                    )
                ):
                    continue
                step_f, step_c = (0 if df == 0 else (1 if df > 0 else -1)), (
                    0 if dc == 0 else (1 if dc > 0 else -1)
                )
                f_act, c_act, obstruido = p.fila + step_f, p.col + step_c, False
                while f_act != fila or c_act != col:
                    if any(
                        x for x in self.piezas if x.fila == f_act and x.col == c_act
                    ):
                        obstruido = True
                        break
                    f_act, c_act = f_act + step_f, c_act + step_c
                if not obstruido:
                    return True
        return False

    def deja_al_rey_en_jaque(self, pieza, n_fila, n_col):
        f_orig, c_orig = pieza.fila, pieza.col
        p_cap = next(
            (
                p
                for p in self.piezas
                if p.fila == n_fila and p.col == n_col and p != pieza
            ),
            None,
        )
        if p_cap:
            self.piezas.remove(p_cap)
        pieza.fila, pieza.col = n_fila, n_col
        rey = self.obtener_rey(pieza.color)
        en_jaque = self.esta_atacada(rey.fila, rey.col, pieza.color) if rey else False
        pieza.fila, pieza.col = f_orig, c_orig
        if p_cap:
            self.piezas.append(p_cap)
        return en_jaque

    def tiene_movimientos_legales(self, color):
        for p in self.piezas:
            if p.color == color:
                # Probamos cada casilla del tablero
                for f in range(8):
                    for c in range(8):
                        # 1. ¿Es un movimiento físicamente posible para la pieza?
                        if self.es_movimiento_valido(p, f, c):
                            # 2. Si lo hace, ¿el rey sigue bajo ataque?
                            # Esta es la parte crítica que salva al rey
                            if not self.deja_al_rey_en_jaque(p, f, c):
                                return True  # ¡Encontró una salida!
        return False

    def verificar_material_insuficiente(self):
        """Retorna True si el material restante no puede dar mate."""
        piezas_vivas = self.piezas
        cant = len(piezas_vivas)

        # 1. Rey vs Rey (Solo 2 piezas)
        if cant == 2:
            return True

        # 2. Rey y Pieza Menor vs Rey (Solo 3 piezas)
        if cant == 3:
            pieza_menor = next((p for p in piezas_vivas if p.nombre != "rey"), None)
            if pieza_menor and pieza_menor.nombre in ["caballo", "alfil"]:
                return True

        # 3. Rey y Alfil vs Rey y Alfil (Solo 4 piezas)
        if cant == 4:
            blancas = [p for p in piezas_vivas if p.color == "blanco"]
            negras = [p for p in piezas_vivas if p.color == "negro"]

            if len(blancas) == 2 and len(negras) == 2:
                a_blanco = next((p for p in blancas if p.nombre == "alfil"), None)
                a_negro = next((p for p in negras if p.nombre == "alfil"), None)

                if a_blanco and a_negro:
                    # Si los alfiles están en el mismo color de cuadro
                    color_b = (a_blanco.fila + a_blanco.col) % 2
                    color_n = (a_negro.fila + a_negro.col) % 2
                    if color_b == color_n:
                        return True

        return False

    def es_movimiento_valido(self, pieza, n_fila, n_col, chequear_enroque=True):
        if not (0 <= n_fila <= 7 and 0 <= n_col <= 7):
            return False
        df, dc = n_fila - pieza.fila, n_col - pieza.col
        p_dest = next(
            (p for p in self.piezas if p.fila == n_fila and p.col == n_col), None
        )
        if p_dest and (p_dest.nombre == "rey" or p_dest.color == pieza.color):
            return False
        if pieza.nombre == "peon":
            dir = -1 if pieza.color == "blanco" else 1
            if dc == 0 and df == dir and not p_dest:
                return True
            if not pieza.ha_movido and dc == 0 and df == 2 * dir:
                if (
                    not any(
                        p.fila == pieza.fila + dir and p.col == n_col
                        for p in self.piezas
                    )
                    and not p_dest
                ):
                    return True
            if abs(dc) == 1 and df == dir:
                if p_dest and p_dest.color != pieza.color:
                    return True
                if self.ultimo_movimiento:
                    uo, co, ud, cd = self.ultimo_movimiento
                    if abs(uo - ud) == 2 and ud == pieza.fila and cd == n_col:
                        return True
            return False
        elif pieza.nombre == "caballo":
            return abs(df) * abs(dc) == 2
        elif pieza.nombre == "rey":
            if abs(df) <= 1 and abs(dc) <= 1:
                return True
            if chequear_enroque and not pieza.ha_movido and df == 0 and abs(dc) == 2:
                if self.esta_atacada(pieza.fila, pieza.col, pieza.color):
                    return False
                ct = 7 if dc > 0 else 0
                torre = next(
                    (
                        p
                        for p in self.piezas
                        if p.fila == pieza.fila and p.col == ct and p.nombre == "torre"
                    ),
                    None,
                )
                if torre and not torre.ha_movido:
                    if all(
                        not any(
                            p.fila == pieza.fila and p.col == c for p in self.piezas
                        )
                        for c in range(min(pieza.col, ct) + 1, max(pieza.col, ct))
                    ):
                        paso = 1 if dc > 0 else -1
                        if not self.esta_atacada(
                            pieza.fila, pieza.col + paso, pieza.color
                        ) and not self.esta_atacada(pieza.fila, n_col, pieza.color):
                            return True
            return False
        elif pieza.nombre in ["torre", "alfil", "dama"]:
            if (
                (pieza.nombre == "torre" and df != 0 and dc != 0)
                or (pieza.nombre == "alfil" and abs(df) != abs(dc))
                or (
                    pieza.nombre == "dama"
                    and df != 0
                    and dc != 0
                    and abs(df) != abs(dc)
                )
            ):
                return False
            pf, pc = (0 if df == 0 else (1 if df > 0 else -1)), (
                0 if dc == 0 else (1 if dc > 0 else -1)
            )
            f_act, c_act = pieza.fila + pf, pieza.col + pc
            while f_act != n_fila or c_act != n_col:
                if any(p.fila == f_act and p.col == c_act for p in self.piezas):
                    return False
                f_act, c_act = f_act + pf, c_act + pc
            return True
        return False

    def actualizar_relojes(self):
        ahora = pygame.time.get_ticks()
        delta = (ahora - self.ultima_actualizacion_tiempo) / 1000.0
        self.ultima_actualizacion_tiempo = ahora
        if self.reloj_iniciado and self.partida_activa and not self.resultado:
            if self.turno == "blanco":
                self.tiempo_blanco = max(0, self.tiempo_blanco - delta)
                if self.tiempo_blanco <= 0:
                    self.resultado = "Ganan Negras por Tiempo"
                    self.reproducir_sonido("Fin")
            else:
                self.tiempo_negro = max(0, self.tiempo_negro - delta)
                if self.tiempo_negro <= 0:
                    self.resultado = "Ganan Blancas por Tiempo"
                    self.reproducir_sonido("Fin")

    def esperar_promocion(self, pieza):
        """Maneja la lógica de selección de pieza con imágenes del color correcto."""
        # Si es el bot el que promociona, siempre elige dama por defecto (puedes cambiarlo)
        if self.turno == self.bot.color:
            pieza.nombre = "dama"
            pieza.cargar_imagen()
            return

        imagenes_menu = {}
        nombres = ["dama", "torre", "alfil", "caballo"]
        color_busqueda = "blanco" if pieza.color in ["blanco", "blanca"] else "negro"

        for p in self.piezas:
            if p.nombre in nombres and p.color == color_busqueda:
                clave = f"{p.nombre}_{color_busqueda}"
                if clave not in imagenes_menu:
                    imagenes_menu[clave] = p.imagen

        if len(imagenes_menu) < 4:
            for nom in nombres:
                clave = f"{nom}_{color_busqueda}"
                if clave not in imagenes_menu:
                    temp_p = PiezaAnimada(
                        nom, color_busqueda, 0, 0, self.tablero.tam_cuadro
                    )
                    imagenes_menu[clave] = temp_p.imagen

        esperando = True
        while esperando:
            opciones = self.tablero.dibujar_ventana_promocion(
                pieza.color, imagenes_menu
            )
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pos = pygame.mouse.get_pos()
                    for rect, nombre_pieza in opciones:
                        if rect.collidepoint(pos):
                            pieza.nombre = nombre_pieza
                            pieza.cargar_imagen()
                            esperando = False
            self.reloj_fps.tick(30)

    def dibujar_cartel_resultado(self):
        if not self.resultado:
            return

        # --- Configuración de dimensiones ---
        ancho_pop, alto_pop = 350, 280  # Un poco más grande para que luzca mejor

        # CAMBIO CLAVE: Usamos el ancho del tablero para centrar en X
        centro_x_tablero = self.tablero.ancho_tablero // 2
        centro_y_pantalla = self.alto_total // 2

        x = centro_x_tablero - (ancho_pop // 2)
        y = centro_y_pantalla - (alto_pop // 2)
        rect_fondo = pygame.Rect(x, y, ancho_pop, alto_pop)

        # 1. Sombra / Overlay (Cubre TODA la ventana)
        overlay = pygame.Surface((self.ancho_total, self.alto_total), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # Un toque más oscuro para más drama
        self.pantalla.blit(overlay, (0, 0))

        # 2. Cuerpo del Pop-up (Bordes redondeados)
        pygame.draw.rect(self.pantalla, (49, 46, 43), rect_fondo, border_radius=12)

        # 3. Título del resultado
        fuente_tit = pygame.font.SysFont("Segoe UI", 26, bold=True)
        texto_res = fuente_tit.render(self.resultado, True, (255, 255, 255))
        txt_rect = texto_res.get_rect(center=(rect_fondo.centerx, y + 45))
        self.pantalla.blit(texto_res, txt_rect)

        # 4. Botón Principal: "Revisión de partida"
        self.rect_revision = pygame.Rect(x + 25, y + 90, ancho_pop - 50, 60)
        pygame.draw.rect(
            self.pantalla, (129, 182, 76), self.rect_revision, border_radius=8
        )

        f_btn = pygame.font.SysFont("Segoe UI", 20, bold=True)
        txt_rev = f_btn.render("Revisión de partida", True, (255, 255, 255))
        self.pantalla.blit(txt_rev, txt_rev.get_rect(center=self.rect_revision.center))

        # 5. Botones Inferiores: "Nuevo Bot" y "Revancha"
        ancho_btn_peq = (ancho_pop - 60) // 2
        self.rect_nuevo_bot = pygame.Rect(x + 25, y + 170, ancho_btn_peq, 50)
        self.rect_revancha = pygame.Rect(
            x + 35 + ancho_btn_peq, y + 170, ancho_btn_peq, 50
        )

        for r, txt in [
            (self.rect_nuevo_bot, "Nuevo Bot"),
            (self.rect_revancha, "Revancha"),
        ]:
            # Dibujamos un fondo gris oscuro para los botones secundarios
            pygame.draw.rect(self.pantalla, (64, 62, 60), r, border_radius=8)
            t_btn = pygame.font.SysFont("Segoe UI", 16, bold=True)
            txt_surf = t_btn.render(txt, True, (255, 255, 255))
            self.pantalla.blit(txt_surf, txt_surf.get_rect(center=r.center))

    def realizar_movimiento(self, pieza, fila, col):
        """Método auxiliar para ejecutar un movimiento (usado por humano y bot)."""
        f_orig, c_orig = pieza.fila, pieza.col
        p_dest = next(
            (p for p in self.piezas if p.fila == fila and p.col == col and p != pieza),
            None,
        )

        es_captura = p_dest is not None or (
            pieza.nombre == "peon" and abs(col - c_orig) == 1 and not p_dest
        )

        texto_mov = self.obtener_notacion_corta(
            f_orig, c_orig, fila, col, pieza, es_captura
        )
        self.historial.append(texto_mov)
        self.actualizar_scroll_automatico()

        # Peón al paso (captura lógica)
        if pieza.nombre == "peon" and abs(col - c_orig) == 1 and not p_dest:
            p_dest = next(
                (p for p in self.piezas if p.fila == f_orig and p.col == col), None
            )

        # Enroque (mover torre)
        if pieza.nombre == "rey" and abs(col - c_orig) == 2:
            col_t_orig = 7 if col > c_orig else 0
            col_t_dest = col - 1 if col > c_orig else col + 1
            torre = next(
                (p for p in self.piezas if p.fila == fila and p.col == col_t_orig), None
            )
            if torre:
                torre.col, torre.x, torre.ha_movido = (
                    col_t_dest,
                    col_t_dest * self.tablero.tam_cuadro,
                    True,
                )

        if p_dest:
            if p_dest.color == "blanco":
                self.capturadas_negras.append(p_dest)
            else:
                self.capturadas_blancas.append(p_dest)
            self.piezas.remove(p_dest)
            self.reproducir_sonido("Captura")
        else:
            self.reproducir_sonido("Movimiento")

        self.ultimo_movimiento = (f_orig, c_orig, fila, col)
        pieza.fila, pieza.col, pieza.ha_movido = fila, col, True
        pieza.x, pieza.y = col * self.tablero.tam_cuadro, fila * self.tablero.tam_cuadro

        if pieza.nombre == "peon" and pieza.fila in [0, 7]:
            self.esperar_promocion(pieza)

        # --- CAMBIO DE TURNO ---
        self.turno = "negro" if self.turno == "blanco" else "blanco"

        # --- VERIFICACIÓN DE ESTADOS FINALES (CORREGIDO) ---

        # 1. Material insuficiente
        if self.verificar_material_insuficiente():
            self.resultado = "TABLAS (Material Insuficiente)"
            self.reproducir_sonido("Fin")
            return  # Salimos si ya terminó

        # 2. Obtener estado del Rey y movimientos legales
        n_rey = self.obtener_rey(self.turno)
        en_jaque = (
            self.esta_atacada(n_rey.fila, n_rey.col, self.turno) if n_rey else False
        )
        tiene_salida = self.tiene_movimientos_legales(self.turno)

        if en_jaque:
            if not tiene_salida:
                ganador = "Blancas" if self.turno == "negro" else "Negras"
                self.resultado = f"¡MATE! Ganan {ganador}"
                self.reproducir_sonido("Fin")
            else:
                self.reproducir_sonido("Jaque")
        else:
            if not tiene_salida:
                self.resultado = "TABLAS (Ahogado)"
                self.reproducir_sonido("Fin")

        # Limpieza y guardado
        self.seleccionada, self.movs_legales = None, []
        self.flechas = []
        self.guardar_estado()
        pygame.display.set_caption(f"Ajedrez - Turno: {self.turno.upper()}")

    def iniciar_partida(self):
        while self.partida_activa:
            pos = pygame.mouse.get_pos()
            self.actualizar_relojes()

            # DETERMINAR ESTADO DEL REY
            rey_act = self.obtener_rey(self.turno)
            rey_en_jaque = (
                rey_act
                if (
                    rey_act and self.esta_atacada(rey_act.fila, rey_act.col, self.turno)
                )
                else None
            )

            # LÓGICA DEL BOT (Se mantiene igual)
            if (
                self.turno == self.bot.color
                and not self.resultado
                and not self.bot_pensando
            ):
                ahora = pygame.time.get_ticks()
                if self.espera_bot == 0:
                    self.espera_bot = ahora
                if ahora - self.espera_bot > 500:
                    self.bot_pensando = True
                    turno_al_iniciar = self.turno

                    def tarea_bot(t_objetivo):
                        movimiento = self.bot.seleccionar_movimiento(self)
                        if self.turno == t_objetivo:
                            self.movimiento_pendiente_bot = movimiento
                        self.bot_pensando = False

                    threading.Thread(
                        target=tarea_bot, args=(turno_al_iniciar,), daemon=True
                    ).start()

            if (
                hasattr(self, "movimiento_pendiente_bot")
                and self.movimiento_pendiente_bot
            ):
                if self.turno == self.bot.color:
                    p_bot, f_bot, c_bot = self.movimiento_pendiente_bot
                    self.realizar_movimiento(p_bot, f_bot, c_bot)
                self.movimiento_pendiente_bot = None
                self.espera_bot = 0

            # 2. PROCESAR EVENTOS
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    self.partida_activa = False

                if evento.type == KEYDOWN:
                    teclas_colores = {K_1: "1", K_2: "2", K_3: "3", K_4: "4"}
                    if evento.key in teclas_colores:
                        self.color_flecha_actual = COLORES_FLECHAS[
                            teclas_colores[evento.key]
                        ]

                if evento.type == MOUSEWHEEL:
                    self.scroll_historial -= evento.y
                    max_scroll = max(0, len(self.historial) - self.max_lineas_visibles)
                    self.scroll_historial = max(
                        0, min(self.scroll_historial, max_scroll)
                    )

                if evento.type == MOUSEBUTTONDOWN:
                    # --- CLIC IZQUIERDO (BOTÓN 1) ---
                    if evento.button == 1:
                        self.flechas = []
                        self.circulos = []  # Borrar dibujos al interactuar

                        # Detección de botones
                        if self.tablero.rect_abandonar.collidepoint(pos):
                            if not self.bot_pensando and not self.resultado:
                                ganador = (
                                    "Negras" if self.turno == "blanco" else "Blancas"
                                )
                                self.resultado = f"Abandono - Ganan {ganador}"
                            continue

                        if self.tablero.rect_deshacer.collidepoint(pos):
                            if not self.bot_pensando:
                                self.deshacer_movimiento()
                            continue

                        # Clic en Tablero
                        if pos[0] < self.tablero.ancho_tablero:
                            col, fila = (
                                pos[0] // self.tablero.tam_cuadro,
                                pos[1] // self.tablero.tam_cuadro,
                            )
                            if not self.resultado and self.turno != self.bot.color:
                                if (
                                    self.seleccionada
                                    and (fila, col) in self.movs_legales
                                ):
                                    self.reloj_iniciado = True
                                    self.realizar_movimiento(
                                        self.seleccionada, fila, col
                                    )
                                else:
                                    p_clic = next(
                                        (
                                            p
                                            for p in self.piezas
                                            if p.fila == fila
                                            and p.col == col
                                            and p.color == self.turno
                                        ),
                                        None,
                                    )
                                    if p_clic:
                                        self.seleccionada = p_clic
                                        self.movs_legales = [
                                            (f, c)
                                            for f in range(8)
                                            for c in range(8)
                                            if self.es_movimiento_valido(p_clic, f, c)
                                            and not self.deja_al_rey_en_jaque(
                                                p_clic, f, c
                                            )
                                        ]
                                    else:
                                        self.seleccionada, self.movs_legales = None, []

                    # --- CLIC DERECHO (BOTÓN 3) ---
                    elif evento.button == 3:
                        if pos[0] < self.tablero.ancho_tablero:
                            col, fila = (
                                pos[0] // self.tablero.tam_cuadro,
                                pos[1] // self.tablero.tam_cuadro,
                            )
                            self.dibujando_flecha = True
                            self.inicio_flecha = (fila, col)

                if evento.type == MOUSEBUTTONUP:
                    if evento.button == 3 and self.dibujando_flecha:
                        # 1. Definimos ff y cf primero para que existan en todo este bloque
                        cf, ff = (
                            pos[0] // self.tablero.tam_cuadro,
                            pos[1] // self.tablero.tam_cuadro,
                        )

                        # 2. LÓGICA DE CÍRCULOS (Si soltamos en la misma casilla)
                        if self.inicio_flecha == (ff, cf):
                            # Estructura: (fila, columna, color)
                            nuevo_circulo = (ff, cf, self.color_flecha_actual)

                            encontrado = None
                            for c in self.circulos:
                                if c[0] == ff and c[1] == cf:
                                    encontrado = c
                                    break

                            if encontrado:
                                self.circulos.remove(encontrado)
                                # Si el color era distinto, ponemos el nuevo
                                if encontrado[2] != self.color_flecha_actual:
                                    self.circulos.append(nuevo_circulo)
                            else:
                                self.circulos.append(nuevo_circulo)

                        # 3. LÓGICA DE FLECHAS (Si soltamos en otra casilla)
                        else:
                            nueva_f = Flecha(
                                self.inicio_flecha[0],
                                self.inicio_flecha[1],
                                ff,
                                cf,
                                self.color_flecha_actual,
                                self.tablero.tam_cuadro,
                            )
                            if nueva_f in self.flechas:
                                self.flechas.remove(nueva_f)
                            else:
                                self.flechas.append(nueva_f)

                        self.dibujando_flecha = False

            # 3. DIBUJADO
            self.pantalla.fill((0, 0, 0))
            inicio_h = int(self.scroll_historial)
            hist_vis = self.historial[inicio_h : inicio_h + self.max_lineas_visibles]

            # Dibujamos el tablero base
            self.tablero.dibujar_tablero(
                self.piezas,
                self.seleccionada,
                rey_en_jaque,
                self.movs_legales,
                self.ultimo_movimiento,
                self.flechas,
                hist_vis,
                self.capturadas_blancas,
                self.capturadas_negras,
                self.tiempo_blanco,
                self.tiempo_negro,
                self.turno,
                inicio_historial=inicio_h,
                color_flecha_actual=self.color_flecha_actual,
                circulos=self.circulos,
            )

            # --- CORRECCIÓN AQUÍ: Llamamos a la nueva función unificada ---
            if hasattr(self.tablero, "dibujar_botones_control"):
                self.tablero.dibujar_botones_control(pos)

            if hasattr(self, "circulos"):  # Por seguridad si no lo has inicializado
                self.tablero.dibujar_circulos(self.circulos)

            # Cambio de cursor (Efecto mano)
            if self.tablero.rect_abandonar.collidepoint(
                pos
            ) or self.tablero.rect_deshacer.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.resultado:
                self.dibujar_cartel_resultado()

            pygame.display.flip()
            self.reloj_fps.tick(60)

        pygame.quit()
