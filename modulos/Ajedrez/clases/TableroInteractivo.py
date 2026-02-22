import pygame
import math

# Colores originales
COLOR_ABANDONAR = (150, 45, 45)
COLOR_ABANDONAR_HOVER = (180, 60, 60)  # Más claro

COLOR_DESHACER = (50, 48, 46)
COLOR_DESHACER_HOVER = (70, 68, 66)  # Más claro


class TableroInteractivo:
    def __init__(self, tam_cuadro=75):
        self.tam_cuadro = tam_cuadro
        self.ancho_tablero = 8 * tam_cuadro
        self.tam_tablero = self.ancho_tablero
        self.ancho_panel = 350
        self.ancho_total = self.ancho_tablero + self.ancho_panel
        self.alto_total = self.ancho_tablero

        self.pantalla = pygame.display.set_mode((self.ancho_total, self.alto_total))
        pygame.display.set_caption("Ajedrez Interactivo - Estilo Moderno")

        # --- PALETA DE COLORES ---
        self.COLOR_CLARO = (235, 235, 210)
        self.COLOR_OSCURO = (115, 149, 82)
        self.COLOR_PANEL_FONDO = (30, 29, 27)
        self.COLOR_PANEL_MOVIMIENTOS = (46, 44, 41)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_TEXTO_SECUNDARIO = (171, 170, 168)
        self.COLOR_ACENTO = (129, 182, 76)
        self.COLOR_RELOJ_CRITICO = (231, 76, 60)
        self.COLOR_ROJO_JAQUE = (255, 0, 0, 160)
        self.COLOR_ULTIMO_MOV = (245, 246, 130, 150)
        self.COLOR_CIRCULO = (0, 255, 0, 140)

        # Fuentes
        pygame.font.init()
        fuente_base = "Segoe UI" if "segoeui" in pygame.font.get_fonts() else "Arial"
        self.fuente_ui = pygame.font.SysFont(fuente_base, 24, bold=True)
        self.fuente_digital = pygame.font.SysFont("Consolas", 36, bold=True)
        self.fuente_pequena = pygame.font.SysFont(fuente_base, 16)
        self.fuente_jugador = pygame.font.SysFont(fuente_base, 20, bold=True)
        self.fuente_emoji = pygame.font.SysFont("Segoe UI Symbol", 16)

        self.rect_abandonar = pygame.Rect(
            0, 0, 150, 40
        )  # Reducimos el ancho de 200 a 150
        self.rect_deshacer = pygame.Rect(
            0, 0, 150, 40
        )  # Reducimos el ancho de 200 a 150

    def dibujar_tablero(
        self,
        piezas,
        seleccionada,
        rey_en_jaque,
        movs_legales,
        ultimo_movimiento,
        flechas,
        historial,
        capturadas_b,
        capturadas_n,
        t_blanco,
        t_negro,
        turno,
        inicio_historial=0,
        color_flecha_actual=(0, 255, 0, 160),
        circulos=None,
    ):

        if circulos is None:
            circulos = []

        # Fondo del panel lateral
        pygame.draw.rect(
            self.pantalla,
            self.COLOR_PANEL_FONDO,
            (self.ancho_tablero, 0, self.ancho_panel, self.alto_total),
        )

        self.dibujar_cuadricula()

        if ultimo_movimiento:
            self.resaltar_ultimo_movimiento(ultimo_movimiento)
        if rey_en_jaque:
            self.dibujar_brillo_jaque(rey_en_jaque)
        if seleccionada:
            self.dibujar_puntos_legales(movs_legales, piezas, seleccionada)

        for pieza in piezas:
            pieza.dibujar(self.pantalla)
        for flecha in flechas:
            flecha.dibujar(self.pantalla)

        self.dibujar_circulos(circulos)

        # UI Lateral
        self.dibujar_panel_lateral(
            historial,
            capturadas_b,
            capturadas_n,
            t_blanco,
            t_negro,
            turno,
            color_flecha_actual,
        )

        # --- AQUÍ LLAMAMOS A LA FUNCIÓN UNIFICADA ---
        # Obtenemos la posición del mouse para el efecto hover
        pos_mouse = pygame.mouse.get_pos()
        self.dibujar_botones_control(pos_mouse)

    def dibujar_cuadricula(self):
        for fila in range(8):
            for col in range(8):
                color = self.COLOR_CLARO if (fila + col) % 2 == 0 else self.COLOR_OSCURO
                x, y = col * self.tam_cuadro, fila * self.tam_cuadro

                pygame.draw.rect(
                    self.pantalla, color, (x, y, self.tam_cuadro, self.tam_cuadro)
                )

                # --- DIBUJAR COORDENADAS ---
                # El color del texto debe ser el opuesto al del cuadro para que sea legible
                # Color dinámico para que resalte sobre el cuadro
                color_texto_coord = (
                    self.COLOR_OSCURO if (fila + col) % 2 == 0 else self.COLOR_CLARO
                )

                # --- NÚMEROS (Eje Vertical) ---
                if col == 0:
                    txt_num = self.fuente_pequena.render(
                        str(8 - fila), True, color_texto_coord
                    )
                    # Margen de 4px desde el borde superior e izquierdo
                    self.pantalla.blit(txt_num, (x + 4, y + 2))

                # --- LETRAS (Eje Horizontal) ---
                if fila == 7:
                    letras = "abcdefgh"
                    txt_letra = self.fuente_pequena.render(
                        letras[col], True, color_texto_coord
                    )
                    # Ajuste: Subimos el texto usando el alto real de la fuente
                    # 'y + tam_cuadro' es el borde inferior. Restamos el alto del texto y un margen.
                    pos_y_letras = y + self.tam_cuadro - txt_letra.get_height() - 2
                    pos_x_letras = x + self.tam_cuadro - txt_letra.get_width() - 4
                    self.pantalla.blit(txt_letra, (pos_x_letras, pos_y_letras))

                # Efecto Biselado (Textura)
                pygame.draw.line(
                    self.pantalla, (255, 255, 255, 30), (x, y), (x + self.tam_cuadro, y)
                )
                pygame.draw.line(
                    self.pantalla, (255, 255, 255, 30), (x, y), (x, y + self.tam_cuadro)
                )
                pygame.draw.line(
                    self.pantalla,
                    (0, 0, 0, 20),
                    (x, y + self.tam_cuadro - 1),
                    (x + self.tam_cuadro, y + self.tam_cuadro - 1),
                )
                pygame.draw.line(
                    self.pantalla,
                    (0, 0, 0, 20),
                    (x + self.tam_cuadro - 1, y),
                    (x + self.tam_cuadro - 1, y + self.tam_cuadro),
                )

    def dibujar_panel_lateral(
        self, historial, cap_b, cap_n, t_b, t_n, turno, color_flecha
    ):
        x_panel = self.ancho_tablero + 20
        ancho_cont = self.ancho_panel - 40

        # Tarjeta Jugador Negro (Arriba)
        self.dibujar_tarjeta_jugador(
            "Oponente (Negras)", t_n, x_panel, 20, turno == "negro", cap_n
        )

        # Indicador de color de flecha
        y_flecha = 135
        txt_flecha = self.fuente_pequena.render(
            "COLOR DE FLECHA:", True, self.COLOR_TEXTO_SECUNDARIO
        )
        self.pantalla.blit(txt_flecha, (x_panel, y_flecha))
        pygame.draw.circle(
            self.pantalla,
            color_flecha,
            (x_panel + txt_flecha.get_width() + 15, y_flecha + 8),
            8,
        )

        # Sección Historial
        y_hist = 165
        alto_hist = self.alto_total - 320  # Ajustado para dejar espacio abajo
        rect_hist = pygame.Rect(x_panel, y_hist, ancho_cont, alto_hist)
        pygame.draw.rect(
            self.pantalla, self.COLOR_PANEL_MOVIMIENTOS, rect_hist, border_radius=8
        )
        self.dibujar_texto_historial(historial, rect_hist)

        # Tarjeta Jugador Blanco (Abajo)
        self.dibujar_tarjeta_jugador(
            "Tú (Blancas)",
            t_b,
            x_panel,
            self.alto_total - 100,
            turno == "blanco",
            cap_b,
        )

    def dibujar_tarjeta_jugador(self, nombre, tiempo, x, y, es_turno, capturadas):
        ancho = self.ancho_panel - 40
        rect_tarjeta = pygame.Rect(x, y, ancho, 75)
        color_bg = (55, 53, 50) if es_turno else (40, 38, 35)

        pygame.draw.rect(self.pantalla, color_bg, rect_tarjeta, border_radius=10)
        if es_turno:
            pygame.draw.rect(
                self.pantalla, self.COLOR_ACENTO, rect_tarjeta, 2, border_radius=10
            )

        txt_nom = self.fuente_jugador.render(nombre, True, self.COLOR_TEXTO)
        self.pantalla.blit(txt_nom, (x + 10, y + 10))

        # Reloj Dinámico con parpadeo crítico
        minutos, segundos = int(max(0, tiempo) // 60), int(max(0, tiempo) % 60)
        color_reloj = self.COLOR_TEXTO
        if tiempo < 60 and es_turno:
            oscilacion = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
            color_reloj = (
                int(
                    self.COLOR_RELOJ_CRITICO[0]
                    + (255 - self.COLOR_RELOJ_CRITICO[0]) * oscilacion
                ),
                int(self.COLOR_RELOJ_CRITICO[1] * (1 - oscilacion)),
                int(self.COLOR_RELOJ_CRITICO[2] * (1 - oscilacion)),
            )

        txt_tiempo = self.fuente_digital.render(
            f"{minutos:02d}:{segundos:02d}", True, color_reloj
        )
        self.pantalla.blit(
            txt_tiempo, (x + ancho - txt_tiempo.get_width() - 10, y + 10)
        )

        # Capturadas dentro de la tarjeta
        self.dibujar_capturadas(capturadas, x + 10, y + 40)

    def dibujar_capturadas(self, lista, x, y):
        conteo = {}
        imagenes_referencia = {}
        for pieza in lista:
            nombre = pieza.nombre.lower()
            conteo[nombre] = conteo.get(nombre, 0) + 1
            imagenes_referencia[nombre] = pieza.imagen

        offset_x = 0
        orden = ["peon", "caballo", "alfil", "torre", "dama"]
        for tipo in orden:
            if tipo in conteo:
                img_original = imagenes_referencia[tipo]
                if img_original:
                    img = pygame.transform.smoothscale(img_original, (20, 20))
                    self.pantalla.blit(img, (x + offset_x, y))
                    if conteo[tipo] > 1:
                        txt_cant = self.fuente_pequena.render(
                            f"x{conteo[tipo]}", True, self.COLOR_TEXTO_SECUNDARIO
                        )
                        self.pantalla.blit(txt_cant, (x + offset_x + 20, y + 2))
                        offset_x += 40
                    else:
                        offset_x += 24

    def dibujar_texto_historial(self, historial, rect):
        area_dibujo = pygame.Rect(
            rect.x + 10, rect.y + 30, rect.width - 20, rect.height - 40
        )

        titulo = self.fuente_pequena.render(
            "HISTORIAL DE JUEGO", True, self.COLOR_TEXTO_SECUNDARIO
        )
        self.pantalla.blit(titulo, (rect.x + 10, rect.y + 5))

        self.pantalla.set_clip(area_dibujo)
        filas_max = 10
        total_movs = len(historial)
        capacidad_vista = filas_max * 2
        idx_inicio = 0
        if total_movs > capacidad_vista:
            idx_inicio = ((total_movs - capacidad_vista) // 2) * 2 + (total_movs % 2)

        movimientos_visibles = historial[idx_inicio:]
        for i, mov in enumerate(movimientos_visibles):
            num_real = idx_inicio + i + 1
            txt = self.fuente_pequena.render(
                f"{num_real}. {mov}", True, self.COLOR_TEXTO
            )
            columna = 0 if i < filas_max else (area_dibujo.width // 2)
            fila_relativa = i if i < filas_max else i - filas_max
            self.pantalla.blit(
                txt, (area_dibujo.x + columna, area_dibujo.y + (fila_relativa * 18))
            )
        self.pantalla.set_clip(None)

    def dibujar_botones_control(self, mouse_pos):
        x_base = self.ancho_tablero + 20
        y_botones = self.alto_total - 145
        espaciado = 10
        ancho_btn = (self.ancho_panel - 40 - espaciado) // 2

        self.rect_deshacer.update(x_base, y_botones, ancho_btn, 35)
        self.rect_abandonar.update(
            x_base + ancho_btn + espaciado, y_botones, ancho_btn, 35
        )

        fuente_txt = pygame.font.SysFont("Segoe UI", 11, bold=True)

        # --- BOTÓN DESHACER ---
        col_des = (
            (70, 68, 66) if self.rect_deshacer.collidepoint(mouse_pos) else (50, 48, 46)
        )
        pygame.draw.rect(self.pantalla, col_des, self.rect_deshacer, border_radius=6)
        pygame.draw.rect(
            self.pantalla, (90, 88, 86), self.rect_deshacer, 1, border_radius=6
        )

        # Icono ↶ y Texto
        ico_des = self.fuente_emoji.render("↶", True, (200, 200, 200))
        txt_des = fuente_txt.render("DESHACER", True, (200, 200, 200))

        # Centrado combinado
        w_total = ico_des.get_width() + 5 + txt_des.get_width()
        start_x = self.rect_deshacer.centerx - w_total // 2
        self.pantalla.blit(ico_des, (start_x, self.rect_deshacer.centery - 10))
        self.pantalla.blit(
            txt_des, (start_x + ico_des.get_width() + 5, self.rect_deshacer.centery - 7)
        )

        # --- BOTÓN ABANDONAR ---
        col_ab = (
            (180, 60, 60)
            if self.rect_abandonar.collidepoint(mouse_pos)
            else (150, 45, 45)
        )
        pygame.draw.rect(self.pantalla, col_ab, self.rect_abandonar, border_radius=6)

        # Icono 🏳 y Texto
        ico_ab = self.fuente_emoji.render(
            "✕", True, (255, 255, 255)
        )  # Símbolo de cerrar/cancelar
        txt_ab = fuente_txt.render("ABANDONAR", True, (255, 255, 255))

        # Centrado combinado
        w_total_ab = ico_ab.get_width() + 5 + txt_ab.get_width()
        start_x_ab = self.rect_abandonar.centerx - w_total_ab // 2
        self.pantalla.blit(ico_ab, (start_x_ab, self.rect_abandonar.centery - 10))
        self.pantalla.blit(
            txt_ab,
            (start_x_ab + ico_ab.get_width() + 5, self.rect_abandonar.centery - 7),
        )

    def dibujar_puntos_legales(self, movimientos, piezas, seleccionada):
        for f, c in movimientos:
            s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
            centro = self.tam_cuadro // 2
            pieza_en_destino = next(
                (p for p in piezas if p.fila == f and p.col == c), None
            )

            if (
                seleccionada
                and seleccionada.nombre.lower() == "rey"
                and abs(c - seleccionada.col) == 2
            ):
                pygame.draw.circle(s, (0, 150, 255, 180), (centro, centro), 15)
                pygame.draw.circle(s, (255, 255, 255, 200), (centro, centro), 16, 2)
            elif pieza_en_destino:
                pygame.draw.circle(
                    s, (255, 0, 0, 180), (centro, centro), (self.tam_cuadro // 2) - 5, 6
                )
            else:
                pygame.draw.circle(s, (0, 0, 0, 50), (centro, centro), 12)

            self.pantalla.blit(s, (c * self.tam_cuadro, f * self.tam_cuadro))

    def dibujar_brillo_jaque(self, rey):
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        s.fill(self.COLOR_ROJO_JAQUE)
        self.pantalla.blit(s, (rey.col * self.tam_cuadro, rey.fila * self.tam_cuadro))

    def resaltar_ultimo_movimiento(self, mov):
        s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
        s.fill(self.COLOR_ULTIMO_MOV)
        self.pantalla.blit(s, (mov[1] * self.tam_cuadro, mov[0] * self.tam_cuadro))
        self.pantalla.blit(s, (mov[3] * self.tam_cuadro, mov[2] * self.tam_cuadro))

    def dibujar_ventana_promocion(self, color, imagenes_piezas):
        centro_x, centro_y = self.ancho_tablero // 2 - 150, self.alto_total // 2 - 50
        rect_fondo = pygame.Rect(centro_x, centro_y, 300, 100)
        pygame.draw.rect(self.pantalla, (45, 45, 45), rect_fondo, border_radius=10)
        pygame.draw.rect(
            self.pantalla, self.COLOR_ACENTO, rect_fondo, 2, border_radius=10
        )

        opciones = ["dama", "torre", "alfil", "caballo"]
        color_fix = "blanco" if color in ["blanco", "blanca"] else "negro"
        rects = []

        for i, tipo in enumerate(opciones):
            r = pygame.Rect(centro_x + 20 + (i * 70), centro_y + 20, 60, 60)
            hover = r.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(
                self.pantalla,
                (75, 75, 75) if hover else (60, 60, 60),
                r,
                border_radius=5,
            )
            clave = f"{tipo}_{color_fix}"
            if clave in imagenes_piezas:
                img = pygame.transform.smoothscale(imagenes_piezas[clave], (50, 50))
                self.pantalla.blit(img, (r.x + 5, r.y + 5))
            rects.append((r, tipo))
        return rects

    def dibujar_circulos(self, circulos):
        for fila, col, color in circulos:  # Ahora recibimos 3 valores
            # Creamos la superficie transparente
            s = pygame.Surface((self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA)
            centro = self.tam_cuadro // 2
            radio = (self.tam_cuadro // 2) - 5

            # Usamos el color guardado en el círculo
            # El color ya viene con transparencia de tu diccionario de colores
            pygame.draw.circle(s, color, (centro, centro), radio, 6)

            self.pantalla.blit(s, (col * self.tam_cuadro, fila * self.tam_cuadro))
