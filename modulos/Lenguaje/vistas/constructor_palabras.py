"""Vistas del módulo vistas."""

import random
import customtkinter as ctk
import time
from .base import JuegoBase
from ..dominio.juegos import ConstructorPalabras
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_palabras_constructor, DISTRACTORES
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro


class VistaConstructorPalabras(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Constructor de Palabras", "#2ECC71")

        todas_las_palabras = obtener_palabras_constructor()
        num_rondas = 15
        palabras_seleccionadas = random.sample(
            todas_las_palabras, min(num_rondas, len(todas_las_palabras))
        )

        self.juego = ConstructorPalabras(palabras_seleccionadas, DISTRACTORES)
        self.gestor = GestorEstado()
        self.configurar_ui()

        # Estadísticas para el resumen final
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()

        # Inicializar variables de estado de ronda para evitar AttributeError
        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        self.start_time = time.time()
        self.timer_id = None
        self.cargar_palabra()
        self._update_timer()

    def configurar_ui(self):
        # Contenedor superior para la imagen y la palabra formada
        top_content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        top_content_frame.pack(pady=(15, 5))

        self.img_label = ctk.CTkLabel(
            top_content_frame, text="", font=("Segoe UI Emoji", 120)
        )
        self.img_label.pack(side="top", pady=(0, 10))  # Imagen en la parte superior

        self.lbl_pista_img = ctk.CTkLabel(
            top_content_frame,
            text="",
            font=("Verdana", 18, "italic", "bold"),
            text_color="#8D6E63",
        )
        self.lbl_pista_img.pack(pady=(0, 10))

        self.lbl_palabra = ctk.CTkLabel(
            top_content_frame,
            text="",
            font=("Verdana", 36, "bold"),
            text_color="#2B2D42",
        )
        self.lbl_palabra.pack(side="bottom")  # Palabra formada debajo de la imagen

        self.lbl_estado = ctk.CTkLabel(
            self.main_container,
            text="Selecciona las sílabas correctas en orden",
            font=("Verdana", 18),
            text_color="#5D4037",  # Color oscuro para contraste con el papel
        )
        self.lbl_estado.pack(pady=(10, 5))

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
            text="📝 INSTRUCCIONES:\n\nOrdena las sílabas para formar la palabra que ves en la imagen.",
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

        # Marco para el "teclado" de sílabas
        keyboard_outer_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#FDF5E6",  # Fondo más claro para el teclado
            corner_radius=20,
            border_width=3,
            border_color="#8D6E63",  # Borde marrón para el marco
        )
        keyboard_outer_frame.pack(pady=(10, 20), padx=50, fill="x")

        self.frame_silabas = ctk.CTkFrame(keyboard_outer_frame, fg_color="transparent")
        self.frame_silabas.pack(
            padx=20, pady=20
        )  # Las sílabas van dentro de este marco

    def cargar_palabra(self):
        if self.juego.completado:
            self.finalizar("¡Has construido todas las palabras!")
            return

        self.actual = self.juego.palabra_actual()
        if self.actual is None:
            self.finalizar("¡Has construido todas las palabras!")
            return

        # Reiniciar contadores de la ronda
        self.errores_ronda = 0
        self.pista_revelada = False
        self.tiempo_inicio_ronda = time.time()

        # Actualizar indicador de ronda
        self.lbl_ronda.configure(
            text=f"Palabra: {self.juego.indice + 1} / {len(self.juego.palabras)}"
        )

        # Reiniciar la palabra formada en la UI
        self.img_label.configure(text=self.actual.imagen)
        self.lbl_pista_img.configure(
            text="🔍 Pista: se revelará pronto...", 
            text_color="#A9A9A9"
        )
        self.lbl_palabra.configure(text="")  # Solo la palabra, sin prefijo
        self.lbl_estado.configure(
            text="Construye la palabra con las sílabas correctas", text_color="#5D4037"
        )
        self.mostrar_silabas()

    def revelar_pista(self):
        """Muestra la palabra oculta como ayuda."""
        self.pista_revelada = True
        self.lbl_pista_img.configure(text=f"¿Qué es? ¡Es un {self.actual.palabra}!", text_color="#8D6E63")

    def mostrar_silabas(self):
        # Sincronización de seguridad: obtener el objeto palabra directamente del dominio
        self.actual = self.juego.palabra_actual()
        if self.actual is None:
            return

        for widget in self.frame_silabas.winfo_children():
            widget.destroy()

        self.botones_silabas = []
        # Estabilizar el grid: definimos un tamaño mínimo para las columnas
        # para que el crecimiento de los botones (hover) no mueva el resto de la UI.
        for i in range(3):
            self.frame_silabas.grid_columnconfigure(i, minsize=160)
        # Aseguramos que las sílabas correctas estén siempre presentes
        num_distractores_necesarios = min(
            15 - len(self.actual.silabas), len(self.juego.distractores)
        )
        distractores_a_usar = random.sample(
            self.juego.distractores, num_distractores_necesarios
        )
        opciones = self.actual.silabas + distractores_a_usar
        random.shuffle(opciones)

        for index, silaba in enumerate(opciones):
            btn = ctk.CTkButton(
                self.frame_silabas,
                text=silaba,
                width=130,
                height=45,
                font=("Verdana", 20, "bold"),
                fg_color=self.color_tema,
                hover_color=self._lighten_color(self.color_tema),
                border_width=3,
                border_color=self.color_borde_tema,
                corner_radius=15,
                command=lambda s=silaba, idx=index: self.seleccionar_silaba(s, idx),
            )
            btn.grid(row=index // 3, column=index % 3, padx=8, pady=6)
            self.botones_silabas.append(btn)

    def seleccionar_silaba(self, silaba: str, idx: int):
        btn_clic = self.botones_silabas[idx]
        valido, estado = self.juego.agregar_silaba(silaba)
        if not valido:
            AudioService.reproducir("incorrecto")
            btn_clic.configure(fg_color="#E74C3C") # Rojo énfasis

            self.errores += 1
            
            # Lógica de pista por errores
            self.errores_ronda += 1
            if self.errores_ronda >= 4:
                self.revelar_pista()

            self.lbl_estado.configure(
                text="¡Incorrecto! Intenta de nuevo", text_color="red"
            )
            # Bloquear clics mientras se muestra el error
            for b in self.botones_silabas:
                b.configure(state="disabled")
            
            self.after(1000, self._resetear_intento_actual)
            return

        AudioService.reproducir("correcto")
        # Color gris para demostrar que ya fue seleccionada
        btn_clic.configure(fg_color="#BDC3C7", state="disabled")

        if estado == "completada":
            self.aciertos += 1
            progreso_incremento = 1.0 / max(1, len(self.juego.palabras))
            self.gestor.actualizar_progreso("Lectura y Escritura", progreso_incremento)
            # Si está completa, mostramos la palabra entera desde el objeto actual
            # para evitar que se vea vacía por el reinicio interno del juego.
            self.lbl_palabra.configure(text=self.actual.palabra)
            self.lbl_estado.configure(
                text="¡Muy bien! Palabra completa", text_color="green"
            )
            self.after(1000, self.cargar_palabra)
        else:
            # Si es parcial, mostramos lo que lleva el niño
            self.lbl_palabra.configure(text=self.juego.palabra_formada)
            self.lbl_estado.configure(
                text="Continúa con la siguiente sílaba", text_color="#5D4037"
            )

    def _resetear_intento_actual(self):
        """Reinicia visualmente el teclado sin mezclar las sílabas."""
        if not self.winfo_exists():
            return
        self.lbl_palabra.configure(text="")
        for b in self.botones_silabas:
            b.configure(fg_color=self.color_tema, state="normal")
        self.lbl_estado.configure(text="Selecciona las sílabas correctas", text_color="#5D4037")

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

        notificar_logro("lenguaje_nivel_2", parent=self)
        self.mostrar_resumen()

    def mostrar_resumen(self):
        """Muestra una pantalla de resultados temática similar al Nivel 1."""
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
            text="📜 REPORTE DEL CONSTRUCTOR 📜",
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

        crear_linea_stat(stats_frame, "✅ Palabras Construidas:", self.aciertos, "#27AE60")
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
            from .constructor_palabras import VistaConstructorPalabras
            VistaConstructorPalabras(parent)

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
            from .carrera_letras import VistaCarreraLetras
            VistaCarreraLetras(parent)

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