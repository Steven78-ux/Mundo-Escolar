"""Vistas del módulo views."""

import pygame
import math


class Flecha:
    def __init__(self, inicio_coord, fin_coord, color, tam_cuadro=75):
        # Aseguramos que tam_cuadro tenga un valor por defecto si llega None
        self.tam_cuadro = tam_cuadro if tam_cuadro is not None else 75

        self.inicio = inicio_coord
        self.fin = fin_coord

        # Gestión de color con transparencia (Alpha)
        if len(color) == 3:
            self.color = (*color, 160)
        else:
            self.color = color

        self.actualizar_coordenadas_px()

    def actualizar_coordenadas_px(self):
        """Calcula los puntos de inicio y fin en píxeles."""
        self.pos_inicio_px = pygame.Vector2(
            self.inicio[1] * self.tam_cuadro + self.tam_cuadro // 2,
            self.inicio[0] * self.tam_cuadro + self.tam_cuadro // 2,
        )
        self.pos_fin_px = pygame.Vector2(
            self.fin[1] * self.tam_cuadro + self.tam_cuadro // 2,
            self.fin[0] * self.tam_cuadro + self.tam_cuadro // 2,
        )

    def __eq__(self, otra):
        """
        Permite el borrado (Toggle).
        Si las coordenadas de inicio y fin coinciden, se consideran iguales.
        """
        if not isinstance(otra, Flecha):
            return False
        return self.inicio == otra.inicio and self.fin == otra.fin

    def dibujar(self, superficie, invertir=False):
        """Dibuja la flecha adaptándose a la inversión del tablero."""
        ancho_cuerpo = 12
        radio_punta = 22

        # 1. TRASLACIÓN DE COORDENADAS (La clave del error)
        # Calculamos la posición visual de inicio y fin según el bando
        # Si invertir es True, la fila 0 pasa a ser 7 y la col 0 pasa a ser 7
        f_ini = 7 - self.inicio[0] if invertir else self.inicio[0]
        c_ini = 7 - self.inicio[1] if invertir else self.inicio[1]
        f_fin = 7 - self.fin[0] if invertir else self.fin[0]
        c_fin = 7 - self.fin[1] if invertir else self.fin[1]

        # 2. CONVERSIÓN A PÍXELES DINÁMICA
        pos_ini_px = pygame.Vector2(
            c_ini * self.tam_cuadro + self.tam_cuadro // 2,
            f_ini * self.tam_cuadro + self.tam_cuadro // 2,
        )
        pos_fin_px = pygame.Vector2(
            c_fin * self.tam_cuadro + self.tam_cuadro // 2,
            f_fin * self.tam_cuadro + self.tam_cuadro // 2,
        )

        # Optimizacion: Crear una superficie pequeña solo para la flecha, no de toda la pantalla
        margin = radio_punta + 10
        min_x = min(pos_ini_px.x, pos_fin_px.x) - margin
        max_x = max(pos_ini_px.x, pos_fin_px.x) + margin
        min_y = min(pos_ini_px.y, pos_fin_px.y) - margin
        max_y = max(pos_ini_px.y, pos_fin_px.y) + margin
        
        temp_surface = pygame.Surface((max_x - min_x, max_y - min_y), pygame.SRCALPHA)
        offset_draw = pygame.Vector2(min_x, min_y)

        direccion = pos_fin_px - pos_ini_px
        if direccion.length() == 0:
            return

        # Ángulo para la punta
        angulo = math.atan2(-direccion.y, direccion.x)

        # Acortamos el cuerpo para que no sobresalga de la punta
        fin_cuerpo = pos_fin_px - direccion.normalize() * (radio_punta * 0.8)

        # Dibujar con el offset local
        pygame.draw.line(temp_surface, self.color, pos_ini_px - offset_draw, fin_cuerpo - offset_draw, ancho_cuerpo)

        # Dibujar Punta (Triángulo)
        offset_angulo = math.radians(150)
        punto1 = pos_fin_px
        punto2 = (pos_fin_px + pygame.Vector2(
                math.cos(angulo + offset_angulo), -math.sin(angulo + offset_angulo)
            ) * radio_punta)
        punto3 = (pos_fin_px + pygame.Vector2(
                math.cos(angulo - offset_angulo), -math.sin(angulo - offset_angulo)
            ) * radio_punta)

        pygame.draw.polygon(temp_surface, self.color, [p - offset_draw for p in [punto1, punto2, punto3]])

        superficie.blit(temp_surface, (min_x, min_y))