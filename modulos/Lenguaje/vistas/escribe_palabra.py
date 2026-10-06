"""Vistas del módulo vistas."""

import customtkinter as ctk
import random
import time
from .base import JuegoBase
from ..dominio.juegos import EscribePalabra
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_palabras_escribe
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro

class VistaEscribePalabra(JuegoBase):
    def __init__(self, parent):
        # -------------------------------------------------------------
        # CONFIGURACIÓN INICIAL
        # -------------------------------------------------------------
        super().__init__(parent, "¡Escribe la Palabra!", "#8E44AD")
        
        todas_las_palabras = obtener_palabras_escribe()
        palabras_seleccionadas = random.sample(
            todas_las_palabras, min(15, len(todas_las_palabras))
        )
        
        self.juego = EscribePalabra(palabras_seleccionadas)
        self.gestor = GestorEstado()

        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()
        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        self.start_time = time.time()
        self.timer_id = None

        self.configurar_ui()
        self.siguiente_palabra()
        self._update_timer()

    def configurar_ui(self):
        # -------------------------------------------------------------
        # ELEMENTOS DE LA INTERFAZ (UI)
        # -------------------------------------------------------------
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(expand=True)

        self.lbl_pista_img = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Verdana", 18, "italic", "bold"),
            text_color="#8D6E63",
        )
        self.lbl_pista_img.pack(pady=(0, 5))

        self.img_label = ctk.CTkLabel(content_frame, text="", font=("Segoe UI Emoji", 120))
        self.img_label.pack(pady=(0, 10))

        self.lbl_pista = ctk.CTkLabel(
            content_frame, 
            text="", 
            font=("Verdana", 18, "italic"),
            text_color="#5D4037"
        )
        self.lbl_pista.pack(pady=5)

        self.entry = ctk.CTkEntry(
            content_frame, 
            font=("Verdana", 32, "bold"), 
            width=400, 
            height=60,
            justify="center",
            border_width=3,
            corner_radius=15
        )
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", lambda e: self.verificar())

        self.btn_verificar = ctk.CTkButton(
            content_frame, 
            text="✅ COMPROBAR",
            command=self.verificar, 
            font=("Verdana", 18, "bold"),
            fg_color=self.color_tema,
            hover_color=self._lighten_color(self.color_tema),
            height=50,
            corner_radius=15,
            border_width=3,
            border_color=self.color_borde_tema
        )
        self.btn_verificar.pack(pady=10)

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
            text="📝 INSTRUCCIONES:\n\nObserva la imagen y escribe su nombre. ¡Fíjate bien en la pista!",
            font=("Verdana", 14, "bold"),
            text_color="#4E342E",
            wraplength=310,
            justify="left",
        ).pack(padx=15, pady=15, fill="both", expand=True)

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
            text="Palabra: 1 / 15",
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

    def siguiente_palabra(self):
        if not self.winfo_exists():
            return

        if self.juego.completado:
            self.finalizar("¡Eres un gran escritor!")
            return

        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        actual = self.juego.palabra_actual()
        # -------------------------------------------------------------
        # ACTUALIZACIÓN DE ESTADO VISUAL
        # -------------------------------------------------------------
        self.lbl_ronda.configure(
            text=f"Palabra: {self.juego.indice + 1} / {len(self.juego.palabras)}"
        )
        self.img_label.configure(text=actual.imagen)
        self.lbl_pista_img.configure(
            text="🔍 Ayuda: se revelará pronto...", 
            text_color="#A9A9A9"
        )
        self.lbl_pista.configure(text=f"Pista: Empieza con la letra '{actual.pista}'")
        self.entry.delete(0, "end")
        self.entry.configure(fg_color="white")
        self._focus_entry()

    def _focus_entry(self):
        if self.entry.winfo_exists():
            try:
                self.entry.focus()
            except Exception:
                pass

    def revelar_pista(self):
        actual = self.juego.palabra_actual()
        if actual and not self.pista_revelada:
            self.pista_revelada = True
            self.lbl_pista_img.configure(
                text=f"¿Qué es? ¡Es un {actual.palabra}!", 
                text_color="#8D6E63"
            )

    def verificar(self):
        # -------------------------------------------------------------
        # LÓGICA DE VALIDACIÓN
        # -------------------------------------------------------------
        texto = self.entry.get().strip().upper()
        if self.juego.verificar_escritura(texto):
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.entry.configure(fg_color="#A9DFBF") 
            self.after(1500, self.siguiente_palabra)
        else:
            self.errores += 1
            self.errores_ronda += 1
            if self.errores_ronda >= 4:
                self.revelar_pista()

            AudioService.reproducir("incorrecto")
            self.entry.configure(fg_color="#F1948A")
            self.after(500, self._reset_entry_color)

    def _reset_entry_color(self):
        if self.entry.winfo_exists():
            self.entry.configure(fg_color="white")

    def _update_timer(self):
        if not self.winfo_exists():
            return

        if not self.pista_revelada:
            tiempo_transcurrido_ronda = time.time() - self.tiempo_inicio_ronda
            if tiempo_transcurrido_ronda >= 30:
                self.revelar_pista()

        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.lbl_timer.configure(text=f"Tiempo: {minutes:02d}:{seconds:02d}")
        self.timer_id = self.after(1000, self._update_timer)

    def finalizar(self, mensaje: str):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        notificar_logro("lenguaje_nivel_4", parent=self)
        self.mostrar_resumen()

    def mostrar_resumen(self):
        # -------------------------------------------------------------
        # PANTALLA DE RESULTADOS
        # -------------------------------------------------------------
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
            text="📜 REPORTE DEL ESCRITOR 📜",
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

        crear_linea_stat(stats_frame, "✅ Palabras Escritas:", self.aciertos, "#27AE60")
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
            from .escribe_palabra import VistaEscribePalabra
            VistaEscribePalabra(parent)

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
            from .rimas import VistaRimas
            VistaRimas(parent)

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