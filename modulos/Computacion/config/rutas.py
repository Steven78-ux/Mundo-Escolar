"""Rutas del proyecto: un solo lugar para localizar assets compartidos (DRY)."""

import os

# modulos/Computacion/config -> subir 3 niveles = raíz del repo Mundo-Escolar
_RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def raiz_proyecto_mundo_escolar() -> str:
    """Directorio raíz del repositorio (donde está main.py y Super Meatball.ttf)."""
    return _RAIZ_PROYECTO


def ruta_fuente_mundo_escolar() -> str:
    """Fuente titular compartida con la app principal."""
    return os.path.join(_RAIZ_PROYECTO, "Super Meatball.ttf")
