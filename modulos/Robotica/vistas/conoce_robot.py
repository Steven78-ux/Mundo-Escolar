"""Vistas del módulo vistas."""

import customtkinter as ctk
import time
import random

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS, FONT_NAME
from core.util_logros import notificar_logro
from ..robotica_dominio import JuegoPartesRobot
from ..servicios.preguntas_robotica import (
    obtener_preguntas_parte_robot
)


class VentanaConoceRobot(ctk.CTkFrame):
    def __init__(self, parent, on_volver, dificultad="basico", modo_extra=None):
        super().__init__(parent, fg_color="transparent")
        self.on_volver = on_volver
        self.dificultad = dificultad
        self.pack(fill="both", expand=True)
        
        # Misión de 6 rondas aleatorias
        preguntas_totales = obtener_preguntas_parte_robot()
        self.juego = JuegoPartesRobot(random.sample(preguntas_totales, min(6, len(preguntas_totales))))
        
        self.global_start_time = time.time()
        self.start_time = time.time()
        self.setup_ui()
        self.mostrar_pregunta()
        self.update_timer()

    def setup_ui(self):
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(
            barra,
            text="🛰️ VOLVER A BASE",
            font=(FONT_NAME, 13, "bold"),
            fg_color="#0A0E1A",
            border_color=COLORS["border"],
            border_width=2,
            hover_color="#006064",
            text_color=COLORS["border"],
            corner_radius=15,
            command=self.on_volver,
        ).pack(side="left")

        # Marco principal con el color Azul Media Noche para coherencia con el Centro de Mando
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=25, border_width=3, border_color=COLORS["border"])
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # --- Panel Superior de Información (Instrucciones y Stats) ---
        info_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        info_panel.pack(fill="x", padx=25, pady=(10, 2))

        # Cuadro de Instrucciones
        instr_frame = ctk.CTkFrame(info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15)
        instr_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        self.lbl_instrucciones = ctk.CTkLabel(
            instr_frame,
            text="¡HOLA EXPLORADOR! 🤖 Observa con atención la imagen central e identifica qué parte del robot es o cuál es su función principal. ¡Selecciona la tarjeta correcta para completar la misión!",
            font=(FONT_NAME, 18),
            text_color=COLORS["text"],
            justify="center",
            wraplength=600
        )
        self.lbl_instrucciones.pack(padx=20, pady=4)

        # Cuadro de Estadísticas (Tiempo y Rondas)
        stats_frame = ctk.CTkFrame(info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15, width=220, height=85)
        stats_frame.pack(side="right", fill="both")
        stats_frame.pack_propagate(False)

        self.lbl_timer = ctk.CTkLabel(stats_frame, text="⏱️ 00:00", font=(FONT_NAME, 28, "bold"), text_color=COLORS["border"])
        self.lbl_timer.pack(pady=(2, 0))

        self.lbl_rondas = ctk.CTkLabel(stats_frame, text="Misión: 1/5", font=(FONT_NAME, 16, "bold"), text_color=COLORS["text"])
        self.lbl_rondas.pack(pady=(0, 2))

        ctk.CTkLabel(
            self.main_frame,
            text="🤖  Partes del Robot  🧩",
            font=(FONT_NAME, 36, "bold"),
            text_color=COLORS["border"],
            anchor="center"
        ).pack(pady=(5, 2))

        self.lbl_imagen = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI Emoji", 60))
        self.lbl_imagen.pack(pady=5)

        self.lbl_pregunta = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=(FONT_NAME, 26, "bold"),
            text_color=COLORS["border"], # Para que la pregunta brille
            wraplength=700,
        )
        self.lbl_pregunta.pack(pady=10)

        self.frame_opciones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_opciones.pack(pady=15, expand=True, fill="both", padx=30)

        self.lbl_feedback = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=(FONT_NAME, 22, "bold"), 
            text_color=COLORS["success"],
            wraplength=800 # Evita que el texto se salga de los márgenes
        )
        self.lbl_feedback.pack(pady=10)

    def update_timer(self):
        if not self.winfo_exists() or self.juego.completado:
            return
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        self.lbl_timer.configure(text=f"⏱️ {m:02d}:{s:02d}")
        self.after(1000, self.update_timer)

    def mostrar_pregunta(self):
        self.lbl_feedback.configure(text="")
        for widget in self.frame_opciones.winfo_children():
            widget.destroy()

        pregunta = self.juego.pregunta_actual()
        if not pregunta:
            self.finalizar()
            return

        self.lbl_rondas.configure(text=f"Misión: {self.juego.indice + 1}/{len(self.juego.preguntas)}")
        self.lbl_imagen.configure(text=pregunta.imagen)
        self.lbl_pregunta.configure(text=pregunta.pregunta)

        # Configurar rejilla 2x2 para las tarjetas
        self.frame_opciones.grid_columnconfigure((0, 1), weight=1, uniform="tarjeta")
        self.frame_opciones.grid_rowconfigure((0, 1), weight=1, uniform="tarjeta")

        for i, opcion in enumerate(pregunta.opciones[:4]):
            fila, col = divmod(i, 2)
            btn = ctk.CTkButton(
                self.frame_opciones,
                text=opcion,
                font=FONTS["subtitulo"], # Fuente más grande para las tarjetas
                fg_color="#151B2D",
                hover_color=COLORS["hover"],
                border_width=2,
                border_color=COLORS["border"],
                corner_radius=25,
                command=lambda opt=opcion: self.responder(opt),
            )
            btn.grid(row=fila, column=col, padx=15, pady=15, sticky="nsew")

    def responder(self, respuesta):
        acierto, explicacion = self.juego.verificar_respuesta(respuesta)
        if acierto:
            self.lbl_feedback.configure(
                text=f"🌟 ¡GENIAL! {explicacion} 🌟", text_color=COLORS["success"]
            )
        else:
            self.lbl_feedback.configure(
                text=f"⚠️ ¡CASI! {explicacion} ⚠️", text_color=COLORS["danger"]
            )
        self.after(1200, self.mostrar_pregunta)

    def finalizar(self):
        GestorEstado().actualizar_progreso("Robotica", 0.1)
        notificar_logro("robotica_partes")

        self.mostrar_resumen()

    def mostrar_resumen(self):
        """Muestra una pantalla de resultados temática de robótica."""
        # Calcular estadísticas
        total_seconds = int(time.time() - self.global_start_time)
        minutos = total_seconds // 60
        segundos = total_seconds % 60
        tiempo_str = f"{minutos:02d}:{segundos:02d}"
        
        aciertos = self.juego.puntaje
        errores = len(self.juego.preguntas) - aciertos

        # Limpiar marco principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título de resultados estilo consola
        ctk.CTkLabel(
            self.main_frame,
            text="🛰️ REPORTE DE MISIÓN ROBÓTICA 🛰️",
            font=(FONT_NAME, 36, "bold"),
            text_color=COLORS["border"],
            fg_color="transparent"
        ).pack(pady=(50, 30))

        # Panel de estadísticas con colores del módulo
        stats_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#151B2D", 
            corner_radius=20, 
            border_width=2, 
            border_color=COLORS["border"]
        )
        stats_frame.pack(pady=20, padx=100, fill="x")

        def crear_linea_stat(parent, etiqueta, valor, color):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=10)
            ctk.CTkLabel(f, text=etiqueta, font=(FONT_NAME, 22, "bold"), text_color="#E0F7FA").pack(side="left")
            ctk.CTkLabel(f, text=str(valor), font=(FONT_NAME, 22, "bold"), text_color=color).pack(side="right")

        crear_linea_stat(stats_frame, "✅ Partes Identificadas:", aciertos, "#00E5FF")
        crear_linea_stat(stats_frame, "⚠️ Errores de Escaneo:", errores, "#FF5252")
        crear_linea_stat(stats_frame, "⏱️ Tiempo de Operación:", tiempo_str, "#FFD700")

        # Contenedor de botones
        btns_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btns_frame.pack(pady=50)

        # Botón Volver a Base
        ctk.CTkButton(
            btns_frame,
            text="🛰️ VOLVER A BASE",
            font=(FONT_NAME, 16, "bold"),
            width=220,
            height=55,
            fg_color="#0A0E1A",
            border_color=COLORS["border"],
            border_width=2,
            hover_color="#006064",
            text_color=COLORS["border"],
            corner_radius=15,
            command=self.on_volver
        ).pack(side="left", padx=20)

        # Botón Reiniciar
        def reiniciar():
            parent = self.master
            self.destroy()
            from .conoce_robot import VentanaConoceRobot
            VentanaConoceRobot(parent, self.on_volver, self.dificultad)

        ctk.CTkButton(
            btns_frame,
            text="🔄 REINICIAR",
            font=(FONT_NAME, 16, "bold"),
            width=220,
            height=55,
            fg_color="#006064",
            hover_color="#004D40",
            corner_radius=15,
            command=reiniciar
        ).pack(side="left", padx=20)

        # Botón Siguiente Misión
        def siguiente():
            parent = self.master
            self.destroy()
            from .sensores_actuadores import VentanaEmparejamiento
            VentanaEmparejamiento(parent, self.on_volver, self.dificultad)

        ctk.CTkButton(
            btns_frame,
            text="➡️ SIGUIENTE MISIÓN",
            font=(FONT_NAME, 16, "bold"),
            width=220,
            height=55,
            fg_color=COLORS["border"],
            hover_color="#00B8D4",
            text_color="#0A0E1A",
            corner_radius=15,
            command=siguiente
        ).pack(side="left", padx=20)