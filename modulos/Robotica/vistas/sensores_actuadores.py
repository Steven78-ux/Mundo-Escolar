"""Vistas del módulo vistas."""

import customtkinter as ctk
import time
import random

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS, FONT_NAME
from core.util_logros import notificar_logro
from ..robotica_dominio import JuegoEmparejar, Tarjeta
from ..servicios.preguntas_robotica import (
    obtener_tarjetas_emparejar
)


class VentanaEmparejamiento(ctk.CTkFrame):
    def __init__(self, parent, on_volver, dificultad="basico", modo_extra=None):
        super().__init__(parent, fg_color="transparent")
        self.on_volver = on_volver
        self.dificultad = dificultad
        self.pack(fill="both", expand=True)

        nombres_totales, funciones_totales = obtener_tarjetas_emparejar()
        # Seleccionamos aleatoriamente 6 pares de entre toda la variedad disponible para esta sesión
        indices = random.sample(range(len(nombres_totales)), min(6, len(nombres_totales)))
        nombres_sesion = [nombres_totales[i] for i in indices]
        funciones_sesion = [funciones_totales[i] for i in indices]

        self.juego = JuegoEmparejar(nombres_sesion, funciones_sesion)

        self.global_start_time = time.time()
        self.aciertos = 0
        self.errores = 0

        self.botones_nombre = {}
        self.botones_funcion = {}
        self.setup_ui()
        self.start_time = time.time()
        self.crear_tablero()
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

        # Marco principal con el color Azul Media Noche
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=25, border_width=3, border_color=COLORS["border"])
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # --- Panel Superior de Información (Instrucciones y Stats) ---
        info_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        info_panel.pack(fill="x", padx=25, pady=(10, 2))

        # Cuadro de Instrucciones
        instr_frame = ctk.CTkFrame(info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15)
        instr_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        self.lbl_instrucciones = ctk.CTkLabel(
            instr_frame,
            text="¡BIENVENIDO INGENIERO! 🔗 Tu misión es conectar cada componente del robot con su función correcta. Selecciona una pieza de la izquierda y luego busca su tarea a la derecha.",
            font=(FONT_NAME, 18),
            text_color=COLORS["text"],
            justify="center",
            wraplength=600
        )
        self.lbl_instrucciones.pack(padx=20, pady=10)

        # Cuadro de Estadísticas (Tiempo y Parejas)
        stats_frame = ctk.CTkFrame(info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15, width=220, height=85)
        stats_frame.pack(side="right", fill="both")
        stats_frame.pack_propagate(False)

        self.lbl_timer = ctk.CTkLabel(stats_frame, text="⏱️ 00:00", font=(FONT_NAME, 28, "bold"), text_color=COLORS["border"])
        self.lbl_timer.pack(pady=(2, 0))

        self.lbl_parejas = ctk.CTkLabel(stats_frame, text=f"Parejas: 0/{self.juego.total_parejas}", font=(FONT_NAME, 16, "bold"), text_color=COLORS["text"])
        self.lbl_parejas.pack(pady=(0, 2))

        ctk.CTkLabel(
            self.main_frame,
            text="🔗  Sincronización de Componentes  🔗",
            font=(FONT_NAME, 36, "bold"),
            text_color=COLORS["border"],
        ).pack(pady=(5, 5))

        self.frame_tablero = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_tablero.pack(expand=True, fill="both")

        self.lbl_mensaje = ctk.CTkLabel(
            self.main_frame, 
            text="Sincronización lista. Esperando comando...", 
            font=(FONT_NAME, 22, "bold"), 
            text_color=COLORS["border"]
        )
        self.lbl_mensaje.pack(pady=10)

    def update_timer(self):
        if not self.winfo_exists() or self.juego.completado:
            return
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        self.lbl_timer.configure(text=f"⏱️ {m:02d}:{s:02d}")
        self.after(1000, self.update_timer)
        
    def crear_tablero(self):
        for widget in self.frame_tablero.winfo_children():
            widget.destroy()
        self.botones_nombre.clear()
        self.botones_funcion.clear()

        frame_izq = ctk.CTkFrame(self.frame_tablero, fg_color="#151B2D", corner_radius=15, border_width=1, border_color=COLORS["border"])
        frame_izq.pack(side="left", padx=15, fill="both", expand=True)
        frame_der = ctk.CTkFrame(self.frame_tablero, fg_color="#151B2D", corner_radius=15, border_width=1, border_color=COLORS["border"])
        frame_der.pack(side="right", padx=15, fill="both", expand=True)

        ctk.CTkLabel(frame_izq, text="🧩 Componente", font=FONTS["subtitulo"], text_color=COLORS["border"]).pack(pady=10)
        ctk.CTkLabel(frame_der, text="🎯 Función", font=FONTS["subtitulo"], text_color=COLORS["border"]).pack(pady=10)

        for t in self.juego.tarjetas_nombre:
            btn = ctk.CTkButton(
                frame_izq,
                text=f"{t.icono} {t.nombre}",
                font=FONTS["botones"],
                corner_radius=10,
                fg_color="#151B2D" if not t.emparejada else COLORS["success"], # Nuevo color de tarjeta
                hover_color=COLORS["hover"],
                state="normal" if not t.emparejada else "disabled",
                command=lambda tarj=t: self.seleccionar_nombre(tarj),
            )
            btn.pack(pady=6, padx=10, fill="x")
            self.botones_nombre[t.id] = btn

        for t in self.juego.tarjetas_funcion:
            btn = ctk.CTkButton(
                frame_der,
                text=f"{t.icono} {t.nombre}",
                font=FONTS["botones"],
                corner_radius=10,
                fg_color="#151B2D" if not t.emparejada else COLORS["success"], # Nuevo color de tarjeta
                hover_color=COLORS["hover"],
                state="normal" if not t.emparejada else "disabled",
                command=lambda tarj=t: self.seleccionar_funcion(tarj),
            )
            btn.pack(pady=6, padx=10, fill="x")
            self.botones_funcion[t.id] = btn

    def _resaltar_seleccion(self):
        for btn in self.botones_nombre.values():
            btn.configure(border_width=0)
        if self.juego.seleccionada_nombre:
            self.botones_nombre[self.juego.seleccionada_nombre.id].configure(
                border_width=3, border_color=COLORS["warning"]
            )

    def seleccionar_nombre(self, tarjeta_nombre: Tarjeta):
        self.juego.seleccionar_nombre(tarjeta_nombre)
        self._resaltar_seleccion()
        if self.juego.seleccionada_nombre:
            self.lbl_mensaje.configure(
                text=f"¿Qué hace el {self.juego.seleccionada_nombre.nombre.lower()}? ¡Busca su función!",
                text_color="#00E5FF",
            )
        else:
            self.lbl_mensaje.configure(
                text="Selecciona un componente de la izquierda.",
                text_color=COLORS["text"]
            )

    def seleccionar_funcion(self, tarjeta_funcion: Tarjeta):
        resultado = self.juego.seleccionar_funcion(tarjeta_funcion)
        self._resaltar_seleccion()

        if resultado is True:
            self.aciertos += 1
            self.lbl_mensaje.configure(text="🌟 ¡ENLACE EXITOSO! Componentes sincronizados. 🌟", text_color=COLORS["success"])
            self.lbl_parejas.configure(text=f"Parejas: {self.juego.parejas_completadas}/{self.juego.total_parejas}")
            self.actualizar_tablero()
            if self.juego.completado:
                self.finalizar()
        elif resultado is False:
            self.errores += 1
            self.lbl_mensaje.configure(
                text="⚠️ ERROR DE CONEXIÓN. Las funciones no coinciden. ⚠️", text_color=COLORS["danger"]
            )
            self.after(1500, lambda: self.lbl_mensaje.configure(text="Inténtalo de nuevo.", text_color=COLORS["text"]))
        else:
            self.lbl_mensaje.configure(
                text="¡Atención! Primero elige una pieza de la izquierda.",
                text_color=COLORS["warning"],
            )

    def actualizar_tablero(self):
        for t in self.juego.tarjetas_nombre:
            if t.emparejada and t.id in self.botones_nombre:
                self.botones_nombre[t.id].configure(state="disabled", fg_color=COLORS["success"])
        for t in self.juego.tarjetas_funcion:
            if t.emparejada and t.id in self.botones_funcion:
                self.botones_funcion[t.id].configure(state="disabled", fg_color=COLORS["success"])

    def finalizar(self):
        GestorEstado().actualizar_progreso("Robotica", 0.12)
        notificar_logro("robotica_emparejar")
        
        self.mostrar_resumen()

    def mostrar_resumen(self):
        """Muestra una pantalla de resultados temática de robótica."""
        total_seconds = int(time.time() - self.global_start_time)
        minutos = total_seconds // 60
        segundos = total_seconds % 60
        tiempo_str = f"{minutos:02d}:{segundos:02d}"

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.main_frame,
            text="🛰️ REPORTE DE SINCRONIZACIÓN 🛰️",
            font=(FONT_NAME, 36, "bold"),
            text_color=COLORS["border"],
            fg_color="transparent"
        ).pack(pady=(50, 30))

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

        crear_linea_stat(stats_frame, "✅ Componentes Enlazados:", self.juego.total_parejas, "#00E5FF")
        crear_linea_stat(stats_frame, "⚠️ Fallos de Conexión:", self.errores, "#FF5252")
        crear_linea_stat(stats_frame, "⏱️ Tiempo de Sincronización:", tiempo_str, "#FFD700")

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
            from .sensores_actuadores import VentanaEmparejamiento
            VentanaEmparejamiento(parent, self.on_volver, self.dificultad)

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
            from .programacion import VentanaProgramacion
            VentanaProgramacion(parent, self.on_volver, self.dificultad)

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