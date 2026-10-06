"""Utilidad para notificar logros desbloqueados desde cualquier módulo."""
import customtkinter as ctk
from core.gestor_estado import GestorEstado
from core.logros_config import MENSAJES_LOGRO
from core.theme import FONT_NAME

class VentanaLogroCustom(ctk.CTkToplevel):
    """Ventana modal estilizada para anuncios de logros con la temática del software."""
    def __init__(self, master, nombre_logro):
        super().__init__(master)
        self.title("¡Logro Conseguido!")
        self.geometry("550x380")
        self.configure(fg_color="#E3F2FD") # Celeste Mundo Escolar
        
        # Configuración de ventana modal
        self.transient(master)
        self.grab_set()
        
        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.winfo_screenheight() // 2) - (380 // 2)
        self.geometry(f"+{x}+{y}")

        # Tarjeta blanca interna para resaltar el contenido
        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=25, border_width=2, border_color="#1976D2")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="🏆", font=("Arial", 60)).pack(pady=(20, 0))
        
        ctk.CTkLabel(
            frame, 
            text="FELICIDADES\nHAS DESBLOQUEADO UN LOGRO", 
            font=(FONT_NAME, 20, "bold"), 
            text_color="#1976D2",
            justify="center"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            frame, 
            text=f"¡CONSEGUISTE: {nombre_logro.upper()}!", 
            font=(FONT_NAME, 15, "bold"), 
            text_color="#333",
            wraplength=450
        ).pack(pady=5)

        ctk.CTkLabel(
            frame, 
            text="VE A VER TUS LOGROS DESBLOQUEADOS\nEN LA SECCION DE LOGROS", 
            font=(FONT_NAME, 12), 
            text_color="#666",
            justify="center"
        ).pack(pady=(5, 20))

        ctk.CTkButton(
            frame, 
            text="¡ESTÁ BIEN!", 
            font=(FONT_NAME, 14, "bold"), 
            fg_color="#2196F3", 
            hover_color="#1976D2", 
            corner_radius=20, 
            height=40, 
            command=self.destroy
        ).pack(pady=(0, 20))

def notificar_logro(logro_id: str, parent=None) -> bool:
    """Desbloquea un logro y muestra mensaje si es nuevo."""
    gestor = GestorEstado()
    if gestor.desbloquear_logro(logro_id):
        nombre = MENSAJES_LOGRO.get(logro_id, logro_id)
        
        # Si no hay parent (llamada desde hilos o lógica pura), buscamos el root
        if parent is None:
            from core.module_factory import get_main_root
            parent = get_main_root()
            
        if parent:
            VentanaLogroCustom(parent, nombre)
        return True
    return False
