"""Vistas del módulo views."""

import threading
import time
import pygame
from ..domain.partida import Partida
from ..domain.tablero_logico import obtener_movimientos_legales, obtener_pieza_en, esta_atacada
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro
from .tablero_render import TableroRender
from .pieza_animada import PiezaAnimada
from ..services.audio import GestorAudio
from ..services.motor_ia import MotorIA
from .Flecha import Flecha


class VentanaJuego:
    def __init__(
        self, tema, dificultad, tiempo, contra_ia, bando_elegido, evento_cierre
    ):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        res = (info.current_w, info.current_h)

        self.clock = pygame.time.Clock()
        self.evento_cierre = evento_cierre

        # Inicialización de Capas
        self.partida = Partida(
            minutos=tiempo, bando_elegido=bando_elegido, contra_ia=contra_ia
        )
        self.vista = TableroRender(self.screen, tema=tema, res=res)
        for p in self.partida.piezas:
            p.tam_cuadro = self.vista.tam_cuadro
            p.imagen = p._cargar_imagen()

        self.ia = MotorIA()
        self.dificultad = dificultad
        self.ia_pensando = False
        self.movimiento_ia_pendiente = None
        self.circulos_tacticos = []
        self.flechas_tacticos = []
        self.right_click_start = None

        self.running = True
        self.seleccionada = None
        self.movimientos_posibles = []
        self.audio_manager = GestorAudio()  # Inicializar el gestor de audio
        self.resultado_accion = None  # 'nuevo', 'revancha', 'salir'
        self.promocion_pendiente = None  # (pieza, fila, col)
        self.reyes_en_jaque = []
        self.verificar_final_partida()

        # Lógica de Nicknames divertidos
        self.nicknames = {
            "jugador": "El Rey Sabio",
            "oponente": (
                "El Rey Maestro"
                if not contra_ia
                else self._obtener_nombre_ia(dificultad)
            ),
        }

    def _obtener_nombre_ia(self, dificultad):
        nombres = {
            "Hierro": "El Recluta",
            "Bronce": "El Saltador",
            "Plata": "El Corredor",
            "Oro": "La Muralla",
            "Diamante": "La Emperatriz",
            "Maestro": "El Profesor",
            "Gran Maestro": "El Hechicero",
            "Élite": "El Vigilante",
            "Galáctico": "El Viajero",
            "Estelar": "El Astro",
            "Solar": "El Sol",
            "Místico": "El Oráculo",
            "Infinito": "El Eterno",
            "Dios de la IA": "Kiyotaka Ayanokoji",
        }
        return nombres.get(dificultad, "El Maestro")

    def run(self):
        while self.running:
            # Comprobación de cierre seguro desde el orquestador
            if self.evento_cierre.is_set():
                self.running = False
                break

            self.partida.actualizar_relojes()
            self.manejar_eventos()

            # Optimizacion: Solo verificar animaciones de forma eficiente
            piezas_moviendose = False
            inv = (self.partida.color_usuario == "negro")
            for p in self.partida.piezas:
                if p.esta_animando(self.vista.offset_x, self.vista.offset_y, inv):
                    piezas_moviendose = True
                    break

            # Turno de la IA
            if (
                self.partida.color_ia is not None
                and self.partida.turno == self.partida.color_ia
                and not self.partida.resultado
                and not piezas_moviendose
                and not self.ia_pensando
                and not self.movimiento_ia_pendiente
            ):
                self.ejecutar_turno_ia()

            # Aplicar movimiento de IA procesado en el hilo principal
            if self.movimiento_ia_pendiente:
                self.aplicar_movimiento_ia(self.movimiento_ia_pendiente)
                self.movimiento_ia_pendiente = None

            mouse_p = pygame.mouse.get_pos()
            self.vista.dibujar(
                self.partida,
                mouse_p,
                self.circulos_tacticos,
                self.flechas_tacticos,
                self.seleccionada,
                self.movimientos_posibles,
                self.nicknames,  # Mantener para compatibilidad con VentanaJuego normal
                reyes_en_jaque=self.reyes_en_jaque,
                draw_panel=True,  # Por defecto, VentanaJuego dibuja el panel
            )

            if self.promocion_pendiente:
                self.vista.dibujar_modal_promocion(self.partida.turno, mouse_p)

            if self.partida.resultado:
                self.mostrar_resultado()

            pygame.display.flip()
            self.clock.tick(30)

        # Liberación controlada de recursos
        pygame.quit()
        self.ia.close()

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.promocion_pendiente:
                    for tipo, rect in self.vista.rects_promo:
                        if rect.collidepoint(event.pos):
                            p, f, c = self.promocion_pendiente
                            self.partida.registrar_movimiento(p, f, c, promocion=tipo)
                            self.promocion_pendiente = None
                            self.verificar_final_partida()
                            self.audio_manager.reproducir("mover")
                            break
                    continue

                if self.partida.resultado:
                    # Eventos del Modal
                    if self.vista.rect_modal_nuevo.collidepoint(event.pos):
                        self.resultado_accion = "nuevo"
                        self.running = False
                    elif self.vista.rect_modal_revancha.collidepoint(event.pos):
                        self.reiniciar_partida()
                    elif self.vista.rect_modal_salir.collidepoint(event.pos):
                        self.resultado_accion = "salir"
                        self.running = False
                    continue  # Ignorar el resto si hay modal

                if event.button == 1:
                    if self.vista.rect_deshacer.collidepoint(event.pos):
                        # Si hay IA, deshacemos dos movimientos
                        if (
                            self.partida.color_ia is not None
                            and len(self.partida.pila_estados) >= 2
                        ):
                            self.partida.deshacer_movimiento()

                        self.partida.deshacer_movimiento()
                        self.verificar_final_partida()

                        # Sincronizar visuales de las piezas restauradas con el tamaño actual del tablero
                        for p in self.partida.piezas:
                            p.tam_cuadro = self.vista.tam_cuadro
                            p.imagen = p._cargar_imagen()

                        self.seleccionada = None
                        self.movimientos_posibles = []
                    elif self.vista.rect_tablas.collidepoint(event.pos):
                        self.partida.resultado = "Tablas por Acuerdo"
                    elif self.vista.rect_abandonar.collidepoint(event.pos):
                        self.partida.resultado = "Partida Abandonada"

                # Navegación del historial
                if event.button == 4:  # Rueda arriba
                    self.vista.scroll_historial = max(
                        0, self.vista.scroll_historial - 20
                    )
                if event.button == 5:  # Rueda abajo
                    self.vista.scroll_historial += 20

            if not self.partida.resultado and not self.ia_pensando:
                es_turno_humano = self.partida.turno != self.partida.color_ia
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and es_turno_humano:
                        self.procesar_clic_izquierdo(event.pos)
                    elif event.button == 3:
                        self.right_click_start = self.get_tablero_coords(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.procesar_clic_derecho(event.pos)

    def get_tablero_coords(self, pos):
        """Convierte posición de mouse en coordenadas (f, c)."""
        c = (pos[0] - self.vista.offset_x) // self.vista.tam_cuadro
        f = (pos[1] - self.vista.offset_y) // self.vista.tam_cuadro

        # Si el tablero está invertido, las coordenadas del mouse también deben invertirse
        if self.partida.color_usuario == "negro":
            f = 7 - f
            c = 7 - c

        if 0 <= f < 8 and 0 <= c < 8:
            return (f, c)
        return None

    def procesar_clic_derecho(self, pos):
        end_coords = self.get_tablero_coords(pos)
        if self.right_click_start and end_coords:
            if self.right_click_start == end_coords:
                # Toggle círculo
                if end_coords in self.circulos_tacticos:
                    self.circulos_tacticos.remove(end_coords)
                else:
                    self.circulos_tacticos.append(end_coords)
            else:
                nueva_flecha = Flecha(
                    self.right_click_start,
                    end_coords,
                    (0, 255, 0),
                    tam_cuadro=self.vista.tam_cuadro,
                )
                if nueva_flecha in self.flechas_tacticos:
                    self.flechas_tacticos.remove(nueva_flecha)
                else:
                    self.flechas_tacticos.append(nueva_flecha)
        self.right_click_start = None

    def procesar_clic_izquierdo(self, pos):
        coords = self.get_tablero_coords(pos)
        if not coords:
            return

        # Limpiar flechas y círculos tácticos al hacer clic izquierdo
        self._limpiar_marcas()

        fila, col = coords
        pieza_clic = obtener_pieza_en(self.partida.piezas, fila, col)

        if self.seleccionada:
            if (fila, col) in self.movimientos_posibles:
                # Detectar Promoción
                if self.seleccionada.tipo == "peon" and (fila == 0 or fila == 7):
                    self.promocion_pendiente = (self.seleccionada, fila, col)
                    self._limpiar_marcas()
                else:
                    self._limpiar_marcas()
                    self.partida.registrar_movimiento(
                        self.seleccionada, fila, col, "Mov"
                    )
                    self.verificar_final_partida()
                    self.audio_manager.reproducir("mover")
                self.seleccionada = None
            elif pieza_clic and pieza_clic.color == self.partida.turno:
                self._seleccionar_pieza(pieza_clic)
            else:
                # Clic en cualquier otro lado: Deseleccionar
                self.seleccionada = None
                self.movimientos_posibles = []
        elif pieza_clic and pieza_clic.color == self.partida.turno:
            self._seleccionar_pieza(pieza_clic)

    def _seleccionar_pieza(self, pieza):
        self.seleccionada = pieza
        self._limpiar_marcas()
        self.movimientos_posibles = obtener_movimientos_legales(
            pieza, self.partida.piezas, self.partida.en_passant_target
        )

    def _limpiar_marcas(self):
        self.circulos_tacticos.clear()
        self.flechas_tacticos.clear()

    def ejecutar_turno_ia(self):
        """Inicia el cálculo de la IA en un hilo separado para no bloquear la UI."""
        self.ia_pensando = True

        def thread_target():
            try:
                time.sleep(0.2)  # Menor latencia para procesadores lentos
                fen = self.partida.obtener_fen()
                movimiento = self.ia.obtener_mejor_jugada(fen, self.dificultad)
                if movimiento:
                    # Almacenamos para que el hilo principal lo ejecute de forma segura
                    self.movimiento_ia_pendiente = movimiento
            except Exception as e:
                print(f"Error crítico en el motor de IA: {e}")
            finally:
                self.ia_pensando = False

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def mostrar_resultado(self):
        """Maneja la visualización del modal."""
        res = self.partida.resultado
        nick = self.nicknames

        ganador = ""
        perdedor = ""

        if any(x in res for x in ["Tablas", "Empate", "Ahogado", "Material"]):
            ganador = "Empate"
            perdedor = "Empate"
        elif "Blancas" in res:
            if self.partida.color_usuario == "blanco":
                ganador, perdedor = nick["jugador"], nick["oponente"]
            else:
                ganador, perdedor = nick["oponente"], nick["jugador"]
        elif "Negras" in res:
            if self.partida.color_usuario == "negro":
                ganador, perdedor = nick["jugador"], nick["oponente"]
            else:
                ganador, perdedor = nick["oponente"], nick["jugador"]
        elif res in ["Jaque Mate", "Partida Abandonada"]:
            # El bando que tiene el turno es el que perdió (se rindió o recibió mate)
            if self.partida.turno == self.partida.color_usuario:
                ganador, perdedor = nick["oponente"], nick["jugador"]
            else:
                ganador, perdedor = nick["jugador"], nick["oponente"]

        # Notificar logro si el jugador venció a la IA
        if self.partida.color_ia is not None and ganador == nick["jugador"]:
            logro_id = f"ajedrez_{self.dificultad.lower().replace(' ', '_')}"
            notificar_logro(logro_id)
            GestorEstado().actualizar_progreso("Ajedrez", 0.07)

        self.vista.dibujar_modal_resultado(
            ganador,
            perdedor,
            res,
            pygame.mouse.get_pos(),
            nick,
            (self.partida.color_ia is not None),
        )

    def reiniciar_partida(self):
        """Reinicia el estado para una revancha."""
        # Reiniciar lógica
        tiempo_original = (
            int(self.partida.tiempo_blanco + self.partida.tiempo_negro) // 120
        )  # Aproximado
        if tiempo_original == 0:
            tiempo_original = 10

        self.partida.__init__(
            minutos=tiempo_original,
            bando_elegido=self.partida.color_usuario,
            contra_ia=(self.partida.color_ia is not None),
        )

        # Re-ajustar piezas para la nueva partida
        for p in self.partida.piezas:
            p.tam_cuadro = self.vista.tam_cuadro
            p.imagen = p._cargar_imagen()

        self.seleccionada = None
        self.movimientos_posibles = []
        self.partida.resultado = None

    def aplicar_movimiento_ia(self, movimiento):
        """Ejecuta el movimiento de la IA y dispara las animaciones."""
        movimiento_uci = str(movimiento)
        # Traducir UCI (ej: e2e4) a coordenadas
        c1 = ord(movimiento_uci[0]) - ord("a")
        f1 = 8 - int(movimiento_uci[1])
        c2 = ord(movimiento_uci[2]) - ord("a")
        f2 = 8 - int(movimiento_uci[3])

        pieza = obtener_pieza_en(self.partida.piezas, f1, c1)
        # Validación de seguridad: La IA solo puede mover sus propias piezas
        if pieza and pieza.color == self.partida.color_ia:
            es_captura = obtener_pieza_en(self.partida.piezas, f2, c2) is not None
            # Si es promoción (UCI tiene 5 caracteres), extraemos la pieza elegida por la IA
            promo = "dama"
            if len(movimiento_uci) == 5:
                map_p = {"q": "dama", "r": "torre", "b": "alfil", "n": "caballo"}
                promo = map_p.get(movimiento_uci[4], "dama")

            self.partida.registrar_movimiento(
                pieza, f2, c2, movimiento_uci, promocion=promo
            )
            self.verificar_final_partida()
            self.audio_manager.reproducir("captura" if es_captura else "mover")

        # Limpiamos cualquier selección previa para evitar que el usuario herede clics
        self.seleccionada = None

    def verificar_final_partida(self):
        # Lógica para detectar si el jugador actual no tiene movimientos
        self.reyes_en_jaque = []
        sin_movimientos = True
        rey_en_jaque = False
        # Usamos una copia de la lista para evitar problemas de concurrencia o reordenamiento
        piezas_actuales = list(self.partida.piezas)
        
        for p in piezas_actuales:
            # Almacenar reyes en jaque para el renderizador (Optimización)
            if p.tipo == "rey":
                es_atacado = esta_atacada(p.fila, p.col, p.color, piezas_actuales)
                if es_atacado:
                    self.reyes_en_jaque.append((p.fila, p.col))
                if p.color == self.partida.turno:
                    rey_en_jaque = es_atacado
                    
            if p.color == self.partida.turno:
                if obtener_movimientos_legales(
                    p, piezas_actuales, self.partida.en_passant_target
                ):
                    sin_movimientos = False
                    
        if sin_movimientos:
            if rey_en_jaque:
                # No hay movimientos y el rey está bajo ataque: JAQUE MATE
                self.partida.resultado = "Jaque Mate"
            else:
                # No hay movimientos pero el rey está a salvo: REY AHOGADO (Tablas)
                self.partida.resultado = "Rey Ahogado (Tablas)"
        
        # Detección de tablas por falta de piezas (solo quedan los dos reyes)
        elif len(self.partida.piezas) == 2:
            self.partida.resultado = "Tablas por Material Insuficiente"