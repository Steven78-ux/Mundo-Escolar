"""Vistas del módulo vistas."""

import customtkinter as ctk
import random
import time
from .base import JuegoBase
from ..dominio.juegos import Rimas
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_rimas
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro

class VistaRimas(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Rimas Divertidas", "#F39C12")
        
        # Selección aleatoria de 15 rimas
        todas_las_rimas = obtener_rimas()
        rimas_seleccionadas = random.sample(
            todas_las_rimas, min(15, len(todas_las_rimas))
        )
        
        self.juego = Rimas(rimas_seleccionadas)
        self.gestor = GestorEstado()

        # Estadísticas para el resumen
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()

        self.start_time = time.time()
        self.timer_id = None
        self.configurar_ui()
        self._update_timer()
        self.siguiente_pregunta()

    def configurar_ui(self):
        # Contenedor central para el juego
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(expand=True)

        self.lbl_palabra = ctk.CTkLabel(
            content_frame, 
            text="", 
            font=("Verdana", 42, "bold"),
            text_color="#2B2D42"
        )
        self.lbl_palabra.pack(pady=(0, 10))

        # Etiqueta para la pista dinámica
        self.lbl_pista = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Verdana", 20, "italic"),
            text_color="#E67E22"
        )
        self.lbl_pista.pack(pady=(0, 30))

        self.frame_opciones = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.frame_opciones.pack(pady=20)

        # Botones de opciones con estilo 3D y temática naranja
        self.btn_op1 = ctk.CTkButton(
            self.frame_opciones, 
            text="", 
            width=280, 
            height=100,
            font=("Verdana", 28, "bold"), 
            corner_radius=25,
            border_width=4,
            border_color=self.color_borde_tema,
            fg_color=self.color_tema,
            hover_color=self._lighten_color(self.color_tema),
            command=lambda: self.verificar(0)
        )
        self.btn_op1.grid(row=0, column=0, padx=25)
        
        self.btn_op2 = ctk.CTkButton(
            self.frame_opciones, 
            text="", 
            width=280, 
            height=100,
            font=("Verdana", 28, "bold"), 
            corner_radius=25,
            border_width=4,
            border_color=self.color_borde_tema,
            fg_color=self.color_tema,
            hover_color=self._lighten_color(self.color_tema),
            command=lambda: self.verificar(1)
        )
        self.btn_op2.grid(row=0, column=1, padx=25)

        self.lbl_feedback = ctk.CTkLabel(
            content_frame, 
            text="¿Cuál suena igual?", 
            font=("Verdana", 20, "bold"),
            text_color="#5D4037"
        )
        self.lbl_feedback.pack(pady=30)

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
            text="📝 INSTRUCCIONES:\n\nEscucha la palabra principal y elige cuál de las dos opciones termina con el mismo sonido.",
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

    def siguiente_pregunta(self):
        if self.juego.completado:
            self.btn_op1.configure(state="disabled")
            self.btn_op2.configure(state="disabled")
            self.finalizar("¡Eres un campeón de las rimas!")
            return
            
        actual = self.juego.pregunta_actual()
        if actual is None:
            self.finalizar("¡Eres un campeón de las rimas!")
            return

        self.lbl_ronda.configure(
            text=f"Ronda: {self.juego.indice + 1} / {len(self.juego.preguntas)}"
        )
        
        self.lbl_palabra.configure(text=f"¿Qué rima con {actual.palabra.upper()}?")
        
        # Pista: Mostrar la terminación (últimas 3 letras)
        terminacion = actual.palabra[-3:].lower()
        self.lbl_pista.configure(text=f"💡 Pista: Busca algo que termine en '...{terminacion}'")
        
        self.btn_op1.configure(text=actual.opciones[0], state="normal", fg_color=self.color_tema)
        self.btn_op2.configure(text=actual.opciones[1], state="normal", fg_color=self.color_tema)
        self.lbl_feedback.configure(text="¡Tú puedes hacerlo!", text_color="#5D4037")

    def verificar(self, idx):
        actual = self.juego.pregunta_actual()
        if actual is None:
            return

        opcion = actual.opciones[idx]
        if self.juego.verificar(opcion):
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.btn_op1.configure(state="disabled")
            self.btn_op2.configure(state="disabled")
            if idx == 0:
                self.btn_op1.configure(fg_color="#27AE60")
            else:
                self.btn_op2.configure(fg_color="#27AE60")
            
            self.lbl_feedback.configure(text="¡Excelente! ¡Riman perfecto!", text_color="#2ECC71")
            self.after(1500, self.siguiente_pregunta)
        else:
            self.errores += 1
            AudioService.reproducir("incorrecto")
            if idx == 0:
                self.btn_op1.configure(fg_color="#C0392B")
                self.after(800, lambda: self.btn_op1.configure(fg_color=self.color_tema))
            else:
                self.btn_op2.configure(fg_color="#C0392B")
                self.after(800, lambda: self.btn_op2.configure(fg_color=self.color_tema))
                
            self.lbl_feedback.configure(text="Esa no rima... ¡Prueba la otra!", text_color="#E74C3C")

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

        notificar_logro("lenguaje_nivel_5", parent=self)
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
            text="📜 REPORTE DE RIMAS 📜",
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

        crear_linea_stat(stats_frame, "✅ Rimas Correctas:", self.aciertos, "#27AE60")
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
            from .rimas import VistaRimas
            VistaRimas(parent)

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
            from .ordena_letras import VistaOrdenaLetras
            VistaOrdenaLetras(parent)

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