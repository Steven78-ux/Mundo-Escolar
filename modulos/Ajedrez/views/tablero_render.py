"""Vistas del módulo views."""

import pygame
import os
from ..domain.tablero_logico import esta_atacada


class TableroRender:
    def __init__(self, pantalla, tema="Madera", res=(1150, 600)):
        self.pantalla = pantalla
        self.res = res
        # Cálculos de Proporciones Dinámicas
        self.MARGEN = 25
        self.lado_tablero = res[1] - (self.MARGEN * 2)
        self.tam_cuadro = self.lado_tablero // 8

        # Centrar el conjunto (Tablero + Panel) en la pantalla
        self.ancho_panel = 420
        espacio_separacion = 30
        ancho_total_contenido = (
            self.lado_tablero + espacio_separacion + self.ancho_panel
        )

        self.offset_x = (res[0] - ancho_total_contenido) // 2
        self.offset_y = self.MARGEN

        self.fuente = pygame.font.SysFont("Arial", 20, bold=True)
        self.fuente_reloj = pygame.font.SysFont("Consolas", 35, bold=True)
        self.fuente_historial = pygame.font.SysFont("Arial", 15, bold=True)
        self.fuente_nombres = pygame.font.SysFont("Arial", 22, bold=True)
        self.fuente_modal_titulo = pygame.font.SysFont("Verdana", 28, bold=True)
        self.fuente_modal_msg = pygame.font.SysFont("Verdana", 20, italic=True)
        self.fuente_coords = pygame.font.SysFont("Verdana", 12, bold=True)

        self.colores = self._obtener_colores_tema(tema)
        self.assets = self._cargar_iconos()

        # Configuración del Panel Lateral
        self.x_panel = self.offset_x + self.lado_tablero + espacio_separacion
        self.alto_panel = self.lado_tablero

        self.scroll_historial = 0
        self.tema_nombre = tema

        # Botones Redondeados (Tres botones ahora)
        espacio_btn = 10
        ancho_btn = (self.ancho_panel - (espacio_btn * 4)) // 3
        y_btns = self.offset_y + self.alto_panel - 55

        self.rect_deshacer = pygame.Rect(
            self.x_panel + espacio_btn, y_btns, ancho_btn, 45
        )
        self.rect_tablas = pygame.Rect(
            self.x_panel + ancho_btn + espacio_btn * 2, y_btns, ancho_btn, 45
        )
        self.rect_abandonar = pygame.Rect(
            self.x_panel + (ancho_btn * 2) + espacio_btn * 3, y_btns, ancho_btn, 45
        )

        # Rectángulos para Selección de Promoción
        self.ancho_promo = 400
        self.alto_promo = 120
        self.rect_modal_promo = pygame.Rect(
            (res[0] - self.ancho_promo) // 2,
            (res[1] - self.alto_promo) // 2,
            self.ancho_promo,
            self.alto_promo,
        )
        self.rects_promo = []  # Se llenan dinámicamente en el dibujo

        # Rectángulos del Modal (Calculados para el centro de la pantalla)
        modal_w, modal_h = 600, 420
        self.rect_modal_caja = pygame.Rect(
            (res[0] - modal_w) // 2, (res[1] - modal_h) // 2, modal_w, modal_h
        )

        btn_w, btn_h = 160, 50
        y_btns_modal = self.rect_modal_caja.bottom - 80
        self.rect_modal_nuevo = pygame.Rect(
            self.rect_modal_caja.x + 30, y_btns_modal, btn_w, btn_h
        )
        self.rect_modal_revancha = pygame.Rect(
            self.rect_modal_caja.centerx - btn_w // 2, y_btns_modal, btn_w, btn_h
        )
        self.rect_modal_salir = pygame.Rect(
            self.rect_modal_caja.right - btn_w - 30, y_btns_modal, btn_w, btn_h
        )

        # Botones Modal Tutorial Final
        btn_w_tut, btn_h_tut = 180, 50
        y_btns_tut = self.rect_modal_caja.bottom - 62
        self.rect_tut_regresar = pygame.Rect(
            self.rect_modal_caja.x + 20, y_btns_tut, btn_w_tut, btn_h_tut
        )
        self.rect_tut_reiniciar = pygame.Rect(
            self.rect_modal_caja.centerx - btn_w_tut // 2,
            y_btns_tut,
            btn_w_tut,
            btn_h_tut,
        )
        self.rect_tut_siguiente = pygame.Rect(
            self.rect_modal_caja.right - btn_w_tut - 20,
            y_btns_tut,
            btn_w_tut,
            btn_h_tut,
        )

        self.fuente_exito = pygame.font.SysFont("Verdana", 28, bold=True)
        self.fuente_modal_exito_msg = pygame.font.SysFont("Verdana", 20)

        # Optimizacion: Cache de superficies estaticas
        self.surf_tablero_cache = None
        self.surf_panel_cache = None
        self._last_invertir = None
        self._last_tema = tema
        self._cache_reloj_textos = {}  # (tiempo_str, color) -> Surface
        self._cache_movimientos_textos = {} # (texto, color) -> Surface
        
        # Pre-renderizado de marcadores tácticos
        self._surf_resplandor_jaque = self._pre_renderizar_resplandor_jaque()
        self._surfs_movimientos = self._pre_renderizar_marcadores_movimiento()

    def _obtener_colores_tema(self, tema):
        temas = {
            "Madera": {
                "claro": (240, 217, 181),
                "oscuro": (130, 90, 60),
                "panel": (42, 38, 34),
                "resaltado": (130, 90, 60),
                "fondo": (30, 22, 18),
            },
            "Bosque": {
                "claro": (235, 236, 208),
                "oscuro": (119, 149, 86),
                "panel": (38, 45, 30),
                "resaltado": (119, 149, 86),
                "fondo": (20, 28, 20),
            },
            "Oceano": {
                "claro": (140, 162, 173),
                "oscuro": (88, 117, 137),
                "panel": (30, 40, 50),
                "resaltado": (88, 117, 137),
                "fondo": (15, 22, 30),
            },
            "Fresa": {
                "claro": (255, 209, 220),
                "oscuro": (255, 105, 180),
                "panel": (50, 20, 35),
                "resaltado": (255, 105, 180),
                "fondo": (35, 15, 20),
            },
            "Algodon": {
                "claro": (255, 245, 250),  # Blanco rosado nube
                "oscuro": (255, 170, 210),  # Rosa pastel chicle
                "panel": (95, 40, 110),    # Púrpura fantasía profundo
                "resaltado": (255, 50, 150), # Fucsia brillante
                "fondo": (40, 20, 45),     # Noche violeta
            },
            "Cristal": {
                "claro": (240, 255, 255),  # Blanco Nieve (Azure)
                "oscuro": (175, 238, 238),  # Turquesa claro (Pale Turquoise)
                "panel": (45, 65, 85),  # Plateado azulado
                "resaltado": (0, 206, 209),  # Turquesa gélido
                "fondo": (10, 25, 35),  # Azul hielo profundo
            },
        }
        res = temas.get(tema, temas["Madera"])
        if "resaltado" not in res:
            res["resaltado"] = (0, 212, 255)
        return res

    def _cargar_iconos(self):
        ruta = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "piezas_animadas"
        )
        iconos = {}
        for t in ["peon", "torre", "caballo", "alfil", "dama", "rey"]:
            for c in ["blanco", "negro"]:
                p = os.path.join(ruta, f"{t}_{c}.png")
                if os.path.exists(p):
                    img = pygame.image.load(p).convert_alpha()
                    iconos[f"{t}_{c}"] = pygame.transform.scale(img, (25, 25))
        return iconos

    def dibujar(self, partida, mouse_pos, circulos_tacticos=[], flechas_tacticos=[],
                seleccionada=None, movimientos_posibles=[], nicknames=None, draw_panel=True,
                reyes_en_jaque=[]):
        
        self.pantalla.fill(self.colores.get("fondo", (20, 20, 20)))
        invertir = partida.color_usuario == "negro"

        # Optimizacion: Redibujar cuadricula solo si cambia la orientacion
        if self.surf_tablero_cache is None or self._last_invertir != invertir:
            self.surf_tablero_cache = pygame.Surface((self.lado_tablero, self.lado_tablero))
            self._dibujar_cuadricula_en_surface(self.surf_tablero_cache, invertir)
            self._last_invertir = invertir

        self.pantalla.blit(self.surf_tablero_cache, (self.offset_x, self.offset_y))

        # Resaltar reyes en jaque (Lichess style)
        for f, c in reyes_en_jaque:
            self._dibujar_resplandor_jaque(f, c, invertir)

        self.dibujar_movimientos_posibles(
            partida, seleccionada, movimientos_posibles, invertir
        )
        self.dibujar_piezas(partida.piezas, invertir)
        self.dibujar_elementos_tacticos(circulos_tacticos, flechas_tacticos, invertir)
        if draw_panel:  # Condicional para dibujar el panel lateral estándar
            self.dibujar_panel_lateral(partida, mouse_pos, nicknames)

    def _dibujar_resplandor_jaque(self, f, c, invertir):
        """Dibuja un resplandor rojo debajo del rey en jaque estilo Lichess."""
        f_v, c_v = (7 - f, 7 - c) if invertir else (f, c)
        x = self.offset_x + c_v * self.tam_cuadro
        y = self.offset_y + f_v * self.tam_cuadro

        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        centro = self.tam_cuadro // 2
        radio_max = self.tam_cuadro // 2

        # Dibujamos capas de brillo radial rojo
        for r in range(radio_max, 0, -2):
            # Alpha decreciente hacia afuera para un efecto difuminado suave
            alpha = int(180 * (1 - (r / radio_max) ** 0.7))
            if alpha > 0:
                pygame.draw.circle(s, (255, 0, 0, alpha), (centro, centro), r)

        self.pantalla.blit(s, (x, y))

    def _pre_renderizar_resplandor_jaque(self):
        """Genera una sola vez la superficie de resplandor para el Rey."""
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        centro = self.tam_cuadro // 2
        radio_max = self.tam_cuadro // 2
        for r in range(radio_max, 0, -2):
            alpha = int(180 * (1 - (r / radio_max) ** 0.7))
            if alpha > 0:
                pygame.draw.circle(s, (255, 0, 0, alpha), (centro, centro), r)
        return s.convert_alpha()

    def _pre_renderizar_marcadores_movimiento(self):
        """Pre-calcula los puntos y círculos de movimiento."""
        surfs = {}
        # Punto normal
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 0, 0, 70), (self.tam_cuadro // 2, self.tam_cuadro // 2), 12)
        surfs["normal"] = s.convert_alpha()
        # Círculo de captura
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 50, 50, 140), (self.tam_cuadro // 2, self.tam_cuadro // 2), self.tam_cuadro // 2 - 5, 6)
        surfs["captura"] = s.convert_alpha()
        # Círculo especial (azul)
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 150, 255, 180), (self.tam_cuadro // 2, self.tam_cuadro // 2), 15)
        surfs["especial"] = s.convert_alpha()
        return surfs

    def dibujar_elementos_tacticos(self, circulos, flechas, invertir):
        """Dibuja elementos tácticos optimizando el uso de superficies."""
        sub_rect = (
            self.offset_x,
            self.offset_y,
            8 * self.tam_cuadro,
            8 * self.tam_cuadro,
        )
        subsurface = self.pantalla.subsurface(sub_rect)

        for f, c in circulos:
            f_v, c_v = (7 - f, 7 - c) if invertir else (f, c)
            s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
            # Color verde con transparencia (Alpha 160)
            pygame.draw.circle(
                s, (0, 255, 0, 160), (self.tam_cuadro // 2, self.tam_cuadro // 2), 33, 5
            )
            subsurface.blit(s, (c_v * self.tam_cuadro, f_v * self.tam_cuadro))

        # Dibujar flechas
        for flecha in flechas:
            # La clase Flecha se encarga de su propio dibujo con transparencia
            flecha.dibujar(subsurface, invertir=invertir)

    def dibujar_movimientos_posibles(
        self, partida, seleccionada, movimientos, invertir
    ):
        """Dibuja sugerencias de movimiento (puntos) y capturas (círculos rojos)."""
        if not seleccionada or not movimientos:
            return

        for f, c in movimientos:
            # Detectar si hay una pieza enemiga en el destino para mostrar círculo de captura
            pieza_dest = next(
                (p for p in partida.piezas if p.fila == f and p.col == c), None
            )

            f_v, c_v = (7 - f, 7 - c) if invertir else (f, c)
            x = self.offset_x + c_v * self.tam_cuadro
            y = self.offset_y + f_v * self.tam_cuadro

            if pieza_dest:
                self.pantalla.blit(self._surfs_movimientos["captura"], (x, y))
            elif (seleccionada.tipo == "rey" and abs(c - seleccionada.col) == 2) or (
                seleccionada.tipo == "peon" and (f, c) == partida.en_passant_target
            ):
                self.pantalla.blit(self._surfs_movimientos["especial"], (x, y))
            else:
                self.pantalla.blit(self._surfs_movimientos["normal"], (x, y))

    def _dibujar_cuadricula_en_surface(self, superficie, invertir):
        letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if invertir: letras.reverse()

        for f in range(8):
            for c in range(8):
                color = (
                    self.colores["claro"]
                    if (f + c) % 2 == 0
                    else self.colores["oscuro"]
                )
                f_v, c_v = (7 - f, 7 - c) if invertir else (f, c)
                rect_x, rect_y = c_v * self.tam_cuadro, f_v * self.tam_cuadro

                pygame.draw.rect(superficie, color, (rect_x, rect_y, self.tam_cuadro, self.tam_cuadro))

                # --- Dibujar Coordenadas ---
                color_texto = (
                    self.colores["oscuro"]
                    if (f + c) % 2 == 0
                    else self.colores["claro"]
                )

                if c_v == 0:
                    num_txt = str(f + 1) if invertir else str(8 - f)
                    lbl_n = self.fuente_coords.render(num_txt, True, color_texto).convert_alpha()
                    superficie.blit(lbl_n, (rect_x + 2, rect_y + 2))

                if f_v == 7:
                    lbl_l = self.fuente_coords.render(letras[c_v], True, color_texto).convert_alpha()
                    superficie.blit(lbl_l, (rect_x + self.tam_cuadro - 12, rect_y + self.tam_cuadro - 15))

    def dibujar_piezas(self, piezas, invertir):
        for p in piezas:
            if hasattr(p, "dibujar"):
                # Pasamos solo los offsets base; la pieza integra su propia col/fila en su target
                p.dibujar(
                    self.pantalla, (self.offset_x, self.offset_y), invertir=invertir
                )

    def dibujar_panel_lateral(self, partida, mouse_pos, nicknames):
        # Panel con Transparencia y Borde Dinámico
        panel_surf = pygame.Surface(
            (self.ancho_panel, self.alto_panel), pygame.SRCALPHA
        )
        # Color del panel con opacidad (Alpha = 220 de 255)
        pygame.draw.rect(
            panel_surf,
            (*self.colores["panel"], 220),
            (0, 0, self.ancho_panel, self.alto_panel),
            border_radius=15,
        )
        # Borde del color de acento del tema
        pygame.draw.rect(
            panel_surf,
            self.colores["resaltado"],
            (0, 0, self.ancho_panel, self.alto_panel),
            2,
            border_radius=15,
        )
        self.pantalla.blit(panel_surf, (self.x_panel, self.offset_y))

        # Relojes: Identificar colores lógicos para las capturas
        op_color = "blanco" if partida.color_usuario == "negro" else "negro"
        pl_color = partida.color_usuario

        # Oponente (Arriba)
        self._dibujar_reloj_estilizado(
            self.x_panel + 10,
            self.offset_y + 10,
            nicknames["oponente"],
            partida.tiempo_negro if op_color == "negro" else partida.tiempo_blanco,
            partida.turno == op_color,
            (
                partida.capturas_negras
                if op_color == "negro"
                else partida.capturas_blancas
            ),
            op_color,
        )
        # Jugador (Abajo)
        self._dibujar_reloj_estilizado(
            self.x_panel + 10,
            self.offset_y + self.alto_panel - 165,
            nicknames["jugador"],
            partida.tiempo_blanco if pl_color == "blanco" else partida.tiempo_negro,
            partida.turno == pl_color,
            (
                partida.capturas_blancas
                if pl_color == "blanco"
                else partida.capturas_negras
            ),
            pl_color,
        )

        # Historial de movimientos en el centro
        alto_historial = self.alto_panel - 290
        self._dibujar_historial(
            self.x_panel + 10, self.offset_y + 110, partida.historial, alto_historial
        )

        # Botones de Acción
        color_deshacer = (
            (52, 152, 219)
            if self.rect_deshacer.collidepoint(mouse_pos)
            else (41, 128, 185)
        )
        color_tablas = (
            (149, 165, 166)
            if self.rect_tablas.collidepoint(mouse_pos)
            else (127, 140, 141)
        )
        color_abandonar = (
            (231, 76, 60)
            if self.rect_abandonar.collidepoint(mouse_pos)
            else (192, 57, 43)
        )

        pygame.draw.rect(
            self.pantalla, color_deshacer, self.rect_deshacer, border_radius=15
        )
        pygame.draw.rect(
            self.pantalla, color_tablas, self.rect_tablas, border_radius=15
        )
        pygame.draw.rect(
            self.pantalla, color_abandonar, self.rect_abandonar, border_radius=15
        )

        if self.rect_deshacer.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.pantalla, "white", self.rect_deshacer, 2, border_radius=15
            )
        if self.rect_tablas.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.pantalla, "white", self.rect_tablas, 2, border_radius=15
            )
        if self.rect_abandonar.collidepoint(mouse_pos):
            pygame.draw.rect(
                self.pantalla, "white", self.rect_abandonar, 2, border_radius=15
            )

        # Textos de botones simplificados
        txt_undo = self.fuente_historial.render("ATRÁS", True, "white")
        txt_draw = self.fuente_historial.render("TABLAS", True, "white")
        txt_exit = self.fuente_historial.render("RENDIR", True, "white")

        self.pantalla.blit(
            txt_undo, (self.rect_deshacer.centerx - 20, self.rect_deshacer.y + 14)
        )
        self.pantalla.blit(
            txt_draw, (self.rect_tablas.centerx - 25, self.rect_tablas.y + 14)
        )
        self.pantalla.blit(
            txt_exit, (self.rect_abandonar.centerx - 25, self.rect_abandonar.y + 14)
        )

    def _dibujar_historial(self, x, y, historial, alto):
        ancho = self.ancho_panel - 20
        bg_hist = tuple(min(255, c + 15) for c in self.colores.get("panel", (25, 25, 30)))
        pygame.draw.rect(
            self.pantalla, bg_hist, (x, y, ancho, alto), border_radius=15
        )
        titulo = self.fuente.render("HISTORIAL", True, (200, 200, 200))
        self.pantalla.blit(titulo, (x + 10, y + 5))

        # Definir área de clip para el scroll
        rect_clip = pygame.Rect(x + 5, y + 30, ancho - 10, alto - 40)
        subsurface_hist = self.pantalla.subsurface(rect_clip)

        for i, mov_data in enumerate(historial):
            # Ahora 2 columnas, cambia a la segunda tras 20 movimientos
            col_idx = i // 20
            fila = i % 20
            pos_x = 10 + (col_idx * 155)
            pos_y = 5 + (fila * 22) - self.scroll_historial

            if pos_y < -30 or pos_y > alto:
                continue

            num_str = str(i+1)
            if num_str not in self._cache_movimientos_textos:
                self._cache_movimientos_textos[num_str] = self.fuente_historial.render(num_str, True, (100, 100, 100)).convert_alpha()
            
            num_txt = self._cache_movimientos_textos[num_str]
            subsurface_hist.blit(num_txt, (pos_x, pos_y))

            offset_txt = 22
            if "O-O" not in mov_data["txt"]:
                key = f"{mov_data['tipo']}_{mov_data['color']}"
                if key in self.assets:
                    subsurface_hist.blit(
                        self.assets[key], (pos_x + offset_txt, pos_y - 4)
                    )
                    offset_txt += 25

            mov_txt_str = mov_data["txt"]
            if (mov_txt_str, "white") not in self._cache_movimientos_textos:
                self._cache_movimientos_textos[(mov_txt_str, "white")] = self.fuente_historial.render(mov_txt_str, True, "white").convert_alpha()
                
            txt_mov = self._cache_movimientos_textos[(mov_txt_str, "white")]
            subsurface_hist.blit(txt_mov, (pos_x + offset_txt, pos_y))

    def _dibujar_reloj_estilizado(
        self, x, y, etiqueta, tiempo, es_activo, capturas, color_logico
    ):
        """Dibuja un marco de reloj con tipografía tecnológica y estado de turno."""
        ancho, alto = self.ancho_panel - 20, 85

        # Lógica de Color de Alerta
        color_reloj = (255, 255, 255)
        if tiempo <= 5:  # Rojo palpitante
            alpha = abs(pygame.time.get_ticks() % 1000 - 500) / 500
            color_reloj = (255, int(50 * alpha), int(50 * alpha))
        elif tiempo <= 10:
            color_reloj = (255, 50, 50)  # Rojo fijo
        elif tiempo <= 30:
            color_reloj = (255, 215, 0)  # Amarillo

        color_borde = self.colores["resaltado"] if es_activo else (60, 60, 65)
        # Fondo del reloj un poco más claro para visibilidad
        pygame.draw.rect(
            self.pantalla, (55, 60, 80), (x, y, ancho, alto), border_radius=15
        )
        pygame.draw.rect(
            self.pantalla, color_borde, (x, y, ancho, alto), 2, border_radius=15
        )

        # Nombre del Jugador (Color blanco y más grande)
        txt_name = self.fuente_nombres.render(etiqueta, True, "white")
        self.pantalla.blit(txt_name, (x + 15, y + 8))

        # Tiempo
        minutos, segundos = divmod(int(tiempo), 60)
        tiempo_str = f"{minutos:02}:{segundos:02}"
        cache_key = (tiempo_str, color_reloj)
        
        if cache_key not in self._cache_reloj_textos:
            self._cache_reloj_textos[cache_key] = self.fuente_reloj.render(tiempo_str, True, color_reloj).convert_alpha()
        
        txt_time = self._cache_reloj_textos[cache_key]
        self.pantalla.blit(txt_time, (x + ancho - 110, y + 25))

        # Piezas capturadas (Subidas un poco para no tocar el borde)
        # Si este reloj es del bando X, muestra las piezas capturadas del bando contrario
        color_iconos = "negro" if color_logico == "blanco" else "blanco"
        y_capturas = y + 52
        for i, p_tipo in enumerate(capturas[-10:]):
            key = f"{p_tipo}_{color_iconos}"
            if key in self.assets:
                self.pantalla.blit(self.assets[key], (x + 15 + (i * 26), y_capturas))

    def _wrap_text_for_modal(self, text, font, max_width):
        """Helper para envolver texto en modales."""
        words = text.split()
        if not words:
            return [""]
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        return lines

    def dibujar_modal_exito_tutorial(self, mensaje, stars_earned, mouse_pos):
        """Dibuja un mensaje central de éxito transitorio con estrellas y botón Siguiente."""
        # Fondo difuminado
        w, h = 500, 180  # Modal más compacto y elegante
        rect = pygame.Rect((self.res[0] - w) // 2, (self.res[1] - h) // 2, w, h)

        overlay = pygame.Surface(self.res, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.pantalla.blit(overlay, (0, 0))

        pygame.draw.rect(self.pantalla, (27, 38, 59), rect, border_radius=20)
        pygame.draw.rect(self.pantalla, (0, 212, 255), rect, 3, border_radius=20)

        # Mensaje envuelto
        wrapped_msg = self._wrap_text_for_modal(
            mensaje, self.fuente_modal_exito_msg, w - 40
        )
        y_offset = rect.y + 20
        for line in wrapped_msg:
            txt_render = self.fuente_modal_exito_msg.render(line, True, (0, 255, 127))
            self.pantalla.blit(
                txt_render, (rect.centerx - txt_render.get_width() // 2, y_offset)
            )
            y_offset += txt_render.get_height() + 5

        # Cargar y mostrar imagen de estrella
        if stars_earned > 0:
            if not hasattr(self, "_star_image"):
                star_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets",
                    "imagenes",
                    "estrella.png",
                )
                if not os.path.exists(star_path):
                    star_path = os.path.join(
                        os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(os.path.abspath(__file__))
                                )
                            )
                        ),
                        "assets",
                        "imagenes",
                        "estrella.png",
                    )
                self._star_image = pygame.image.load(star_path).convert_alpha()
                self._star_image = pygame.transform.scale(
                    self._star_image, (35, 35)
                )  # Tamaño de la estrella

            total_stars_width = (
                stars_earned * (self._star_image.get_width() + 5)
                - 5  # Ancho total de las estrellas
            )
            start_x_stars = rect.centerx - total_stars_width // 2
            for i in range(stars_earned):  # Dibujar cada estrella
                self.pantalla.blit(
                    self._star_image,
                    (
                        start_x_stars + i * (self._star_image.get_width() + 5),
                        y_offset + 5,
                    ),
                )
            y_offset += (
                self._star_image.get_height() + 15
            )  # Ajustar offset para el botón

        # Botones "Reiniciar" y "Siguiente"
        btn_w, btn_h = 140, 35
        gap = 20
        total_w = btn_w * 2 + gap
        start_x = rect.centerx - total_w // 2

        rect_reiniciar_btn = pygame.Rect(start_x, rect.bottom - 52, btn_w, btn_h)
        rect_siguiente_btn = pygame.Rect(
            start_x + btn_w + gap, rect.bottom - 52, btn_w, btn_h
        )

        # Dibujar botón Reiniciar
        re_color = (149, 165, 166)
        if rect_reiniciar_btn.collidepoint(mouse_pos):
            re_color = tuple(min(255, c + 30) for c in re_color)
            pygame.draw.rect(
                self.pantalla, "white", rect_reiniciar_btn, 2, border_radius=15
            )
        pygame.draw.rect(self.pantalla, re_color, rect_reiniciar_btn, border_radius=15)
        txt_re = self.fuente_historial.render("REINICIAR", True, "white")
        self.pantalla.blit(
            txt_re,
            (
                rect_reiniciar_btn.centerx - txt_re.get_width() // 2,
                rect_reiniciar_btn.centery - txt_re.get_height() // 2,
            ),
        )

        # Dibujar botón Siguiente
        btn_color = (39, 174, 96)  # Verde
        if rect_siguiente_btn.collidepoint(mouse_pos):
            btn_color = tuple(
                min(255, c + 20) for c in btn_color
            )  # Verde más oscuro al pasar el ratón
            pygame.draw.rect(
                self.pantalla, "white", rect_siguiente_btn, 2, border_radius=15
            )  # Borde blanco al pasar el ratón
        pygame.draw.rect(self.pantalla, btn_color, rect_siguiente_btn, border_radius=15)
        txt_btn = self.fuente_historial.render("SIGUIENTE", True, "white")
        self.pantalla.blit(
            txt_btn,
            (
                rect_siguiente_btn.centerx - txt_btn.get_width() // 2,
                rect_siguiente_btn.centery - txt_btn.get_height() // 2,
            ),
        )

        return {"siguiente": rect_siguiente_btn, "reiniciar": rect_reiniciar_btn}

    def dibujar_modal_seccion_completa(self, titulo, mouse_pos, lesson_stats):
        """Dibuja el modal de fin de sección con 3 opciones."""
        overlay = pygame.Surface(self.res, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.pantalla.blit(overlay, (0, 0))

        # Caja
        pygame.draw.rect(
            self.pantalla, (27, 38, 59), self.rect_modal_caja, border_radius=40
        )
        pygame.draw.rect(
            self.pantalla, (0, 212, 255), self.rect_modal_caja, 4, border_radius=40
        )

        # Título
        tit_render = self.fuente_modal_titulo.render(
            "¡SECCIÓN COMPLETADA!", True, (255, 215, 0)
        )
        self.pantalla.blit(
            tit_render,
            (
                self.rect_modal_caja.centerx - tit_render.get_width() // 2,
                self.rect_modal_caja.y + 20,  # Ajustado Y
            ),
        )

        msg_render = self.fuente_modal_msg.render(titulo, True, "white")
        self.pantalla.blit(
            msg_render,
            (
                self.rect_modal_caja.centerx - msg_render.get_width() // 2,
                self.rect_modal_caja.y + 70,  # Ajustado Y
            ),
        )

        # Mostrar estadísticas de la lección
        total_lesson_time = sum(s["time"] for s in lesson_stats.values())
        total_lesson_stars = sum(s["stars"] for s in lesson_stats.values())
        num_sub_sections = len(lesson_stats)

        # 1. Dibujar Trofeo Central (Simplificación)
        ruta_trofeo = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "imagenes",
            "trofeo.png",
        )
        y_content = self.rect_modal_caja.y + 110
        if os.path.exists(ruta_trofeo):
            img_trofeo = pygame.image.load(ruta_trofeo).convert_alpha()
            img_trofeo = pygame.transform.scale(img_trofeo, (110, 110))
            self.pantalla.blit(
                img_trofeo, (self.rect_modal_caja.centerx - 55, y_content)
            )
            y_content += 120
        else:
            y_content += 20

        # 2. Resumen de Estrellas (Estrella única = Total)
        star_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "imagenes",
            "estrella.png",
        )

        # Fallback de ruta para robustez
        if not os.path.exists(star_path):
            star_path = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    )
                ),
                "assets",
                "imagenes",
                "estrella.png",
            )

        if os.path.exists(star_path):
            star_img = pygame.image.load(star_path).convert_alpha()
            star_img = pygame.transform.scale(star_img, (45, 45))

            # Dibujar "⭐ = X"
            txt_stars = self.fuente_modal_titulo.render(
                f" = {total_lesson_stars}", True, (255, 215, 0)
            )
            total_w = star_img.get_width() + txt_stars.get_width() + 15
            start_x = self.rect_modal_caja.centerx - total_w // 2

            # Alineación vertical perfecta centrando el texto respecto a la estrella
            star_rect = star_img.get_rect(topleft=(start_x, y_content))
            text_rect = txt_stars.get_rect(midleft=(star_rect.right + 15, star_rect.centery))
            
            self.pantalla.blit(star_img, star_rect)
            self.pantalla.blit(txt_stars, text_rect)

            y_content += 55
        else:
            # Fallback de texto si falla la carga de imagen
            txt_fallback = self.fuente_modal_titulo.render(
                f"Puntaje: {total_lesson_stars} ⭐", True, (255, 215, 0)
            )
            self.pantalla.blit(
                txt_fallback,
                (
                    self.rect_modal_caja.centerx - txt_fallback.get_width() // 2,
                    y_content,
                ),
            )
            y_content += 65

        # 3. Mostrar estadísticas restantes ordenadas
        stats_lines = [
            f"Misiones completadas: {num_sub_sections}",
            f"Tiempo total: {total_lesson_time // 60:02d}:{total_lesson_time % 60:02d}",
        ]

        for line in stats_lines:
            rend = self.fuente_modal_msg.render(line, True, "white")
            self.pantalla.blit(
                rend, (self.rect_modal_caja.centerx - rend.get_width() // 2, y_content)
            )
            y_content += 30

        # Botones
        btns = [
            (self.rect_tut_regresar, (41, 128, 185), "MENÚ ACADEMIA"),
            (self.rect_tut_reiniciar, (149, 165, 166), "REINICIAR"),
            (self.rect_tut_siguiente, (39, 174, 96), "SIGUIENTE"),
        ]

        for rect, color, texto in btns:
            if rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 40) for c in color)
                pygame.draw.rect(self.pantalla, "white", rect, 2, border_radius=15)

            pygame.draw.rect(self.pantalla, color, rect, border_radius=15)
            txt_btn = self.fuente_historial.render(texto, True, "white")
            self.pantalla.blit(
                txt_btn,
                (
                    rect.centerx - txt_btn.get_width() // 2,
                    rect.centery - txt_btn.get_height() // 2,
                ),
            )

    def dibujar_modal_promocion(self, color, mouse_pos):
        """Dibuja el selector de piezas para la promoción del peón."""
        overlay = pygame.Surface(self.res, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.pantalla.blit(overlay, (0, 0))

        pygame.draw.rect(
            self.pantalla,
            self.colores.get("panel", (27, 38, 59)),
            self.rect_modal_promo,
            border_radius=20,
        )
        pygame.draw.rect(
            self.pantalla,
            self.colores.get("resaltado", (0, 212, 255)),
            self.rect_modal_promo,
            2,
            border_radius=20,
        )

        txt = self.fuente_historial.render(
            "ELIGE UNA PIEZA PARA TU PEÓN:", True, "white"
        )
        self.pantalla.blit(
            txt,
            (
                self.rect_modal_promo.centerx - txt.get_width() // 2,
                self.rect_modal_promo.y + 10,
            ),
        )

        piezas = ["dama", "torre", "alfil", "caballo"]
        self.rects_promo = []

        for i, tipo in enumerate(piezas):
            r = pygame.Rect(
                self.rect_modal_promo.x + 20 + (i * 95),
                self.rect_modal_promo.y + 40,
                80,
                70,
            )
            self.rects_promo.append((tipo, r))

            # Hover
            if r.collidepoint(mouse_pos):
                pygame.draw.rect(self.pantalla, (52, 152, 219), r, border_radius=10)

            # Dibujar icono grande
            key = f"{tipo}_{color}"
            if key in self.assets:
                img = pygame.transform.scale(self.assets[key], (50, 50))
                self.pantalla.blit(img, (r.centerx - 25, r.centery - 25))

    def dibujar_modal_resultado(
        self, ganador, perdedor, motivo, mouse_pos, nicknames, contra_ia=False
    ):
        """Dibuja la ventana emergente de fin de partida."""
        # 1. Capa de Fondo (Alpha 160)
        overlay = pygame.Surface(self.res, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.pantalla.blit(overlay, (0, 0))

        # 2. Determinar Estilo y Ganador
        es_empate = any(
            x in motivo for x in ["Tablas", "Empate", "Ahogado", "Material"]
        )

        if es_empate:
            color_borde = (52, 152, 219)  # Azul
            titulo_txt = "¡Es un Empate!"
            img_key = "empate"
        elif contra_ia:
            if ganador == nicknames["jugador"]:
                color_borde = (255, 215, 0) # Dorado
                titulo_txt = f"¡VICTORIA! {ganador.upper()} GANA"
                img_key = "victoria"
            else:
                color_borde = (231, 76, 60) # Rojo
                titulo_txt = "¡Derrota! Has perdido"
                img_key = "derrota"
        else:
            # Modo Local: Siempre estilo Victoria en Dorado para el ganador
            color_borde = (255, 215, 0)
            titulo_txt = f"¡{ganador.upper()} HA GANADO!"
            img_key = "victoria"

        # 3. Caja Central Redondeada
        pygame.draw.rect(
            self.pantalla, (27, 38, 59), self.rect_modal_caja, border_radius=40
        )
        pygame.draw.rect(
            self.pantalla, color_borde, self.rect_modal_caja, 3, border_radius=40
        )

        # 4. Textos
        titulo_render = self.fuente_modal_titulo.render(titulo_txt, True, color_borde)
        self.pantalla.blit(
            titulo_render,
            (
                self.rect_modal_caja.centerx - titulo_render.get_width() // 2,
                self.rect_modal_caja.y + 30,
            ),
        )

        # Frase del Rey Sabio
        frases_map = {
            "Jaque Mate": "¡Un Jaque Mate magistral!",
            "Tiempo": "¡El tiempo se ha agotado!",
            "Abandono": "¡Victoria por abandono!",
            "Tablas por Acuerdo": "¡Han decidido que son iguales!",
            "Rey Ahogado": "¡El Rey no tiene a donde ir!",
            "Insuficiencia de Material": "¡No quedan piezas para ganar!",
            "Tablas": "¡Nadie puede atrapar al otro!",
        }
        frase = frases_map.get(motivo, motivo)

        # Mostrar ganador o motivo
        sub_txt = f"Perdedor: {perdedor}" if not es_empate else "¡Gran esfuerzo!"

        msg_render = self.fuente_modal_msg.render(f"{sub_txt} | {frase}", True, "white")
        self.pantalla.blit(
            msg_render,
            (
                self.rect_modal_caja.centerx - msg_render.get_width() // 2,
                self.rect_modal_caja.y + 85,
            ),
        )

        # 5. Imagen Central
        ruta_img = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "imagenes",
            f"{img_key}.png",
        )
        if os.path.exists(ruta_img):
            img = pygame.image.load(ruta_img).convert_alpha()
            img = pygame.transform.scale(img, (180, 180))
            self.pantalla.blit(
                img, (self.rect_modal_caja.centerx - 90, self.rect_modal_caja.y + 130)
            )

        # 5. Botones de Acción
        botones = [
            (self.rect_modal_nuevo, (39, 174, 96), "NUEVO JUEGO"),
            (self.rect_modal_revancha, (41, 128, 185), "REVANCHA"),
            (self.rect_modal_salir, (192, 57, 43), "SALIR"),
        ]

        for rect, color, texto in botones:
            # Hover
            if rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 30) for c in color)
                pygame.draw.rect(self.pantalla, "white", rect, 2, border_radius=15)

            pygame.draw.rect(self.pantalla, color, rect, border_radius=15)
            txt_btn = self.fuente_historial.render(texto, True, "white")
            self.pantalla.blit(
                txt_btn,
                (
                    rect.centerx - txt_btn.get_width() // 2,
                    rect.centery - txt_btn.get_height() // 2,
                ),
            )