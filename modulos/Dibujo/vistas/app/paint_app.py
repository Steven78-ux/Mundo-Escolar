"""Archivo del módulo Dibujo."""

import tkinter as tk
from tkinter import colorchooser, filedialog
import customtkinter as ctk
from PIL import Image, ImageGrab, ImageTk
import random
import math

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS


def crear_frame(parent, on_back_callback):
    """Punto de entrada embebido para ModuleFactory."""
    contenedor = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
    contenedor.pack(fill="both", expand=True)

    barra = ctk.CTkFrame(contenedor, fg_color=COLORS["sidebar"], height=50, corner_radius=0)
    barra.pack(fill="x")
    barra.pack_propagate(False)
    ctk.CTkButton(
        barra,
        text="← Volver al menú",
        font=FONTS["botones"],
        fg_color="transparent",
        hover_color=COLORS["sidebar_hover"],
        text_color="white",
        corner_radius=15,
        command=on_back_callback,
    ).pack(side="left", padx=15, pady=8)

    ctk.CTkLabel(
        barra,
        text="🎨 Mini Paint",
        font=FONTS["subtitulo"],
        text_color="white",
    ).pack(side="left", padx=20)

    area = ctk.CTkFrame(contenedor, fg_color="transparent")
    area.pack(fill="both", expand=True)
    PaintApp(area, embebido=True)
    GestorEstado().actualizar_progreso("Dibujo", 0.05)
    return contenedor


