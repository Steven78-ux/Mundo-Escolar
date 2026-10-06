"""Archivo del módulo Lenguaje."""

import customtkinter as ctk
import random
import math
import os
from PIL import Image
from .vistas.detective_sonidos import VistaDetectiveSonidos
from .vistas.constructor_palabras import VistaConstructorPalabras
from .vistas.carrera_letras import VistaCarreraLetras
from .vistas.escribe_palabra import VistaEscribePalabra
from .vistas.rimas import VistaRimas
from .vistas.ordena_letras import VistaOrdenaLetras
from .vistas.lee_encuentra import VistaLeeEncuentra
from .vistas.sopa_letras import VistaSopaLetras
from core.gestor_estado import GestorEstado


def crear_frame(parent, on_back_callback):
    """Punto de entrada embebido para ModuleFactory."""
    menu = LenguajeMenu(parent, on_back_callback)
    menu.pack(fill="both", expand=True)
    return menu


class LenguajeMenu(ctk.CTkFrame):
    """Menú principal del módulo de Lenguaje (embebido en panel principal)."""

    def __init__(self, parent, on_back_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back_callback

        # --- PERSISTENCIA Y USUARIO ---
        self.gestor_estado = GestorEstado()
        self.nombre_usuario = getattr(self.gestor_estado, "usuario_actual", "Escritor")

        # --- DEFINICIÓN DE NIVELES ---
        self.niveles = [
            {
                "id": 1,
                "text": "🎧\nDetective de Sonidos",
                "desc": "Identifica los sonidos\nde cada letra.",
                "color": "#3498DB",
                "border": "#1B4F72",
                "pos": (0.15, 0.20),
                "cmd": VistaDetectiveSonidos,
                "logro_id": "lenguaje_nivel_1",
            },
            {
                "id": 2,
                "text": "🧱\nConstructor",
                "desc": "Forma palabras uniendo\nsus letras.",
                "color": "#2ECC71",
                "border": "#186A3B",
                "pos": (0.40, 0.30),
                "cmd": VistaConstructorPalabras,
                "logro_id": "lenguaje_nivel_2",
            },
            {
                "id": 3,
                "text": "🚂\nCarrera de Letras",
                "desc": "Diferencia letras que\nse parecen.",
                "color": "#E74C3C",
                "border": "#7B241C",
                "pos": (0.65, 0.20),
                "cmd": VistaCarreraLetras,
                "logro_id": "lenguaje_nivel_3",
            },
            {
                "id": 4,
                "text": "✍️\nEscribe Palabras",
                "desc": "Mira la imagen y\nescribe su nombre.",
                "color": "#8E44AD",
                "border": "#4A235A",
                "pos": (0.85, 0.30),
                "cmd": VistaEscribePalabra,
                "logro_id": "lenguaje_nivel_4",
            },
            {
                "id": 5,
                "text": "🎵\nRimas Divertidas",
                "desc": "Busca palabras que\nsuenan igual.",
                "color": "#F39C12",
                "border": "#7E5109",
                "pos": (0.85, 0.70),
                "cmd": VistaRimas,
                "logro_id": "lenguaje_nivel_5",
            },
            {
                "id": 6,
                "text": "🔤\nOrdena Letras",
                "desc": "Pon las letras en el\nlugar correcto.",
                "color": "#1ABC9C",
                "border": "#0E6251",
                "pos": (0.65, 0.80),
                "cmd": VistaOrdenaLetras,
                "logro_id": "lenguaje_nivel_6",
            },
            {
                "id": 7,
                "text": "📖\nLee y Encuentra",
                "desc": "Lee la palabra y\nselecciona su dibujo.",
                "color": "#E67E22",
                "border": "#6E2C00",
                "pos": (0.40, 0.70),
                "cmd": VistaLeeEncuentra,
                "logro_id": "lenguaje_nivel_7",
            },
            {
                "id": 8,
                "text": "🔍\nSopa de Letras",
                "desc": "¡Encuentra las palabras\nocultas!",
                "color": "#9B59B6",
                "border": "#512E5F",
                "pos": (0.15, 0.80),
                "cmd": VistaSopaLetras,
                "logro_id": "lenguaje_nivel_8",
            },
        ]

        # --- CARGA DE ICONOS DE MAPA ---
        self.iconos_mapa = {}
        ruta_assets = os.path.join(os.path.dirname(__file__), "assets")
        for nombre in ["diccionario", "libros", "lupa", "pluma"]:
            path = os.path.join(ruta_assets, f"{nombre}.png")
            if os.path.exists(path):
                try:
                    img_pil = Image.open(path)
                    self.iconos_mapa[nombre] = ctk.CTkImage(
                        light_image=img_pil, size=(70, 70)
                    )
                except Exception as e:
                    print(f"Error cargando {nombre}.png: {e}")

        # --- LOGROS PANEL (DERECHA) ---
        self.logros_visible = False
        self._setup_logros_panel()

        # --- CABECERA ESTILO PERGAMINO/ESCRITURA ---
        self.header_card = ctk.CTkFrame(
            self,
            fg_color="#FEF9E7",  # Crema cálido tipo papel
            corner_radius=25,
            border_width=3,
            border_color="#8D6E63",  # Marrón tinta
        )
        self.header_card.pack(fill="x", padx=40, pady=25)

        # Botón para volver al menú principal integrado en la temática
        if self.on_back:
            btn_atras = ctk.CTkButton(
                self.header_card,
                text="⬅ MENU",
                width=110,
                height=45,
                fg_color="#8D6E63", # Color Tinta
                hover_color="#5D4037",
                text_color="#FEF9E7", # Color Pergamino
                corner_radius=15,
                font=("Verdana", 13, "bold"),
                command=self.on_back,
            )
            btn_atras.place(x=25, rely=0.5, anchor="w")
            
        # Perfil del Escritor (Derecha de la tarjeta)
        self.profile_btn = ctk.CTkFrame(
            self.header_card,
            fg_color="#FDF5E6",
            corner_radius=15,
            border_width=2,
            border_color="#8D6E63",
            cursor="hand2",
        )
        self.profile_btn.place(relx=0.97, rely=0.5, anchor="e")

        ctk.CTkLabel(
            self.profile_btn,
            text=f"✒️ {self.nombre_usuario.upper()}",
            font=("Verdana", 14, "bold"),
            text_color="#5D4037",
        ).pack(padx=15, pady=8)

        # Eventos para el perfil
        self.profile_btn.bind("<Button-1>", lambda e: self.toggle_logros())
        for child in self.profile_btn.winfo_children():
            child.bind("<Button-1>", lambda e: self.toggle_logros())

        self.profile_btn.bind(
            "<Enter>", lambda e: self.profile_btn.configure(border_color="#E67E22")
        )
        self.profile_btn.bind(
            "<Leave>", lambda e: self.profile_btn.configure(border_color="#8D6E63")
        )

        # Contenedor de Textos (Título, Subtítulo y Descripción)
        text_container = ctk.CTkFrame(self.header_card, fg_color="transparent")
        text_container.pack(
            expand=True, pady=15
        )  # Centrado automático al no tener side="left"

        ctk.CTkLabel(
            text_container,
            text="🖋️ MUNDO DE LENGUAJE Y ESCRITURA 📜",
            font=("Verdana", 30, "bold"),
            text_color="#2B2D42",
        ).pack()

        ctk.CTkLabel(
            text_container,
            text="📖 Crónicas de un Pequeño Escritor",
            font=("Verdana", 18, "bold"),
            text_color="#E67E22",
        ).pack()

        ctk.CTkLabel(
            text_container,
            text="✍️ Traza tu camino, lee con atención y descubre el poder de las palabras",
            font=("Verdana", 14, "italic"),
            text_color="#5D4037",
        ).pack()

        # --- CONTENEDOR DEL MAPA (CANVAS) ---
        # Usamos un frame con scroll o simplemente un frame grande para el camino
        self.map_container = ctk.CTkFrame(
            self,
            fg_color="#FDF5E6",  # Color papel antiguo (OldLace)
            corner_radius=20,
            border_width=30,  # Borde más grueso para simular un marco de madera/libro
            border_color="#4E342E",  # Marrón muy oscuro para contraste
        )
        self.map_container.pack(expand=True, fill="both", padx=50, pady=(0, 40))

        self.canvas = ctk.CTkCanvas(
            self.map_container, bg="#FDF5E6", highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")

        self.after(100, self.dibujar_mapa)

    def _setup_logros_panel(self):
        """Configura el panel de logros lateral."""
        if hasattr(self, "logros_frame") and self.logros_frame.winfo_exists():
            self.logros_frame.destroy()

        self.logros_frame = ctk.CTkScrollableFrame(
            self,
            width=320,
            height=500,
            fg_color="#FEF9E7",
            border_width=4,
            border_color="#8D6E63",
            label_text="📜 TUS LOGROS DE ESCRITOR 📜",
            label_font=("Verdana", 14, "bold"),
            label_text_color="#5D4035",
            label_fg_color="#FDF5E6",
            corner_radius=20,
        )

        for nivel in self.niveles:
            unlocked = bool(nivel.get("logro_id")) and self.gestor_estado.tiene_logro(nivel["logro_id"])

            if unlocked:
                item = ctk.CTkFrame(
                    self.logros_frame,
                    fg_color="#FDF5E6",
                    corner_radius=12,
                    border_width=1,
                    border_color="#D7CCC8",
                )
                item.pack(fill="x", pady=6, padx=8)

                emoji = nivel["text"].split("\n")[0]
                nombre_logro = nivel["text"].replace("\n", " ")

                ctk.CTkLabel(item, text=emoji, font=("Arial", 22)).pack(
                    side="left", padx=10
                )
                ctk.CTkLabel(
                    item,
                    text=f"Maestro de:\n{nombre_logro}",
                    font=("Verdana", 10, "bold"),
                    text_color="#2B2D42",
                    justify="left",
                ).pack(side="left", pady=10)

                # Marcador de completado
                ctk.CTkLabel(
                    item, text="⭐", text_color="#FFD700", font=("Arial", 18)
                ).pack(side="right", padx=15)
            else:
                # Estilo BLOQUEADO solicitado
                item = ctk.CTkFrame(
                    self.logros_frame,
                    fg_color="#D1D1D1", # Gris para bloqueado
                    corner_radius=12,
                    border_width=1,
                    border_color="#A9A9A9",
                )
                item.pack(fill="x", pady=6, padx=8)

                ctk.CTkLabel(item, text="🔒", font=("Arial", 22)).pack(
                    side="left", padx=10
                )
                ctk.CTkLabel(
                    item,
                    text="BLOQUEADO",
                    font=("Verdana", 10, "bold"),
                    text_color="#666666",
                ).pack(side="left", pady=10)

    def toggle_logros(self):
        """Muestra u oculta el panel de logros."""
        if self.logros_visible:
            self.logros_frame.place_forget()
        else:
            self._setup_logros_panel()
            self.logros_frame.place(relx=0.97, y=140, anchor="ne")
            self.logros_frame.lift()
        self.logros_visible = not self.logros_visible

    def dibujar_mapa(self):
        """Dibuja el sendero y los botones en el canvas."""
        self.update_idletasks()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        self.canvas.delete("all")

        # Dibujar un borde interno fino decorativo (doble marco)
        self.canvas.create_rectangle(10, 10, w - 10, h - 10, outline="#A1887F", width=2)

        # 1. Dibujar Textura de Papel Arrugado
        self.dibujar_textura_papel(w, h)

        # Dibujar Iconos Decorativos en las esquinas del papel
        posiciones_iconos = {
            "diccionario": (0.04, 0.08),
            "libros": (0.93, 0.08),
            "lupa": (0.04, 0.92),
            "pluma": (0.93, 0.92),
        }
        for nombre, rel_pos in posiciones_iconos.items():
            if nombre in self.iconos_mapa:
                lbl_icon = ctk.CTkLabel(
                    self.canvas,
                    image=self.iconos_mapa[nombre],
                    text="",
                    fg_color="transparent",
                )
                self.canvas.create_window(
                    rel_pos[0] * w, rel_pos[1] * h, window=lbl_icon
                )

        # 2. Dibujar el sendero (Línea punteada)
        puntos = []
        for nivel in self.niveles:
            px = nivel["pos"][0] * w
            py = nivel["pos"][1] * h
            puntos.append((px, py))

        for i in range(len(puntos) - 1):
            p1 = puntos[i]
            p2 = puntos[i + 1]
            # Línea de sombra de la ruta
            self.canvas.create_line(
                p1[0],
                p1[1] + 4,
                p2[0],
                p2[1] + 4,
                fill="#D7CCC8",  # Sombra de tinta más suave
                width=8,
                dash=(10, 8),
            )
            # Línea principal
            self.canvas.create_line(
                p1[0], p1[1], p2[0], p2[1], fill="#8D6E63", width=6, dash=(10, 8)
            )

        # 3. Crear los botones
        for nivel in self.niveles:
            self.crear_boton_3d(nivel, w, h)

    def dibujar_textura_papel(self, w, h):
        """Dibuja líneas y polígonos aleatorios muy tenues para simular papel arrugado."""
        # Pliegues grandes aleatorios (grietas de papel viejo)
        for _ in range(15):
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = random.randint(0, w), random.randint(0, h)
            self.canvas.create_line(x1, y1, x2, y2, fill="#EADBC8", width=1)

        # Pequeñas arrugas de textura (grano del papel)
        for _ in range(80):
            x = random.randint(0, w)
            y = random.randint(0, h)
            length = random.randint(10, 50)
            angle = random.uniform(0, 2 * math.pi)
            x2 = x + length * math.cos(angle)
            y2 = y + length * math.sin(angle)
            self.canvas.create_line(x, y, x2, y2, fill="#F2E4C9", width=1)

    def crear_boton_3d(self, nivel, w, h):
        """Crea un botón con efecto 3D y bordes redondeados."""
        px = nivel["pos"][0] * w
        py = nivel["pos"][1] * h

        # Contenedor para simular sombra/3D
        # El efecto 3D se logra con un borde grueso y colores contrastantes
        btn = ctk.CTkButton(
            self.canvas,
            text=f"NIVEL {nivel['id']}\n{nivel['text']}",
            font=("Verdana", 14, "bold"),
            width=180,
            height=100,
            corner_radius=30,
            fg_color=nivel["color"],
            hover_color=self.lighten_color(nivel["color"]),
            border_width=4,
            border_color=nivel["border"],  # Borde más oscuro para efecto de profundidad
            command=lambda n=nivel: n["cmd"](self),
        )

        # Colocar el botón en el canvas usando coordenadas absolutas
        # Usamos window_create del canvas de tkinter subyacente
        self.canvas.create_window(px, py, window=btn)

        # --- TARJETA DE DESCRIPCIÓN CONECTADA ---
        # Calculamos una posición debajo del botón
        desc_y = py + 65

        # Dibujar línea de conexión sutil
        self.canvas.create_line(
            px, py + 50, px, desc_y - 15, fill="#8D6E63", width=2, dash=(2, 2)
        )

        # Fondo de la tarjeta de descripción (Pequeño pergamino)
        self.canvas.create_rectangle(
            px - 85,
            desc_y - 15,
            px + 85,
            desc_y + 35,
            fill="#FFF9C4",
            outline="#BCAAA4",
            width=1,
        )

        # Texto de descripción
        self.canvas.create_text(
            px,
            desc_y + 10,
            text=nivel["desc"],
            font=("Verdana", 9, "italic"),
            fill="#4E342E",
            justify="center",
        )

    def lighten_color(self, hex_color):
        """Aclara un color hex para el efecto hover."""
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, c + 30) for c in rgb)
        return "#%02x%02x%02x" % new_rgb