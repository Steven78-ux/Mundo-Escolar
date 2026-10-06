"""Archivo del módulo Dibujo."""

import customtkinter as ctk
from modulos.Dibujo.vistas.app.paint_app import PaintApp

class DibujoMenu(ctk.CTkToplevel):
    """
    Menú principal del módulo de Dibujo.
    Permite acceder al Paint.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Área de Creatividad - Mundo Escolar")
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#F0F9FF") # Celeste pastel
        self.grab_set()
        self.focus_force()

        # Ocultar menú principal
        if self.parent and hasattr(self.parent, "withdraw"):
            self.parent.withdraw()

        # Barra de navegación simple
        navbar = ctk.CTkFrame(self, fg_color="#CAF0F8", height=80, corner_radius=0)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)

        # Botón Regresar
        self.btn_regresar = ctk.CTkButton(navbar, text="⬅ Regresar", 
                                          width=120, height=45,
                                          fg_color="#0077B6", hover_color="#00B4D8",
                                          font=("Arial", 16, "bold"),
                                          command=self.regresar)
        self.btn_regresar.place(relx=0.02, rely=0.5, anchor="w")

        ctk.CTkLabel(navbar, text="🎨 DIBUJO - MENÚ",
                     font=("Arial", 26, "bold"), text_color="#023E8A").pack(expand=True)

        # Contenido
        self.lbl_bienvenida = ctk.CTkLabel(self, text="¡Crea tu obra maestra!",
                                           font=("Arial", 32, "bold"), text_color="#0077B6")
        # Inicialmente fuera de pantalla para la animación
        self.lbl_bienvenida.place(relx=0.5, rely=1.2, anchor="center")

        self.btn_paint = ctk.CTkButton(self, text="🖌️ Abrir Paint",
                                       font=("Arial", 22, "bold"), width=320, height=110,
                                       fg_color="#0077B6", hover_color="#00B4D8",
                                       corner_radius=25,
                                       command=self.abrir_paint)
        self.btn_paint.place(relx=0.5, rely=1.5, anchor="center")

        # Iniciar animaciones después de un breve delay
        self.after(100, lambda: self.animar_elemento(self.lbl_bienvenida, 0.4))
        self.after(200, lambda: self.animar_elemento(self.btn_paint, 0.6))

    def animar_elemento(self, widget, target_rely, current_rely=1.2):
        """Mueve un widget suavemente desde abajo hacia su posición objetivo."""
        if current_rely > target_rely:
            # Reducir la distancia (ajusta 0.03 para velocidad)
            next_rely = max(target_rely, current_rely - 0.04)
            widget.place(relx=0.5, rely=next_rely, anchor="center")
            self.after(10, lambda: self.animar_elemento(widget, target_rely, next_rely))

    def regresar(self):
        if self.parent:
            self.parent.deiconify()
            self.parent.focus_force()
        self.destroy()

    def abrir_paint(self):
        # Crear una nueva ventana Toplevel para el Paint
        paint_window = ctk.CTkToplevel(self)
        paint_window.title("Paint - Mundo Escolar")
        paint_window.attributes("-fullscreen", True)
        PaintApp(paint_window)
        paint_window.grab_set()
        paint_window.focus_force()