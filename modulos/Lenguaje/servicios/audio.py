"""Servicio de audio usando pygame."""
import os
import pygame

class AudioService:
    _inicializado = False
    _cache_sonidos = {}
    _last_warning = None

    @classmethod
    def _init(cls):
        if not cls._inicializado:
            try:
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
                cls._inicializado = True
            except Exception as e:
                print(f"Error al inicializar audio: {e}")

    @staticmethod
    def _play_feedback_tone(frecuencia: int, duracion: float = 0.12, volumen: float = 0.22):
        import array
        import math

        sample_rate = 44100
        num_samples = int(sample_rate * duracion)
        buffer = array.array('h')
        for i in range(num_samples):
            sample = int(volumen * 32767 * math.sin(2 * math.pi * frecuencia * i / sample_rate))
            buffer.append(sample)

        try:
            tono = pygame.mixer.Sound(buffer=buffer)
            tono.play()
        except Exception:
            pass

    @staticmethod
    def reproducir(texto: str):
        """Reproduce un sonido. Busca .mp3, .wav o .ogg en el módulo y en assets."""
        AudioService._init()
        if not AudioService._inicializado:
            return

        nombre_base = texto.strip().lower().replace(' ', '_')
        feedback_tonos = {
            'correcto': 880,
            'incorrecto': 220,
        }

        if nombre_base in feedback_tonos:
            AudioService._play_feedback_tone(feedback_tonos[nombre_base])
            return

        servicios_dir = os.path.dirname(os.path.abspath(__file__))
        modulo_root = os.path.abspath(os.path.join(servicios_dir, '..'))
        candidate_dirs = [
            os.path.join(modulo_root, 'assets', 'sonidos'),
            os.path.join(modulo_root, 'assets', 'Sonidos'),
            os.path.join(modulo_root, 'Sonidos'),
            os.path.join(servicios_dir, '..', '..', '..', 'assets', 'sonidos'),
            os.path.join(servicios_dir, '..', '..', '..', 'assets', 'Sonidos'),
            os.path.join(servicios_dir, '..', '..', '..', 'assets', 'sonidos', 'lenguaje'),
        ]

        extensiones = ['.mp3', '.wav', '.ogg']
        for ruta in candidate_dirs:
            ruta = os.path.abspath(ruta)
            if not os.path.isdir(ruta):
                continue
            try:
                for archivo_real in os.listdir(ruta):
                    nombre_real, ext_real = os.path.splitext(archivo_real)
                    if nombre_real.lower() == nombre_base and ext_real.lower() in extensiones:
                        ruta_completa = os.path.join(ruta, archivo_real)
                        if ruta_completa not in AudioService._cache_sonidos:
                            try:
                                AudioService._cache_sonidos[ruta_completa] = pygame.mixer.Sound(ruta_completa)
                            except Exception:
                                try:
                                    pygame.mixer.music.load(ruta_completa)
                                    pygame.mixer.music.play()
                                except Exception:
                                    pass
                                return
                        AudioService._cache_sonidos[ruta_completa].play()
                        return
            except OSError:
                continue

        if AudioService._last_warning != nombre_base:
            print(f"⚠️ Audio no encontrado: {nombre_base} en las rutas configuradas.")
            AudioService._last_warning = nombre_base