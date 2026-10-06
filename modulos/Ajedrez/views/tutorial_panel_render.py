"""Vistas del módulo views."""

import pygame
import os


class TutorialPanelRender:
    """
    Clase encargada de renderizar todos los elementos visuales del panel lateral
    específico del tutorial de ajedrez.
    """

    def __init__(self, screen, vista_tablero, lessons_data):
        self.screen = screen
        self.vista = vista_tablero  # Para obtener dimensiones del panel y colores
        self.lessons_data = lessons_data

        # Fuentes
        self.font_timer = pygame.font.SysFont("Consolas", 30, bold=True)
        self.font_header = pygame.font.SysFont("Verdana", 18, bold=True)
        self.font_text = pygame.font.SysFont("Verdana", 14)

        # Dimensiones del panel lateral obtenidas de TableroRender
        self.x_panel = self.vista.x_panel
        self.y_base = self.vista.offset_y
        self.w_panel = self.vista.ancho_panel
        self.h_panel = self.vista.alto_panel

        # Cargar imagen de check (listo.png)
        self.img_listo = None
        listo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "imagenes",
            "listo.png",
        )
        if os.path.exists(listo_path):
            orig_img = pygame.image.load(listo_path).convert_alpha()
            # Escalar a un tamaño adecuado para el texto de la misión
            self.img_listo = pygame.transform.scale(orig_img, (20, 20))

        # Rectángulos de botones (calculados desde abajo hacia arriba para evitar solapamientos)
        # Botón REGRESAR AL MENÚ (más abajo)
        self.rect_regresar_default = pygame.Rect(
            self.x_panel + 20,
            self.y_base + self.h_panel - 50,  # 50px desde el borde inferior
            self.w_panel - 40,
            40,
        )
        # Botón REINICIAR MISIÓN (encima de REGRESAR)
        self.rect_reiniciar_default = pygame.Rect(
            self.x_panel + 20,
            self.rect_regresar_default.y - 10 - 40,  # 10px de margen + 40px de alto
            self.w_panel - 40,
            40,
        )
        self.dialog_scroll = 0
        self.dialog_scroll_max = 0
        self.rect_regresar = self.rect_regresar_default
        self.rect_reiniciar = self.rect_reiniciar_default
        self.rect_siguiente = None
        self.interlineado = 20 # Definir interlineado aquí para que siempre esté disponible
        
        # Optimizacion: Cache de texto envuelto
        self._cached_lines = []
        self._cached_key = None # (sid, sub_id)
        self._cached_dialog_surf = None
        # Posición base para los botones de subsección (encima de REINICIAR)
        # Se calcula en VentanaTutorial, no en este renderizador.

    def _wrap_text(self, text, font, max_width):
        """Divide un texto en varias líneas para que quepa en un ancho determinado."""
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

    def dibujar(
        self,
        current_sid,
        current_sub_id,
        task_count,
        task_goal,
        peon_mission_step,
        stars_earned,
        level_step,
        elapsed_time,
        peon_mission_failed_2_step,  # Nuevo parámetro
        mouse_pos,
        enroque_ready=False,  # Nuevo parámetro para Enroque
        promotions_completed=None,  # Nuevo parámetro para Promoción
    ):
        """
        Dibuja todos los elementos del panel lateral del tutorial.
        Recibe el estado actual del tutorial como parámetros.
        """
        # Limpiar el área del panel (fondo y borde)
        pygame.draw.rect(
            self.screen,
            self.vista.colores["panel"],
            (self.x_panel, self.y_base, self.w_panel, self.h_panel),
            border_radius=20,
        )
        pygame.draw.rect(
            self.screen,
            self.vista.colores["resaltado"],
            (self.x_panel, self.y_base, self.w_panel, self.h_panel),
            2,
            border_radius=20,
        )

        # 1. Cronómetro "REY SABIO"
        m, s = divmod(elapsed_time, 60)
        color_timer_bg = tuple(max(0, c - 20) for c in self.vista.colores["panel"])
        pygame.draw.rect(
            self.screen,
            color_timer_bg,
            (self.x_panel + 20, self.y_base + 20, self.w_panel - 40, 80),
            border_radius=15,
        )
        pygame.draw.rect(
            self.screen,
            self.vista.colores["resaltado"],
            (self.x_panel + 20, self.y_base + 20, self.w_panel - 40, 80),
            2,
            border_radius=15,
        )
        lbl_cadete = self.font_header.render(
            "REY SABIO", True, self.vista.colores["resaltado"]
        )
        self.screen.blit(lbl_cadete, (self.x_panel + 40, self.y_base + 30))
        txt_timer = self.font_timer.render(f"{m:02d}:{s:02d}", True, "white")
        self.screen.blit(
            txt_timer, (self.x_panel + self.w_panel - 110, self.y_base + 45)
        )

        # 2. Área de Diálogo: "PALABRAS DEL DIOS DEL AJEDREZ"
        y_dialogo = self.y_base + 115
        h_dialogo = (
            self.h_panel - 260
        )  # Ajustado para dejar espacio a los botones inferiores
        color_dialogo_bg = tuple(max(0, c - 10) for c in self.vista.colores["panel"])
        pygame.draw.rect(
            self.screen,
            color_dialogo_bg,
            (self.x_panel + 20, y_dialogo, self.w_panel - 40, h_dialogo),
            border_radius=15,
        )
        txt_h = self.font_header.render(
            "PALABRAS DEL DIOS DEL AJEDREZ", True, (255, 215, 0)
        )
        self.screen.blit(txt_h, (self.x_panel + 30, y_dialogo + 15))

        # Area de texto scrollable
        content_top = y_dialogo + 55
        content_left = self.x_panel + 30
        content_width = self.w_panel - 60
        content_height = h_dialogo - 80
        self.dialog_area_rect = pygame.Rect(
            content_left, content_top, content_width, content_height
        )

        # Optimizacion: No envolver texto si es la misma leccion
        key = (current_sid, current_sub_id)
        if self._cached_key != key:
            teoria_data = self.lessons_data[current_sid]["data"][current_sub_id]
            self._cached_lines = []
            for bloque in teoria_data:
                self._cached_lines.extend(self._wrap_text(bloque, self.font_text, content_width))
            
            # Pre-renderizar todo el bloque de texto en una sola superficie
            total_h = len(self._cached_lines) * self.interlineado
            self._cached_dialog_surf = pygame.Surface((content_width, total_h), pygame.SRCALPHA)
            for i, linea in enumerate(self._cached_lines):
                txt_render = self.font_text.render(linea, True, "white").convert_alpha()
                self._cached_dialog_surf.blit(txt_render, (0, i * self.interlineado))
            
            self._cached_key = key

        self.dialog_scroll_max = max(0, self._cached_dialog_surf.get_height() - content_height)
        self.dialog_scroll = min(max(0, self.dialog_scroll), self.dialog_scroll_max)

        self.screen.blit(
            self._cached_dialog_surf,
            (content_left, content_top),
            area=pygame.Rect(0, self.dialog_scroll, content_width, content_height),
        )

        # 3. Anclaje Fijo de Misión (al fondo del área de diálogo)
        y_mision_start = y_dialogo + h_dialogo - 150
        fixed_position_subs = [
            "clavada",
            "ahogado",
            "tablas",
            "insuficiencia_material",
        ]
        self.rect_siguiente = None
        self.rect_regresar = self.rect_regresar_default
        self.rect_reiniciar = (
            None
            if current_sid == "5" and current_sub_id in fixed_position_subs
            else self.rect_reiniciar_default
        )

        if current_sid == "5" and current_sub_id in fixed_position_subs:
            button_y = self.rect_regresar_default.y - 10 - 40
            self.rect_siguiente = pygame.Rect(
                self.x_panel + 30,
                button_y,
                self.w_panel - 60,
                40,
            )
            pygame.draw.rect(
                self.screen,
                (39, 174, 96),
                self.rect_siguiente,
                border_radius=12,
            )
            label = (
                "TERMINAR SECCION"
                if current_sub_id == "clavada"
                else "SIGUIENTE"
            )
            txt_siguiente = self.font_header.render(label, True, "white")
            self.screen.blit(
                txt_siguiente,
                (
                    self.rect_siguiente.centerx - txt_siguiente.get_width() // 2,
                    self.rect_siguiente.centery - txt_siguiente.get_height() // 2,
                ),
            )

        if not (current_sid == "5" and current_sub_id in fixed_position_subs):
            pygame.draw.line(
                self.screen,
                self.vista.colores["resaltado"],
                (self.x_panel + 30, y_mision_start),
                (self.x_panel + self.w_panel - 30, y_mision_start),
                2,
            )

        # 5. Dibujar Misión (Anclada)
        fixed_position_subs = [
            "clavada",
            "ahogado",
            "tablas",
            "insuficiencia_material",
        ]
        if not (current_sid == "5" and current_sub_id in fixed_position_subs):
            txt_m = self.font_header.render("TU MISION", True, (0, 255, 127))
            self.screen.blit(txt_m, (self.x_panel + 40, y_mision_start + 15))

            # Lógica de misión para el peón (dos líneas)
            if current_sid == "1" and current_sub_id == "peon":
                # Misión 1: Mover dos pasos
                color_mision1 = (
                    (255, 50, 50) if peon_mission_failed_2_step else (0, 255, 127)
                )
                text_mision1 = "1. Mueve el peon 2 pasos a la vez"

                # Misión 2: Mover un paso
                color_mision2 = (0, 255, 127)  # Siempre verde
                text_mision2 = "2. Mueve el peon 1 paso a la vez"

                # Dibujar Misión 1
                lineas_mision1 = self._wrap_text(
                    text_mision1, self.font_text, self.w_panel - 80
                )
                for i, lm in enumerate(lineas_mision1):
                    txt_task = self.font_text.render(lm, True, color_mision1)
                    self.screen.blit(
                        txt_task, # Usar self.interlineado
                        (self.x_panel + 40, y_mision_start + 45 + i * self.interlineado),
                    )

                # Dibujar Misión 2 (desplazado por la altura de la Misión 1)
                y_offset_mision2 = ( # Usar self.interlineado
                    y_mision_start + 45 + len(lineas_mision1) * self.interlineado + 5
                )  # 5px de padding
                lineas_mision2 = self._wrap_text(
                    text_mision2, self.font_text, self.w_panel - 80
                )
                for i, lm in enumerate(lineas_mision2):
                    txt_task = self.font_text.render(lm, True, color_mision2)
                    self.screen.blit( # Usar self.interlineado
                        txt_task, (self.x_panel + 40, y_offset_mision2 + i * self.interlineado)
                    )

            elif current_sid == "3" and current_sub_id == "enroque" and level_step >= 2:
                # Misiones de seguridad del enroque (Dos líneas)
                m1_txt = (
                    "1. Captura al atacante"
                    if level_step in [3, 5]
                    else "1. Bloquea el ataque"
                )
                m2_txt = "2. ¡Ya puedes hacer el enroque!"

                c1 = (0, 255, 127) if enroque_ready else self.vista.colores["resaltado"]
                c2 = (
                    (0, 255, 127) if enroque_ready else (100, 100, 100)
                )  # Apagado si no está listo

                txt1 = self.font_text.render(m1_txt, True, c1)
                self.screen.blit(txt1, (self.x_panel + 40, y_mision_start + 45))

                if enroque_ready and self.img_listo:
                    self.screen.blit(
                        self.img_listo,
                        (self.x_panel + 45 + txt1.get_width(), y_mision_start + 45),
                    )

                txt2 = self.font_text.render(m2_txt, True, c2)
                self.screen.blit(txt2, (self.x_panel + 40, y_mision_start + 45 + self.interlineado))

            elif current_sid == "3" and current_sub_id == "promocion":
                # Misiones de Promoción (4 líneas)
                promos = ["dama", "torre", "alfil", "caballo"]
                y_offset_mission = y_mision_start + 45
                for i, p_type in enumerate(promos):
                    articulo = "una" if p_type in ["dama", "torre"] else "un"
                    mission_text = f"{i+1}. Convierte tu peón en {articulo} {p_type}"

                    is_completed = promotions_completed.get(p_type, False)
                    color = (0, 255, 127) if is_completed else (100, 100, 100)

                    txt_mission = self.font_text.render(mission_text, True, color)
                    self.screen.blit(txt_mission, (self.x_panel + 40, y_offset_mission))

                    if is_completed and self.img_listo:
                        self.screen.blit(
                            self.img_listo,
                            (self.x_panel + 45 + txt_mission.get_width(), y_offset_mission),
                        )

                    y_offset_mission += self.interlineado + 5  # Más espacio entre misiones

            else:
                mision_text_color = (0, 255, 127)  # Verde por defecto
                mision_text = "Realiza la acción indicada"
                if current_sid == "1":  # Movimientos (otras piezas)
                    mision_text = (
                        f"Misión: Mueve la pieza ({task_goal - task_count} restantes)"
                    )
                elif current_sid == "2":  # Capturas
                    mision_text = (
                        f"Nivel {level_step + 1}: Captura ({task_count}/{task_goal})"
                    )
                elif current_sid == "4" and current_sub_id == "jaque":
                    if level_step < 3:
                        mision_text = f"Nivel {level_step + 1}: ¡ESCAPA del jaque!"
                    elif level_step < 6:
                        mision_text = f"Nivel {level_step + 1}: ¡BLOQUEA el jaque!"
                    else:
                        mision_text = f"Nivel {level_step + 1}: ¡CAPTURA al atacante!"

                lineas_mision = self._wrap_text(
                    mision_text, self.font_text, self.w_panel - 80
                )
                for i, lm in enumerate(lineas_mision):
                    txt_task = self.font_text.render(lm, True, mision_text_color)
                    self.screen.blit(
                        txt_task, # Usar self.interlineado
                        (self.x_panel + 40, y_mision_start + 45 + i * self.interlineado),
                    )
        elif current_sid == "5" and current_sub_id in fixed_position_subs:
            # No hay misión visible para escenarios cargados.
            # El flujo de reglas se presenta como un tutorial estático sin objetivos extra.
            pass

        # Las estrellas y los botones de navegación de subsecciones se dibujan ahora en VentanaTutorial

        # 6. Botón REINICIAR MISIÓN
        if self.rect_reiniciar:
            pygame.draw.rect(
                self.screen, (52, 152, 219), self.rect_reiniciar, border_radius=15
            )
            txt_restart = self.font_header.render("REINICIAR MISIÓN", True, "white")
            restart_x = self.rect_reiniciar.centerx - txt_restart.get_width() // 2
            restart_y = self.rect_reiniciar.centery - txt_restart.get_height() // 2
            self.screen.blit(txt_restart, (restart_x, restart_y))

        # 7. Botón REGRESAR AL MENÚ
        pygame.draw.rect(
            self.screen, (192, 57, 43), self.rect_regresar, border_radius=15
        )
        txt_back = self.font_header.render("REGRESAR AL MENÚ", True, "white")
        back_x = self.rect_regresar.centerx - txt_back.get_width() // 2
        back_y = self.rect_regresar.centery - txt_back.get_height() // 2
        self.screen.blit(txt_back, (back_x, back_y))

    def get_button_rects(self):
        """Retorna los rectángulos de los botones para la detección de clics."""
        return {
            "regresar": self.rect_regresar,
            "reiniciar": self.rect_reiniciar,
            "siguiente": self.rect_siguiente,
        }