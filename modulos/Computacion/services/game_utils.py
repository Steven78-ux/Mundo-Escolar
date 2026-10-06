"""Servicios del módulo services."""

import pygame
import time
import unicodedata
import random

from modulos.Computacion.config.rutas import ruta_fuente_mundo_escolar
from modulos.Computacion.domain.base_module import BaseModule
from modulos.Computacion.domain.texts import LIBROS_MECANOGRAFIA
from modulos.Computacion.views.ui_components import Boton
from .logic_utils import VisualFeedbackManager, ComboManager, ResultadoMecanografia


class TypingModule(BaseModule):
    TITULO = "Mecanografía Progresiva"
    COLOR_FONDO = (10, 15, 30)
    COLOR_ACTUAL = (0, 255, 255)

    def __init__(
        self, libro_id: str = "el_principito", capitulo_inicial: int = 1
    ) -> None:
        # -------------------------------------------------------------
        # INICIALIZACIÓN DE DATOS Y ESTADO
        # -------------------------------------------------------------
        self.libro = LIBROS_MECANOGRAFIA[libro_id]
        self.capitulos = self.libro.capitulos
        self.indice_capitulo = 0
        for idx, cap in enumerate(self.capitulos):
            if cap.numero == capitulo_inicial:
                self.indice_capitulo = idx
                break

        self.indice_fragmento = 0
        self.texto_objetivo = self.capitulos[self.indice_capitulo].fragmentos[0]

        self._layout_texto = []
        self._cache_glifos = {}

        self.posicion_actual = 0

        self.feedback = VisualFeedbackManager()
        self.stats_manager = ComboManager()
        self.errores_locales = 0
        self.en_error = False
        self.inicio_tiempo = None
        self.resultado_final = None
        self.es_fin_capitulo = False
        self.exit_reason = None

        self.puntos_cap = 0
        self.tiempo_cap = 0.0
        self.errores_cap = 0
        self.total_fragmentos = sum(len(cap.fragmentos) for cap in self.capitulos)

        pygame.init()
        info = pygame.display.Info()
        self.ancho, self.alto = info.current_w, info.current_h
        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto), pygame.FULLSCREEN | pygame.NOFRAME
        )
        # -------------------------------------------------------------
        # RECURSOS VISUALES (FUENTES Y RECTÁNGULOS)
        # -------------------------------------------------------------
        ruta_fuente = ruta_fuente_mundo_escolar()

        def cargar_f(t, b=False):
            fuentes_tech = ["consolas", "lucida console", "monaco", "courier new"]
            for f in fuentes_tech:
                try:
                    return pygame.font.SysFont(f, t, bold=b)
                except:
                    continue
            return pygame.font.SysFont("monospace", t, bold=b)

        self.fuente_texto = cargar_f(32, True)
        self.fuente_ui = cargar_f(26)
        self.fuente_titulo = cargar_f(48, True)
        self.fuente_terminal = pygame.font.SysFont("consolas", 20)

        self.panel_rect = pygame.Rect(40, 90, self.ancho - 80, self.alto - 140)
        self.caja_texto_rect = pygame.Rect(
            self.panel_rect.centerx - 460, self.panel_rect.y + 115, 920, 310
        )
        self.boton_volver = Boton(
            "Volver",
            pygame.Rect(15, 14, 140, 38),
            (15, 25, 45),
            (180, 20, 40),
            (0, 255, 255),
            (0, 200, 255),
            5,
        )
        self.tarjeta_rect = pygame.Rect(
            self.panel_rect.centerx - 300, self.panel_rect.centery - 200, 600, 420
        )

        self.btn_siguiente = Boton(
            "Continuar",
            pygame.Rect(
                self.tarjeta_rect.centerx + 20, self.tarjeta_rect.bottom - 80, 200, 50
            ),
            (25, 135, 84),
            (35, 165, 95),
        )
        self.btn_volver_res = Boton(
            "Volver",
            pygame.Rect(
                self.tarjeta_rect.centerx - 220, self.tarjeta_rect.bottom - 80, 200, 50
            ),
            (220, 53, 69),
            (200, 35, 51),
        )
        self.reloj = pygame.time.Clock()
        self.fondo_lab = self._crear_fondo_estetico()
        self._precalcular_layout()

    def _crear_fondo_estetico(self):
        surf = pygame.Surface((self.ancho, self.alto))
        surf.fill((10, 15, 30))
        piso_y = int(self.alto * 0.75)
        for i in range(15):
            y = piso_y + (i * i * 2)
            if y < self.alto:
                pygame.draw.line(surf, (0, 150, 255, 20), (0, y), (self.ancho, y), 1)
        return surf

    def _precalcular_layout(self):
        # -------------------------------------------------------------
        # CÁLCULO DINÁMICO DE POSICIONES DE TEXTO (WORD-WRAP)
        # -------------------------------------------------------------
        self._layout_texto = []
        x_orig, y_orig = self.caja_texto_rect.x + 40, self.caja_texto_rect.y + 40
        x, y = x_orig, y_orig

        for i, char in enumerate(self.texto_objetivo):
            if char != " " and (i == 0 or self.texto_objetivo[i - 1] == " "):
                fin_palabra = i
                while (
                    fin_palabra < len(self.texto_objetivo)
                    and self.texto_objetivo[fin_palabra] != " "
                ):
                    fin_palabra += 1

                palabra_ancho = self.fuente_texto.size(
                    self.texto_objetivo[i:fin_palabra]
                )[0]
                if x > x_orig and x + palabra_ancho > self.caja_texto_rect.right - 40:
                    x = x_orig
                    y += 55

            if char == " " and x == x_orig:
                continue

            self._layout_texto.append({"char": char, "pos": (x, y), "idx": i})
            x += self.fuente_texto.size(char)[0]

    def _titulo_actual(self) -> str:
        capitulo = self.capitulos[self.indice_capitulo]
        return f"MISION: {self.libro.titulo.upper()} > NIVEL {capitulo.numero} > FRAGMENTO {self.indice_fragmento + 1}"

    def _normalizar(self, c: str) -> str:
        return "".join(
            x
            for x in unicodedata.normalize("NFD", c.lower())
            if unicodedata.category(x) != "Mn"
        )

    def _avanzar_fragmento(self):
        cap_act = self.capitulos[self.indice_capitulo]
        if self.indice_fragmento < len(cap_act.fragmentos) - 1:
            self.indice_fragmento += 1
        else:
            self.puntos_cap = 0
            self.tiempo_cap = 0.0
            self.errores_cap = 0

            if self.indice_capitulo < len(self.capitulos) - 1:
                self.indice_capitulo += 1
                self.indice_fragmento = 0
            else:
                self.exit_reason = "chapters"
                return

        self.texto_objetivo = self.capitulos[self.indice_capitulo].fragmentos[
            self.indice_fragmento
        ]
        self._precalcular_layout()
        self._reset_intento()

    def _reset_intento(self):
        self.posicion_actual = 0
        self.en_error = False
        self.inicio_tiempo = None
        self.resultado_final = None
        self.es_fin_capitulo = False
        self.errores_locales = 0
        self.stats_manager = ComboManager()

    def _retroceder(self) -> None:
        if self.resultado_final:
            return
        if self.posicion_actual > 0:
            self.posicion_actual -= 1
            self.en_error = False
            self.feedback.agregar(
                "Retroceso",
                self.ancho // 2,
                self.panel_rect.centery + 130,
                (255, 215, 0),
                self.fuente_ui,
            )

    def _procesar_tecla(self, unicode_char: str) -> None:
        # -------------------------------------------------------------
        # GESTIÓN DE ENTRADA DE TECLADO Y RACHAS
        # -------------------------------------------------------------
        if self.resultado_final:
            return

        if not unicode_char or len(unicode_char) != 1:
            return
        if not self.inicio_tiempo:
            self.inicio_tiempo = time.time()

        esperado = self.texto_objetivo[self.posicion_actual]
        if self.en_error:
            if self._normalizar(esperado) == self._normalizar(unicode_char):
                self.en_error = False
                p_final, combo, hito = self.stats_manager.registrar_acierto(10)
                self.feedback.agregar(
                    f"+{p_final}",
                    self.ancho // 2,
                    self.panel_rect.centery + 130,
                    (25, 135, 84),
                    self.fuente_ui,
                )
                self.posicion_actual += 1
            else:
                self.errores_locales += 1
        else:
            if self._normalizar(esperado) == self._normalizar(unicode_char):
                p_final, combo, hito = self.stats_manager.registrar_acierto(10)
                color = self.stats_manager.obtener_rango_recompensa()
                self.feedback.agregar(
                    f"+{p_final}",
                    self.ancho // 2,
                    self.panel_rect.centery + 130,
                    color,
                    self.fuente_ui,
                )
                if hito:
                    mensajes = {
                        5: "¡MUY BIEN!", 
                        10: "¡INCREÍBLE!", 
                        15: "¡ERES UN GENIO!", 
                        20: "¡MÁXIMA POTENCIA!",
                        30: "¡IMPARABLE!",
                        40: "¡MAESTRO!",
                        50: "¡SÚPER VELOCIDAD!",
                        75: "¡NIVEL LEYENDA!",
                        100: "¡DIOS DEL TECLADO!"
                    }
                    txt_msg = mensajes.get(combo, f"¡COMBO x{combo}!")
                    color_rnd = (random.randint(50, 255), random.randint(150, 255), random.randint(150, 255))
                    
                    self.feedback.agregar(
                        txt_msg,
                        self.ancho // 2,
                        120,
                        color_rnd,
                        self.fuente_titulo,
                        True,
                    )
                self.posicion_actual += 1
            else:
                self.errores_locales += 1
                self.en_error = True
                self.stats_manager.registrar_fallo(5)
                self.feedback.agregar(
                    "¡Ups!",
                    self.ancho // 2,
                    self.panel_rect.centery + 130,
                    (220, 53, 69),
                    self.fuente_ui,
                )

        if self.posicion_actual >= len(self.texto_objetivo):
            t_transcurrido = time.time() - self.inicio_tiempo
            self.resultado_final = ResultadoMecanografia(
                self.stats_manager.puntos_totales // 10,
                self.errores_locales,
                t_transcurrido,
            )

            self.puntos_cap += self.stats_manager.puntos_totales
            self.errores_cap += self.errores_locales
            self.tiempo_cap += t_transcurrido

            cap_act = self.capitulos[self.indice_capitulo]
            if self.indice_fragmento == len(cap_act.fragmentos) - 1:
                self.es_fin_capitulo = True

    def _dibujar(self) -> None:
        # -------------------------------------------------------------
        # RENDERIZADO DE LA CONSOLA Y TEXTO
        # -------------------------------------------------------------
        self.pantalla.blit(self.fondo_lab, (0, 0))

        pygame.draw.rect(self.pantalla, (10, 20, 40), (0, 0, self.ancho, 66))
        pygame.draw.rect(self.pantalla, (0, 255, 255), (0, 64, self.ancho, 2))

        pygame.draw.rect(
            self.pantalla, (5, 5, 20, 240), self.panel_rect, border_radius=20
        )
        pygame.draw.rect(
            self.pantalla, (0, 255, 255), self.panel_rect, 2, border_radius=20
        )

        mouse = pygame.mouse.get_pos()
        self.boton_volver.dibujar(self.pantalla, self.fuente_ui, mouse)

        txt_tit = self.fuente_titulo.render(
            "CONSOLA DE ENTRENAMIENTO", True, (0, 255, 255)
        )
        self.pantalla.blit(txt_tit, (self.ancho // 2 - txt_tit.get_width() // 2, 8))

        if not self.resultado_final:
            info_label = self._titulo_actual()
            info_surf = self.fuente_terminal.render(info_label, True, (0, 255, 255))
            
            ancho_dinamico = info_surf.get_width() + 30
            indicador_rect = pygame.Rect(self.panel_rect.x + 35, self.panel_rect.y + 20, ancho_dinamico, 40)
            
            pygame.draw.rect(self.pantalla, (15, 30, 60), indicador_rect, border_radius=10)
            pygame.draw.rect(self.pantalla, (0, 255, 255), indicador_rect, 2, border_radius=10)
            
            self.pantalla.blit(
                info_surf, (indicador_rect.x + 15, indicador_rect.y + 10)
            )

            guia = (
                "¡Fíjate en las letras azules y escribe!"
                if not self.en_error
                else "¡Corrige la letra marcada en rojo! Usa retroceso para regresar."
            )
            guia_surf = self.fuente_ui.render(guia, True, (110, 125, 140))
            self.pantalla.blit(
                guia_surf,
                (self.ancho // 2 - guia_surf.get_width() // 2, self.panel_rect.y + 72),
            )

            caja = pygame.Rect(
                self.panel_rect.centerx - 460, self.panel_rect.y + 115, 920, 310
            )
            pygame.draw.rect(self.pantalla, (0, 20, 0), caja, border_radius=20)
            pygame.draw.rect(
                self.pantalla, (0, 100, 0), caja, width=2, border_radius=20
            )

            x_orig, y_orig = caja.x + 40, caja.y + 40
            x, y = x_orig, y_orig

            for i, char in enumerate(self.texto_objetivo):
                if char != " " and (i == 0 or self.texto_objetivo[i - 1] == " "):
                    fin_palabra = i
                    while (
                        fin_palabra < len(self.texto_objetivo)
                        and self.texto_objetivo[fin_palabra] != " "
                    ):
                        fin_palabra += 1

                    palabra_ancho = self.fuente_texto.size(
                        self.texto_objetivo[i:fin_palabra]
                    )[0]
                    if x > x_orig and x + palabra_ancho > caja.right - 40:
                        x = x_orig
                        y += 55

                if char == " " and x == x_orig:
                    continue

                color = (140, 150, 165)
                if i < self.posicion_actual:
                    color = (57, 255, 20) 
                elif i == self.posicion_actual:
                    color = (220, 53, 69) if self.en_error else (0, 255, 255)

                surf = self.fuente_texto.render(char, True, color)
                self.pantalla.blit(surf, (x, y))
                x += surf.get_width()

            self.feedback.actualizar_y_dibujar(self.pantalla)

            prog = (
                self.posicion_actual / len(self.texto_objetivo)
                if self.texto_objetivo
                else 0
            )
            bar_rect = pygame.Rect(
                self.panel_rect.x + 100,
                self.panel_rect.bottom - 110,
                self.panel_rect.width - 200,
                16,
            )
            pygame.draw.rect(self.pantalla, (30, 45, 60), bar_rect, border_radius=8)
            pygame.draw.rect(
                self.pantalla,
                self.COLOR_ACTUAL,
                (bar_rect.x, bar_rect.y, bar_rect.width * prog, bar_rect.height),
                border_radius=8,
            )

            txt = f"PUNTOS: {self.stats_manager.puntos_totales}    |    RACHA: x{self.stats_manager.combo}"
            st_surf = self.fuente_ui.render(txt, True, (0, 255, 255))
            self.pantalla.blit(
                st_surf,
                (
                    self.ancho // 2 - st_surf.get_width() // 2,
                    self.panel_rect.bottom - 80,
                ),
            )
        else:
            self._dibujar_resultado(mouse)

        pygame.display.flip()

    def _dibujar_resultado(self, mouse_pos):
        pygame.draw.rect(
            self.pantalla, (5, 5, 15, 245), self.tarjeta_rect, border_radius=24
        )
        borde_col = (0, 255, 255) if self.es_fin_capitulo else (0, 200, 255)
        pygame.draw.rect(
            self.pantalla, borde_col, self.tarjeta_rect, width=3, border_radius=24
        )

        nota = self.resultado_final.nota
        if nota == 100:
            estimulo = "SISTEMA OPTIMIZADO AL 100% "
        elif nota >= 90:
            estimulo = "PROCESAMIENTO DE ALTA VELOCIDAD "
        elif nota >= 80:
            estimulo = "ANÁLISIS DE DATOS EXITOSO "
        else:
            estimulo = "RE-CALIBRANDO SISTEMAS... "

        titulo = (
            "¡MISIÓN COMPLETADA!" if self.es_fin_capitulo else "¡BLOQUE FINALIZADO!"
        )

        puntos_viz = (
            self.puntos_cap
            if self.es_fin_capitulo
            else self.stats_manager.puntos_totales
        )
        tiempo_viz = int(
            self.tiempo_cap if self.es_fin_capitulo else self.resultado_final.segundos
        )

        lineas = [
            (titulo, self.fuente_titulo, borde_col),
            (estimulo, self.fuente_ui, (200, 230, 255)), 
            (f"Puntaje Obtenido: {puntos_viz}", self.fuente_ui, (0, 255, 255)), 
            (
                f"Tiempo Total: {tiempo_viz} segundos",
                self.fuente_ui,
                (0, 255, 255),
            ),
            (f"Precisión Final: {nota}%", self.fuente_ui, (57, 255, 20)),  # Verde Neón
        ]

        for i, (txt, f, col) in enumerate(lineas):
            surf = f.render(txt, True, col)
            self.pantalla.blit(
                surf,
                (
                    self.ancho // 2 - surf.get_width() // 2,
                    self.tarjeta_rect.y + 45 + i * 60,
                ),
            )

        self.btn_volver_res.dibujar(self.pantalla, self.fuente_ui, mouse_pos)
        self.btn_siguiente.dibujar(self.pantalla, self.fuente_ui, mouse_pos)

    def run(self) -> str | None:
        # -------------------------------------------------------------
        # BUCLE PRINCIPAL DEL JUEGO (PYGAME)
        # -------------------------------------------------------------
        try:
            while True:
                if self.exit_reason:
                    return self.exit_reason
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        return None
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_BACKSPACE:
                            self._retroceder()
                        else:
                            self._procesar_tecla(e.unicode)
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if self.boton_volver.contiene(e.pos):
                            return "chapters"
                        if self.resultado_final:
                            if self.btn_volver_res.contiene(e.pos):
                                self.exit_reason = "chapters"
                            if self.btn_siguiente.contiene(e.pos):
                                self._avanzar_fragmento()
                self._dibujar()
                self.reloj.tick(60)
        finally:
            pygame.quit() # Garantiza liberar el lock de video al cerrar