class PaintApp:
    PALETTE = [
        "#000000", "#464646", "#780000", "#FF0000", "#FF8700", "#FFD300", "#DEFF0A", "#A1FF0A", 
        "#0AFF99", "#0AEFFF", "#147DF5", "#580AFF", "#BE0AFF", "#FF0A92", "#FFFFFF", "#C1C1C1"
    ]
    
    THEME = {
        "bg": "#E3F2FD",
        "toolbar": "#BBDEFB",
        "canvas_bg": "#FFFFFF",
        "accent": "#1976D2"
    }

    def __init__(self, parent, embebido=False):
        self.parent = parent
        self.embebido = embebido
        if not embebido and hasattr(parent, "title"):
            self.parent.title("Mini Paint")
        if hasattr(parent, "configure"):
            try:
                self.parent.configure(fg_color="transparent" if embebido else None)
            except Exception:
                if not embebido:
                    self.parent.configure(bg="#dff9fb")
        if not embebido:
            self.parent.minsize(900, 650)
        self.color_actual = "#22223b"
        self.grosor = 7
        self.herramienta = "lapiz"
        self.pincel_tipo = "redondo"
        self.objetos = [] # Almacena tuplas (tipo, coords, color, grosor, relleno)
        self.history_redo = []
        self.zoom_level = 1.0
        self.start_x = None
        self.start_y = None
        self.bg_image_obj = None # Para cargar imágenes
        self.preview_id = None
        self.trazo_actual = None

        self._make_toolbar()
        self._make_canvas()
        self._make_status_bar()

        self.parent.bind("<Control-plus>", lambda _: self.zoom(1.1))
        self.parent.bind("<Control-minus>", lambda _: self.zoom(0.9))
        self.parent.bind("<Control-z>", lambda _: self.undo())
        self.parent.bind("<Control-y>", lambda _: self.redo())
        if not embebido:
            self.parent.bind("<Escape>", lambda _: self.parent.destroy())
            self.parent.protocol("WM_DELETE_WINDOW", self.parent.destroy)
            self.parent.grab_set()
            self.parent.focus_force()

    def _make_toolbar(self):
        toolbar = ctk.CTkFrame(self.parent, height=125, fg_color=self.THEME["toolbar"], corner_radius=0)
        toolbar.pack(side="top", fill="x")
        
        # Contenedor estático para organizar las herramientas sin desplazamiento
        container = ctk.CTkFrame(toolbar, fg_color="transparent")
        container.pack(expand=True, fill="y", padx=5, pady=2)

        # --- Sección 0: Acciones ---
        action_frame = ctk.CTkFrame(container, fg_color="#A5D6A7", corner_radius=12, border_width=1, border_color="#81C784")
        action_frame.pack(side="left", padx=2, pady=2)
        ctk.CTkLabel(action_frame, text="Acciones", font=("Arial", 10, "bold"), text_color="#1B5E20").grid(row=2, column=0, columnspan=4)
        
        self.save_btn = ctk.CTkButton(action_frame, text="💾", font=("Arial", 18), width=34, height=34, command=self.guardar_imagen, fg_color="#2ECC71", hover_color="#27AE60", corner_radius=10)
        self.save_btn.grid(row=0, column=0, padx=1, pady=1)
        self.load_btn = ctk.CTkButton(action_frame, text="📂", font=("Arial", 18), width=34, height=34, command=self.cargar_imagen, fg_color="#3498DB", hover_color="#2980B9", corner_radius=10)
        self.load_btn.grid(row=0, column=1, padx=1, pady=1)
        self.undo_btn = ctk.CTkButton(action_frame, text="↩️", font=("Arial", 18), width=34, height=34, command=self.undo, fg_color="#F39C12", hover_color="#E67E22", corner_radius=10)
        self.undo_btn.grid(row=0, column=2, padx=1, pady=1)
        self.redo_btn = ctk.CTkButton(action_frame, text="↪️", font=("Arial", 18), width=34, height=34, command=self.redo, fg_color="#F39C12", hover_color="#E67E22", corner_radius=10)
        self.redo_btn.grid(row=0, column=3, padx=1, pady=1)
        
        ctk.CTkButton(action_frame, text="➕", font=("Arial", 18), width=34, height=34, command=lambda: self.zoom(1.2), fg_color="#48CAE4", hover_color="#00B4D8", corner_radius=10).grid(row=1, column=0, padx=1)
        ctk.CTkButton(action_frame, text="➖", font=("Arial", 18), width=34, height=34, command=lambda: self.zoom(0.8), fg_color="#48CAE4", hover_color="#00B4D8", corner_radius=10).grid(row=1, column=1, padx=1)
        ctk.CTkButton(action_frame, text="🗑️", font=("Arial", 18), width=34, height=34, fg_color="#E74C3C", hover_color="#C0392B", command=self.limpiar_lienzo, corner_radius=10).grid(row=1, column=2, padx=1)

        # --- Sección 1: Herramientas y Pinceles ---
        tools_frame = ctk.CTkFrame(container, fg_color="#90CAF9", corner_radius=12, border_width=1, border_color="#64B5F6")
        tools_frame.pack(side="left", padx=2, pady=2)
        ctk.CTkLabel(tools_frame, text="Herramientas", font=("Arial", 10, "bold"), text_color="#023E8A").grid(row=2, column=0, columnspan=4)
        
        self.lapiz_btn = ctk.CTkButton(tools_frame, text="✏️", font=("Arial", 18), width=34, height=34, command=lambda: self.set_tool("lapiz"), fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        self.lapiz_btn.grid(row=0, column=0, padx=1)
        self.borrador_btn = ctk.CTkButton(tools_frame, text="🧼", font=("Arial", 18), width=34, height=34, command=lambda: self.set_tool("borrador"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.borrador_btn.grid(row=0, column=1, padx=1)
        self.gotero_btn = ctk.CTkButton(tools_frame, text="🧪", font=("Arial", 18), width=34, height=34, command=lambda: self.set_tool("gotero"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.gotero_btn.grid(row=0, column=2, padx=1)
        self.balde_btn = ctk.CTkButton(tools_frame, text="🪣", font=("Arial", 18), width=34, height=34, command=lambda: self.set_tool("balde"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.balde_btn.grid(row=0, column=3, padx=1)
        
        self.brush_round = ctk.CTkButton(tools_frame, text="●", font=("Arial", 18), width=34, height=34, command=lambda: self.set_brush("redondo"), fg_color="#1976D2", corner_radius=10)
        self.brush_round.grid(row=1, column=0, padx=1)
        self.brush_square = ctk.CTkButton(tools_frame, text="■", font=("Arial", 18), width=34, height=34, command=lambda: self.set_brush("cuadrado"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.brush_square.grid(row=1, column=1, padx=1)
        self.brush_cali = ctk.CTkButton(tools_frame, text="🖋️", font=("Arial", 18), width=34, height=34, command=lambda: self.set_brush("caligrafico"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.brush_cali.grid(row=1, column=2, padx=1)
        self.brush_spray = ctk.CTkButton(tools_frame, text="✨", font=("Arial", 18), width=34, height=34, command=lambda: self.set_brush("spray"), fg_color="transparent", text_color="black", hover_color="#BBDEFB", corner_radius=10)
        self.brush_spray.grid(row=1, column=3, padx=1)

        # --- Sección 3: Formas Geométricas ---
        shapes_frame = ctk.CTkFrame(container, fg_color="#BBDEFB", border_width=1, border_color="#90CAF9", corner_radius=12)
        shapes_frame.pack(side="left", padx=2, pady=2)
        ctk.CTkLabel(shapes_frame, text="Formas", font=("Arial", 10, "bold"), text_color="#023E8A").grid(row=2, column=0, columnspan=4)
        
        ctk.CTkButton(shapes_frame, text="╱", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("linea"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=0, column=0, padx=1)
        ctk.CTkButton(shapes_frame, text="▭", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("rectangulo"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=0, column=1, padx=1)
        ctk.CTkButton(shapes_frame, text="○", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("circulo"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=0, column=2, padx=1)
        ctk.CTkButton(shapes_frame, text="△", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("triangulo"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=0, column=3, padx=1)
        ctk.CTkButton(shapes_frame, text="⭐", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("estrella"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=1, column=0, padx=1)
        ctk.CTkButton(shapes_frame, text="⬡", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("hexagono"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=1, column=1, padx=1)
        ctk.CTkButton(shapes_frame, text="♢", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("diamante"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=1, column=2, padx=1)
        ctk.CTkButton(shapes_frame, text="❤", font=("Arial", 16), width=30, height=34, command=lambda: self.set_tool("corazon"), fg_color="transparent", text_color="black", hover_color="#90CAF9", corner_radius=8).grid(row=1, column=3, padx=1)

        # --- Sección 4: Estilo (Grosor y Color) ---
        settings_frame = ctk.CTkFrame(container, fg_color="#BBDEFB", corner_radius=12, border_width=1, border_color="#90CAF9")
        settings_frame.pack(side="left", padx=2, pady=2)
        ctk.CTkLabel(settings_frame, text="Estilo", font=("Arial", 10, "bold"), text_color="#023E8A").grid(row=2, column=0, columnspan=2)

        self.color_btn = ctk.CTkButton(settings_frame, text="", width=34, height=34, fg_color=self.color_actual, command=self.elegir_color, corner_radius=18)
        self.color_btn.grid(row=0, column=0, padx=3)
        self.grosor_slider = ctk.CTkSlider(settings_frame, from_=1, to=50, width=55, command=self.cambiar_grosor, progress_color="#0077B6", button_color="#023E8A")
        self.grosor_slider.set(self.grosor)
        self.grosor_slider.grid(row=0, column=1, padx=1)
        self._make_palette(settings_frame)

    def _make_palette(self, parent):
        paleta_frame = ctk.CTkFrame(parent, fg_color="transparent")
        paleta_frame.grid(row=1, column=0, columnspan=2, padx=3, pady=2)
        
        for idx, color in enumerate(self.PALETTE):
            r, c = divmod(idx, 8)
            # Swatches de color más grandes y redondeados para mejor visibilidad
            swatch = ctk.CTkLabel(
                paleta_frame, 
                text="", 
                width=20, 
                height=20, 
                fg_color=color, 
                corner_radius=6,
                cursor="hand2"
            )
            swatch.grid(row=r, column=c, padx=1, pady=1)
            swatch.bind("<Button-1>", lambda e, col=color: self.seleccionar_palette(col))

    def _make_canvas(self):
        # Contenedor para el canvas y scrollbars
        self.canvas_container = ctk.CTkFrame(self.parent, fg_color=self.THEME["bg"])
        self.canvas_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.v_scroll = tk.Scrollbar(self.canvas_container, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll = tk.Scrollbar(self.canvas_container, orient="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(
            self.canvas_container, 
            bg=self.THEME["canvas_bg"], 
            cursor="cross",
            scrollregion=(0, 0, 2000, 2000),
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )
        self.canvas.pack(fill="both", expand=True)
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        self.canvas.bind("<Button-1>", self.iniciar_trazo)
        self.canvas.bind("<B1-Motion>", self.pintar)
        self.canvas.bind("<ButtonRelease-1>", self.fin_trazo)

    def _make_status_bar(self):
        self.status_var = tk.StringVar(value="Herramienta: Lápiz | Pincel: Redondo | Zoom: 100%")
        status_bar = ctk.CTkLabel(self.parent, textvariable=self.status_var, font=("Arial", 11), anchor="w", padx=20)
        status_bar.pack(side="bottom", fill="x")

    def set_brush(self, tipo):
        self.pincel_tipo = tipo
        self.update_status()
        # Actualizar visual de botones de pincel
        for btn, name in [(self.brush_round, "redondo"), (self.brush_square, "cuadrado"), (self.brush_cali, "caligrafico"), (self.brush_spray, "spray")]:
            if btn: btn.configure(fg_color="#0077B6" if self.pincel_tipo == name else "transparent",
                                  text_color="white" if self.pincel_tipo == name else "black")

    def set_tool(self, tool):
        self.herramienta = tool
        
        # Cambio dinámico de cursor
        cursor_map = {
            "lapiz": "crosshair",
            "borrador": "dot",
            "gotero": "plus",
            "balde": "target",
            "linea": "crosshair",
            "rectangulo": "cross",
            "circulo": "cross",
            "triangulo": "cross",
            "estrella": "cross",
            "hexagono": "cross",
            "diamante": "cross",
            "corazon": "cross"
        }
        self.canvas.configure(cursor=cursor_map.get(tool, "cross"))
        self.update_status()
        for btn, name in [(self.lapiz_btn, "lapiz"), (self.borrador_btn, "borrador"), (self.gotero_btn, "gotero"), (self.balde_btn, "balde"), (self.brush_round, "redondo"), (self.brush_square, "cuadrado"), (self.brush_cali, "caligrafico"), (self.brush_spray, "spray")]:
            if btn: btn.configure(fg_color=self.THEME["accent"] if (self.herramienta == name or self.pincel_tipo == name) else "transparent",
                                  text_color="white" if self.herramienta == name else "black")

    def elegir_color(self):
        color = colorchooser.askcolor(title="Color", parent=self.parent)
        if color and color[1]:
            self.seleccionar_palette(color[1])

    def undo(self):
        if self.objetos:
            # Al deshacer, eliminamos el último objeto y redibujamos
            obj = self.objetos.pop()
            self.history_redo.append(obj)
            self.render()

    def redo(self):
        if self.history_redo:
            # Al rehacer, recuperamos el objeto y redibujamos
            obj = self.history_redo.pop()
            self.objetos.append(obj)
            self.render()

    def seleccionar_palette(self, color):
        self.color_actual = color
        self.color_btn.configure(fg_color=color)

    def cambiar_grosor(self, valor):
        self.grosor = int(float(valor))

    def limpiar_lienzo(self):
        self.canvas.delete("all")
        self.objetos = []
        self.history_redo = []
        self.bg_image_obj = None
        self.THEME["canvas_bg"] = "#FFFFFF"
        self.render()

    def update_status(self):
        self.status_var.set(f"Herramienta: {self.herramienta.capitalize()} | Pincel: {self.pincel_tipo.capitalize()} | Zoom: {int(self.zoom_level*100)}%")

    def zoom(self, factor):
        self.zoom_level *= factor
        self.render()
        self.update_status()

    def iniciar_trazo(self, event):
        # Capturamos coordenadas lógicas (independientes del zoom)
        self.start_x = self.canvas.canvasx(event.x) / self.zoom_level
        self.start_y = self.canvas.canvasy(event.y) / self.zoom_level
        
        if self.herramienta == "gotero":
            self.pick_color(event)
            return

        if self.herramienta == "balde":
            self.rellenar_area(event)
            return

        if self.herramienta == "borrador":
            # El borrador siempre usa pincel redondo sólido para mayor fiabilidad
            self.trazo_actual = {"tipo": "redondo", "puntos": [(self.start_x, self.start_y)]}
        elif self.herramienta == "lapiz":
            color_val = "borrador" if self.herramienta == "borrador" else self.color_actual
            self.trazo_actual = {"tipo": self.pincel_tipo, "puntos": [(self.start_x, self.start_y)]}

    def _get_star_points(self, cx, cy, rx, ry):
        """Calcula los puntos de una estrella de 5 puntas inscrita en el rectángulo."""
        pts = []
        center_x, center_y = (cx + rx) / 2, (cy + ry) / 2
        r_out = min(abs(rx - cx), abs(ry - cy)) / 2
        r_in = r_out / 2.5
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = r_out if i % 2 == 0 else r_in
            pts.extend([center_x + r * math.cos(angle), center_y + r * math.sin(angle)])
        return pts

    def _get_hexagon_points(self, cx, cy, rx, ry):
        """Calcula los puntos de un hexágono inscrito en el rectángulo."""
        pts = []
        center_x, center_y = (cx + rx) / 2, (cy + ry) / 2
        r_w = abs(rx - cx) / 2
        r_h = abs(ry - cy) / 2
        for i in range(6):
            angle = math.radians(i * 60)
            pts.extend([center_x + r_w * math.cos(angle), center_y + r_h * math.sin(angle)])
        return pts

    def _get_diamond_points(self, cx, cy, rx, ry):
        """Calcula los puntos de un diamante (rombo) inscrito en el rectángulo."""
        center_x, center_y = (cx + rx) / 2, (cy + ry) / 2
        return [center_x, cy, rx, center_y, center_x, ry, cx, center_y]

    def _get_heart_points(self, cx, cy, rx, ry):
        """Calcula los puntos de un corazón inscrito en el rectángulo."""
        pts = []
        center_x, center_y = (cx + rx) / 2, (cy + ry) / 2
        width = abs(rx - cx)
        height = abs(ry - cy)
        scale_x = width / 32
        scale_y = height / 32
        for i in range(0, 361, 10):
            t = math.radians(i)
            x = 16 * math.sin(t)**3
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            pts.extend([center_x + x * scale_x, center_y + y * scale_y])
        return pts

    def pintar(self, event):
        if self.herramienta in ["gotero", "balde"]: return

        # Coordenadas actuales lógicas
        cur_x_logic = self.canvas.canvasx(event.x) / self.zoom_level
        cur_y_logic = self.canvas.canvasy(event.y) / self.zoom_level
        
        # Coordenadas para dibujar preview (con zoom)
        sx, sy = self.start_x * self.zoom_level, self.start_y * self.zoom_level
        cx, cy = cur_x_logic * self.zoom_level, cur_y_logic * self.zoom_level
        
        color = self.THEME["canvas_bg"] if self.herramienta == "borrador" else self.color_actual
        w = self.grosor * self.zoom_level

        if self.herramienta in ["lapiz", "borrador"] and self.trazo_actual:
            self.trazo_actual["puntos"].append((cur_x_logic, cur_y_logic))
            if self.pincel_tipo == "spray" and self.herramienta != "borrador":
                # Efecto spray: añade puntos aleatorios alrededor del cursor
                for _ in range(5):
                    rx = cx + random.uniform(-w, w)
                    ry = cy + random.uniform(-w, w)
                    self.canvas.create_oval(rx, ry, rx+1, ry+1, fill=color, outline=color, tags="temp")
            else:
                if len(self.trazo_actual["puntos"]) > 1:
                    px, py = self.trazo_actual["puntos"][-2][0] * self.zoom_level, self.trazo_actual["puntos"][-2][1] * self.zoom_level
                    
                    cap = "round"
                    if self.pincel_tipo == "cuadrado" or self.herramienta == "borrador": cap = "butt"
                    elif self.pincel_tipo == "caligrafico": cap = "projecting"
                    
                    self.canvas.create_line(px, py, cx, cy, width=w, fill=color, capstyle=cap, tags="temp")
        else:
            # Preview de formas (eliminamos la anterior para evitar rayas)
            self.canvas.delete("preview")
            if self.herramienta == "linea":
                self.canvas.create_line(sx, sy, cx, cy, width=w, fill=color, tags="preview")
            elif self.herramienta == "rectangulo":
                self.canvas.create_rectangle(sx, sy, cx, cy, width=w, outline=color, tags="preview")
            elif self.herramienta == "circulo":
                self.canvas.create_oval(sx, sy, cx, cy, width=w, outline=color, tags="preview")
            elif self.herramienta == "triangulo":
                # Triángulo isósceles basado en el área de arrastre
                pts = [(sx + cx)/2, sy, sx, cy, cx, cy]
                self.canvas.create_polygon(pts, outline=color, fill="", width=w, tags="preview")
            elif self.herramienta == "estrella":
                self.canvas.create_polygon(self._get_star_points(sx, sy, cx, cy), outline=color, fill="", width=w, tags="preview")
            elif self.herramienta == "hexagono":
                self.canvas.create_polygon(self._get_hexagon_points(sx, sy, cx, cy), outline=color, fill="", width=w, tags="preview")
            elif self.herramienta == "diamante":
                self.canvas.create_polygon(self._get_diamond_points(sx, sy, cx, cy), outline=color, fill="", width=w, tags="preview")
            elif self.herramienta == "corazon":
                self.canvas.create_polygon(self._get_heart_points(sx, sy, cx, cy), outline=color, fill="", width=w, tags="preview")

    def rellenar_area(self, event):
        """Rellena figuras o dibujos a mano con mayor tolerancia de clic."""
        # Obtenemos coordenadas exactas en el canvas (considerando el zoom)
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        
        # Buscamos qué hay debajo del click con un margen de tolerancia generoso (20x20 px)
        items = self.canvas.find_overlapping(cx-10, cy-10, cx+10, cy+10)
        
        # Si no hay colisión directa, buscamos el objeto más cercano en el área
        if not items:
            items = self.canvas.find_closest(cx, cy, halo=20)
        
        encontrado = False
        if items:
            # Recorremos los items de arriba hacia abajo (orden inverso de creación)
            for item_id in reversed(items):
                tags = self.canvas.gettags(item_id)
                for tag in tags:
                    if tag.startswith("obj_"):
                        idx = int(tag.split("_")[1])
                        if idx >= len(self.objetos): continue
                        
                        obj = list(self.objetos[idx])
                        while len(obj) < 5: obj.append(None)
                        
                        # No permitimos que el balde afecte a los trazos del borrador
                        if obj[2] == "borrador":
                            continue
                            
                        # Aplicamos el color al trazo y al relleno.
                        obj[2] = self.color_actual
                        obj[4] = self.color_actual
                        
                        self.objetos[idx] = tuple(obj)
                        encontrado = True
                        break
                if encontrado: break

        if encontrado:
            # Limpiar historial de rehacer y actualizar la vista de forma inmediata
            self.history_redo.clear()
            self.render()

    def fin_trazo(self, event):
        if self.herramienta in ["gotero", "balde"]: return

        cur_x = self.canvas.canvasx(event.x) / self.zoom_level
        cur_y = self.canvas.canvasy(event.y) / self.zoom_level
        
        # Usamos un marcador para que el borrador sea dinámico si cambia el fondo
        color_val = "borrador" if self.herramienta == "borrador" else self.color_actual

        if self.herramienta in ["lapiz", "borrador"]:
            if self.trazo_actual:
                self.objetos.append(("trazo", self.trazo_actual.copy(), color_val, self.grosor, None))
                self.history_redo.clear()
        else:
            self.objetos.append((self.herramienta, (self.start_x, self.start_y, cur_x, cur_y), color_val, self.grosor, None))
            self.history_redo.clear()
        self.trazo_actual = None
        self.canvas.delete("temp")
        self.canvas.delete("preview")
        self.render()

    def render(self):
        self.canvas.delete("all")
        z = self.zoom_level
        
        # ACTUALIZACIÓN CRÍTICA: Ajustar scrollregion al tamaño visual con zoom
        # Esto evita que el lienzo se desplace o centre incorrectamente
        base_size = 2000
        self.canvas.configure(bg=self.THEME["canvas_bg"], 
                               scrollregion=(0, 0, base_size * z, base_size * z))
        
        if self.bg_image_obj:
            self.canvas.create_image(0, 0, image=self.bg_image_obj, anchor="nw")
            
        for idx, obj in enumerate(self.objetos):
            # Seguridad en el desempaquetado de datos
            tipo, data, color_val, grosor, relleno = obj if len(obj) == 5 else (*obj, None)
            w = grosor * z
            
            # El borrador siempre debe ser igual al color actual del lienzo
            color = self.THEME["canvas_bg"] if color_val == "borrador" else color_val
            
            if tipo == "trazo":
                puntos = data["puntos"]
                estilo = data["tipo"]
                
                if estilo == "spray":
                    for px, py in puntos:
                        rx, ry = px*z, py*z
                        self.canvas.create_oval(rx, ry, rx+1, ry+1, fill=color, outline=color, tags=f"obj_{idx}")
                elif len(puntos) > 1:
                    # Optimización: Dibujar el trazo completo como una sola línea para eliminar el lag
                    coords = []
                    for p in puntos:
                        coords.extend([p[0]*z, p[1]*z])
                    
                    cap = "round"
                    if estilo == "cuadrado" or color_val == "borrador": cap = "butt"
                    elif estilo == "caligrafico": cap = "projecting"
                    
                    if relleno and color_val != "borrador":
                        # Si el trazo manual tiene relleno, se dibuja como polígono para cerrar el área
                        self.canvas.create_polygon(coords, fill=relleno, outline=color, width=w, joinstyle="round", tags=f"obj_{idx}")
                    else:
                        self.canvas.create_line(coords, width=w, fill=color, capstyle=cap, joinstyle="round", tags=f"obj_{idx}")

            elif tipo == "linea":
                self.canvas.create_line(data[0]*z, data[1]*z, data[2]*z, data[3]*z, width=w, fill=color, capstyle="round", tags=f"obj_{idx}")
            elif tipo == "rectangulo":
                self.canvas.create_rectangle(data[0]*z, data[1]*z, data[2]*z, data[3]*z, width=w, outline=color, fill=relleno if relleno else "", tags=f"obj_{idx}")
            elif tipo == "circulo":
                self.canvas.create_oval(data[0]*z, data[1]*z, data[2]*z, data[3]*z, width=w, outline=color, fill=relleno if relleno else "", tags=f"obj_{idx}")
            elif tipo == "triangulo":
                x1, y1, x2, y2 = data
                pts = [((x1 + x2) / 2) * z, y1 * z, x1 * z, y2 * z, x2 * z, y2 * z]
                self.canvas.create_polygon(pts, outline=color, fill=relleno if relleno else "", width=w, tags=f"obj_{idx}")
            elif tipo == "estrella":
                scaled_pts = [p * z for p in self._get_star_points(data[0], data[1], data[2], data[3])]
                self.canvas.create_polygon(scaled_pts, outline=color, fill=relleno if relleno else "", width=w, tags=f"obj_{idx}")
            elif tipo == "hexagono":
                scaled_pts = [p * z for p in self._get_hexagon_points(data[0], data[1], data[2], data[3])]
                self.canvas.create_polygon(scaled_pts, outline=color, fill=relleno if relleno else "", width=w, tags=f"obj_{idx}")
            elif tipo == "diamante":
                scaled_pts = [p * z for p in self._get_diamond_points(data[0], data[1], data[2], data[3])]
                self.canvas.create_polygon(scaled_pts, outline=color, fill=relleno if relleno else "", width=w, tags=f"obj_{idx}")
            elif tipo == "corazon":
                scaled_pts = [p * z for p in self._get_heart_points(data[0], data[1], data[2], data[3])]
                self.canvas.create_polygon(scaled_pts, outline=color, fill=relleno if relleno else "", width=w, tags=f"obj_{idx}")

    def guardar_imagen(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
        if not path: return
        
        self.parent.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        try:
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            img.save(path)
        except Exception as e:
            print(f"Error al guardar: {e}")

    def cargar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not path: return
        
        try:
            img = Image.open(path)
            # Ajustar al tamaño del canvas actual
            img = img.resize((2000, 2000), Image.Resampling.LANCZOS)
            self.bg_image_obj = ImageTk.PhotoImage(img)
            self.render()
        except Exception as e:
            print(f"Error al cargar: {e}")

    def pick_color(self, event):
        # Gotero de alta precisión usando coordenadas de pantalla directas
        x = event.x_root
        y = event.y_root
        try:
            # Captura el color exacto del píxel en la pantalla
            rgb = ImageGrab.grab(bbox=(x, y, x + 1, y + 1)).getpixel((0,0))
            hex_color = '#%02x%02x%02x' % rgb
            self.seleccionar_palette(hex_color)
        except:
            pass

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1000x700")
    PaintApp(root)
    root.mainloop()