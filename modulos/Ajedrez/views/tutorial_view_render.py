"""Vistas del módulo views."""

import pygame
import os
from .pieza_animada import PiezaAnimada


class TutorialViewRender:
    """Maneja elementos visuales adicionales del tutorial como botones de navegación."""

    def __init__(self, screen, vista_tablero):
        self.screen = screen
        self.vista = vista_tablero
        self._cache_iconos_botones = {}

    def dibujar_botones_subseccion(self, subsecciones, sub_id_actual, mouse_pos):
        """Dibuja los botones laterales de navegación de lecciones."""
        start_x = self.vista.offset_x - 70
        start_y = self.vista.offset_y + 50
        btn_size = 60
        padding = 10
        rects_dict = {}

        for i, subid in enumerate(subsecciones):
            rect = pygame.Rect(
                start_x, start_y + i * (btn_size + padding), btn_size, btn_size
            )

            # Determinar imágenes del botón
            piece_images = self._obtener_imagenes_boton(subid, btn_size)

            # Color y Hover
            color = (0, 212, 255) if subid == sub_id_actual else (40, 45, 60)
            if rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 20) for c in color)
                pygame.draw.rect(self.screen, "white", rect, 2, border_radius=10)

            pygame.draw.rect(self.screen, color, rect, border_radius=10)

            # Dibujar iconos de piezas
            for img, offset in piece_images:
                img_x = rect.centerx - img.get_width() // 2 + offset
                img_y = rect.centery - img.get_height() // 2
                self.screen.blit(img, (img_x, img_y))

            rects_dict[subid] = rect
        return rects_dict

    def _obtener_imagenes_boton(self, subid, size):
        """Helper para obtener las imágenes adecuadas para cada botón de lección con cache."""
        key = (subid, size)
        if key in self._cache_iconos_botones:
            return self._cache_iconos_botones[key]

        img_size = int(size * 0.45)
        res = []
        if subid == "enroque":
            p1 = PiezaAnimada("rey", "blanco", 0, 0, tam_cuadro=img_size).imagen
            p2 = PiezaAnimada("torre", "blanco", 0, 0, tam_cuadro=img_size).imagen
            res = [(p1, -12), (p2, 12)]
        elif subid == "paso":
            p1 = PiezaAnimada("peon", "blanco", 0, 0, tam_cuadro=img_size).imagen
            p2 = PiezaAnimada("peon", "negro", 0, 0, tam_cuadro=img_size).imagen
            res = [(p1, -12), (p2, 12)]
        elif subid == "promocion":
            p1 = PiezaAnimada("peon", "blanco", 0, 0, tam_cuadro=img_size).imagen
            p2 = PiezaAnimada("dama", "blanco", 0, 0, tam_cuadro=img_size).imagen
            res = [(p1, -12), (p2, 12)]
        elif subid == "jaque_mate":
            p1 = PiezaAnimada("rey", "blanco", 0, 0, tam_cuadro=img_size).imagen
            p2 = PiezaAnimada("rey", "negro", 0, 0, tam_cuadro=img_size).imagen
            res = [(p1, -12), (p2, 12)]
        elif subid in ["ahogado", "tablas", "insuficiencia_material"]:
            res = self._cargar_asset_png("empate.png", size)
        elif subid == "jaque":
            res = self._cargar_asset_png("mate.png", size)
        elif subid == "clavada":
            res = self._cargar_asset_png("clavada.png", size)
        else:
            img = PiezaAnimada(subid, "blanco", 0, 0, tam_cuadro=int(size * 0.6)).imagen
            res = [(img, 0)]
        
        self._cache_iconos_botones[key] = res
        return res

    def _cargar_asset_png(self, nombre, size):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "imagenes",
            nombre,
        )
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (int(size * 0.8), int(size * 0.8)))
            return [(img, 0)]
        return []