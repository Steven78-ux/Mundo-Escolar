"""Vistas del módulo views."""

import customtkinter as ctk
import threading
from ..config.tutorial_config import LESSONS


class TutorialAjedrez(ctk.CTkToplevel):
    def __init__(self, parent, tema="Oceano"):
        super().__init__(parent)
        self.tema = tema
        self.title("Academia de Ajedrez")
        self.attributes("-fullscreen", True)
        self.bg_color = "#0D1B2A"
        self.card_color = "#1B263B"
        self.accent_color = "#00E5FF"
        self.configure(fg_color=self.bg_color)
        self.evento_cierre = threading.Event()
        self.setup_ui()
        self.grab_set()

    def setup_ui(self):
        ctk.CTkLabel(
            self,
            text="🚀 ACADEMIA DE CADETES",
            font=("Verdana", 42, "bold"),
            text_color=self.accent_color,
        ).pack(pady=40)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)
        num_cards = len(LESSONS)
        cols = 3
        for i, (lid, data) in enumerate(LESSONS.items()):
            row = i // cols
            col = i % cols
            if row == (num_cards - 1) // cols and num_cards % cols != 0:
                remainder = num_cards % cols
                col = (cols - remainder) // 2 + (i % cols)

            card = ctk.CTkFrame(
                container,
                fg_color=self.card_color,
                width=260,
                height=220,
                corner_radius=30,
                border_width=3,
                border_color=self.accent_color,
            )
            card.grid(row=row, column=col, padx=20, pady=20)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=data["icono"], font=("Arial", 60)).pack(
                pady=(15, 0)
            )
            ctk.CTkLabel(
                card,
                text=data["titulo"],
                font=("Verdana", 18, "bold"),
                text_color="white",
            ).pack()
            ctk.CTkLabel(
                card,
                text=data["desc"],
                font=("Verdana", 13),
                text_color=self.accent_color,
            ).pack()
            ctk.CTkButton(
                card,
                text="ESTUDIAR",
                fg_color="#27AE60",
                corner_radius=15,
                command=lambda l=lid: self.lanzar_leccion(l),
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="VOLVER AL MENÚ",
            fg_color="#00D4FF",
            hover_color="#00B8CC",
            font=("Verdana", 20, "bold"),
            height=55,
            command=self.destroy,
        ).pack(pady=30)

    def lanzar_leccion(self, lid):
        from ..tutorial_ajedrez import VentanaTutorial

        self.evento_cierre.clear()
        threading.Thread(
            target=lambda: VentanaTutorial(
                lid, self.evento_cierre, tema=self.tema
            ).run(),
            daemon=True,
        ).start()

    def destroy(self):
        self.evento_cierre.set()
        super().destroy()