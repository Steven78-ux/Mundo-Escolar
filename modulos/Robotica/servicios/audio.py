"""Servicio de audio usando pygame."""
import os
import pygame

class AudioService:
    _inicializado = False

    @classmethod
    def _init(cls):
        if not cls._inicializado:
            pygame.mixer.init()
            cls._inicializado = True

    @staticmethod
    def reproducir(texto: str):
        """Reproduce un archivo MP3 desde assets/sonidos/lenguaje/{texto}.mp3"""
        AudioService._init()
        base_dir = os.path.dirname(os.path.abspath(__file__))  # servicios/
        ruta_sonidos = os.path.join(base_dir, '..', '..', 'assets', 'sonidos', 'lenguaje')
        nombre_archivo = f"{texto.lower().replace(' ', '_')}.mp3"
        ruta_completa = os.path.join(ruta_sonidos, nombre_archivo)
        if os.path.exists(ruta_completa):
            pygame.mixer.music.load(ruta_completa)
            pygame.mixer.music.play()
        else:
            print(f"Audio no encontrado: {ruta_completa}")