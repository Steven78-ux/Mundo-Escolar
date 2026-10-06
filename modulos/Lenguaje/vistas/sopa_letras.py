"""Vistas del módulo vistas."""

import customtkinter as ctk
import random
import time
from .base import JuegoBase
from ..dominio.juegos import SopaLetras
from ..servicios.audio import AudioService
from ..servicios.preguntas import obtener_sopas
from core.gestor_estado import GestorEstado
from core.util_logros import notificar_logro

class VistaSopaLetras(JuegoBase):
    def __init__(self, parent):
        super().__init__(parent, "Sopa de Letras", "#9B59B6")
        
        # Lógica de Rondas recalibrada: 2 fáciles, 2 medias, 2 difíciles
        todas = obtener_sopas()
        faciles = [s for s in todas if len(s.tablero) <= 6]
        medios = [s for s in todas if 7 <= len(s.tablero) <= 9]
        dificiles = [s for s in todas if len(s.tablero) >= 10]
        
        # Selección ordenada por dificultad: 2 fáciles -> 2 medias -> 2 difíciles
        rondas_seleccionadas = (
            random.sample(faciles, 2) + 
            random.sample(medios, 2) + 
            random.sample(dificiles, 2)
        )
        
        self.juego = SopaLetras(rondas_seleccionadas)
        self.secuencia_ui = []  # botones ya acertados
        self.gestor = GestorEstado()

        # Estadísticas para el resumen
        self.aciertos = 0
        self.errores = 0
        self.global_start_time = time.time()
        
        # Estado de ronda para el reloj
        self.round_time_limit = 45
        self.round_start_time = time.time()

        self.timer_id = None # ID para cancelar el timer de tkinter
        
        self.configurar_ui()
        self.cargar_sopa()
        self._update_timer() # Iniciar el timer después de cargar la primera sopa

    def configurar_ui(self):
        # Contenedor central
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(expand=True)

        self.lbl_exito = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Verdana", 24, "bold"),
            text_color="#27AE60",
        )
        self.lbl_exito.pack(pady=(5, 0))

        self.lbl_pista = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Verdana", 32, "bold"),
            text_color="#2B2D42",
        )
        self.lbl_pista.pack(pady=(5, 10))

        self.grid_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.grid_frame.pack(pady=10)

        # Pre-crear el máximo número de botones para la sopa de letras
        self.max_grid_dim = 12 # Max 12x12 grid (para "CONSTRUCCIÓN", "REFRIGERADOR", "ENCICLOPEDIA")
        self.celdas = []
        for i in range(self.max_grid_dim):
            fila_botones = []
            for j in range(self.max_grid_dim):
                btn = ctk.CTkButton(
                    self.grid_frame,
                    text="", # Placeholder text
                    width=42, # Smallest possible size, will be updated
                    height=42,
                    font=("Verdana", 16, "bold"), # Smallest possible font, will be updated
                    fg_color="#FDF5E6",
                    text_color="#2B2D42",
                    border_width=1,
                    border_color="#BCAAA4",
                    corner_radius=5,
                    command=lambda f=i, c=j: self.click_celda(f, c),
                )
                btn.grid(row=i, column=j, padx=1, pady=1) # Place them to configure grid
                btn.grid_remove() # Initially hide all buttons
                fila_botones.append(btn)
            self.celdas.append(fila_botones)

        # Configure grid columns/rows for the maximum size once
        for i in range(self.max_grid_dim):
            self.grid_frame.grid_columnconfigure(i, weight=1)
            self.grid_frame.grid_rowconfigure(i, weight=1)

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
            text="📝 INSTRUCCIONES:\n\nBusca la palabra en el tablero y pulsa sus letras en orden. ¡Cuidado, la última ronda es un gran desafío!",
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
            text="Palabra: 1 / 6",
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

    def _update_timer(self):
        if not self.winfo_exists() or self.juego.completado:
            return

        # Cálculo de tiempo de ronda
        ahora = time.time()
        restante = int(self.round_time_limit - (ahora - self.round_start_time))
        
        if restante <= 0:
            self.lbl_timer.configure(text="Tiempo: 00:00", text_color="#E74C3C")
            self.perder_ronda()
            return

        # Lógica de colores del reloj
        color = "#27AE60" # Verde (Mantenemos el verde por defecto)
        if self.round_time_limit == 45:
            if restante < 5:
                # Rojo pulsante alternando cada 0.2s
                color = "#E74C3C" if int(ahora * 5) % 2 == 0 else "#FFFFFF"
            elif restante < 10:
                color = "#E74C3C" # Rojo
            elif restante < 20:
                color = "#F1C40F" # Amarillo
        else: # 90 segundos
            if restante < 5:
                color = "#E74C3C" if int(ahora * 5) % 2 == 0 else "#FFFFFF"
            elif restante < 10:
                color = "#E74C3C" # Rojo
            elif restante < 30:
                color = "#F1C40F" # Amarillo
        
        m = restante // 60
        s = restante % 60
        self.lbl_timer.configure(text=f"Tiempo: {m:02d}:{s:02d}", text_color=color)
        self.timer_id = self.after(100, self._update_timer)

    def perder_ronda(self):
        self.errores += 1
        AudioService.reproducir("incorrecto")
        self.lbl_exito.configure(text="⌛ ¡TIEMPO AGOTADO! ⌛", text_color="#E74C3C")
        self.lbl_pista.configure(text="¡No te rindas! Inténtalo en la próxima", text_color="#A9A9A9")
        
        self.juego.indice += 1
        self.after(3000, self.cargar_sopa)

    def finalizar(self, mensaje: str):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        notificar_logro("lenguaje_nivel_8", parent=self)
        self.mostrar_resumen()

    def cargar_sopa(self):
        if self.juego.completado:
            self.finalizar("¡Increíble! Eres un maestro de las Sopas de Letras.")
            return
            
        self.secuencia_ui = []
        self.lbl_exito.configure(text="")

        sopa = self.juego.sopa_actual()
        self.lbl_ronda.configure(text=f"Palabra: {self.juego.indice + 1} / 6")
        
        # Configurar tiempo de ronda
        n = len(sopa.tablero)
        self.round_time_limit = 45 if n <= 7 else 90
        self.round_start_time = time.time()
        
        # Ajuste granular del tamaño según la cantidad de celdas (n x n)
        if n <= 5: # Tableros muy pequeños (SOL, GATO)
            btn_size = 85
            font_size = 32
        elif n <= 7: # Tableros medianos (BARCO, ESCUELA)
            btn_size = 65
            font_size = 24
        elif n <= 9: # Tableros grandes (MARIPOSA, ELEFANTE)
            btn_size = 48
            font_size = 18
        else: # Tableros extra grandes (DINOSAURIO, COMPUTADORA)
            btn_size = 42
            font_size = 16

        self.lbl_pista.configure(text=f"🔍 BUSCA: {sopa.palabra.upper()}")
        if not self.timer_id:
            self._update_timer()

        # --- ACTUALIZACIÓN DE BOTONES REUTILIZADOS ---
        for i in range(self.max_grid_dim):
            for j in range(self.max_grid_dim):
                btn = self.celdas[i][j]
                if i < n and j < n: 
                    letra = sopa.tablero[i][j]
                    btn.configure(
                        text=letra,
                        width=btn_size,
                        height=btn_size,
                        font=("Verdana", font_size, "bold"),
                        fg_color="#FDF5E6",
                        text_color="#2B2D42",
                        state="normal",
                    )
                    btn.grid() # Mostrar si está en el rango n x n
                else:
                    btn.grid_remove() # Ocultar si está fuera del rango

    def click_celda(self, fila, columna):
        acierto, completa = self.juego.intentar_posicion(fila, columna)
        if acierto:
            # marcar la celda como correcta
            self.celdas[fila][columna].configure(fg_color="#27AE60", state="disabled")
            self.secuencia_ui.append((fila, columna))
            if completa:
                self.aciertos += 1
                if self.timer_id:
                    self.after_cancel(self.timer_id)
                    self.timer_id = None
                AudioService.reproducir("correcto")
                self.lbl_exito.configure(text="✨ FELICIDADES ENCONTRASTES LA PALABRA ✨")
                self.after(2000, self.cargar_sopa)
            else:
                AudioService.reproducir("correcto")
        else:
            # error: quitar marcas y reiniciar secuencia en la UI
            for f, c in self.secuencia_ui:
                self.celdas[f][c].configure(
                    fg_color="#FDF5E6",
                    state="normal",
                )
            self.secuencia_ui.clear()
            AudioService.reproducir("incorrecto")

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
            text="📜 REPORTE DEL EXPLORADOR 📜",
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

        crear_linea_stat(stats_frame, "✅ Palabras Logradas:", self.aciertos, "#27AE60")
        crear_linea_stat(stats_frame, "❌ Palabras Perdidas:", self.errores, "#E74C3C")
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
            from .sopa_letras import VistaSopaLetras
            VistaSopaLetras(parent)

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

        # Botón Finalizar (Derecha)
        ctk.CTkButton(
            btns_frame,
            text="🏆 ¡TERMINAR!",
            font=("Verdana", 16, "bold"),
            width=220,
            height=55,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            corner_radius=15,
            command=self.destroy
        ).pack(side="left", padx=20)