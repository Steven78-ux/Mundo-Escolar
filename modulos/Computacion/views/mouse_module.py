"""Vistas del módulo views."""

import math
import os
import random
import time

import pygame

from modulos.Computacion.config.rutas import ruta_fuente_mundo_escolar
from modulos.Computacion.domain.base_module import BaseModule
from modulos.Computacion.services.logic_utils import ComboManager, VisualFeedbackManager
from modulos.Computacion.views.ui_components import Boton


class MouseModule(BaseModule):
    def __init__(self) -> None:
        pygame.init()
        info = pygame.display.Info()
        self.ancho = info.current_w
        self.alto = info.current_h
        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto), pygame.FULLSCREEN | pygame.NOFRAME
        )
        self.reloj = pygame.time.Clock()

        self.area_rect = pygame.Rect(0, 0, 0, 0)

        def cargar_fuente(tam, negrita=False):
            # Priorizamos fuentes tipo terminal para la temática de computación
            fuentes_tech = [
                "consolas",
                "lucida console",
                "monaco",
                "courier new",
                "monospace",
            ]
            for f in fuentes_tech:
                try:
                    fuente = pygame.font.SysFont(f, tam, bold=negrita)
                    if fuente:
                        return fuente
                except:
                    continue
            return pygame.font.SysFont("monospace", tam, bold=negrita)

        self.fuente_titulo = cargar_fuente(48, True)
        self.fuente_texto = cargar_fuente(34, True)
        self.fuente_ui = cargar_fuente(26)
        self.fuente_control = cargar_fuente(20)
        self.fuente_combo = cargar_fuente(80, True)
        self.fuente_puntaje = cargar_fuente(64, True)

        # Cargar imagen de tiempo desde assets
        ruta_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        path_tiempo = os.path.join(ruta_assets, "tiempo.png")
        self.img_tiempo = None
        if os.path.exists(path_tiempo):
            try:
                self.img_tiempo = pygame.image.load(path_tiempo).convert_alpha()
                self.img_tiempo = pygame.transform.scale(self.img_tiempo, (30, 30))
            except:
                self.img_tiempo = None

        self.dificultad = 5
        self.area_tam = self._calcular_area(self.dificultad)
        self.circulos = []

        self.fallos_totales = 0
        self.fallos_consecutivos = 0
        self.max_fallos_totales = 40
        self.max_fallos_consecutivos = 8
        self.mensaje_derrota = ""
        self.estado = "menu"

        self.feedback = VisualFeedbackManager()
        self.stats = ComboManager()

        self.boton_reiniciar = Boton(
            texto="Reiniciar",
            rect=pygame.Rect(170, 14, 150, 38),
            color_normal=(25, 135, 84),
            color_hover=(21, 115, 71),
        )
        self.boton_salir = Boton(
            texto="Volver",
            rect=pygame.Rect(15, 14, 140, 38),
            color_normal=(220, 53, 69),
            color_hover=(200, 35, 51),
            color_texto=(255, 255, 255),
        )
        self.fondo_suave = self._crear_fondo_suave()
        self._crear_textos_estaticos()

    def _crear_fondo_suave(self):
        superficie = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)

        # 1. Degradado de fondo (Azul profundo estilo laboratorio digital)
        for i in range(self.alto):
            # De azul oscuro a negro azulado
            r = int(5 + (15 - 5) * i / self.alto)
            g = int(10 + (25 - 10) * i / self.alto)
            b = int(25 + (45 - 25) * i / self.alto)
            pygame.draw.line(superficie, (r, g, b), (0, i), (self.ancho, i))

        # 2. Rejilla de perspectiva (Piso de laboratorio)
        piso_y = int(self.alto * 0.75)
        color_grid = (0, 150, 255, 35)

        # Líneas horizontales con perspectiva (se juntan hacia el horizonte)
        for i in range(12):
            y = piso_y + (i * i * 3)
            if y < self.alto:
                pygame.draw.line(superficie, color_grid, (0, y), (self.ancho, y), 1)

        # Líneas verticales que convergen en un punto de fuga central
        centro_x = self.ancho // 2
        for x in range(-self.ancho, self.ancho * 2, 160):
            pygame.draw.line(
                superficie, color_grid, (centro_x, piso_y - 80), (x, self.alto), 2
            )

        # 3. Ventanas de explorador sutiles (Decorativas) - HEREDADO DE MENU
        ventanas_rects = []
        intentos = 0
        while len(ventanas_rects) < 8 and intentos < 100:
            intentos += 1
            w_vent = random.randint(180, 350)
            h_vent = random.randint(120, 250)
            x_vent = random.randint(50, self.ancho - w_vent - 50)
            y_vent = random.randint(50, self.alto - h_vent - 70)
            nuevo_rect = pygame.Rect(x_vent, y_vent, w_vent, h_vent)
            if any(nuevo_rect.colliderect(r.inflate(30, 30)) for r in ventanas_rects):
                continue
            ventanas_rects.append(nuevo_rect)
            surf_vent = pygame.Surface((w_vent, h_vent), pygame.SRCALPHA)
            pygame.draw.rect(
                surf_vent, (0, 150, 255, 10), (0, 0, w_vent, h_vent), border_radius=10
            )
            pygame.draw.rect(
                surf_vent,
                (0, 200, 255, 25),
                (0, 0, w_vent, h_vent),
                1,
                border_radius=10,
            )
            pygame.draw.rect(
                surf_vent,
                (0, 120, 255, 30),
                (0, 0, w_vent, 22),
                border_top_left_radius=10,
                border_top_right_radius=10,
            )
            for i in range(3):
                pygame.draw.circle(surf_vent, (255, 255, 255, 30), (12 + i * 14, 11), 3)
            superficie.blit(surf_vent, (x_vent, y_vent))

        # 4. Elementos de datos y circuitos (Bits hasta abajo)
        color_tech = (0, 200, 255, 15)
        # Bits aleatorios (0 y 1)
        for _ in range(100):
            bx = random.randint(0, self.ancho)
            by = random.randint(0, self.alto)
            char = random.choice(["0", "1"])
            surf_bit = self.fuente_ui.render(char, True, color_tech)
            superficie.blit(surf_bit, (bx, by))

        return superficie

    def _crear_textos_estaticos(self):
        self.titulo_juego = self.fuente_titulo.render(
            "EJECUTANDO CALIBRACIÓN", True, (0, 255, 255)
        )
        self.instruccion_juego = self.fuente_ui.render(
            "INTERCEPTAR CÍRCULOS DE DATOS ANTES DE LA EXPIRACIÓN.",
            True,
            (150, 170, 190),
        )

    def _calcular_area(self, dificultad):
        lado = 700 + (dificultad * 30)  # Crecimiento más controlado
        max_lado_w = self.ancho - 700
        max_lado_h = self.alto - 350
        return min(lado, max_lado_w, max_lado_h)

    def _obtener_area_rect(self):
        lado = self.area_tam
        x = int(self.ancho / 2 - lado / 2)
        y = int(self.alto / 2 - lado / 2) + 70
        return pygame.Rect(x, y, lado, lado)

    def _color_for_level(self, nivel):
        if nivel <= 4:
            return (57, 255, 20)  # Verde Neón
        elif nivel <= 8:
            return (255, 215, 0)  # Amarillo Eléctrico
        elif nivel <= 12:
            return (255, 128, 0)  # Naranja
        elif nivel <= 16:
            return (255, 50, 50)  # Rojo Alerta
        else:
            return (170, 0, 255)  # Morado Máxima Dificultad

    def _color_area(self):
        return self._color_for_level(self.dificultad)

    def _obtener_dif_tiempo(self):
        if self.estado != "juego":
            return 0
        transcurrido = time.time() - self.inicio_sesion
        return min(1.0, transcurrido / 90)

    def _calcular_intervalo(self, dificultad):
        return max(0.5, 1.7 - (dificultad * 0.05))

    def _reset_juego(self):
        self.circulos = []
        self.fallos_totales = 0
        self.fallos_consecutivos = 0
        # Integridad del sistema: Ajustada para ser un poco más permisiva en niveles altos
        self.max_fallos_totales = max(25, 65 - (self.dificultad * 4))
        self.max_fallos_consecutivos = max(7, 17 - self.dificultad)
        self.stats = ComboManager()
        self.inicio_sesion = time.time()
        self.tiempo_restante = 90
        self.tiempo_ultimo_spawn = 0
        self.intervalo = self._calcular_intervalo(self.dificultad)
        self.area_tam = self._calcular_area(self.dificultad)
        self.area_rect = self._obtener_area_rect()
        self.estado = "juego"
        self.boton_reiniciar.rect.topleft = (170, 14)
        self.boton_salir.rect.topleft = (15, 14)
        self.boton_salir.texto = "Volver"

    def _spawn_objetivo(self):
        progreso_tiempo = self._obtener_dif_tiempo()

        # Nueva lógica: Azul (Izquierdo) o Verde (Derecho)
        tipo = random.choice(["azul", "verde"])
        color = (77, 163, 255) if tipo == "azul" else (46, 204, 113)

        # Tamaño del radio disminuye con dificultad
        factor_tam = max(0.07, 0.16 - self.dificultad * 0.004)
        radio = int(self.area_tam * factor_tam)

        x = random.randint(
            self.area_rect.left + radio + 10, self.area_rect.right - radio - 10
        )
        y = random.randint(
            self.area_rect.top + radio + 10, self.area_rect.bottom - radio - 10
        )

        # Velocidad de movimiento incrementada
        if self.dificultad <= 2:
            vel_mult = 0.2 + (progreso_tiempo * 0.5)
        else:
            vel_mult = 0.6 + (self.dificultad * 0.2) + (progreso_tiempo * 1.2)

        vx, vy = random.uniform(-1, 1) * vel_mult, random.uniform(-1, 1) * vel_mult

        self.circulos.append(
            {
                "x": x,
                "y": y,
                "r": radio,
                "tipo": tipo,
                "clicks": 1,
                "max_clicks": 1,
                "color": color,
                "vx": vx,
                "vy": vy,
                "creacion": time.time(),
                "duracion": (
                    max(0.8, 4.5 - (self.dificultad * 0.15))
                ),
            }
        )

    def _procesar_click_juego(self, mx, my, boton):
        if self.estado != "juego":
            return
        hit = False
        for c in self.circulos[:]:
            dist = math.hypot(mx - c["x"], my - c["y"])
            if dist <= c["r"]:
                # Verificar si el botón es correcto para el color
                # 1: Izquierdo (Azul), 3: Derecho (Verde)
                if (c["tipo"] == "azul" and boton == 1) or (c["tipo"] == "verde" and boton == 3):
                    hit = True
                    c["clicks"] -= 1
                    self.fallos_consecutivos = 0

                    puntos_base = 15
                    p_final, combo, hito = self.stats.registrar_acierto(puntos_base)
                    color_feedback = self.stats.obtener_rango_recompensa()

                    self.feedback.agregar(
                        f"+{p_final}", mx, my, color_feedback, self.fuente_ui
                    )
                    if hito:
                        # Sistema de Mensajes de Emoción por Combos (Igual a mecanografía)
                        mensajes = {
                            5: "¡MUY BIEN!", 
                            10: "¡INCREÍBLE!", 
                            15: "¡ERES UN GENIO!", 
                            20: "¡MÁXIMA POTENCIA!",
                            30: "¡IMPARABLE!",
                            40: "¡MAESTRO!",
                            50: "¡SÚPER VELOCIDAD!",
                            75: "¡NIVEL LEYENDA!",
                            100: "¡DIOS DEL MOUSE!"
                        }
                        txt_msg = mensajes.get(combo, f"¡COMBO x{combo}!")
                        color_rnd = (random.randint(50, 255), random.randint(150, 255), random.randint(150, 255))

                        self.feedback.agregar(
                            txt_msg,
                            self.ancho // 2,
                            self.alto // 2,
                            color_rnd,
                            self.fuente_titulo,
                            True,
                        )

                    if c["clicks"] <= 0:
                        self.circulos.remove(c)
                else:
                    # Clic con botón equivocado cuenta como fallo
                    hit = False # Forzar fallo
                break

        if not hit and self.area_rect.collidepoint(mx, my):
            penalizacion = self.stats.registrar_fallo(10)
            self.fallos_totales += 1
            self.fallos_consecutivos += 1
            self.feedback.agregar(
                f"-{penalizacion}", mx, my, (255, 0, 0), self.fuente_ui
            )

            if (
                self.fallos_totales >= self.max_fallos_totales
                or self.fallos_consecutivos >= self.max_fallos_consecutivos
            ):
                self.mensaje_derrota = (
                    "¡Exceso de fallos!"
                    if self.fallos_totales >= self.max_fallos_totales
                    else "¡Racha de errores crítica!"
                )
                self.estado = "perdido"

    def _dibujar_perdido(self):
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.pantalla.blit(overlay, (0, 0))

        msg = self.fuente_titulo.render("¡INTÉNTALO DE NUEVO!", True, (255, 60, 60))
        sub = self.fuente_texto.render(
            f"Puntaje: {self.stats.puntos_totales}", True, (0, 255, 255)
        )
        txt = self.fuente_ui.render(
            getattr(self, "mensaje_derrota", "El sistema ha colapsado."),
            True,
            (200, 200, 200),
        )

        self.pantalla.blit(
            msg, (self.ancho // 2 - msg.get_width() // 2, self.alto // 2 - 140)
        )
        self.pantalla.blit(
            sub, (self.ancho // 2 - sub.get_width() // 2, self.alto // 2 - 60)
        )
        self.pantalla.blit(
            txt, (self.ancho // 2 - txt.get_width() // 2, self.alto // 2 - 10)
        )

        self.boton_reiniciar.rect.center = (self.ancho // 2 - 110, self.alto // 2 + 100)
        self.boton_salir.rect.center = (self.ancho // 2 + 110, self.alto // 2 + 100)
        self.boton_salir.texto = "Volver"

        mouse = pygame.mouse.get_pos()
        self.boton_reiniciar.dibujar(self.pantalla, self.fuente_ui, mouse)
        self.boton_salir.dibujar(self.pantalla, self.fuente_ui, mouse)

    def _dibujar_finalizado(self):
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.pantalla.blit(overlay, (0, 0))

        msg = self.fuente_titulo.render("¡CALIBRACIÓN EXITOSA!", True, (57, 255, 20))
        sub = self.fuente_texto.render(
            f"Puntaje Total: {self.stats.puntos_totales}", True, (0, 255, 255)
        )
        detalles = f"Errores Totales: {self.fallos_totales} | Combo Máximo: {self.stats.max_combo}"
        txt = self.fuente_ui.render(detalles, True, (200, 200, 200))

        self.pantalla.blit(
            msg, (self.ancho // 2 - msg.get_width() // 2, self.alto // 2 - 140)
        )
        self.pantalla.blit(
            sub, (self.ancho // 2 - sub.get_width() // 2, self.alto // 2 - 60)
        )
        self.pantalla.blit(
            txt, (self.ancho // 2 - txt.get_width() // 2, self.alto // 2 - 10)
        )

        self.boton_reiniciar.rect.center = (self.ancho // 2 - 110, self.alto // 2 + 100)
        self.boton_salir.rect.center = (self.ancho // 2 + 110, self.alto // 2 + 100)
        self.boton_salir.texto = "Volver"

        mouse = pygame.mouse.get_pos()
        self.boton_reiniciar.dibujar(self.pantalla, self.fuente_ui, mouse)
        self.boton_salir.dibujar(self.pantalla, self.fuente_ui, mouse)

    def run(self) -> str:
        en_ejecucion = True
        retorno = "salir"
        try:
            while en_ejecucion:  # Bucle optimizado
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        retorno = "salir"
                        en_ejecucion = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = evento.pos
                        if self.boton_reiniciar.contiene((mx, my)) and evento.button == 1:
                            self._reset_juego()
                        elif self.boton_salir.contiene((mx, my)) and evento.button == 1:
                            retorno = "volver"
                            en_ejecucion = False
                        elif self.estado == "juego":
                            self._procesar_click_juego(mx, my, evento.button)

                if self.estado == "juego":  # Actualización de física
                    self.tiempo_restante = max(
                        0, 90 - int(time.time() - self.inicio_sesion)
                    )
                    if self.tiempo_restante <= 0:
                        self.estado = "finalizado"

                    if time.time() - self.tiempo_ultimo_spawn > self.intervalo:
                        self._spawn_objetivo()
                        self.tiempo_ultimo_spawn = time.time()

                    for c in self.circulos[:]:
                        c["x"] += c["vx"]
                        c["y"] += c["vy"]
                        if (
                            c["x"] - c["r"] < self.area_rect.left
                            or c["x"] + c["r"] > self.area_rect.right
                        ):
                            c["vx"] *= -1
                        if (
                            c["y"] - c["r"] < self.area_rect.top
                            or c["y"] + c["r"] > self.area_rect.bottom
                        ):
                            c["vy"] *= -1

                        if time.time() - c["creacion"] > c["duracion"]:
                            self.circulos.remove(c)
                            self.fallos_totales += 1
                            self.fallos_consecutivos += 1
                            if (
                                self.fallos_totales >= self.max_fallos_totales
                                or self.fallos_consecutivos
                                >= self.max_fallos_consecutivos
                            ):
                                self.mensaje_derrota = (
                                    "Se escaparon demasiados objetivos"
                                )
                                self.estado = "perdido"

                self.pantalla.fill((10, 15, 30))  # Fondo base oscuro
                self.pantalla.blit(self.fondo_suave, (0, 0))

                if self.estado == "juego":
                    self._dibujar_juego()
                elif self.estado == "perdido":
                    self._dibujar_perdido()
                elif self.estado == "finalizado":
                    self._dibujar_finalizado()
                pygame.display.flip()
                self.reloj.tick(60)
        finally:
            pygame.quit()
        return retorno

    def _dibujar_juego(self):
        area_rect = self._obtener_area_rect()

        # --- CONTENEDOR DE VENTANA DE PROTOCOLO ---
        # Creamos una ventana que englobe todo (stats + zona de juego)
        ancho_ventana = area_rect.width + 650
        alto_ventana = area_rect.height + 210
        rect_ventana = pygame.Rect(0, 0, ancho_ventana, alto_ventana)
        rect_ventana.centerx = self.ancho // 2
        rect_ventana.y = 85  # Fijar posición para no chocar con botones superiores

        # Sombra/Resplandor exterior
        for i in range(5):
            pygame.draw.rect(
                self.pantalla,
                (0, 255, 255, 10),
                rect_ventana.inflate(i * 8, i * 8),
                border_radius=25,
            )

        # Fondo de la Ventana
        pygame.draw.rect(self.pantalla, (5, 5, 20, 245), rect_ventana, border_radius=20)
        pygame.draw.rect(
            self.pantalla, (0, 255, 255), rect_ventana, 2, border_radius=20
        )

        # Barra de Título (Estilo Windows/Consola)
        pygame.draw.rect(
            self.pantalla,
            (15, 30, 75),
            (rect_ventana.x, rect_ventana.y, rect_ventana.width, 45),
            border_top_left_radius=20,
            border_top_right_radius=20,
        )
        # Botones decorativos de ventana
        for i, col in enumerate([(255, 80, 80), (255, 200, 0), (80, 255, 80)]):
            pygame.draw.circle(
                self.pantalla,
                col,
                (rect_ventana.x + 25 + i * 25, rect_ventana.y + 22),
                8,
            )

        tit_v = self.fuente_ui.render(
            "SYS_PROTOCOL: PRECISION_CALIBRATION_ACTIVE", True, (0, 255, 255)
        )
        self.pantalla.blit(
            tit_v, (rect_ventana.centerx - tit_v.get_width() // 2, rect_ventana.y + 12)
        )
        # ------------------------------------------

        # 1. Área de Juego (Caja Principal)
        pygame.draw.rect(self.pantalla, (0, 20, 40, 100), area_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, (5, 5, 10), area_rect, border_radius=20)
        pygame.draw.rect(
            self.pantalla, self._color_area(), area_rect, width=4, border_radius=20
        )

        # --- SISTEMA DE MONITOREO DE ERRORES (BARRAS LATERALES) ---

        # 2. Barra de Integridad (Izquierda) - Salud total del sistema
        integ_rect = pygame.Rect(
            area_rect.left - 55, area_rect.top, 35, area_rect.height
        )
        pygame.draw.rect(
            self.pantalla, (30, 35, 45), integ_rect, border_radius=12
        )  # Fondo

        pct_integ = max(0.0, 1.0 - (self.fallos_totales / self.max_fallos_totales))
        h_integ = int((integ_rect.height - 8) * pct_integ)
        color_integ = (50, 215, 100) if pct_integ > 0.4 else (215, 180, 40)
        if pct_integ < 0.2:
            color_integ = (220, 50, 50)  # Peligro

        if h_integ > 0:
            fill_integ = pygame.Rect(
                integ_rect.x + 4,
                integ_rect.bottom - 4 - h_integ,
                integ_rect.width - 8,
                h_integ,
            )
            pygame.draw.rect(self.pantalla, color_integ, fill_integ, border_radius=8)

        pygame.draw.rect(
            self.pantalla, (180, 190, 210), integ_rect, width=3, border_radius=12
        )  # Borde

        label_integ = self.fuente_ui.render("INTEGRIDAD", True, (255, 255, 255))
        label_integ = pygame.transform.rotate(label_integ, 90)
        self.pantalla.blit(
            label_integ,
            (integ_rect.left - 35, integ_rect.centery - label_integ.get_height() // 2),
        )

        # 3. Barra de Sobrecarga (Derecha) - Errores consecutivos
        panic_rect = pygame.Rect(
            area_rect.right + 20, area_rect.top, 35, area_rect.height
        )

        # Vibración dinámica cuando se acerca al límite de racha
        if (
            self.fallos_consecutivos >= max(1, self.max_fallos_consecutivos - 3)
            and self.fallos_consecutivos > 0
        ):
            intensidad = (
                self.fallos_consecutivos - (self.max_fallos_consecutivos - 4)
            ) * 3
            panic_rect.x += random.randint(-intensidad, intensidad)
            panic_rect.y += random.randint(-intensidad, intensidad)

        pygame.draw.rect(
            self.pantalla, (40, 30, 30), panic_rect, border_radius=12
        )  # Fondo

        pct_panic = min(1.0, self.fallos_consecutivos / self.max_fallos_consecutivos)
        h_panic = int((panic_rect.height - 8) * pct_panic)
        if h_panic > 0:
            fill_panic = pygame.Rect(
                panic_rect.x + 4,
                panic_rect.bottom - 4 - h_panic,
                panic_rect.width - 8,
                h_panic,
            )
            color_panic = (255, 100, 100) if pct_panic < 0.7 else (255, 0, 0)
            pygame.draw.rect(self.pantalla, color_panic, fill_panic, border_radius=8)

        pygame.draw.rect(
            self.pantalla, (230, 180, 180), panic_rect, width=3, border_radius=12
        )  # Borde

        label_panic = self.fuente_ui.render(
            "SOBRECARGA", True, (220, 50, 50) if pct_panic > 0.7 else (255, 255, 255)
        )
        label_panic = pygame.transform.rotate(label_panic, -90)
        self.pantalla.blit(
            label_panic,
            (panic_rect.right + 10, panic_rect.centery - label_panic.get_height() // 2),
        )

        # --- DASHBOARD SUPERIOR (PUNTAJE Y STATS) ---

        # --- DASHBOARD SUPERIOR (DISTRIBUIDO) ---

        # 1. PUNTUACIÓN (Centrada sobre zona de clics)
        score_txt = f"{self.stats.puntos_totales}"
        score_surf = self.fuente_puntaje.render(score_txt, True, (255, 255, 255))
        score_label = self.fuente_ui.render("PUNTUACIÓN", True, (0, 255, 255))

        self.pantalla.blit(
            score_label,
            (self.ancho // 2 - score_label.get_width() // 2, rect_ventana.y + 65),
        )
        self.pantalla.blit(
            score_surf,
            (self.ancho // 2 - score_surf.get_width() // 2, rect_ventana.y + 100),
        )

        # 2. TIEMPO (Izquierda, donde antes estaba el puntaje)
        txt_tiempo = f"{self.tiempo_restante}s"
        surf_tiempo = self.fuente_texto.render(txt_tiempo, True, (255, 255, 255))
        label_tiempo = self.fuente_ui.render("TIEMPO", True, (200, 230, 255))
        x_col_izq = rect_ventana.x + (area_rect.left - rect_ventana.x) // 2

        self.pantalla.blit(
            label_tiempo,
            (x_col_izq - label_tiempo.get_width() // 2, rect_ventana.y + 65),
        )

        y_vals = rect_ventana.y + 110
        if self.img_tiempo:
            w_total = self.img_tiempo.get_width() + 10 + surf_tiempo.get_width()
            x_start = x_col_izq - w_total // 2
            self.pantalla.blit(
                self.img_tiempo,
                (
                    x_start,
                    y_vals
                    - (self.img_tiempo.get_height() - surf_tiempo.get_height()) // 2,
                ),
            )
            self.pantalla.blit(
                surf_tiempo, (x_start + self.img_tiempo.get_width() + 10, y_vals)
            )
        else:
            self.pantalla.blit(
                surf_tiempo, (x_col_izq - surf_tiempo.get_width() // 2, y_vals)
            )

        # 3. COMBO (Derecha)
        txt_combo = f"x{self.stats.combo}"
        surf_combo = self.fuente_texto.render(txt_combo, True, (255, 255, 255))
        label_combo = self.fuente_ui.render("COMBO", True, (200, 230, 255))
        x_col_der = area_rect.right + (rect_ventana.right - area_rect.right) // 2

        self.pantalla.blit(
            label_combo, (x_col_der - label_combo.get_width() // 2, rect_ventana.y + 65)
        )
        self.pantalla.blit(
            surf_combo, (x_col_der - surf_combo.get_width() // 2, y_vals)
        )

        # Indicador de Daño Acumulado (Para que el 0 de 100 tenga sentido visual)
        err_txt = f"DAÑO AL SISTEMA: {self.fallos_totales}/{self.max_fallos_totales}"

        if pct_integ > 0.7:
            color_err = (57, 255, 20)
        elif pct_integ > 0.3:
            color_err = (255, 215, 0)
        else:
            color_err = (255, 50, 50)

        err_surf = self.fuente_ui.render(err_txt, True, color_err)
        self.pantalla.blit(
            err_surf,
            (self.ancho // 2 - err_surf.get_width() // 2, area_rect.bottom + 10),
        )

        # 3. Indicadores de Dashboard (Top)
        for c in self.circulos:
            # Sombra
            pygame.draw.circle(
                self.pantalla,
                (200, 200, 200),
                (int(c["x"] + 3), int(c["y"] + 3)),
                c["r"],
            )
            pygame.draw.circle(
                self.pantalla, c["color"], (int(c["x"]), int(c["y"])), c["r"]
            )
            pygame.draw.circle(
                self.pantalla, (255, 255, 255), (int(c["x"]), int(c["y"])), c["r"], 2
            )

        # Asegurar posición de botones en UI de juego
        self.boton_reiniciar.rect.topleft = (170, 14)
        self.boton_salir.rect.topleft = (15, 14)
        self.boton_salir.texto = "Volver"

        mouse = pygame.mouse.get_pos()
        self.boton_reiniciar.dibujar(self.pantalla, self.fuente_ui, mouse)
        self.boton_salir.dibujar(self.pantalla, self.fuente_ui, mouse)

        # Feedback de combos y puntos
        self.feedback.actualizar_y_dibujar(self.pantalla)

        # 4. Parpadeo de Alerta Roja (Bordes de pantalla) cuando la integridad es crítica (< 20%)
        if pct_integ < 0.2:
            alpha = int(
                (math.sin(time.time() * 12) + 1) / 2 * 100
            )  # Oscila entre 0 y 100 de opacidad
            alerta_surf = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            pygame.draw.rect(
                alerta_surf, (220, 53, 69, alpha), (0, 0, self.ancho, self.alto), 15
            )
            self.pantalla.blit(alerta_surf, (0, 0))