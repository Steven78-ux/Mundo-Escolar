"""Vistas del módulo vistas."""

import customtkinter as ctk


class JuegoBase(ctk.CTkToplevel):
    """Ventana base para todos los juegos de Lenguaje."""

    def __init__(self, parent, titulo: str, color_tema: str):
        super().__init__(parent)
        self.title(titulo)
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#F0F4F8")  # Fondo claro y amigable

        self.color_tema = color_tema
        self.color_borde_tema = self._darken_color(color_tema)

        # --- CABECERA ESTILO LIBRO ---
        self.header = ctk.CTkFrame(
            self,
            fg_color="#FEF9E7",
            corner_radius=20,
            border_width=4,
            border_color="#8D6E63",
        )
        self.header.pack(fill="x", padx=40, pady=20)

        # Botón Volver (Estilo 3D)
        self.btn_volver = ctk.CTkButton(
            self.header,
            text="⬅ VOLVER",
            width=110,
            height=45,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            border_width=4,
            border_color="#7B241C",
            corner_radius=15,
            font=("Verdana", 12, "bold"),
            command=self.destroy,
        )
        self.btn_volver.place(x=30, rely=0.5, anchor="w")


        ctk.CTkLabel(
            self.header,
            text=f"✨ {titulo.upper()} ✨",
            font=("Verdana", 28, "bold"),
            text_color="#2B2D42",
        ).pack(pady=20)

        # --- CONTENEDOR PRINCIPAL (EL PAPEL) ---
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="#FDF5E6",
            corner_radius=25,
            border_width=15,
            border_color="#4E342E",
        )
        self.main_container.pack(expand=True, fill="both", padx=40, pady=(0, 40))

        self.grab_set()
        self.focus_force()

    def _darken_color(self, hex_color):
        """Genera un tono más oscuro para los bordes 3D."""
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, c - 40) for c in rgb)
        return "#%02x%02x%02x" % new_rgb

    def _lighten_color(self, hex_color):
        """Aclara un color hex para el efecto hover."""
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, c + 30) for c in rgb)
        return "#%02x%02x%02x" % new_rgb