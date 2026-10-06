"""Vistas del módulo vistas."""

import customtkinter as ctk
import time

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS, FONT_NAME
from core.util_logros import notificar_logro
from ..robotica_dominio import ConstructorRobot, RobotProgramable
from ..servicios.preguntas_robotica import (
    obtener_componentes_construccion,
    obtener_mision_ejemplo,
    obtener_obstaculos_por_dificultad,
)


class VentanaProgramacion(ctk.CTkFrame):
    """Construcción de robot y programación con flechas (embebido)."""

    def __init__(self, parent, on_volver, dificultad="basico", modo_extra=None):
        super().__init__(parent, fg_color="transparent")
        self.on_volver = on_volver
        self.dificultad = dificultad
        self.modo_extra = modo_extra
        self.pack(fill="both", expand=True)
        self.componentes = obtener_componentes_construccion()
        self.mision = obtener_mision_ejemplo()
        self.constructor = ConstructorRobot(self.componentes, self.mision)
        self.robot_programable = None

        # Estadísticas para el resumen
        self.global_start_time = time.time()
        self.aciertos = 0
        self.errores = 0
        self.ronda_actual = 1
        self.total_rondas = 4
        self.vidas = 3

        self._saltar_construccion = modo_extra == "lineas"
        self.setup_ui()
        if self._saltar_construccion:
            self.iniciar_programacion(solo_lineas=True)
        else:
            self.mostrar_paso_construccion()

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

        # Marco principal Azul Media Noche
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=25, border_width=3, border_color=COLORS["border"])
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # --- Panel Superior de Información (Instrucciones y Stats) ---
        self.info_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.info_panel.pack(fill="x", padx=25, pady=(10, 2))

        # Cuadro de Instrucciones
        instr_frame = ctk.CTkFrame(self.info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15)
        instr_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        self.lbl_instrucciones = ctk.CTkLabel(
            instr_frame,
            text="Cargando protocolos de misión...",
            font=(FONT_NAME, 16),
            text_color=COLORS["text"],
            justify="center",
            wraplength=600
        )
        self.lbl_instrucciones.pack(padx=20, pady=10)

        # Cuadro de Estadísticas
        stats_frame = ctk.CTkFrame(self.info_panel, fg_color="#151B2D", border_width=1, border_color=COLORS["border"], corner_radius=15, width=280, height=110)
        stats_frame.pack(side="right", fill="both")
        stats_frame.pack_propagate(False)

        self.lbl_timer = ctk.CTkLabel(stats_frame, text="⏱️ 00:00", font=(FONT_NAME, 24, "bold"), text_color=COLORS["border"])
        self.lbl_timer.pack(pady=(5, 0))

        self.lbl_vidas = ctk.CTkLabel(stats_frame, text="🤖 x 3", font=(FONT_NAME, 20, "bold"), text_color="#2ECC71")
        self.lbl_vidas.pack(pady=0)

        self.lbl_extra_stat = ctk.CTkLabel(stats_frame, text="Iniciando...", font=(FONT_NAME, 13, "bold"), text_color=COLORS["text"])
        self.lbl_extra_stat.pack(pady=(0, 5))

        if self.modo_extra == "lineas":
            titulo_texto = "〰️  Misión: Sigue el Camino  〰️"
        elif self.modo_extra == "circuito":
            titulo_texto = "🔌  Misión: Circuito Eléctrico  🔌"
        else:
            titulo_texto = "🛠️  Misión: Ingeniería de Robots  🛠️"
            
        self.lbl_titulo = ctk.CTkLabel(
            self.main_frame,
            text=titulo_texto,
            font=(FONT_NAME, 32, "bold"),
            text_color=COLORS["border"],
            fg_color="transparent",
            anchor="center"
        )
        self.lbl_titulo.pack(pady=(5, 5), fill="x")

        self.lbl_mision = ctk.CTkLabel(
            self.main_frame,
            text=f"OBJETIVO: {self.mision.nombre.upper()}",
            font=(FONT_NAME, 16, "bold"),
            text_color=COLORS["text"],
            justify="center",
            fg_color="transparent",
            anchor="center"
        )
        self.lbl_mision.pack(pady=8, fill="x")

        self.frame_contenido = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_contenido.pack(expand=True, fill="both")
        self.update_timer()

    def update_timer(self):
        # Validación robusta para evitar TclError al cerrar la ventana
        if not self.winfo_exists() or not hasattr(self, 'lbl_timer') or not self.lbl_timer.winfo_exists():
            return
            
        elapsed = int(time.time() - self.global_start_time)
        m, s = divmod(elapsed, 60)
        self.lbl_timer.configure(text=f"⏱️ {m:02d}:{s:02d}")
        self.after(1000, self.update_timer)

    def mostrar_paso_construccion(self):
        self.lbl_instrucciones.configure(text="🔧 FASE 1: ENSAMBLAJE. Elige las piezas correctas de la izquierda para armar tu robot según los requisitos de la misión.")
        self.lbl_extra_stat.configure(text=f"Piezas: {len(self.constructor.seleccionados)}/5")

        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        izquierda = ctk.CTkFrame(self.frame_contenido, fg_color="#151B2D", corner_radius=15, border_width=1, border_color=COLORS["border"]) # Nuevo color de tarjeta
        izquierda.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(
            izquierda, text="📦 Componentes", font=FONTS["subtitulo"], text_color=COLORS["border"]
        ).pack(pady=10)

        for comp in self.componentes:
            ctk.CTkButton(
                izquierda,
                text=f"{comp.icono} {comp.nombre}",
                font=FONTS["tarjetas"],
                fg_color="#151B2D", # Nuevo color de tarjeta
                hover_color=COLORS["hover"],
                text_color=COLORS["text"],
                corner_radius=15,
                command=lambda c=comp: self.agregar_componente(c),
            ).pack(pady=4, padx=10, fill="x")

        derecha = ctk.CTkFrame(self.frame_contenido, fg_color="#151B2D", corner_radius=15, border_width=1, border_color=COLORS["border"]) # Nuevo color de tarjeta
        derecha.pack(side="right", padx=10, fill="both", expand=True)
        ctk.CTkLabel(derecha, text="🤖 Tu robot", font=FONTS["subtitulo"], text_color=COLORS["border"]).pack(pady=10)

        self.lista_seleccionados = ctk.CTkScrollableFrame(derecha, fg_color="transparent")
        self.lista_seleccionados.pack(fill="both", expand=True, pady=10)

        self.lbl_feedback = ctk.CTkLabel(derecha, text="", font=FONTS["tarjetas"], text_color=COLORS["text"])
        self.lbl_feedback.pack(pady=5)

        ayuda = (
            "Circuito: motor + batería + controlador"
            if self.modo_extra == "circuito"
            else "Necesitas: sensor + actuador + estructura"
        )
        ctk.CTkLabel(
            derecha, text=ayuda, font=FONTS["pequeno"], text_color=COLORS["text"], wraplength=280
        ).pack(pady=5)

        ctk.CTkButton(
            derecha,
            text="✅ Verificar",
            fg_color=COLORS["border"],
            hover_color=COLORS["hover"],
            text_color=COLORS["text"],
            corner_radius=15,
            font=FONTS["botones"],
            command=self.verificar_y_continuar,
        ).pack(pady=10)

        self.actualizar_lista_seleccionados()

    def agregar_componente(self, comp):
        if self.constructor.agregar_componente(comp):
            self.lbl_feedback.configure(
                text=self.constructor.mensaje_feedback, text_color=COLORS["success"]
            )
            self.actualizar_lista_seleccionados()
        else:
            self.lbl_feedback.configure(
                text=self.constructor.mensaje_feedback, text_color=COLORS["danger"]
            )

    def actualizar_lista_seleccionados(self):
        for widget in self.lista_seleccionados.winfo_children():
            widget.destroy()
        for comp in self.constructor.seleccionados:
            frame_comp = ctk.CTkFrame(self.lista_seleccionados, fg_color="#151B2D", border_width=1, border_color=COLORS["border"]) # Nuevo color de tarjeta
            frame_comp.pack(fill="x", pady=4)
            ctk.CTkLabel(
                frame_comp, 
                text=f"{comp.icono} {comp.nombre}", 
                font=FONTS["tarjetas"],
                text_color=COLORS["text"]
            ).pack(side="left", padx=5)
            ctk.CTkButton(
                frame_comp,
                text="❌",
                width=30,
                fg_color=COLORS["danger"],
                corner_radius=10,
                command=lambda c=comp: self.quitar_componente(c),
            ).pack(side="right", padx=5)

    def quitar_componente(self, comp):
        self.constructor.quitar_componente(comp)
        self.lbl_feedback.configure(
            text=self.constructor.mensaje_feedback, text_color=COLORS["warning"]
        )
        self.actualizar_lista_seleccionados()

    def verificar_y_continuar(self):
        ok, mensaje = self.constructor.verificar_mision()

        if ok:
            self.aciertos += 1
            self.lbl_feedback.configure(text=mensaje, text_color=COLORS["success"])
            self.after(800, self.iniciar_programacion)
        else:
            self.errores += 1
            self.lbl_feedback.configure(text=f"⚠️ {mensaje}", text_color=COLORS["danger"])

    def iniciar_programacion(self, solo_lineas=False):
        if hasattr(self, 'tam_celda_fijo'):
            del self.tam_celda_fijo

        self.lbl_instrucciones.configure(
            text=f"🎮 RONDA {self.ronda_actual}: PROGRAMACIÓN. Lleva al robot 🤖 hasta la estrella ⭐. ¡Los mapas crecen en cada ronda!"
        )
        self.lbl_extra_stat.configure(text=f"Ronda: {self.ronda_actual}/{self.total_rondas} | Pasos: 0")
        self.lbl_titulo.configure(text="🎮 Programa los movimientos")
        texto = f"Misión: Trayectoria Nivel {self.ronda_actual}"
        self.lbl_mision.configure(text=texto)

        # Progresión: 1:6x6, 2:7x7, 3:8x8, 4:9x9
        size_val = 5 + self.ronda_actual
        grid_size = (size_val, size_val)
        
        num_obs = 5 + (self.ronda_actual * 3)
        obstaculos = obtener_obstaculos_por_dificultad(self.dificultad, personalizado=(size_val, size_val, num_obs))
        
        meta = (grid_size[0] - 1, grid_size[1] - 1)
        self.robot_programable = RobotProgramable(
            tamano_mapa=grid_size, obstaculos=obstaculos, meta=meta
        )

        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Contenedor para centrar el tablero y evitar efecto zoom
        self.tablero_container = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.tablero_container.pack(side="left", padx=15, pady=15, expand=True, fill="both")

        # MARCO DEL TABLERO (Para que no parezca que vuela)
        self.board_border_frame = ctk.CTkFrame(
            self.tablero_container,
            fg_color="transparent",
            border_width=4,
            border_color=COLORS["border"],
            corner_radius=10
        )
        self.board_border_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = ctk.CTkCanvas(
            self.board_border_frame, bg="#1C1E26", highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)

        panel = ctk.CTkFrame(self.frame_contenido, fg_color="#151B2D", corner_radius=20, border_width=2, border_color=COLORS["border"])
        panel.pack(side="right", padx=20, pady=20) # Reducido para que sea compacto

        ctk.CTkLabel(
            panel, 
            text="SISTEMA DE NAVEGACIÓN", 
            font=(FONT_NAME, 14, "bold"), 
            text_color="#00E5FF",
            fg_color="#0A0E1A",
            corner_radius=10,
            anchor="center"
        ).pack(pady=(10, 5), padx=10, fill="x")
        
        frame_flechas = ctk.CTkFrame(panel, fg_color="transparent")
        frame_flechas.pack(pady=5)
        for txt, row, col, cmd in [
            ("↑", 0, 1, "↑"),
            ("←", 1, 0, "←"),
            ("↓", 1, 1, "↓"),
            ("→", 1, 2, "→"),
        ]:
            ctk.CTkButton(
                frame_flechas,
                text=txt,
                width=55,
                height=55,
                font=("Arial", 28),
                corner_radius=15,
                fg_color="#151B2D", # Nuevo color de tarjeta
                hover_color=COLORS["hover"],
                text_color=COLORS["text"],
                command=lambda d=cmd: self.mover_robot(d),
            ).grid(row=row, column=col, padx=4, pady=4)

        self.lbl_mensaje_prog = ctk.CTkLabel(panel, text="Esperando ruta...", font=(FONT_NAME, 14, "italic"), wraplength=180, text_color=COLORS["text"], justify="center")
        self.lbl_mensaje_prog.pack(pady=10)
        
        # Forzar cálculo de tamaño fijo una sola vez para evitar efecto zoom
        self.update_idletasks()
        self.tam_celda_fijo = self._tam_celda()
        self.dibujar_tablero()

    def _tam_celda(self):
        # Usamos el contenedor para calcular un tamaño estable
        w = self.tablero_container.winfo_width()
        h = self.tablero_container.winfo_height()
        
        # Fallback para el primer renderizado
        if w <= 1: w = 450
        if h <= 1: h = 450
            
        lado_disponible = min(w, h) - 20
        return max(40, lado_disponible // self.robot_programable.columnas)

    def dibujar_tablero(self):
        self.canvas.delete("all")
        # Usar el tamaño pre-calculado para evitar saltos visuales (zoom)
        if not hasattr(self, 'tam_celda_fijo'):
            self.tam_celda_fijo = self._tam_celda()
        
        tam = self.tam_celda_fijo
        filas, cols = self.robot_programable.filas, self.robot_programable.columnas
        
        # Ajustar dimensiones del canvas para que sea cuadrado y estable
        self.canvas.configure(width=tam * cols, height=tam * filas)

        for f in range(filas):
            for c in range(cols):
                x1, y1 = c * tam, f * tam
                x2, y2 = x1 + tam, y1 + tam
                if (f, c) in self.robot_programable.obstaculos:
                    color, texto = "#455A64", "🧱"
                elif (f, c) == self.robot_programable.meta:
                    color, texto = "#FFD600", "⭐"
                else:
                    color, texto = "#263238", ""
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=COLORS["border"], width=1
                )
                if texto:
                    self.canvas.create_text(
                        x1 + tam / 2, y1 + tam / 2, text=texto, font=("Arial", max(20, tam // 3))
                    )
        # Dibujar Robot con base Cian Brillante
        fx, fy = self.robot_programable.pos
        cx, cy = fy * tam + tam / 2, fx * tam + tam / 2
        
        # Base circular brillante (Cian)
        self.canvas.create_oval(cx - tam*0.35, cy - tam*0.35, cx + tam*0.35, cy + tam*0.35, 
                                fill=COLORS["border"], outline="white", width=2)
        
        self.canvas.create_text(
            cx, cy, text="🤖", font=("Arial", max(24, tam // 2))
        )

    def mover_robot(self, direccion):
        valido, mensaje = self.robot_programable.mover(direccion)
        if valido:
            self.lbl_extra_stat.configure(text=f"Ronda: {self.ronda_actual}/{self.total_rondas} | Pasos: {len(self.robot_programable.historial)}")
            self.dibujar_tablero()
            if self.robot_programable.exito:
                if self.ronda_actual < self.total_rondas:
                    self.lbl_mensaje_prog.configure(text="🌟 ¡RONDA SUPERADA! 🌟\nCargando nuevo mapa...", text_color=COLORS["success"])
                    self.ronda_actual += 1
                    self.after(1500, self.iniciar_programacion)
                else:
                    self.lbl_mensaje_prog.configure(text="🏆 ¡MISIÓN CUMPLIDA! 🏆", text_color=COLORS["success"])
                    self.finalizar_programacion(exito=True)
            else:
                self.lbl_mensaje_prog.configure(text="")
        else:
            self.vidas -= 1
            # Color dinámico de vidas
            color_v = "#2ECC71" if self.vidas == 3 else "#F1C40F" if self.vidas == 2 else "#FF5252"
            self.lbl_vidas.configure(text=f"🤖 x {self.vidas}", text_color=color_v)
            
            self.errores += 1
            self.lbl_mensaje_prog.configure(text=mensaje, text_color=COLORS["danger"])
            
            # Efecto de daño y reinicio de posición
            self.robot_programable.reiniciar()
            self.dibujar_tablero()
            self._efecto_dano()
            
            if self.vidas <= 0:
                self.lbl_mensaje_prog.configure(text="⚠️ CRÍTICO: Energía agotada. Transfiriendo reporte...", text_color="#FF5252")
                self.after(1500, self.mostrar_resumen)

    def _efecto_dano(self):
        """Hace que el marco del tablero palpite en rojo sin cubrir el contenido."""
        original_color = COLORS["border"]
        
        def toggle(count):
            if not self.winfo_exists() or not hasattr(self, 'board_border_frame'):
                return
            
            if count >= 6:
                self.board_border_frame.configure(border_color=original_color)
                return
            
            color = "#FF5252" if count % 2 == 0 else original_color
            self.board_border_frame.configure(border_color=color)
            self.after(150, lambda: toggle(count + 1))
        
        toggle(0)

    def deshacer_movimiento(self):
        if self.robot_programable and self.robot_programable.deshacer():
            self.dibujar_tablero()
            self.lbl_mensaje_prog.configure(text="Deshecho último movimiento")
        else:
            self.lbl_mensaje_prog.configure(text="No hay movimientos para deshacer")

    def reiniciar_programacion(self):
        if self.robot_programable:
            self.robot_programable.reiniciar()
            self.dibujar_tablero()
            self.lbl_mensaje_prog.configure(text="¡Reiniciado!")

    def finalizar_programacion(self, exito):
        if exito:
            incremento = 0.15 if self.dificultad == "experto" else 0.1
            GestorEstado().actualizar_progreso("Robotica", incremento)
            notificar_logro("robotica_programacion")
            
            self.after(1000, self.mostrar_resumen)

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
            text="🛰️ REPORTE DE INGENIERÍA ROBÓTICA 🛰️",
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

        estado_mision = "SISTEMA OPERATIVO" if self.vidas > 0 else "FALLO DE SISTEMA"
        color_estado = "#00E5FF" if self.vidas > 0 else "#FF5252"
        
        crear_linea_stat(stats_frame, "✅ Estado de Misión:", estado_mision, color_estado)
        crear_linea_stat(stats_frame, "⚠️ Alertas de Hardware:", self.errores, "#FF5252")
        crear_linea_stat(stats_frame, "⏱️ Tiempo de Ejecución:", tiempo_str, "#FFD700")

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
            from .programacion import VentanaProgramacion
            VentanaProgramacion(parent, self.on_volver, self.dificultad, self.modo_extra)

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

        # Botón Siguiente Misión (Lleva de Misión 3 a Misión 4)
        def siguiente():
            parent = self.master
            self.destroy()
            from .programacion import VentanaProgramacion
            # Si terminamos Misión 3 (None), vamos a Misión 4 (lineas)
            VentanaProgramacion(parent, self.on_volver, self.dificultad, "lineas")

        if self.modo_extra is None:
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