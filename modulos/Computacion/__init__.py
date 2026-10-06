"""Módulo Computación (Mundo Escolar).

Arquitectura por capas (alineada al resto de materiales):
- `config/`: rutas y constantes compartidas.
- `domain/`: contratos (`BaseModule`) y datos de mecanografía (`texts`).
- `services/`: lógica de mecanografía y estadísticas (`game_utils`).
- `views/`: interfaz Pygame (menú, mouse, componentes).

El menú principal invoca `abrir_menu_computacion` vía `core.module_factory.ModuleFactory`.
"""

from modulos.Computacion.computacion_menu import abrir_menu_computacion

__all__ = ["abrir_menu_computacion"]
