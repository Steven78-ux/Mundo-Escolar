"""Funciones auxiliares de interfaz de usuario para la aplicación."""

import customtkinter as ctk

def crear_navbar(window, title, color):
    """
    Crea una barra de navegación en la parte superior con un botón de salida estilo Windows.
    """
    navbar = ctk.CTkFrame(window, fg_color=color, height=50)
    navbar.pack(side="top", fill="x")
    
    # Título del módulo
    label = ctk.CTkLabel(navbar, text=title, font=("Arial", 16, "bold"), text_color="white")
    label.pack(side="left", padx=20, pady=10)
    
    # Botón de Salida estilo Windows (Rojo con X)
    btn_salir = ctk.CTkButton(
        navbar,
        text="❌ CERRAR",
        width=100,
        fg_color="#D32F2F",    # Rojo Windows
        hover_color="#B71C1C", # Rojo oscuro al pasar el mouse
        command=window.destroy # Cierra la ventana actual
    )
    btn_salir.pack(side="right", padx=10, pady=8)