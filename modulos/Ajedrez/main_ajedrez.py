"""Archivo del módulo Ajedrez."""

import tkinter as tk
import customtkinter as ctk
import os
import threading
import random
from PIL import Image
from core.gestor_estado import GestorEstado
from .views.ventana_juego import VentanaJuego
from .views.tutorial_menu import TutorialAjedrez
from core.theme import COLORS, FONTS


def crear_frame(parent, on_back_callback):
    """Punto de entrada embebido para ModuleFactory."""
    menu = AjedrezMenu(parent, on_back_callback)
    menu.pack(fill="both", expand=True)
    return menu


class AjedrezMenu(ctk.CTkFrame):
    """Configuración y lanzamiento del módulo de Ajedrez (panel embebido)."""

    def __init__(self, parent, on_back_callback=None):
        super().__init__(parent, fg_color="#0D1B2A")
        self.on_back = on_back_callback
        self.gestor = GestorEstado()
        self.nombre_usuario = getattr(self.gestor, "usuario_actual", "Explorador")
        self.logros_visible = False
        self.logros_frame = None

        # Configuración de estilos visuales
        self.font_titulo = ("Verdana", 42, "bold")
        self.font_ui = ("Segoe UI Variable Display", 16, "bold")
        self.font_cards = ("Segoe UI Variable Display", 14, "bold")

        # Evento para detener el hilo de Pygame
        self.evento_cierre = threading.Event()

        # Listener global para cerrar logros
        self.bind("<Button-1>", self._check_click_outside)

        self.setup_ui()

    def setup_ui(self):
        # Fondo espacial dinámico
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#0D1B2A")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_canvas.bind("<Button-1>", self._check_click_outside)

        # Dibujar burbujas de fondo para dar profundidad (Estilo Espacial)
        for _ in range(60):
            x = random.randint(0, screen_w)
            y = random.randint(0, screen_h)
            r = random.randint(3, 15)
            color = random.choice(["#1B263B", "#2C3E50", "#1B263B", "#0D1B2A"])
            self.bg_canvas.create_oval(x, y, x + r, y + r, fill=color, outline="")

        # Asegurar que el panel de logros esté listo
        self._setup_logros_panel()

        self.diff_cards = []
        self.bando_cards = []
        self.tiempo_cards = []
        self.tema_cards = []

        # Cargar imágenes para selección de bando (estilo Lichess)
        path_p = os.path.join(os.path.dirname(__file__), "assets", "piezas_animadas")
        try:
            self.img_bando_blanco = ctk.CTkImage(
                light_image=Image.open(os.path.join(path_p, "rey_blanco.png")),
                size=(100, 100),
            )
            self.img_bando_negro = ctk.CTkImage(
                light_image=Image.open(os.path.join(path_p, "rey_negro.png")),
                size=(100, 100),
            )
        except Exception:
            # Si no se pueden cargar las imágenes, usamos iconos simples.
            self.img_bando_blanco = "♔"
            self.img_bando_negro = "♚"

        # Botón de Salir Personalizado
        self.btn_exit_top = ctk.CTkButton(
            self,
            text="← Volver al menú",
            font=self.font_ui,
            fg_color=COLORS["sidebar"],
            text_color="white",
            hover_color=COLORS["sidebar_hover"],
            width=180,
            height=40,
            corner_radius=15,
            command=self.cerrar_juego,
        )
        self.btn_exit_top.place(x=40, y=40)

        # Perfil del Piloto (Superior Derecha) - Estilo Espacial
        self.profile_btn = ctk.CTkFrame(
            self,
            fg_color="#1B263B",
            corner_radius=15,
            border_width=2,
            border_color="#00D4FF",
            cursor="hand2",
        )
        self.profile_btn.place(relx=0.97, y=40, anchor="ne")
        
        self.lbl_perfil = ctk.CTkLabel(
            self.profile_btn,
            text=f"👤 {self.nombre_usuario.upper()}",
            font=self.font_ui,
            text_color="#00D4FF",
        )
        self.lbl_perfil.pack(padx=15, pady=8)

        self.profile_btn.bind("<Button-1>", lambda e: self.toggle_logros())
        for child in self.profile_btn.winfo_children():
            child.bind("<Button-1>", lambda e: self.toggle_logros())

        self.frame_config = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_config.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.frame_config,
            text="BIENVENIDO AL MUNDO DEL AJEDREZ",
            font=self.font_titulo,
            text_color="#F5F5DC",  # Blanco Crema
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.frame_config,
            text="Domina el arte de la estrategia",
            font=("Verdana", 22),
            text_color="#00D4FF",  # Cian Vibrante
        ).pack(pady=(0, 10))

        # CONTENEDOR PRINCIPAL AZUL MEDIANOCHE
        self.marco_central = ctk.CTkFrame(
            self.frame_config,
            fg_color="#1B263B",
            border_width=0,
            corner_radius=40,
        )
        self.marco_central.pack(padx=20, pady=5, fill="both")
        self.marco_central.bind("<Button-1>", self._check_click_outside)

        self.contra_ia_var = ctk.BooleanVar(value=True)
        self.seg_modo = ctk.CTkSegmentedButton(
            self.marco_central,
            values=["💻 JUGAR CON IA", "👥 JUGAR CON AMIGO"],
            command=self.toggle_modo,
            height=50,
            font=self.font_ui,
            selected_color="#27AE60",
            unselected_color="#0D1B2A",
            corner_radius=20,
        )
        self.seg_modo.pack(pady=10, padx=30)

        self.bando_var = ctk.StringVar(value="blanco")
        self.container_bando = ctk.CTkFrame(self.marco_central, fg_color="transparent")
        self.container_bando.pack(pady=5, fill="x", padx=40)

        self._crear_label_seccion(self.container_bando, "🎯 ELIGE TU BANDO")

        frame_bando_box = ctk.CTkFrame(self.container_bando, fg_color="transparent")
        frame_bando_box.pack()

        bandos = [
            ("blanco", self.img_bando_blanco, "Blancas"),
            ("aleatorio", "🎲", "Aleatorio"),
            ("negro", self.img_bando_negro, "Negras"),
        ]
        for val, content, nombre in bandos:
            card = self._crear_base_card(frame_bando_box, 180, 160, 40)
            card.pack(side="left", padx=10)

            if isinstance(content, ctk.CTkImage):
                ctk.CTkLabel(card, image=content, text="").pack(
                    expand=True, pady=(10, 0)
                )
            else:
                ctk.CTkLabel(
                    card, text=content, font=("Arial", 60), text_color="white"
                ).pack(expand=True, pady=(10, 0))

            ctk.CTkLabel(
                card, text=nombre, font=self.font_cards, text_color="#00D4FF"
            ).pack(pady=(0, 10))
            self._bind_click(
                card, lambda e, v=val: self._seleccionar_opcion("bando", v)
            )
            self.bando_cards.append((val, card))
            self._setup_hover(card, val, "bando")

        self.diff_var = ctk.StringVar(value="Hierro")
        self._crear_label_seccion(self.marco_central, "🏆 RANGOS DE DESAFÍO")

        self.lbl_diff_desc = ctk.CTkLabel(
            self.marco_central,
            text=" ¡Selecciona tu rango! ",
            font=self.font_cards,
            text_color="#0D1B2A",
            fg_color="#00D4FF",
            corner_radius=15,
            height=30,
        )
        self.lbl_diff_desc.pack(pady=(5, 10))

        # --- CARRUSEL DE DIFICULTADES ---
        self.scroll_offset = 0
        frame_carousel = ctk.CTkFrame(self.marco_central, fg_color="transparent")
        frame_carousel.pack(pady=8, padx=20)

        # Botón Izquierda
        self.btn_prev = ctk.CTkButton(
            frame_carousel,
            text="<",
            font=("Arial", 32, "bold"),
            fg_color="transparent",
            text_color="#00D4FF",
            hover_color="#2C3E50",
            width=40,
            command=lambda: self._scroll_carousel(-1),
        )
        self.btn_prev.pack(side="left")

        # Ventana de Visualización (Viewport) para 4 tarjetas
        # Calculamos el ancho del carrusel proporcionalmente al ancho de pantalla
        ancho_viewport = min(530, int(screen_w * 0.45))
        
        self.viewport_diff = ctk.CTkFrame(
            frame_carousel, width=ancho_viewport, height=130, fg_color="transparent"
        )
        self.viewport_diff.pack(side="left", padx=10)
        self.viewport_diff.pack_propagate(False)

        self.container_diff_inner = ctk.CTkFrame(
            self.viewport_diff, fg_color="transparent"
        )
        self.container_diff_inner.place(x=0, y=5)

        # Botón Derecha
        self.btn_next = ctk.CTkButton(
            frame_carousel,
            text=">",
            font=("Arial", 32, "bold"),
            fg_color="transparent",
            text_color="#00D4FF",
            hover_color="#2C3E50",
            width=40,
            command=lambda: self._scroll_carousel(1),
        )
        self.btn_next.pack(side="right")

        # Cargar imagen especial para el rango supremo (Ayanokoji)
        path_kiyo = os.path.join(os.path.dirname(__file__), "assets", "imagenes", "kiyo.jpg")
        self.img_kiyo = None
        if os.path.exists(path_kiyo):
            try:
                self.img_kiyo = ctk.CTkImage(light_image=Image.open(path_kiyo), size=(50, 50))
            except: pass

        difficulties = [
            ("⚔️", "300", "Hierro", "#B0BEC5"),
            ("🥉", "500", "Bronce", "#CD7F32"),
            ("🥈", "800", "Plata", "#E0E0E0"),
            ("🥇", "1000", "Oro", "#FFD700"),
            ("💎", "1300", "Diamante", "#00D4FF"),
            ("👑", "1500", "Maestro", "#A349A4"),
            ("☄️", "1800", "Gran Maestro", "#FF4500"),
            ("🔯", "2000", "Élite", "#FF00FF"),
            ("🌌", "2300", "Galáctico", "#483D8B"),
            ("🌟", "2500", "Estelar", "#FFFACD"),
            ("☀️", "2800", "Solar", "#FFA500"),
            ("🔮", "3000", "Místico", "#9370DB"),
        ]

        for i, (icon, elo, nom, color) in enumerate(difficulties):
            card = self._crear_base_card(self.container_diff_inner, 120, 100, 25)
            card.grid(row=0, column=i, padx=5)
            
            ctk.CTkLabel(card, text=icon, font=("Arial", 36), text_color=color).pack(pady=(10, 0))
            display_name = nom

            ctk.CTkLabel(
                card, text=display_name, 
                font=("Segoe UI Variable Display", 14, "bold"),
                text_color=color
            ).pack()

            card._rango_color = color  # Guardar color temático en el widget
            self._bind_click(card, lambda e, n=nom: self.seleccionar_dificultad(n))
            self.diff_cards.append((nom, card))
            self._setup_hover(card, nom, "diff")
            if nom == "Hierro":
                self.seleccionar_dificultad(nom)

        self._seleccionar_opcion("bando", "blanco")
        self.frame_bot = ctk.CTkFrame(self.marco_central, fg_color="transparent")
        self.frame_bot.pack(pady=5, padx=40)

        self.tiempo_var = ctk.IntVar(value=10)
        self._crear_label_grid(self.frame_bot, "⏳ TIEMPO", 0)
        self.frame_tiempo_cards = ctk.CTkFrame(self.frame_bot, fg_color="transparent")
        self.frame_tiempo_cards.grid(row=0, column=1, padx=20)

        for i, t in enumerate(["1", "3", "5", "10", "15", "30"]):
            card = self._crear_base_card(self.frame_tiempo_cards, 60, 45, 25)
            card.grid(row=0, column=i, padx=3)
            ctk.CTkLabel(
                card, text=f"⌛{t}'", font=self.font_cards, text_color="white"
            ).pack(expand=True, fill="both")
            self._bind_click(
                card, lambda e, v=t: self._seleccionar_opcion("tiempo", int(v))
            )
            self.tiempo_cards.append((t, card))
            self._setup_hover(card, t, "tiempo")
            if t == "10":
                self._seleccionar_opcion("tiempo", 10)

        self.tema_var = ctk.StringVar(value="Oceano")
        self._crear_label_grid(self.frame_bot, "🎨 ESTILO", 1)
        self.frame_tema_cards = ctk.CTkFrame(self.frame_bot, fg_color="transparent")
        self.frame_tema_cards.grid(row=1, column=1, padx=20, pady=10)

        temas_ajedrez = [
            "Madera",
            "Bosque",
            "Oceano",
            "Fresa",
            "Algodon",
            "Cristal",
        ]
        for i, t in enumerate(temas_ajedrez):
            card = self._crear_base_card(
                self.frame_tema_cards, 120 if len(t) > 10 else 90, 40, 25
            )
            card.grid(row=0, column=i, padx=4)
            ctk.CTkLabel(card, text=t, font=self.font_cards, text_color="white").pack(
                expand=True, fill="both"
            )
            self._bind_click(card, lambda e, v=t: self._seleccionar_opcion("tema", v))
            self.tema_cards.append((t, card))
            self._setup_hover(card, t, "tema")
            if t == "Oceano":
                self._seleccionar_opcion("tema", "Oceano")

        # Asegurar que el selector de modo muestre la opción activa por defecto.
        self.seg_modo.set("💻 JUGAR CON IA")

        self.btn_play = ctk.CTkButton(
            self.frame_config,
            text="🚀 EMPEZAR PARTIDA",
            command=self.lanzar_pygame,
            height=60,
            font=("Verdana", 24, "bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            corner_radius=30,
            border_width=4,
            border_color="#145A32",  # Sombra de color
        )
        self.btn_play.pack(pady=(15, 10))

        self.btn_tutorial = ctk.CTkButton(
            self.frame_config,
            text="🚀 TUTORIAL",
            command=self.abrir_tutorial,
            height=60,
            font=("Verdana", 22, "bold"),
            fg_color="#00E5FF",
            hover_color="#00B8CC",
            text_color="#0D1B2A",
            corner_radius=30,
            border_width=2,
            border_color="#FFFFFF",
        )
        self.btn_tutorial.pack(pady=10)

    def _setup_logros_panel(self):
        """Configura el panel de logros lateral con temática de ajedrez."""
        self.logros_frame = ctk.CTkScrollableFrame(
            self,
            width=350,
            height=500,
            fg_color="#0A0E1A",
            border_width=4,
            border_color="#00D4FF",
            label_text="🏆 SALÓN DE LA ESTRATEGIA 🏆",
            label_font=("Verdana", 14, "bold"),
            label_text_color="#00D4FF",
            label_fg_color="#1B263B",
            corner_radius=20,
        )

        dificultades = ["Hierro", "Bronce", "Plata", "Oro", "Diamante", "Maestro", 
                        "Gran Maestro", "Élite", "Galáctico", "Estelar", "Solar", 
                        "Místico"]
        
        conquistados = 0
        for d in dificultades:
            logro_id = f"ajedrez_{d.lower().replace(' ', '_')}"
            unlocked = self.gestor.tiene_logro(logro_id)
            if unlocked: conquistados += 1

            item = ctk.CTkFrame(
                self.logros_frame,
                fg_color="#1B263B" if unlocked else "#34495E",
                corner_radius=12,
                border_width=1,
                border_color="#00D4FF" if unlocked else "#5D6D7E",
            )
            item.pack(fill="x", pady=6, padx=8)

            ctk.CTkLabel(item, text="⭐" if unlocked else "🔒", font=("Arial", 22)).pack(side="left", padx=10)
            
            info = ctk.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, pady=10)

            ctk.CTkLabel(
                info, 
                text=d if unlocked else "BLOQUEADO", 
                font=("Verdana", 13, "bold"), 
                text_color="white", 
                anchor="w"
            ).pack(fill="x")

            desc = f"¡Rango {d} conquistado!" if unlocked else f"Para desbloquearlo tienes que derrotar al rango {d}"
            
            ctk.CTkLabel(info, text=desc, font=("Verdana", 11, "italic"), text_color="#00D4FF" if unlocked else "#AAAAAA", wraplength=220, anchor="w", justify="left").pack(fill="x")

            if unlocked:
                ctk.CTkLabel(item, text="✔️", text_color="#2ECC71", font=("Arial", 18)).pack(side="right", padx=10)

        if hasattr(self, 'lbl_perfil'):
            self.lbl_perfil.configure(text=f"👤 {self.nombre_usuario.upper()} ({conquistados}/13)")

    def toggle_logros(self):
        if self.logros_visible:
            self.logros_frame.place_forget()
        else:
            self._setup_logros_panel() # Refrescar datos
            self.logros_frame.place(relx=0.97, y=100, anchor="ne")
            self.logros_frame.lift()
        self.logros_visible = not self.logros_visible

    def _check_click_outside(self, event):
        if not self.logros_visible: return
        try:
            widget = self.winfo_containing(event.x_root, event.y_root)
            curr = widget
            while curr:
                if curr == self.logros_frame or curr == self.profile_btn: return
                curr = curr.master if hasattr(curr, 'master') else None
            self.toggle_logros()
        except: pass

    def _crear_label_seccion(self, parent, texto):
        ctk.CTkLabel(parent, text=texto, font=self.font_ui, text_color="#00D4FF").pack(
            pady=5
        )

    def _crear_label_grid(self, parent, texto, fila):
        ctk.CTkLabel(parent, text=texto, font=self.font_ui, text_color="#00D4FF").grid(
            row=fila, column=0, sticky="e", padx=10, pady=10
        )

    def abrir_tutorial(self):
        """Inicia el módulo de lecciones interactivas."""
        TutorialAjedrez(self, tema=self.tema_var.get())

    def _crear_base_card(self, parent, w, h, radius):
        """Helper para crear la estructura base de una tarjeta."""
        card = ctk.CTkFrame(
            parent,
            fg_color="#0D1B2A",
            width=w,
            height=h,
            corner_radius=radius,
            border_width=4,
            border_color="#1B263B",
        )
        card.pack_propagate(False)
        return card

    def _bind_click(self, widget, callback):
        """Vincula el clic a un widget y todos sus hijos."""
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            child.bind("<Button-1>", callback)

    def _setup_hover(self, card, val, type_cat):
        """Configura efectos de hover para las tarjetas."""

        def on_enter(e):
            if type_cat == "diff" and not self.contra_ia_var.get():
                return
            var = getattr(self, f"{type_cat}_var")
            # Si no está seleccionado, aplicamos color de hover
            if str(var.get()) != str(val):
                card.configure(border_color="#5D6D7E", border_width=4)

        def on_leave(e):
            if type_cat == "diff" and not self.contra_ia_var.get():
                return
            var = getattr(self, f"{type_cat}_var")
            # Si no está seleccionado, volvemos al borde base
            if str(var.get()) != str(val):
                card.configure(border_color="#1B263B", border_width=4)
            else:
                # Si está seleccionado, mantenemos su color de destaque
                sel_color = "#2ECC71" if type_cat == "diff" else "#00D4FF"
                card.configure(border_color=sel_color, border_width=4)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        # Propagar eventos a los hijos (labels e iconos)
        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def seleccionar_dificultad(self, nombre):
        if not self.contra_ia_var.get():
            return
        self._seleccionar_opcion("diff", nombre)
        msg = {
            "Hierro": "¡El comienzo de tu forja!",
            "Bronce": "¡Aprendiendo las bases!",
            "Plata": "¡Refinando la estrategia!",
            "Oro": "¡Nivel competitivo!",
            "Diamante": "¡Desafío extremo!",
            "Maestro": "¡Dominando el tablero!",
            "Gran Maestro": "¡Al borde de la perfección!",
            "Élite": "¡Solo para los mejores!",
            "Galáctico": "¡Estrategia de otra dimensión!",
            "Estelar": "¡Brillas como un sol!",
            "Solar": "¡Energía pura en cada jugada!",
            "Místico": "¡Lógica que parece magia!",
        }.get(nombre, "")
        self.lbl_diff_desc.configure(text=f"  💡 {msg}  ")

    def _scroll_carousel(self, direction):
        """Mueve el carrusel de dificultades horizontalmente."""
        card_step = 130  # Ancho de tarjeta + padding
        visible_count = 4
        total_count = len(self.diff_cards)

        self.scroll_offset += direction

        # Limitar el desplazamiento
        if self.scroll_offset < 0:
            self.scroll_offset = 0
        elif self.scroll_offset > total_count - visible_count:
            self.scroll_offset = total_count - visible_count

        new_x = -(self.scroll_offset * card_step)
        self.container_diff_inner.place(x=new_x)

    def _seleccionar_opcion(self, categoria, val):
        """Centraliza la lógica de selección para bando, tiempo, tema y dificultad."""
        getattr(self, f"{categoria}_var").set(val)

        for key, widget in getattr(self, f"{categoria}_cards"):
            is_sel = str(key) == str(val)
            # Borde verde #2ECC71 para dificultad seleccionada
            sel_color = "#2ECC71" if categoria == "diff" else "#00D4FF"
            color = sel_color if is_sel else "#1B263B"
            bg = (
                "#1E2A1E"
                if is_sel and categoria == "diff"
                else ("#1B3A57" if is_sel else "#0D1B2A")
            )
            widget.configure(border_color=color, fg_color=bg)

            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    if categoria == "diff":
                        txt_color = getattr(widget, "_rango_color", "white")
                    else:
                        txt_color = (
                            getattr(widget, "_rango_color", "white")
                            if is_sel and categoria == "diff"
                            else "white"
                        )
                        if categoria == "bando" and child.cget("text") in [
                            "Blancas",
                            "Aleatorio",
                            "Negras",
                        ]:
                            txt_color = "#00D4FF"
                    child.configure(text_color=txt_color)

    def toggle_modo(self, value):
        self.contra_ia_var.set(value == "💻 JUGAR CON IA")
        if self.contra_ia_var.get():
            self.seleccionar_dificultad(self.diff_var.get())
            self.lbl_diff_desc.configure(fg_color="#00D4FF", text_color="#0D1B2A")
        else:
            for _, card in self.diff_cards:
                card.configure(border_color="#1B263B", fg_color="#0D1B2A")
                for c in card.winfo_children():
                    if isinstance(c, ctk.CTkLabel):
                        c.configure(text_color="gray")
            self.lbl_diff_desc.configure(
                text=" ¡Dificultad desactivada en modo 👥! ",
                fg_color="#2C3E50",
                text_color="white",
            )

    def lanzar_pygame(self):
        """Inicia el hilo de Pygame."""
        self.frame_config.pack_forget()
        ctk.CTkLabel(
            self,
            text="Presiona ESCAPE en cualquier momento para volver al menú",
            font=("Arial", 14),
        ).pack(side="bottom", pady=20)

        # Iniciar thread
        self.pygame_thread = threading.Thread(target=self.ejecutar_ciclo_pygame)
        self.pygame_thread.daemon = True
        self.pygame_thread.start()

    def ejecutar_ciclo_pygame(self):
        """Bucle de Pygame corriendo en un hilo separado."""
        juego = VentanaJuego(
            tema=self.tema_var.get(),
            dificultad=self.diff_var.get(),
            tiempo=self.tiempo_var.get(),
            contra_ia=self.contra_ia_var.get(),
            bando_elegido=self.bando_var.get(),
            evento_cierre=self.evento_cierre,
        )
        juego.run()

        # Al salir del bucle, revisamos qué eligió el niño en el modal
        if juego.resultado_accion == "salir":
            self.after(0, self.cerrar_juego)
        else:
            # Volver al panel del módulo si la partida terminó o se cerró sin seleccionar "Salir"
            self.after(0, lambda: self.frame_config.pack(expand=True))

    def cerrar_juego(self):
        """Cierra Pygame y vuelve al menú principal si hay callback."""
        try:
            self.grab_release()
        except Exception:
            pass
        self.evento_cierre.set()
        if hasattr(self, "pygame_thread"):
            self.pygame_thread.join(timeout=1.0)
        if self.on_back:
            self.on_back()
        else:
            self.destroy()


def main_ajedrez(parent, on_back_callback=None):
    """Compatibilidad con lanzadores antiguos."""
    return crear_frame(parent, on_back_callback or (lambda: None))