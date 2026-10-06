"""Servicios del módulo services."""

import pygame
import os


class GestorAudio:
    """Servicio centralizado para la gestión de sonidos del juego."""

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Ruta base hacia los assets de sonido
        self.base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "sonidos"
        )

        # Diccionario de sonidos para evitar recargas constantes
        self.sonidos = {
            "movimiento": self._cargar("move.wav"),
            "captura": self._cargar("capture.wav"),
            "jaque": self._cargar("check.wav"),
            "fin": self._cargar("game_over.wav"),
        }

    def _cargar(self, nombre_archivo):
        ruta = os.path.join(self.base_path, nombre_archivo)
        if os.path.exists(ruta):
            return pygame.mixer.Sound(ruta)
        return None

    def reproducir(self, clave):
        """Reproduce el sonido asociado a la clave."""
        sonido = self.sonidos.get(clave)
        if sonido:
            sonido.play()