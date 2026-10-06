"""Factory Method: carga dinámica de módulos educativos (vistas embebidas)."""

import importlib
import logging

from core.module_manager import ModuleManager

logger = logging.getLogger(__name__)
_main_root = None


def set_main_root(root):
    """Debe llamarse desde main tras crear la ventana principal (CTk)."""
    global _main_root
    _main_root = root


def get_main_root():
    return _main_root


class ModuleFactory:
    """
    Fábrica que instancia/importa dinámicamente los módulos
    según su identificador. Cada módulo expone crear_frame(parent, on_back).
    """

    SUBJECTS = {
        "lectura_escritura": {
            "nombre": "Lectura y Escritura",
            "icono": "📚",
            "imagen": "imagenes/lectura.png",
            "import_path": "modulos.Lenguaje.lenguaje_menu",
            "callable": "crear_frame",
            "needs_thread": False,
        },
        "ajedrez": {
            "nombre": "Ajedrez",
            "icono": "♟️",
            "imagen": "imagenes/ajedrez.png",
            "import_path": "modulos.Ajedrez.main_ajedrez",
            "callable": "crear_frame",
            "needs_thread": False,
        },
        "computacion": {
            "nombre": "Computación",
            "icono": "💻",
            "imagen": "imagenes/computacion.png",
            "import_path": "modulos.Computacion.computacion_menu",
            "callable": "crear_frame",
            "needs_thread": False,
        },
        "robotica": {
            "nombre": "Robotica",
            "icono": "🤖",
            "imagen": "imagenes/robotica.png",
            "import_path": "modulos.Robotica.robotica_menu",
            "callable": "crear_frame",
            "needs_thread": False,
            "bg": "#1A1C23",
            "sidebar": "#2D323E",
            "border": "#00E5FF",
            "text": "#E0E0E0",
            "hover": "#3E4556"
        },
        "dibujo": {
            "nombre": "Dibujo",
            "icono": "🎨",
            "imagen": "imagenes/dibujo.png",
            "import_path": "modulos.Dibujo.vistas.app.paint_app",
            "callable": "crear_frame",
            "needs_thread": False,
        },
    }

    @staticmethod
    def get_module_frame(subject_id, parent, on_back_callback):
        """Devuelve un CTkFrame con el contenido del módulo embebido."""
        config = ModuleFactory.SUBJECTS.get(subject_id)
        if not config:
            return None

        try:
            module = importlib.import_module(config["import_path"])
            crear_frame = getattr(module, config["callable"])
        except (ImportError, AttributeError):
            logger.exception("Error cargando módulo %s", subject_id)
            return None

        try:
            frame = crear_frame(parent, on_back_callback)
            if frame is not None:
                frame._volver_callback = on_back_callback

                def _escape_volver(_event=None):
                    if callable(on_back_callback):
                        on_back_callback()
                    return "break"

                frame.bind("<Escape>", _escape_volver)
                ModuleManager().open_module(frame)
            return frame
        except Exception:
            logger.exception("Error al crear frame de %s", subject_id)
            return None

    @staticmethod
    def get_launcher(subject_id):
        """Compatibilidad: devuelve función que embebe en el panel si hay root."""

        def launcher():
            root = get_main_root()
            if root is None:
                return
            import main as main_mod

            main_mod.launch_subject(subject_id)

        return launcher


SUBJECTS = ModuleFactory.SUBJECTS
