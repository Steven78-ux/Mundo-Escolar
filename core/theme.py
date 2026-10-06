"""Tema visual compartido entre main.py y todos los módulos educativos."""
import os
import sys

from tkextrafont import Font

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLORS = {
    "bg": "#87CEEB",
    "sidebar": "#4DA3FF",
    "sidebar_hover": "#3C5179",
    "text_dark": "#2B2B2B",
    "white": "#FFFFFF",
    "card1": "#00B1B1",
    "card2": "#00925A",
    "card3": "#E88800",
    "card4": "#2040E0",
    "card5": "#7E2BB3",
    "card6": "#B12300",
    "progress_fill": "#4DA3FF",
    "progress_bg": "#E0E0E0",
    "bronze": "#CD7F32",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "locked": "#E0E0E0",
    "success": "#27AE60",
    "danger": "#E74C3C",
    "warning": "#F39C12",
}

try:
    Font(file=os.path.join(BASE_DIR, "Super Meatball.ttf"), family="Super Meatball")
    FONT_NAME = "Super Meatball"
except Exception:
    FONT_NAME = "Arial Rounded MT Bold"


def fuentes_responsivas(ancho_pantalla: int) -> dict:
    """Calcula tamaños de fuente proporcionales al ancho de pantalla."""
    ancho = max(1200, min(ancho_pantalla, 2560))
    return {
        "titulo": (FONT_NAME, max(20, min(int(ancho / 36), 42)), "bold"),
        "subtitulo": (FONT_NAME, max(14, min(int(ancho / 50), 32)), "bold"),
        "sidebar": (FONT_NAME, max(12, min(int(ancho / 60), 18))),
        "botones": (FONT_NAME, max(12, min(int(ancho / 68), 18))),
        "tarjetas": (FONT_NAME, max(11, min(int(ancho / 80), 18))),
        "pequeno": (FONT_NAME, max(10, min(int(ancho / 95), 14))),
    }


def tamano_tarjeta(ancho: int, alto: int) -> tuple:
    """Tamaño proporcional para imágenes de tarjetas del menú principal."""
    ancho = max(160, min(ancho, 2560))
    alto = max(120, min(alto, 1440))
    return (
        max(160, min(int(ancho * 0.14), 300)),
        max(110, min(int(alto * 0.14), 180)),
    )


# Fuentes por defecto (se actualizan en main al redimensionar)
FONTS = fuentes_responsivas(1920)
