"""Archivo del módulo Ajedrez."""

import customtkinter as ctk
import pygame
import threading
import time
import random
from .views.ventana_juego import VentanaJuego
from .views.tablero_render import TableroRender
from .domain.tablero_logico import (
    obtener_pieza_en,
    esta_atacada,
    obtener_movimientos_legales,
)
from .views.pieza_animada import PiezaAnimada
from .views.tutorial_panel_render import TutorialPanelRender
from .views.tutorial_view_render import TutorialViewRender
from .services.audio import GestorAudio
from .domain.partida_tutorial import PartidaTutorial
from .config.tutorial_config import LESSONS
from core.util_logros import notificar_logro


class VentanaTutorial(VentanaJuego):
    def __init__(self, lesson_id, evento_cierre, tema="Oceano"):
        # -------------------------------------------------------------
        # INICIALIZACIÓN DE PYGAME Y ESCENARIO
        # -------------------------------------------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        res = (info.current_w, info.current_h)

        self.clock = pygame.time.Clock()
        self.evento_cierre = evento_cierre
        self.sid = lesson_id
        self.tema = tema
        self.sub_id = LESSONS[lesson_id]["subsecciones"][0]

        self.task_count = 0
        self.level_step = 0
        self.task_goal = 1
        self.final_time = None
        self.seccion_completada = False
        self.ia_pensando = False
        self.moves_made = 0 
        self.movimiento_ia_pendiente = None
        self.enroque_pre_condition_met = False
        self.promocion_pendiente = None
        self.resultado_accion = None
        self.circulos_tacticos = []
        self.flechas_tacticos = []
        self.reyes_en_jaque = []
        self.peon_mission_step = 0
        self.stars_earned = 0  # Para mostrar estrellas al completar subsección
        self.peon_mission_failed_2_step = False 
        self.king_moved_instead_of_blocking = False
        self.mission_failed_msg = None
        self.lesson_stats = {} 
        self.current_sub_section_start_time = (
            time.time()
        ) 
        self.rule_subsection_completed = False

        self.vista = TableroRender(self.screen, tema=self.tema, res=res)
        self.partida = PartidaTutorial(self.sid, self.sub_id, self)
        self.partida.cargar_escenario(self.sid, self.sub_id)

        PiezaAnimada._CACHE_IMAGENES.clear()
        for p in self.partida.piezas:
            p.tam_cuadro = self.vista.tam_cuadro
            p.imagen = p._cargar_imagen()

        self.right_click_start = None
        self.running = True
        self.seleccionada = None
        self.movimientos_posibles = []
        self.audio_manager = GestorAudio()

        self.tutorial_panel_render = TutorialPanelRender(
            self.screen, self.vista, LESSONS
        )
        self.gui_render = TutorialViewRender(self.screen, self.vista)

        self.nicknames = {"jugador": "REY SABIO", "oponente": "DIOS DEL AJEDREZ"}
        self.start_time = time.time()
        self.show_sub_section_success_modal = False
        self.success_modal_buttons_rects = {"siguiente": None, "reiniciar": None}
        self.sub_section_nav_buttons_rects = {}

    def run(self):
        # -------------------------------------------------------------
        # BUCLE DE RENDERIZADO DEL TUTORIAL
        # -------------------------------------------------------------
        while self.running and not self.evento_cierre.is_set():
            self.manejar_eventos()

            mouse_p = pygame.mouse.get_pos()
            self.vista.dibujar(
                self.partida,
                mouse_p,
                self.circulos_tacticos,
                self.flechas_tacticos,
                self.seleccionada,
                self.movimientos_posibles,
                self.nicknames,
                reyes_en_jaque=self.reyes_en_jaque,
                draw_panel=False,
            )

            if self.final_time is not None:
                elapsed = self.final_time
            else:
                elapsed = int(time.time() - self.start_time)
            self.tutorial_panel_render.dibujar(
                self.sid,
                self.sub_id,
                self.task_count,
                self.task_goal,
                self.peon_mission_step,
                self.stars_earned,
                self.level_step,
                elapsed,
                self.peon_mission_failed_2_step,
                mouse_p,
                self.enroque_pre_condition_met,
                self.promotions_completed,  # Pasar el estado de promociones
            )
            self.sub_section_nav_buttons_rects = (
                self.gui_render.dibujar_botones_subseccion(
                    LESSONS[self.sid]["subsecciones"], self.sub_id, mouse_p
                )
            )

            if self.promocion_pendiente:
                self.vista.dibujar_modal_promocion(self.partida.turno, mouse_p)

            if self.show_sub_section_success_modal:
                msg = self._generar_mensaje_exito()
                self.success_modal_buttons_rects = (
                    self.vista.dibujar_modal_exito_tutorial(
                        msg,
                        self.stars_earned,
                        mouse_p,
                    )
                )

            if self.seccion_completada:
                msg = "Has completado toda la sección básica."
                self.vista.dibujar_modal_seccion_completa(
                    msg, pygame.mouse.get_pos(), self.lesson_stats
                )

            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()
    
    # -------------------------------------------------------------
    # MÉTODOS DE SOPORTE Y LÓGICA
    # -------------------------------------------------------------
    def _generar_mensaje_exito(self):
        if self.mission_failed_msg:
            return self.mission_failed_msg

            if self.level_step == 0:
                return "¡FELICIDADES! Ya sabes cómo es el enroque corto"
            if self.level_step == 1:
                return "¡FELICIDADES! Ya sabes cómo es el enroque largo"
            return "¡FELICIDADES! Dominas la seguridad del Rey"

        if self.sid == "5":
            msgs = {
                "ahogado": "Felicidades ahora sabes que es el rey ahogado despues de experimentarlo",
                "tablas": "Vaya llevaste esta partida a tablas ahora conoces lo que son las tablas",
                "insuficiencia_material": "Felicidades ahora sabes lo que es la insuficiencia de material",
            }
            return msgs.get(self.sub_id, "¡Nivel completado!")

        pieza_nombre = self.sub_id.upper()
        verbo = "captura" if self.sid == "2" else "se mueve"
        articulo = "la" if self.sub_id in ["dama", "torre"] else "el"
        return f"¡FELICIDADES! Ya sabes cómo {verbo} {articulo} {pieza_nombre}"

    def cambiar_subseccion(self, subid):
        self.sub_id = subid
        self.level_step = 0 
        self.partida.cargar_escenario(self.sid, self.sub_id)
        self.verificar_final_partida()
        for p in self.partida.piezas:
            p.tam_cuadro = self.vista.tam_cuadro
            p.imagen = p._cargar_imagen()

        self.seleccionada = None
        self.movimientos_posibles = []
        self.circulos_tacticos.clear()
        self.reiniciar_contadores()  # Esto también resetea stars_earned
        if hasattr(self, "tutorial_panel_render"):
            self.tutorial_panel_render.dialog_scroll = 0
        self.rule_subsection_completed = (
            self.sid == "5"
            and self.sub_id
            in ["ahogado", "tablas", "insuficiencia_material", "clavada"]
        )
        if self.rule_subsection_completed:
            self.finalizar_subseccion()

    def reiniciar_contadores(self):
        self.task_count = 0
        self.peon_mission_step = 0
        self.stars_earned = 0
        self.moves_made = 0
        self.promotions_completed = {
            "dama": False,
            "torre": False,
            "alfil": False,
            "caballo": False,
        }
        self.enroque_pre_condition_met = False
        self.peon_mission_failed_2_step = False  # Resetear flag de fallo del peón
        self.king_moved_instead_of_blocking = False
        self.mission_failed_msg = None
        self.current_sub_section_start_time = (
            time.time()
        )  # Reiniciar tiempo para la subsección actual

    def reiniciar_subseccion(self):
        """Reinicia el estado de la subsección actual."""
        self.cambiar_subseccion(
            self.sub_id
        )  # Recarga el escenario y resetea contadores

    def finalizar_subseccion(self):
        """Maneja el éxito de una pieza y avanza a la siguiente."""
        # Calcular estrellas ganadas
        if self.sid == "1":
            # Sección de MOVIMIENTOS: 1 estrella por pieza, excepto peón (2 o 1)
            if self.sub_id == "peon":
                self.stars_earned = 1 if self.peon_mission_failed_2_step else 2
            else:
                self.stars_earned = 1
        elif self.sid == "4":
            if self.sub_id == "jaque" and 3 <= self.level_step <= 5:
                # En niveles de bloqueo, 0 estrellas si movió al rey
                self.stars_earned = 0 if self.king_moved_instead_of_blocking else 1
            else:
                # 1 estrella por cada escape o captura exitosa
                self.stars_earned = 1
        elif self.sid == "5":
            self.stars_earned = 1
        elif self.sid == "2" or (self.sid == "3" and self.sub_id == "paso"):
            if self.sub_id in ["peon", "paso"]:
                self.stars_earned = max(1, self.task_count)
            else:
                self.stars_earned = 3
        elif self.sid == "3" and self.sub_id == "promocion":
            self.stars_earned = sum(
                self.promotions_completed.values()
            )  # Estrellas = número de promociones diferentes
        else:
            self.stars_earned = 3

        # Registrar estadísticas
        elapsed_sub = int(time.time() - self.current_sub_section_start_time)
        if self.sub_id in self.lesson_stats:
            self.lesson_stats[self.sub_id]["time"] += elapsed_sub
            self.lesson_stats[self.sub_id]["stars"] += self.stars_earned
        else:
            self.lesson_stats[self.sub_id] = {
                "time": elapsed_sub,
                "stars": self.stars_earned,
            }

        if self.sid == "5":
            self.rule_subsection_completed = True
            self.show_sub_section_success_modal = False
        else:
            self.show_sub_section_success_modal = True
    def avanzar_seccion(self):
        proxima_sid = str(int(self.sid) + 1)
        if proxima_sid in LESSONS:
            self.sid = proxima_sid
            self.reiniciar_seccion()
        else:
            self.running = False

    def reiniciar_seccion(self):
        """Reinicia la sección actual del tutorial en su primer subtema."""
        self.sub_id = LESSONS[self.sid]["subsecciones"][0]
        self.cambiar_subseccion(self.sub_id)
        self.seccion_completada = False
        self.show_sub_section_success_modal = False
        self.final_time = None

    def procesar_clic_izquierdo(self, pos):
        if self.sid == "5" and self.sub_id == "clavada":
            return

        coords = self.get_tablero_coords(pos)
        if not coords:
            return
        fila, col = coords
        pieza_clic = obtener_pieza_en(self.partida.piezas, fila, col)
        pieza_objetivo = (
            pieza_clic
            if (pieza_clic and pieza_clic.color != self.partida.turno)
            else None
        )

        if self.seleccionada:
            f_ori = self.seleccionada.fila
            c_ori = self.seleccionada.col  # Definir c_ori aquí
            if (fila, col) in self.movimientos_posibles:
                # Detectar si el movimiento es una captura (normal o al paso)
                is_capture = pieza_objetivo is not None
                if not is_capture and self.sid == "3" and self.sub_id == "paso":
                    if (fila, col) == self.partida.en_passant_target:
                        is_capture = True

                # Detectar Promoción ANTES de registrar el movimiento normal
                if self.seleccionada.tipo == "peon" and (fila == 0 or fila == 7):
                    self.promocion_pendiente = (self.seleccionada, fila, col)
                    self._limpiar_marcas()
                    self.seleccionada = None
                    return  # Detener aquí para esperar al modal

                self.partida.registrar_movimiento(self.seleccionada, fila, col)
                self.audio_manager.reproducir("mover")

                # Lógica especial para Enroque (Niveles de seguridad 2-5)
                if self.sid == "3" and self.sub_id == "enroque":
                    if self.level_step in [2, 3, 4, 5]:
                        if not self.enroque_pre_condition_met:
                            if self.level_step in [3, 5]:  # Niveles de Captura
                                if is_capture:
                                    self.enroque_pre_condition_met = True
                            else:  # Niveles de Bloqueo
                                # Verificar si el camino del enroque ya no está atacado
                                casilla_critica = (
                                    5 if self.level_step == 2 else 3
                                )  # f1 o d1
                                if not esta_atacada(
                                    7, casilla_critica, "blanco", self.partida.piezas
                                ):
                                    self.enroque_pre_condition_met = True

                        # Si ya se cumplió la pre-condición, finalizar solo si hace el enroque
                        if self.enroque_pre_condition_met:
                            if (
                                self.seleccionada.tipo == "rey"
                                and abs(col - c_ori) == 2
                            ):
                                self.finalizar_subseccion()
                        self.seleccionada = None
                        self.movimientos_posibles = []
                        return  # Salir para no procesar contadores normales
                    else:  # Niveles 0 y 1 (Enroque directo)
                        if self.seleccionada.tipo == "rey" and abs(col - c_ori) == 2:
                            self.finalizar_subseccion()
                        return

                if self.sid == "1":  # Movimientos
                    if self.sub_id == "peon":
                        dist = abs(fila - f_ori)
                        if self.peon_mission_step == 0:  # Fase 1: Paso doble
                            if dist == 2:
                                self.peon_mission_step = 1
                                self.task_count += 1
                            elif dist == 1:  # Error: Movió solo uno
                                self.peon_mission_failed_2_step = True
                                self.peon_mission_step = 1  # Avanzar forzosamente
                                self.task_count += 1
                        elif self.peon_mission_step == 1:  # Fase 2: Paso simple
                            if dist == 1:
                                self.task_count += 1
                    else:  # Otras piezas: solo contar movimientos
                        self.task_count += 1
                    if self.task_count >= self.task_goal:
                        self.finalizar_subseccion()
                elif self.sid == "2":  # Lección de CAPTURAS
                    if is_capture:
                        self.task_count += 1

                    if self.sub_id == "peon":
                        self.moves_made += 1
                        if self.moves_made >= self.task_goal:
                            self.finalizar_subseccion()
                    elif self.task_count >= self.task_goal:
                        self.finalizar_subseccion()
                elif self.sid == "3" and self.sub_id == "paso":
                    # Lógica de respuesta del Negro para el Peón al Paso
                    if fila == 3:  # Si el blanco llega a la fila 5 (index 3)
                        # Buscamos peón negro adyacente en su origen (fila 1)
                        p_negro = None
                        for dc in [-1, 1]:
                            target_col = col + dc
                            if 0 <= target_col < 8:
                                p = obtener_pieza_en(self.partida.piezas, 1, target_col)
                                if (
                                    p
                                    and p.tipo == "peon"
                                    and p.color == "negro"
                                    and not p.ha_movido
                                ):
                                    p_negro = p
                                    break

                        if p_negro:
                            p_negro.fila = 3  # Salto doble
                            p_negro.ha_movido = True
                            self.partida.en_passant_target = (2, target_col)
                            self.audio_manager.reproducir("mover")
                            self.moves_made += 1

                    if is_capture:
                        self.task_count += 1
                        if self.moves_made >= self.task_goal:
                            self.finalizar_subseccion()
                    elif self.moves_made >= self.task_goal and fila != 3:
                        # Si ya se hicieron los 3 saltos y el niño movió otra cosa, termina la lección
                        self.finalizar_subseccion()
                elif self.sid == "4":  # Lección de JAQUE / MATE
                    if self.sub_id == "jaque":
                        # En la lección de escapar de jaque, el éxito es que el rey ya no esté atacado
                        rey_blanco = next(
                            (
                                p
                                for p in self.partida.piezas
                                if p.tipo == "rey" and p.color == "blanco"
                            ),
                            None,
                        )
                        if rey_blanco and not esta_atacada(
                            rey_blanco.fila,
                            rey_blanco.col,
                            "blanco",
                            self.partida.piezas,
                        ):
                            self.finalizar_subseccion()

                    elif self.sub_id == "jaque_mate":
                        # Verificación de Mate para las negras
                        rey_negro = next(
                            (
                                p
                                for p in self.partida.piezas
                                if p.tipo == "rey" and p.color == "negro"
                            ),
                            None,
                        )
                        # Obtener todos los movimientos posibles de las negras
                        movs_negros = []
                        for p in [p for p in self.partida.piezas if p.color == "negro"]:
                            movs_negros.extend(
                                obtener_movimientos_legales(
                                    p,
                                    self.partida.piezas,
                                    self.partida.en_passant_target,
                                )
                            )

                        es_jaque = esta_atacada(
                            rey_negro.fila, rey_negro.col, "negro", self.partida.piezas
                        )

                        if es_jaque and not movs_negros:
                            # ¡ES JAQUE MATE!
                            self.finalizar_subseccion()
                        elif es_jaque:
                            # Es solo jaque, el Rey negro escapa automáticamente
                            movs_rey = obtener_movimientos_legales(
                                rey_negro, self.partida.piezas
                            )
                            if movs_rey:
                                caps_prev = len(self.partida.capturas_negras)

                                rf, rc = random.choice(movs_rey)
                                self.partida.registrar_movimiento(rey_negro, rf, rc)
                                self.audio_manager.reproducir("mover")

                                # Si el rey capturó una pieza blanca (fallo)
                                if len(self.partida.capturas_negras) > caps_prev:
                                    self.stars_earned = 0
                                    self.mission_failed_msg = "Ups Creo que no esta bien este ejercicio\npuedes intentarlo otra vez y hacerlo mejor"
                                    self.show_sub_section_success_modal = True

                        # Si no es jaque ni mate, el niño debe seguir intentando en este nivel

                elif self.sid == "5":
                    if self.sub_id == "ahogado":
                        if self.seleccionada.tipo == "rey" and fila == 7 and col == 7:
                            self.partida.registrar_movimiento(
                                self.seleccionada, fila, col
                            )
                            self.audio_manager.reproducir("mover")
                            self._limpiar_marcas()
                            self.seleccionada = None

                            # Respuesta automática: Dama Negra a g6 para ahogar
                            dama = next(
                                (
                                    p
                                    for p in self.partida.piezas
                                    if p.tipo == "dama" and p.color == "negro"
                                ),
                                None,
                            )
                            if dama:
                                self.partida.registrar_movimiento(dama, 2, 6)
                                self.audio_manager.reproducir("mover")
                                self.finalizar_subseccion()
                            return

                    elif self.sub_id == "tablas":
                        if self.seleccionada.tipo == "rey" and fila == 4 and col == 4:
                            self._limpiar_marcas()
                            self.movimientos_posibles = []
                            self.partida.registrar_movimiento(
                                self.seleccionada, fila, col
                            )
                            self.audio_manager.reproducir("captura")
                            self.seleccionada = None

                            # Respuesta automática: Rey Negro captura Peón Blanco en c7
                            rey_n = next(
                                (
                                    p
                                    for p in self.partida.piezas
                                    if p.tipo == "rey" and p.color == "negro"
                                ),
                                None,
                            )
                            if rey_n:
                                self.partida.registrar_movimiento(rey_n, 1, 2)
                                self.audio_manager.reproducir("captura")
                                self.finalizar_subseccion()
                            return

                    elif self.sub_id == "clavada":
                        # El niño debe mover el caballo de b1 a c3 (7,1 -> 5,2)
                        if (
                            self.seleccionada.tipo == "caballo"
                            and fila == 5
                            and col == 2
                        ):
                            self._limpiar_marcas()
                            self.movimientos_posibles = []
                            self.partida.registrar_movimiento(
                                self.seleccionada, fila, col
                            )
                            self.audio_manager.reproducir("mover")
                            self.seleccionada = None

                            # Respuesta automática: Alfil Negro a b4 (0,5 -> 4,1) para clavar al Rey
                            alfil = next(
                                (
                                    p
                                    for p in self.partida.piezas
                                    if p.tipo == "alfil"
                                    and p.color == "negro"
                                    and p.fila == 0
                                    and p.col == 5
                                ),
                                None,
                            )
                            if alfil:
                                self.partida.registrar_movimiento(alfil, 4, 1)
                                self.audio_manager.reproducir("mover")
                                # Finalizar la subsección tras mostrar la clavada
                                self.finalizar_subseccion()
                            return

                    elif self.sub_id == "insuficiencia_material":
                        is_capture = pieza_objetivo is not None
                        if is_capture and pieza_objetivo.tipo == "dama":
                            self._limpiar_marcas()
                            self.movimientos_posibles = []
                            self.partida.registrar_movimiento(
                                self.seleccionada, fila, col
                            )
                            self.audio_manager.reproducir("captura")
                            self.seleccionada = None
                            self.finalizar_subseccion()
                            return

                    self.seleccionada = None
                    self.movimientos_posibles = []
                    return

                self.seleccionada = None
                self.movimientos_posibles = []
            elif pieza_clic and pieza_clic.color == self.partida.turno:
                self._seleccionar_pieza(pieza_clic)
        elif pieza_clic and pieza_clic.color == self.partida.turno:
            self._seleccionar_pieza(pieza_clic)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # 0. Prioridad: Modal de Promoción
                if self.promocion_pendiente:
                    for tipo, r_promo in self.vista.rects_promo:
                        if r_promo.collidepoint(pos):
                            p, f, c = self.promocion_pendiente
                            self.partida.registrar_movimiento(p, f, c, promocion=tipo)
                            self.promocion_pendiente = None
                            self.audio_manager.reproducir("mover")
                            # Registrar misión de promoción si aplica
                            if self.sid == "3" and self.sub_id == "promocion":
                                if not self.promotions_completed[tipo]:
                                    self.promotions_completed[tipo] = True

                                # Incrementar siempre para que la subsección termine al procesar los 4 peones
                                self.task_count += 1
                                if self.task_count >= self.task_goal:
                                    self.finalizar_subseccion()
                            return
                    return

                # 1. Prioridad Máxima: Modal de fin de lección (Cartel Final)
                if self.seccion_completada:
                    if self.vista.rect_tut_regresar.collidepoint(pos):
                        self.running = False
                        return
                    elif self.vista.rect_tut_reiniciar.collidepoint(pos):
                        self.reiniciar_seccion()
                        return
                    elif self.vista.rect_tut_siguiente.collidepoint(pos):
                        self.avanzar_seccion()
                        return
                    return  # Bloquear otros clics si el modal final está activo

                # 2. Prioridad: Modal de éxito de subsección (Siguiente)
                if self.show_sub_section_success_modal:
                    btn_next = self.success_modal_buttons_rects.get("siguiente")
                    btn_re = self.success_modal_buttons_rects.get("reiniciar")

                    if btn_re and btn_re.collidepoint(pos):
                        self.show_sub_section_success_modal = False
                        self.mission_failed_msg = None
                        self.reiniciar_subseccion()
                        return

                    if btn_next and btn_next.collidepoint(pos):
                        self.show_sub_section_success_modal = False
                        self.mission_failed_msg = None
                        # Lógica para avanzar
                        subs = LESSONS[self.sid]["subsecciones"]
                        idx = subs.index(self.sub_id)
                        max_steps = 1
                        if self.sid == "4":
                            max_steps = 9 if self.sub_id == "jaque" else 3
                        if self.sub_id == "enroque":
                            max_steps = 6
                        if self.sub_id == "promocion":
                            max_steps = 1  # Solo un escenario para promoción
                        if self.sid == "5":
                            if self.sub_id == "insuficiencia_material":
                                max_steps = 4
                            elif self.sub_id == "clavada":
                                max_steps = 1
                            else:
                                max_steps = 1

                        if self.level_step < max_steps - 1:
                            self.level_step += 1
                            self.partida.cargar_escenario(self.sid, self.sub_id)
                            for p in self.partida.piezas:
                                p.tam_cuadro = self.vista.tam_cuadro
                                p.imagen = p._cargar_imagen()
                            self.seleccionada = None
                            self.movimientos_posibles = []
                            self.reiniciar_contadores()
                        elif idx < len(subs) - 1:
                            self.cambiar_subseccion(subs[idx + 1])
                        else:
                            self.seccion_completada = True
                            if self.final_time is None:
                                self.final_time = int(time.time() - self.start_time)
                    return  # Bloquear clics del tablero si el modal de éxito está activo

                # 3. Botones del Panel Lateral
                botones_panel = self.tutorial_panel_render.get_button_rects()
                if botones_panel.get("siguiente") and botones_panel["siguiente"].collidepoint(pos):
                    if self.sid == "5" and self.sub_id in [
                        "ahogado",
                        "tablas",
                        "insuficiencia_material",
                        "clavada",
                    ]:
                        subs = LESSONS[self.sid]["subsecciones"]
                        idx = subs.index(self.sub_id)
                        if self.sub_id == "clavada":
                            self.seccion_completada = True
                            if self.final_time is None:
                                self.final_time = int(time.time() - self.start_time)
                            return
                        elif idx < len(subs) - 1:
                            self.cambiar_subseccion(subs[idx + 1])
                            return
                        else:
                            self.seccion_completada = True
                            if self.final_time is None:
                                self.final_time = int(time.time() - self.start_time)
                            return
                if botones_panel.get("reiniciar") and botones_panel["reiniciar"].collidepoint(pos):
                    self.reiniciar_subseccion()
                    return
                if botones_panel.get("regresar") and botones_panel["regresar"].collidepoint(pos):
                    self.running = False
                    return

                # 4. Botones de Navegación de Subsecciones (Izquierda)
                for subid, rect in self.sub_section_nav_buttons_rects.items():
                    if rect.collidepoint(pos):
                        if subid != self.sub_id:
                            self.cambiar_subseccion(subid)
                        return

                # 5. Finalmente, Clic en el Tablero
                self.procesar_clic_izquierdo(pos)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                # Scroll del panel de diálogo en el tutorial
                if hasattr(self.tutorial_panel_render, "dialog_area_rect") and self.tutorial_panel_render.dialog_area_rect.collidepoint(event.pos):
                    delta = -20 if event.button == 4 else 20
                    self.tutorial_panel_render.dialog_scroll = min(
                        max(0, self.tutorial_panel_render.dialog_scroll + delta),
                        self.tutorial_panel_render.dialog_scroll_max,
                    )
                    return

            # Manejo de clic derecho para dibujo táctico
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.right_click_start = self.get_tablero_coords(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                self.procesar_clic_derecho(event.pos)