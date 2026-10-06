"""Vistas del módulo vistas."""

import customtkinter as ctk
import random
import time
from .base import JuegoBase
from ..dominio.juegos import OrdenaLetras
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_ordenar_letras
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro

class VistaOrdenaLetras(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Ordena las Letras", "#1ABC9C")
        
        # Selección aleatoria de 15 palabras
        todas_las_palabras = obtener_ordenar_letras()
        palabras_seleccionadas = random.sample(
            todas_las_palabras, min(15, len(todas_las_palabras))
        )
        
        self.juego = OrdenaLetras(palabras_seleccionadas)
        self.letras_seleccionadas = []
        self.gestor = GestorEstado()

        # Estadísticas para el resumen
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()

        # Estado de la ronda para pista dinámica
        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        self.start_time = time.time()
        self.timer_id = None
        
        self.configurar_ui()
        self._update_timer()
        self.cargar_palabra()

    def configurar_ui(self):
        # Contenedor central para el juego
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

        self.lbl_palabra_formada = ctk.CTkLabel(
            content_frame, 
            text="", 
            font=("Verdana", 42, "bold"),
            text_color="#2B2D42",
            height=70
        )
        self.lbl_palabra_formada.pack(pady=10)

        self.frame_letras = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.frame_letras.pack(pady=20)

        # Marco para botones de control
        self.buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=10)

        self.btn_borrar = ctk.CTkButton(
            self.buttons_frame, 
            text="⌫ BORRAR", 
            command=self.borrar_letra,
            font=("Verdana", 16, "bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=150,
            height=50,
            corner_radius=15
        )
        self.btn_borrar.pack(side="left", padx=10)

        self.btn_comprobar = ctk.CTkButton(
            self.buttons_frame, 
            text="✅ COMPROBAR", 
            command=self.comprobar,
            font=("Verdana", 16, "bold"),
            fg_color=self.color_tema,
            hover_color=self._lighten_color(self.color_tema),
            width=180,
            height=50,
            corner_radius=15,
            border_width=3,
            border_color=self.color_borde_tema
        )
        self.btn_comprobar.pack(side="left", padx=10)

        self.lbl_feedback = ctk.CTkLabel(
            content_frame, 
            text="¡Ordena las letras!", 
            font=("Verdana", 18, "italic"),
            text_color="#5D4037"
        )
        self.lbl_feedback.pack(pady=20)

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
            text="📝 INSTRUCCIONES:\n\nObserva el dibujo y pulsa las letras en el orden correcto para formar su nombre.",
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

    def cargar_palabra(self):
        if self.juego.completado:
            self.finalizar("¡Eres un experto ordenando letras!")
            return

        # Reiniciar estado de ronda
        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        self.letras_seleccionadas = []
        self.actual = self.juego.palabra_actual()
        self.lbl_ronda.configure(
            text=f"Palabra: {self.juego.indice + 1} / {len(self.juego.palabras)}"
        )
        self.img_label.configure(text=self.actual.imagen)
        self.lbl_pista_img.configure(
            text="🔍 Ayuda: se revelará pronto...", 
            text_color="#A9A9A9"
        )
        self.lbl_palabra_formada.configure(text="", text_color="#2B2D42")
        self.lbl_feedback.configure(text="Pulsa las letras en orden", text_color="#5D4037")
        self.mostrar_letras(self.actual.letras)

    def revelar_pista(self):
        """Muestra la palabra completa como ayuda."""
        if self.actual and not self.pista_revelada:
            self.pista_revelada = True
            self.lbl_pista_img.configure(
                text=f"¿Qué es? ¡Es un {self.actual.palabra}!", 
                text_color="#8D6E63"
            )

    def mostrar_letras(self, letras):
        for widget in self.frame_letras.winfo_children():
            widget.destroy()
            
        # Colocar todas las letras en una sola fila (row=0)
        for col, letra in enumerate(letras):
            btn = ctk.CTkButton(
                self.frame_letras,
                text=letra,
                width=80,
                height=80,
                font=("Verdana", 32, "bold"),
                fg_color="white",
                text_color="#2B2D42",
                hover_color="#F5F5F5",
                border_width=3,
                border_color="#BCAAA4",
                corner_radius=15,
            )
            btn.configure(command=lambda l=letra, b=btn: self.agregar_letra(l, b))
            btn.grid(row=0, column=col, padx=8, pady=8)

    def agregar_letra(self, letra, btn):
        # Guardamos la letra y la referencia al botón para poder restaurarlo
        self.letras_seleccionadas.append((letra, btn))
        # Cambiamos color a verde y deshabilitamos
        btn.configure(fg_color="#27AE60", state="disabled")
        self.lbl_palabra_formada.configure(text="".join([x[0] for x in self.letras_seleccionadas]))

    def borrar_letra(self):
        if self.letras_seleccionadas:
            letra, btn = self.letras_seleccionadas.pop()
            # Restauramos el botón
            btn.configure(fg_color="white", state="normal")
            self.lbl_palabra_formada.configure(text="".join([x[0] for x in self.letras_seleccionadas]))

    def comprobar(self):
        palabra_intento = "".join([x[0] for x in self.letras_seleccionadas])
        if self.juego.verificar(palabra_intento):
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.lbl_palabra_formada.configure(text_color="#27AE60")
            self.lbl_feedback.configure(text="¡Perfecto!", text_color="#2ECC71")
            self.after(1500, self.cargar_palabra)
        else:
            self.errores += 1
            self.errores_ronda += 1
            if self.errores_ronda >= 4:
                self.revelar_pista()
                
            AudioService.reproducir("incorrecto")
            self.lbl_palabra_formada.configure(text_color="#C0392B")
            self.lbl_feedback.configure(text="Orden incorrecto, inténtalo de nuevo", text_color="#E74C3C")
            
            # Restaurar todos los botones usados en el intento fallido
            for letra, btn in self.letras_seleccionadas:
                btn.configure(fg_color="white", state="normal")
                
            self.after(1000, lambda: self.lbl_palabra_formada.configure(text="", text_color="#2B2D42"))
            self.letras_seleccionadas = []

    def _update_timer(self):
        """Actualiza el cronómetro en la UI."""
        if not self.winfo_exists():
            return

        # Verificar tiempo de la ronda para revelar pista (30 segundos)
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
        """Detiene el cronómetro al finalizar el juego."""
        if self.timer_id:
            self.after_cancel(self.timer_id)

        notificar_logro("lenguaje_nivel_6", parent=self)
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
            text="📜 REPORTE DEL ORDENADOR 📜",
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

        crear_linea_stat(stats_frame, "✅ Palabras Ordenadas:", self.aciertos, "#27AE60")
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
            from .ordena_letras import VistaOrdenaLetras
            VistaOrdenaLetras(parent)

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
            from .lee_encuentra import VistaLeeEncuentra
            VistaLeeEncuentra(parent)

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