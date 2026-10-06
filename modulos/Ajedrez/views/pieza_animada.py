"""Vistas del módulo views."""

import pygame
import os
from ..domain.pieza import Pieza


class PiezaAnimada(Pieza):
    """Representación visual con animaciones y caché de imágenes."""

    _CACHE_IMAGENES = {}

    def __init__(self, tipo, color, fila, col, tam_cuadro=75):
        super().__init__(tipo, color, fila, col)
        self.tam_cuadro = tam_cuadro
        self.velocidad_suavizado = 0.7
        self.imagen = self._cargar_imagen()
        self.x_visual = None
        self.y_visual = None

    def _cargar_imagen(self):
        """Carga la imagen usando un sistema de caché para mejorar rendimiento."""
        key = f"{self.tipo}_{self.color}_{self.tam_cuadro}"
        if key in self._CACHE_IMAGENES:
            return self._CACHE_IMAGENES[key]

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(
            base_dir, "assets", "piezas_animadas", f"{self.tipo}_{self.color}.png"
        )

        try:
            img = pygame.image.load(ruta_imagen).convert_alpha()
            tam = int(
                self.tam_cuadro * 0.75
            )  # Tamaño ajustado para que luzcan bien dentro del cuadro
            res = pygame.transform.scale(img, (tam, tam))
            self._CACHE_IMAGENES[key] = res
            return res
        except (pygame.error, FileNotFoundError):
            cuadro_rosa = pygame.Surface(
                (self.tam_cuadro, self.tam_cuadro), pygame.SRCALPHA
            )
            cuadro_rosa.fill((255, 192, 203, 180))  # Rosa con transparencia
            pygame.draw.rect(cuadro_rosa, (255, 0, 0), cuadro_rosa.get_rect(), 2)
            return cuadro_rosa

    def _calcular_destino(self, offset_x, offset_y, invertir):
        """Helper centralizado para calcular coordenadas en pantalla."""
        f_v, c_v = (7 - self.fila, 7 - self.col) if invertir else (self.fila, self.col)
        tx = offset_x + c_v * self.tam_cuadro
        ty = offset_y + f_v * self.tam_cuadro
        return tx, ty

    def actualizar_animacion(self, offset_x, offset_y, invertir=False):
        """Calcula la nueva posición visual acercándola a la posición lógica del tablero."""
        target_x, target_y = self._calcular_destino(offset_x, offset_y, invertir)

        if self.x_visual is None:
            self.x_visual = target_x
            self.y_visual = target_y
            return

        dx = target_x - self.x_visual
        dy = target_y - self.y_visual

        if abs(dx) > 1.0 or abs(dy) > 1.0:
            self.x_visual += dx * self.velocidad_suavizado
            self.y_visual += dy * self.velocidad_suavizado
        else:
            self.x_visual = target_x
            self.y_visual = target_y

    def esta_animando(self, offset_x, offset_y, invertir=False):
        """Devuelve True si la posición visual aún no ha llegado a la posición lógica."""
        if self.x_visual is None or self.y_visual is None:
            return False
        target_x, target_y = self._calcular_destino(offset_x, offset_y, invertir)

        return (
            abs(self.x_visual - target_x) > 0.5 or abs(self.y_visual - target_y) > 0.5
        )

    def dibujar(self, pantalla, offset=(0, 0), invertir=False):
        self.actualizar_animacion(offset[0], offset[1], invertir)
        centro_offset = (self.tam_cuadro - self.imagen.get_width()) // 2
        pantalla.blit(
            self.imagen,
            (self.x_visual + centro_offset, self.y_visual + centro_offset),
        )

    def __repr__(self):
        return f"PiezaAnimada({self.color[:1].upper()}{self.tipo[:2]} ({self.fila},{self.col}))"