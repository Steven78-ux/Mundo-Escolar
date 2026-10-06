"""Vistas del módulo vistas."""

import customtkinter as ctk
import random
import time
from .base import JuegoBase
from ..dominio.juegos import LeeEncuentra
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_frases_lectura
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro

class VistaLeeEncuentra(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Lee y Encuentra", "#E67E22")
        
        # Selección aleatoria de 15 frases para el nivel
        todas_las_frases = obtener_frases_lectura()
        frases_seleccionadas = random.sample(
            todas_las_frases, min(15, len(todas_las_frases))
        )
        
        self.juego = LeeEncuentra(frases_seleccionadas)
        self.gestor = GestorEstado()

        # Diccionario para convertir emojis a palabras para el refuerzo lector
        self.EMOJI_A_PALABRA = {
            "🐱": "gato", "🚗": "auto", "🐢": "tortuga", "🌙": "luna", "📚": "libro",
            "🍎": "manzana", "🐕": "perro", "🐵": "mono", "🐦": "pájaro", "🐝": "abeja",
            "🐰": "conejo", "🦁": "león", "☀️": "sol", "🌸": "flor", "🌳": "árbol",
            "❄️": "nieve", "🔥": "fuego", "✏️": "lápiz", "🍦": "helado", "🥛": "leche",
            "👑": "corona", "🎈": "globo", "👟": "zapato", "🐔": "gallina", "🧀": "queso",
            "⛵": "barco", "⏰": "reloj", "🧥": "chaqueta", "🤡": "payaso", "🕷️": "araña",
            "🌽": "maíz", "🥖": "pan", "🦷": "diente"
        }

        # Estadísticas para el resumen
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()

        self.start_time = time.time()
        self.timer_id = None
        
        self.configurar_ui()
        self._update_timer()
        self.siguiente_frase()

    def configurar_ui(self):
        # Contenedor central para el juego (dentro del papel)
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(expand=True)

        self.lbl_frase = ctk.CTkLabel(
            content_frame, 
            text="", 
            font=("Verdana", 32, "bold"), 
            text_color="#2B2D42",
            wraplength=800
        )
        self.lbl_frase.pack(pady=(0, 30))

        self.lbl_frase_texto = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Verdana", 24, "italic"),
            text_color="#8D6E63"
        )
        self.lbl_frase_texto.pack(pady=(0, 20))

        self.frame_opciones = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.frame_opciones.pack(pady=20)

        self.botones = []
        for i in range(3):
            btn = ctk.CTkButton(
                self.frame_opciones, 
                text="", 
                font=("Segoe UI Emoji", 80),
                width=220, 
                height=220, 
                corner_radius=30,
                border_width=5,
                border_color=self.color_borde_tema,
                fg_color="white",
                text_color="black",
                hover_color="#F5F5F5",
                command=lambda idx=i: self.verificar(idx),
                anchor="center"
            )
            btn.grid(row=0, column=i, padx=25)
            self.botones.append(btn)

        self.lbl_feedback = ctk.CTkLabel(
            content_frame, 
            text="Lee y elige el dibujo correcto", 
            font=("Verdana", 18, "italic"),
            text_color="#5D4037"
        )
        self.lbl_feedback.pack(pady=40)

        # --- Caja de Instrucciones (Superior Izquierda) ---
        self.instruction_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFF9C4",
            corner_radius=15,
            border_width=2,
            border_color="#BCAAA4",
            width=350,
            height=130,
        )
        self.instruction_frame.place(x=20, y=20)
        ctk.CTkLabel(
            self.instruction_frame,
            text="📝 INSTRUCCIONES:\n\nLee la frase con mucha atención y selecciona el dibujo que corresponde a lo que acabas de leer.",
            font=("Verdana", 14, "bold"),
            text_color="#4E342E",
            wraplength=310,
            justify="left",
        ).pack(padx=15, pady=15, fill="both", expand=True)

        # --- Indicador de Progreso y Cronómetro (Superior Derecha) ---
        self.info_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFF9C4",
            corner_radius=15,
            border_width=2,
            border_color="#BCAAA4",
            width=200,
            height=120,
        )
        self.info_frame.place(relx=0.98, y=20, anchor="ne")
        self.lbl_ronda = ctk.CTkLabel(
            self.info_frame,
            text="Ronda: 1 / 15",
            font=("Verdana", 14, "bold"),
            text_color="#4E342E",
        )
        self.lbl_ronda.pack(pady=(15, 5))
        self.lbl_timer = ctk.CTkLabel(
            self.info_frame,
            text="Tiempo: 00:00",
            font=("Verdana", 18, "bold"),
            text_color="#E67E22",
        )
        self.lbl_timer.pack(pady=(5, 15))

    def siguiente_frase(self):
        if self.juego.completado:
            self.finalizar("¡Excelente lectura! Has encontrado todos los dibujos.")
            return
            
        actual = self.juego.pregunta_actual()
        self.lbl_ronda.configure(
            text=f"Ronda: {self.juego.indice + 1} / {len(self.juego.preguntas)}"
        )
        
        # Ocultamos el emoji de la frase para incentivar la comprensión lectora y la inferencia
        # lógica basada en el contexto de la oración.
        frase_desafio = actual.frase.replace(actual.correcta, "[ ? ]")
        self.lbl_frase.configure(text=frase_desafio)
        for i, btn in enumerate(self.botones):
            opcion = actual.opciones[i]
            # Ajuste de tamaño: los iconos se ven bien a 80, pero las palabras necesitan menos para centrarse
            # Usamos un umbral de longitud (3 caracteres) para detectar palabras vs iconos/emojis
            f_size = 80 if len(opcion) <= 3 else 35
            btn.configure(
                text=opcion, 
                state="normal",
                fg_color="white",
                font=("Segoe UI Emoji", f_size)
            )
        self.lbl_feedback.configure(text="¿Cuál es el dibujo correcto?", text_color="#5D4037")

    def verificar(self, idx):
        actual = self.juego.pregunta_actual()
        opcion = actual.opciones[idx]
        if self.juego.verificar(opcion):
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.botones[idx].configure(fg_color="#A9DFBF") # Verde claro
            
            # Mostramos la frase completa como confirmación del éxito y refuerzo visual
            self.lbl_frase.configure(text=actual.frase)
            
            # Creamos el refuerzo de texto (ej: "El gato toma leche")
            palabra = self.EMOJI_A_PALABRA.get(actual.correcta, "").lower()
            frase_texto = actual.frase.replace(actual.correcta, palabra)
            self.lbl_frase_texto.configure(text=frase_texto)
            
            self.lbl_feedback.configure(text="¡Muy bien! ¡Leíste perfectamente!", text_color="#2ECC71")
            for btn in self.botones:
                btn.configure(state="disabled")
            self.after(3000, self.siguiente_frase)
        else:
            self.errores += 1
            AudioService.reproducir("incorrecto")
            self.botones[idx].configure(fg_color="#F1948A") # Rojo claro
            self.lbl_feedback.configure(text="Ese no es... Lee de nuevo con cuidado", text_color="#E74C3C")
            self.after(800, lambda: self.botones[idx].configure(fg_color="white"))

    def _update_timer(self):
        """Actualiza el cronómetro en la UI."""
        if not self.winfo_exists():
            return

        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.lbl_timer.configure(text=f"Tiempo: {minutes:02d}:{seconds:02d}")
        self.timer_id = self.after(1000, self._update_timer)

    def finalizar(self, mensaje: str):
        """Detiene el cronómetro al finalizar el juego."""
        if self.timer_id:
            self.after_cancel(self.timer_id)

        notificar_logro("lenguaje_nivel_7", parent=self)
        self.mostrar_resumen()

    def mostrar_resumen(self):
        """Muestra una pantalla de resultados temática similar a los niveles anteriores."""
        # Calcular tiempo total
        total_seconds = int(time.time() - self.global_start_time)
        minutos = total_seconds // 60
        segundos = total_seconds % 60
        tiempo_str = f"{minutos:02d}:{segundos:02d}"

        # Limpiar contenedor principal para mostrar el resumen
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Título de resultados
        ctk.CTkLabel(
            self.main_container,
            text="📜 REPORTE DE LECTURA 📜",
            font=("Verdana", 36, "bold"),
            text_color="#5D4037"
        ).pack(pady=(50, 30))

        # Panel de estadísticas
        stats_frame = ctk.CTkFrame(self.main_container, fg_color="#FFF9C4", corner_radius=20, border_width=2, border_color="#8D6E63")
        stats_frame.pack(pady=20, padx=100, fill="x")

        def crear_linea_stat(parent, etiqueta, valor, color):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=10)
            ctk.CTkLabel(f, text=etiqueta, font=("Verdana", 24, "bold"), text_color="#4E342E").pack(side="left")
            ctk.CTkLabel(f, text=str(valor), font=("Verdana", 24, "bold"), text_color=color).pack(side="right")

        crear_linea_stat(stats_frame, "✅ Lecturas Correctas:", self.aciertos, "#27AE60")
        crear_linea_stat(stats_frame, "❌ Errores cometidos:", self.errores, "#E74C3C")
        crear_linea_stat(stats_frame, "⏱️ Tiempo Total:", tiempo_str, "#E67E22")

        # Contenedor de botones
        btns_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btns_frame.pack(pady=50)

        # Botón Volver (Izquierda)
        ctk.CTkButton(
            btns_frame,
            text="🏠 VOLVER AL MENÚ",
            font=("Verdana", 16, "bold"),
            width=220,
            height=55,
            fg_color="#8D6E63",
            hover_color="#5D4037",
            corner_radius=15,
            command=self.destroy
        ).pack(side="left", padx=20)

        # Botón Reiniciar (Centro)
        def reiniciar():
            parent = self.master
            self.destroy()
            from .lee_encuentra import VistaLeeEncuentra
            VistaLeeEncuentra(parent)

        ctk.CTkButton(
            btns_frame,
            text="🔄 REINICIAR",
            font=("Verdana", 16, "bold"),
            width=220,
            height=55,
            fg_color="#E67E22",
            hover_color="#D35400",
            corner_radius=15,
            command=reiniciar
        ).pack(side="left", padx=20)

        # Botón Siguiente (Derecha)
        def siguiente():
            parent = self.master
            self.destroy()
            from .sopa_letras import VistaSopaLetras
            VistaSopaLetras(parent)

        ctk.CTkButton(
            btns_frame,
            text="➡️ SIGUIENTE NIVEL",
            font=("Verdana", 16, "bold"),
            width=220,
            height=55,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            corner_radius=15,
            command=siguiente
        ).pack(side="left", padx=20)