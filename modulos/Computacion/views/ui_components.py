"""Componentes reutilizables para interfaz en Pygame."""

from dataclasses import dataclass

import pygame


@dataclass
class Boton:
    texto: str
    rect: pygame.Rect
    color_normal: tuple[int, int, int]
    color_hover: tuple[int, int, int]
    color_texto: tuple[int, int, int] = (255, 255, 255)
    color_borde: tuple[int, int, int] = (222, 226, 230)
    radio: int = 10

    def __post_init__(self) -> None:
        self._cache_render: dict[
            tuple[tuple[int, int, int], pygame.font.Font], pygame.Surface
        ] = {}

    def _get_rendered_text(
        self, fuente: pygame.font.Font, color: tuple[int, int, int]
    ) -> pygame.Surface:
        clave = (color, fuente)
        if clave not in self._cache_render:
            self._cache_render[clave] = fuente.render(self.texto, True, color)
        return self._cache_render[clave]

    def dibujar(
        self,
        superficie: pygame.Surface,
        fuente: pygame.font.Font,
        mouse_pos: tuple[int, int],
    ) -> None:
        color = (
            self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal
        )
        pygame.draw.rect(superficie, color, self.rect, border_radius=self.radio)
        # Borde personalizado para dar un aspecto más tecnológico/neón
        pygame.draw.rect(
            superficie, self.color_borde, self.rect, width=2, border_radius=self.radio
        )
        texto_render = self._get_rendered_text(fuente, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)

    def contiene(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
