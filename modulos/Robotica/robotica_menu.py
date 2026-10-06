"""Menú de Robótica embebido en el panel principal de Mundo Escolar."""
import random
import customtkinter as ctk

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS, FONT_NAME
from modulos.Robotica.vistas.conoce_robot import VentanaConoceRobot
from modulos.Robotica.vistas.sensores_actuadores import VentanaEmparejamiento
from modulos.Robotica.vistas.programacion import VentanaProgramacion
from .servicios.preguntas_robotica import obtener_datos_curiosos_robotica


def crear_frame(parent, on_back_callback):
    """Punto de entrada para ModuleFactory."""
    panel = PanelRobotica(parent, on_back_callback)
    panel.pack(fill="both", expand=True)
    return panel


class PanelRobotica(ctk.CTkFrame):
    """Menú del laboratorio de robótica dentro del panel principal."""

    def __init__(self, parent, on_back_callback):
        super().__init__(parent, fg_color=COLORS["bg"], corner_radius=0)
        self.on_back = on_back_callback
        self.gestor = GestorEstado()
        self.nombre_usuario = getattr(self.gestor, "usuario_actual", "Explorador")
        self.dificultad_actual = "basico"
        self.vista_mision = None
        self._contenedor_misiones = None
        self.logros_visible = False
        self._setup_ui()

        # Listener global para cerrar logros al tocar fuera
        self.bind("<Button-1>", self._check_click_outside)

    def _boton_volver(self, parent_frame):
        ctk.CTkButton(
            parent_frame,
            text="🛰️ VOLVER A BASE",
            font=(FONT_NAME, 13, "bold"),
            fg_color="#0A0E1A",
            border_color=COLORS["border"],
            border_width=2,
            hover_color="#006064",
            text_color=COLORS["border"],
            corner_radius=15,
            command=self.on_back,
        ).place(x=25, y=25)

    def _setup_ui(self):
        # Asegurar que el panel de logros esté listo
        self.logros_visible = False
        self._setup_logros_panel()

        # Header Estilo Consola/Mando
        header = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=25, border_width=3, border_color=COLORS["border"])
        header.pack(fill="x", padx=30, pady=20)
        header.bind("<Button-1>", self._check_click_outside)

        self._boton_volver(header)

        # Perfil del Piloto (Superior Derecha)
        self.profile_btn = ctk.CTkFrame(
            header,
            fg_color="#151B2D", # Azul noche Sidebar
            corner_radius=15,
            border_width=2,
            border_color=COLORS["border"],
            cursor="hand2",
        )
        self.profile_btn.place(relx=0.97, y=25, anchor="ne")

        ctk.CTkLabel(
            self.profile_btn,
            text=f"👨‍🚀 {self.nombre_usuario.upper()}",
            font=(FONT_NAME, 14, "bold"),
            text_color=COLORS["border"],
        ).pack(padx=15, pady=8)

        # Eventos para desplegar logros
        self.profile_btn.bind("<Button-1>", lambda e: self.toggle_logros())
        for child in self.profile_btn.winfo_children():
            child.bind("<Button-1>", lambda e: self.toggle_logros())

        ctk.CTkLabel(
            header,
            text="🛸 CENTRO DE MANDO ROBÓTICO 🛸",
            font=(FONT_NAME, 44, "bold"), # Título más grande e imponente
            text_color=COLORS["border"],
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            header,
            text="ESTADO DEL SISTEMA: ÓPTIMO | ELIGE TU MISIÓN",
            font=(FONT_NAME, 18, "bold"), # Subtítulo con tamaño ajustado
            text_color=COLORS["text"],
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            header,
            text="Sube de nivel para desbloquear desafíos más complejos.\nCada nivel pondrá a prueba tus conocimientos de ingeniería y programación.",
            font=(FONT_NAME, 16), # Texto descriptivo con mayor claridad
            text_color=COLORS["border"],
            justify="center"
        ).pack(pady=(0, 25))

        self._contenedor_misiones = ctk.CTkFrame(self, fg_color="transparent")
        self._contenedor_misiones.pack(expand=True, fill="both", padx=30, pady=20)
        self._contenedor_misiones.bind("<Button-1>", self._check_click_outside)
        self._mostrar_misiones()

    def _mostrar_misiones(self):
        for w in self._contenedor_misiones.winfo_children():
            w.destroy()

        titulos = ["🔍 Partes del Robot", "🤝 Empareja y Aprende", "〰️ Sigue el Camino"]
        descs = ["Identifica sensores y motores.", "Une piezas con su función.", "Programa una ruta y llega a la meta."]
        sub_descs = [
            "📡 Protocolo de escaneo activo. Sensores al 100%.",
            "🧠 Sincronización de hardware requerida para el enlace.",
            "🚀 Cálculo de trayectoria optimizado. 4 Rondas.",
        ]

        misiones = [
            {
                "titulo": titulos[0],
                "desc": descs[0],
                "color": "#2D323E",
                "clase": VentanaConoceRobot,
            },
            {
                "titulo": titulos[1],
                "desc": descs[1],
                "color": "#2D323E",
                "clase": VentanaEmparejamiento,
            },
            {
                "titulo": titulos[2],
                "desc": descs[2],
                "color": "#2D323E",
                "clase": VentanaProgramacion,
                "extra": "lineas",
            },
        ]

        # Rejilla de 3 columnas para un cuadrado simétrico de 3 elementos
        for i in range(3):
            self._contenedor_misiones.grid_columnconfigure(i, weight=1)

        for i, m in enumerate(misiones):
            card = ctk.CTkFrame(
                self._contenedor_misiones,
                fg_color="#151B2D", # Azul noche Sidebar
                corner_radius=25,
                border_width=3,
                border_color=COLORS["border"],
            )
            # Diseño responsivo: las tarjetas se expanden equitativamente
            card.grid(row=0, column=i, padx=15, pady=15, sticky="nsew")
            card.bind("<Button-1>", self._check_click_outside)
            
            ctk.CTkLabel(
                card,
                text=f"MISIÓN {i+1}",
                font=(FONT_NAME, 14, "bold"),
                text_color="#80DEEA",
                anchor="center"
            ).pack(pady=(15, 0))

            ctk.CTkLabel(
                card,
                text=m["titulo"],
                font=(FONT_NAME, 20, "bold"),
                text_color=COLORS["border"],
                anchor="center"
            ).pack(pady=(15, 10), padx=15)
            
            ctk.CTkLabel(
                card,
                text=m["desc"],
                font=FONTS["tarjetas"],
                text_color=COLORS["border"], # Para que la descripción también brille
                wraplength=220,
                justify="center"
            ).pack(pady=(5, 5), padx=15)

            ctk.CTkLabel(
                card,
                text=sub_descs[i],
                font=(FONT_NAME, 12, "italic"),
                text_color="#80DEEA", # Cian claro para el estatus de sistema
                wraplength=220,
                justify="center"
            ).pack(pady=(2, 10), padx=15)
            
            ctk.CTkButton(
                card,
                text="INICIAR NIVEL",
                font=FONTS["botones"],
                fg_color=COLORS["border"], # El botón principal brilla
                hover_color=COLORS["hover"], # Hover con el color de acción
                text_color=COLORS["text"],
                corner_radius=20,
                height=45,
                command=lambda info=m: self._abrir_mision(info),
            ).pack(side="bottom", pady=20, padx=30)

        # --- BANNER DE TRANSMISIÓN DE DATOS (Dato curioso del día) ---
        self._mostrar_banner_datos()

    def _mostrar_banner_datos(self):
        """Crea un recuadro estilizado que muestra un dato curioso aleatorio."""
        banner_frame = ctk.CTkFrame(
            self._contenedor_misiones,
            fg_color="#0A0E1A", # Azul Media Noche
            border_width=2,
            border_color=COLORS["border"], # Cian Diamante
            corner_radius=15
        )
        # Ubicado en la fila 1 (debajo de las misiones) ocupando las 3 columnas
        banner_frame.grid(row=1, column=0, columnspan=3, padx=15, pady=(5, 15), sticky="nsew")
        
        datos = obtener_datos_curiosos_robotica()
        dato_hoy = random.choice(datos)
        
        ctk.CTkLabel(
            banner_frame,
            text=f"📡 TRANSMISIÓN DE DATOS ENTRANTE:\n{dato_hoy}",
            font=(FONT_NAME, 14, "bold"),
            text_color="#00E5FF", # Cian brillante
            wraplength=850,
            justify="center"
        ).pack(padx=25, pady=15)

    def _setup_logros_panel(self):
        """Configura el panel de logros lateral con temática de robótica."""
        self.logros_frame = ctk.CTkScrollableFrame(
            self,
            width=320,
            height=300,
            fg_color="#0A0E1A", # Azul Media Noche
            border_width=4,
            border_color=COLORS["border"],
            label_text="🚀 REGISTRO DE MISIONES 🚀",
            label_font=(FONT_NAME, 14, "bold"),
            label_text_color=COLORS["border"],
            label_fg_color="#151B2D",
            corner_radius=20,
        )

        # Mapeo de logros del módulo
        logros_robotica = [
            {"id": "robotica_partes", "nombre": "Ingeniero de Partes", "emoji": "🔍"},
            {"id": "robotica_emparejar", "nombre": "Sincronizador Pro", "emoji": "🤝"},
            {"id": "robotica_programacion", "nombre": "Gran Programador", "emoji": "🚀"},
        ]

        for m in logros_robotica:
            unlocked = self.gestor.tiene_logro(m["id"])

            item = ctk.CTkFrame(
                self.logros_frame,
                fg_color="#151B2D" if unlocked else "#1A1C23",
                corner_radius=12,
                border_width=1,
                border_color=COLORS["border"] if unlocked else "#2D323E",
            )
            item.pack(fill="x", pady=6, padx=8)

            ctk.CTkLabel(item, text=m["emoji"] if unlocked else "🔒", font=("Arial", 22)).pack(
                side="left", padx=10
            )
            ctk.CTkLabel(
                item,
                text=m["nombre"] if unlocked else "BLOQUEADO",
                font=(FONT_NAME, 11, "bold"),
                text_color=COLORS["text"] if unlocked else "#666666",
                justify="left",
            ).pack(side="left", pady=10)

            if unlocked:
                ctk.CTkLabel(
                    item, text="✔️", text_color="#00E5FF", font=("Arial", 18)
                ).pack(side="right", padx=15)

    def toggle_logros(self):
        """Muestra u oculta el panel de logros."""
        if self.logros_visible:
            self.logros_frame.place_forget()
        else:
            self.logros_frame.place(relx=0.97, y=140, anchor="ne")
            self.logros_frame.lift()
        self.logros_visible = not self.logros_visible

    def _check_click_outside(self, event):
        """Cierra el panel de logros si se detecta un clic fuera de él."""
        if not self.logros_visible:
            return
        
        # Obtener el widget bajo el mouse usando coordenadas globales
        try:
            widget = self.winfo_containing(event.x_root, event.y_root)
            
            # Subir en la jerarquía para ver si el click pertenece al panel o al botón
            curr = widget
            while curr:
                if curr == self.logros_frame or curr == self.profile_btn:
                    return # Click interno, ignorar
                curr = curr.master if hasattr(curr, 'master') else None
            
            self.toggle_logros()
        except:
            pass

    def _abrir_mision(self, info_mision):
        if self.vista_mision:
            self.vista_mision.destroy()
            self.vista_mision = None
        for w in self.winfo_children():
            w.destroy()

        contenedor = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        contenedor.pack(fill="both", expand=True)

        extra = info_mision.get("extra")
        self.vista_mision = info_mision["clase"](
            contenedor,
            on_volver=lambda: self._regresar_menu(contenedor),
            dificultad=self.dificultad_actual,
            modo_extra=extra,
        )

    def _regresar_menu(self, contenedor_mision):
        if self.vista_mision:
            self.vista_mision.destroy()
            self.vista_mision = None
        if contenedor_mision.winfo_exists():
            contenedor_mision.destroy()
        for w in self.winfo_children():
            w.destroy()
        self._setup_ui()


# Alias para compatibilidad con código antiguo
RoboticaMenu = PanelRobotica
