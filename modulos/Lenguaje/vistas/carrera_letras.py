"""Vistas del módulo vistas."""

import customtkinter as ctk
import time
import random
from .base import JuegoBase
from ..dominio.juegos import CarreraLetras
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_preguntas_carrera
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro


class VistaCarreraLetras(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Carrera de Letras Espejo", "#E74C3C")

        todas_las_preguntas = obtener_preguntas_carrera()
        num_rondas = 15
        preguntas_seleccionadas = random.sample(
            todas_las_preguntas, min(num_rondas, len(todas_las_preguntas))
        )
        self.juego = CarreraLetras(preguntas_seleccionadas)
        self.gestor = GestorEstado()

        # Estadísticas para el resumen
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()

        self.start_time = time.time()
        self.timer_id = None
        self.configurar_ui()
        self._update_timer()
        self.mostrar_pregunta()

    def configurar_ui(self):
        # Contenedor para los textos centrales
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.pack(expand=True)

        self.lbl_instrucciones = ctk.CTkLabel(
            center_frame,
            text="¿La palabra mostrada es igual a la palabra original?",
            font=("Verdana", 24, "bold"),
            text_color="#2B2D42",
        )
        self.lbl_instrucciones.pack(pady=20)

        self.lbl_original = ctk.CTkLabel(
            center_frame, text="", font=("Verdana", 50, "bold"), text_color="#2E7D32"
        )
        self.lbl_original.pack(pady=15)

        self.lbl_muestra = ctk.CTkLabel(
            center_frame, text="", font=("Verdana", 45), text_color="#C62828"
        )
        self.lbl_muestra.pack(pady=15)

        self.frame_botones = ctk.CTkFrame(center_frame, fg_color="transparent")
        self.frame_botones.pack(pady=30)

        # Estabilizar el grid para que el crecimiento de los botones no mueva los textos
        self.frame_botones.grid_columnconfigure(0, minsize=220)
        self.frame_botones.grid_columnconfigure(1, minsize=220)
        self.frame_botones.grid_rowconfigure(0, minsize=100)

        # --- Caja de Instrucciones (Superior Izquierda) ---
        self.instruction_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFF9C4",
            corner_radius=15,
            border_width=2,
            border_color="#BCAAA4",
            width=350,
            height=150,
        )
        self.instruction_frame.place(x=20, y=20)
        ctk.CTkLabel(
            self.instruction_frame,
            text="📝 INSTRUCCIONES:\n\nObserva bien ambas palabras. ¿Son exactamente iguales o alguna letra está al revés?",
            font=("Verdana", 14, "bold"),
            text_color="#4E342E",
            wraplength=310,
            justify="left",
        ).pack(padx=10, pady=10, fill="both", expand=True)

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
            text="Pregunta: 1 / 8",
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

        self.btn_si = ctk.CTkButton(
            self.frame_botones,
            text="SÍ ✅",
            width=180,
            height=80,
            fg_color="#27AE60",
            hover_color=self._lighten_color("#27AE60"),
            command=lambda: self.responder(True),
            font=("Verdana", 24, "bold"),
            corner_radius=40,
            border_width=4,
            border_color="#1B5E20",
        )
        self.btn_si.grid(row=0, column=0, padx=20)

        self.btn_no = ctk.CTkButton(
            self.frame_botones,
            text="NO ❌",
            width=180,
            height=80,
            fg_color="#C0392B",
            hover_color=self._lighten_color("#C0392B"),
            command=lambda: self.responder(False),
            font=("Verdana", 24, "bold"),
            corner_radius=40,
            border_width=4,
            border_color="#7B1F16",
        )
        self.btn_no.grid(row=0, column=1, padx=20)

        self.lbl_feedback = ctk.CTkLabel(
            center_frame, text="", font=("Verdana", 18, "italic")
        )
        self.lbl_feedback.pack(pady=10)

    def mostrar_pregunta(self):
        if self.juego.completado:
            self.finalizar("¡Has completado la carrera de letras!")
            return

        # Reiniciar cronómetro y actualizar ronda
        self.start_time = time.time()
        self.lbl_ronda.configure(
            text=f"Pregunta: {self.juego.indice + 1} / {len(self.juego.preguntas)}"
        )

        actual = self.juego.pregunta_actual()
        self.lbl_original.configure(text=f"Original: {actual.original}")
        self.lbl_muestra.configure(text=f"Muestra: {actual.muestra}")
        self.lbl_feedback.configure(
            text="Elige la respuesta correcta", text_color="#5D4037"
        )

    def responder(self, es_igual: bool):
        correcto = self.juego.verificar(es_igual)
        if correcto:
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.lbl_feedback.configure(
                text="¡Correcto! Avanzando...", text_color="#2ECC71"
            )
        else:
            self.errores += 1
            AudioService.reproducir("incorrecto")
            self.lbl_feedback.configure(
                text="No es correcto. Intenta de nuevo.", text_color="#E74C3C"
            )

        self.after(800, self.mostrar_pregunta)

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

        notificar_logro("lenguaje_nivel_3", parent=self)
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
            text="📜 REPORTE DE LA CARRERA 📜",
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

        crear_linea_stat(stats_frame, "✅ Palabras Correctas:", self.aciertos, "#27AE60")
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
            from .carrera_letras import VistaCarreraLetras
            VistaCarreraLetras(parent)

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
            from .escribe_palabra import VistaEscribePalabra
            VistaEscribePalabra(parent)

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