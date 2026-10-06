"""Control central de la ventana Toplevel/CTkToplevel del módulo activo (Escape = cerrar)."""

import tkinter as tk


def _invocar_protocolo_cierre(window):
    """
    Ejecuta el callback WM_DELETE_WINDOW si existe (misma lógica que la X).
    Así Ajedrez puede llamar a cerrar_juego y liberar el hilo de Pygame.
    """
    try:
        cmd = window.tk.call("wm", "protocol", window._w, "WM_DELETE_WINDOW")
    except tk.TclError:
        cmd = ""
    if cmd:
        try:
            window.tk.eval(cmd)
            return
        except tk.TclError:
            pass
    try:
        if window.winfo_exists():
            window.destroy()
    except Exception:
        pass


class ModuleManager:
    """Singleton: una ventana de módulo registrada; Escape dispara el cierre correcto."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._ventana_activa = None
        return cls._instancia

    def open_module(self, window):
        """Registra la ventana del módulo y aplica atajo Escape."""
        self.close_module()
        if window is None:
            return
        self._ventana_activa = window
        self._configure_module(window)

    def close_module(self):
        """Cierra el módulo activo respetando protocol WM_DELETE_WINDOW."""
        win = self._ventana_activa
        self._ventana_activa = None
        if win is not None:
            try:
                if win.winfo_exists():
                    _invocar_protocolo_cierre(win)
            except Exception:
                pass
        self._on_module_close()

    def _configure_module(self, window):
        """Escape equivale a pulsar la X (protocolo de cierre)."""

        def _escape_cerrar(event=None):
            if self._ventana_activa is window:
                _invocar_protocolo_cierre(window)
            return "break"

        try:
            window.bind("<Escape>", _escape_cerrar)
        except Exception:
            pass

        def _al_destruir(_event=None):
            if self._ventana_activa is window:
                self._ventana_activa = None
                self._on_module_close()

        try:
            window.bind("<Destroy>", _al_destruir, add="+")
        except Exception:
            pass

    def _on_module_close(self):
        """Hook interno tras cerrar o destruir el módulo (extensible)."""
        pass
