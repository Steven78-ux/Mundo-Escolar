"""Vistas del módulo vistas."""

import customtkinter as ctk
from .base import JuegoBase
from ..dominio.juegos import DetectiveSonidos
import time
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_preguntas_detective
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro


class VistaDetectiveSonidos(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Detective de Sonidos", "#3498DB")
        self.juego = DetectiveSonidos(obtener_preguntas_detective())
        self.gestor = GestorEstado()
        self.global_start_time = time.time()
        self.aciertos = 0
        self.errores = 0
        self.start_time = time.time()
        self.timer_id = None
        self.nombres_objetos = {
            "🍎": "MANZANA",
            "🎈": "GLOBO",
            "🏠": "CASA",
            "🍩": "DONA",
            "🐘": "ELEFANTE",
            "🌸": "FLOR",
            "🎸": "GUITARRA",
            "🍋": "LIMÓN",
            "🧸": "OSO",
            "🍐": "PERA",
            "🍓": "FRESA",
            "🍅": "TOMATE",
        }
        self.configurar_ui()
        self._update_timer()  # Iniciar el cronómetro
        self.siguiente_pregunta()

    def configurar_ui(self):
        # Usamos main_container para el contenido
        self.lbl_instruccion = (
            ctk.CTkLabel(  # Mantenemos esta etiqueta para la pregunta
                self.main_container,
                text="🕵️ Escucha y encuentra el objeto que empieza con el sonido...",
                font=("Verdana", 22, "bold"),
                text_color="#2B2D42",
            )
        )
        self.lbl_instruccion.pack(pady=40)

        self.btn_escuchar = ctk.CTkButton(
            self.main_container,
            text="🔊 ESCUCHAR SONIDO",
            command=self.reproducir_sonido,
            font=("Verdana", 18, "bold"),
            width=250,
            height=60,
            corner_radius=20,
            fg_color=self.color_tema,
            border_width=4,
            border_color=self.color_borde_tema,
        )
        self.btn_escuchar.pack(pady=20)

        self.lbl_pista_texto = ctk.CTkLabel(
            self.main_container,
            text="",
            font=("Verdana", 28, "bold"),
            text_color="#E67E22",
        )
        self.lbl_pista_texto.pack(pady=10)

        # --- Caja de Instrucciones (Superior Izquierda) ---
        self.instruction_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFF9C4",  # Color pergamino claro
            corner_radius=15,
            border_width=2,
            border_color="#BCAAA4",  # Borde grisáceo
            width=350,
            height=150,
        )
        self.instruction_frame.place(x=20, y=20)
        ctk.CTkLabel(
            self.instruction_frame,
            text="📝 INSTRUCCIONES:\n\nEscucha el sonido y elige la imagen que empieza con él.",
            font=("Verdana", 14, "bold"),
            text_color="#4E342E",
            wraplength=310,
            justify="left",
        ).pack(padx=10, pady=10, fill="both", expand=True)

        # --- Indicador de Progreso y Cronómetro (Superior Derecha) ---
        self.info_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FFF9C4",  # Color pergamino claro
            corner_radius=15,
            border_width=2,
            border_color="#BCAAA4",  # Borde grisáceo
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

        self.opciones_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.opciones_frame.pack(expand=True, fill="both", pady=20)
        for i in range(3):
            self.opciones_frame.grid_columnconfigure(i, weight=1)
        self.opciones_frame.grid_rowconfigure(0, weight=1)

        self.botones = []
        for i in range(3):
            btn = ctk.CTkButton(
                self.opciones_frame,
                text="",
                font=("Segoe UI Emoji", 90),
                width=220,
                height=220,
                corner_radius=35,
                border_width=5,
                border_color="#BCAAA4",
                fg_color="white",
                hover_color="#F5F5F5",
                text_color="black",
                command=lambda idx=i: self.verificar(idx),
            )
            btn.grid(row=0, column=i, padx=20, pady=20)
            self.botones.append(btn)

    def siguiente_pregunta(self):
        if self.juego.completado:
            self.finalizar("¡Has completado Detective de Sonidos!")
            return

        # Reiniciar cronómetro y actualizar ronda
        self.start_time = time.time()
        self.lbl_ronda.configure(
            text=f"Pregunta: {self.juego.indice + 1} / {len(self.juego.preguntas)}"
        )
        pregunta = self.juego.pregunta_actual()
        for i, btn in enumerate(self.botones):
            btn.configure(
                text=pregunta.opciones[i],
                state="normal",
                fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            )
        # Se elimina la llamada automática para que el sonido solo se reproduzca al tocar el botón.
        self.lbl_instruccion.configure(
            text="🕵️ Escucha y encuentra el objeto que empieza con el sonido...",
            text_color="#2B2D42",
        )
        self.lbl_pista_texto.configure(text="")

    def reproducir_sonido(self):
        pregunta = self.juego.pregunta_actual()
        if pregunta is None:
            return

        AudioService.reproducir(pregunta.sonido)
        palabra = self.nombres_objetos.get(pregunta.sonido, pregunta.letra)
        self.lbl_pista_texto.configure(text=f"PALABRA: {palabra}")

    def verificar(self, idx):
        pregunta = self.juego.pregunta_actual()
        if pregunta is None:
            return
        if self.juego.verificar(pregunta.opciones[idx]):
            self.aciertos += 1
            AudioService.reproducir("correcto")
            self.botones[idx].configure(fg_color="green")
            self.lbl_instruccion.configure(
                text="✨ ¡FELICIDADES! ESA ES LA IMAGEN CORRECTA ✨",
                text_color="#27AE60",
            )
            for b in self.botones:  # Deshabilitar botones para evitar múltiples clics
                b.configure(state="disabled")
            self.after(2000, self.siguiente_pregunta)
        else:
            self.errores += 1
            AudioService.reproducir("incorrecto")
            self.botones[idx].configure(fg_color="red")
            self.after(
                500,
                lambda b=self.botones[idx]: b.configure(
                    fg_color="white"
                ),
            )
            self.lbl_instruccion.configure(
                text="❌ INCORRECTO ESA NO ES PRUEBA DE NUEVO ❌", text_color="#E74C3C"
            )

    def _update_timer(self):
        """Actualiza el cronómetro en la UI."""
        if not self.winfo_exists():  # Detener si la ventana ya no existe
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

        notificar_logro("lenguaje_nivel_1", parent=self)
        self.mostrar_resumen()

    def mostrar_resumen(self):
        """Muestra una pantalla de resultados temática en lugar de un messagebox."""
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
            text="📜 REPORTE DEL DETECTIVE 📜",
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

        crear_linea_stat(stats_frame, "✅ Imágenes Correctas:", self.aciertos, "#27AE60")
        crear_linea_stat(stats_frame, "❌ Imágenes Incorrectas:", self.errores, "#E74C3C")
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
            from .detective_sonidos import VistaDetectiveSonidos
            VistaDetectiveSonidos(parent)

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
            from .constructor_palabras import VistaConstructorPalabras
            VistaConstructorPalabras(parent)

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