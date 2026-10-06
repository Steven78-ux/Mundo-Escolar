"""Fachada de lanzamiento: integra Computación con el panel principal."""

import sys
import threading
import random
import customtkinter as ctk

from core.gestor_estado import GestorEstado
from core.theme import COLORS, FONTS, FONT_NAME
from modulos.Computacion.domain.texts import LIBROS_MECANOGRAFIA

DATOS_CURIOSOS_COMP = [
    "El primer ratón de ordenador fue inventado en 1964 y estaba hecho de madera.",
    "Ada Lovelace es considerada la primera programadora de la historia.",
    "El primer ordenador, ENIAC, pesaba más de 27 toneladas y ocupaba una habitación.",
    "El término 'bug' surgió porque una polilla real causó un fallo en un ordenador en 1947.",
    "Aproximadamente el 90% de las divisas del mundo solo existen en ordenadores.",
    "El primer disco duro de 5MB pesaba más de una tonelada.",
    "Google fue originalmente llamado 'BackRub'.",
    "El primer teclado QWERTY se diseñó para evitar que las máquinas de escribir se atascaran.",
    "La primera cámara digital de 1975 tenía solo 0.01 megapíxeles.",
    "Se estima que el 80% de los correos electrónicos enviados son spam.",
    "El primer videojuego de la historia se llamó 'Tennis for Two'.",
    "La World Wide Web fue inventada por Sir Tim Berners-Lee en 1989.",
    "HP, Apple y Microsoft empezaron en garajes.",
    "Un usuario de PC parpadea solo 7 veces por minuto frente a las 20 normales.",
    "El símbolo @ fue elegido en 1971 para separar el usuario de la máquina.",
    "La primera página web de la historia todavía está en línea.",
    "El primer mensaje enviado por Internet fue 'LO'.",
    "Cada minuto se suben más de 500 horas de video a YouTube.",
    "El primer lenguaje de programación de alto nivel fue Fortran.",
    "En 1956, un disco duro de 5 megas era del tamaño de una nevera.",
    "Toy Story tomó 800,000 horas de computación para ser renderizada.",
    "Existen más de 700 lenguajes de programación diferentes.",
    "El primer dominio registrado fue symbolics.com en 1985.",
    "Más de 3.500 millones de personas usan Internet hoy en día.",
    "CAPTCHA significa 'Completamente Automatizado Test de Turing para distinguir Humanos de Computadoras'.",
    "El primer banner publicitario en Internet apareció en 1994.",
    "Linux es el sistema operativo más usado en los servidores del mundo.",
    "Un código QR puede almacenar hasta 7.089 caracteres numéricos.",
    "El primer microprocesador fue el Intel 4004 lanzado en 1971.",
    "Tu smartphone es miles de veces más potente que el ordenador que llevó al hombre a la Luna.",
    "Bluetooth lleva el nombre de un antiguo rey vikingo.",
    "Wi-Fi no significa 'Wireless Fidelity', es solo un nombre de marca.",
    "El primer SMS enviado decía 'Merry Christmas'.",
    "Steve Jobs y Wozniak vendieron una calculadora para fundar Apple.",
    "La primera computadora portátil, Osborne 1, pesaba 11 kilos.",
    "El primer ratón óptico se inventó en 1980.",
    "En 1984, solo había 1.000 dispositivos conectados a Internet.",
    "Hoy hay más dispositivos conectados a Internet que personas en el planeta.",
    "Amazon empezó vendiendo solo libros en el garaje de Jeff Bezos.",
    "Python debe su nombre al grupo de comedia Monty Python.",
    "JavaScript no tiene nada que ver con el lenguaje Java.",
    "El primer cable submarino transatlántico se instaló en 1858.",
    "El primer buscador de Internet se llamaba Archie.",
    "Windows 1.0 fue lanzado oficialmente en 1985.",
    "El término 'Software' fue utilizado por primera vez en 1958.",
    "El primer virus informático se llamaba 'Creeper'.",
    "La mayoría de los programadores empezaron a programar antes de los 15 años.",
    "El primer ordenador con ratón e interfaz gráfica fue el Xerox Alto.",
    "Apolo 11 tenía menos memoria que una calculadora básica de hoy.",
    "El dominio 'pizza.com' se vendió por millones de dólares.",
    "El 15 de agosto se celebra el Día del Programador."
]


def crear_frame(parent, on_back_callback):
    """Punto de entrada para ModuleFactory."""
    panel = PanelComputacion(parent, on_back_callback)
    panel.pack(fill="both", expand=True)
    return panel


class PanelComputacion(ctk.CTkFrame):
    """Menú tecnológico integrado en el panel principal."""

    def __init__(self, parent, on_back_callback):
        # Usamos el color de fondo Cyber del tema de computación
        super().__init__(parent, fg_color="#0A0F1E", corner_radius=0)
        self.on_back = on_back_callback
        self.gestor = GestorEstado()
        self.nombre_usuario = getattr(self.gestor, "usuario_actual", "Explorador")
        
        self.logros_visible = False
        self.vista_actual = "menu" # Para rastrear el refresco
        self._setup_ui()
        
        # Listener global para cerrar logros al tocar fuera
        self.bind("<Button-1>", self._check_click_outside)

    def _setup_ui(self):
        self.logros_visible = False

        # --- Header Estilo Terminal ---
        header = ctk.CTkFrame(self, fg_color="#0F192D", corner_radius=20, border_width=2, border_color="#00FFFF")
        header.pack(fill="x", padx=30, pady=20)
        header.bind("<Button-1>", self._check_click_outside)

        ctk.CTkButton(
            header,
            text="⬅ Volver al Menú",
            font=(FONT_NAME, 13, "bold"),
            fg_color="transparent",
            border_color="#00FFFF",
            border_width=2,
            hover_color="#005F5F",
            text_color="#00FFFF",
            corner_radius=15,
            command=self.on_back,
        ).place(x=20, y=20)

        # Botón Logros (Superior Derecha)
        self.btn_logros = ctk.CTkButton(
            header,
            text="🏆 LOGROS",
            font=(FONT_NAME, 13, "bold"),
            fg_color="transparent",
            border_color="#00FFFF",
            border_width=2,
            hover_color="#005F5F",
            text_color="#00FFFF",
            corner_radius=15,
            command=self.toggle_logros,
        )
        self.btn_logros.place(relx=0.98, y=20, anchor="ne")

        # Título Neón
        ctk.CTkLabel(
            header,
            text="⌨️ TERMINAL DE COMPUTACIÓN 💻",
            font=(FONT_NAME, 40, "bold"),
            text_color="#00FFFF",
        ).pack(pady=(35, 5))

        # Subtítulo de descripción del módulo
        ctk.CTkLabel(
            header,
            text="Explora el mundo digital: Domina el teclado escribiendo cuentos y entrena tu precisión con el mouse.",
            font=(FONT_NAME, 16),
            text_color="#80DEEA",
            justify="center"
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            header,
            text=f"SISTEMA OPERATIVO LISTO | USUARIO: {self.nombre_usuario.upper()}",
            font=(FONT_NAME, 14, "bold"),
            text_color="#39FF14", # Verde fósforo terminal
        ).pack(pady=(0, 20))

        # --- Contenedor de Actividades ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=30, pady=10)
        self.container.bind("<Button-1>", self._check_click_outside)
        
        self._mostrar_menu_principal()

    def _mostrar_menu_principal(self):
        self._limpiar_container()
        self.container.grid_columnconfigure((0, 1), weight=1)
        self.container.grid_rowconfigure(0, weight=0) # No estirar verticalmente

        # Tarjeta Mecanografía
        meca_card = self._crear_tarjeta_actividad(
            self.container, 
            "MECANOGRAFÍA", 
            "Escribe historias fantásticas mientras mejoras tu velocidad y agilidad con las teclas.", 
            "⌨️", 
            "#00FFFF",
            self._mostrar_selector_libros
        )
        meca_card.grid(row=0, column=0, padx=40, pady=20, sticky="nsew")

        # Tarjeta Mouse
        mouse_card = self._crear_tarjeta_actividad(
            self.container, 
            "PRECISIÓN MOUSE", 
            "LOS OBJETIVOS AQUI SERAN DE DOS COLORES LOS CIRCULOS AZULES TENDRAS QUE PULSARLOS CON EL CLICK IZQUIERDO Y LOS CIRCULOS VERDES TENDRAS QUE PULSARLO CON EL CLIC DERECHO", 
            "🖱️", 
            "#FFB400",
            self._mostrar_selector_mouse
        )
        mouse_card.grid(row=0, column=1, padx=40, pady=20, sticky="nsew")

        self._mostrar_banner_curiosidades(fila_inicio=1, columnas=2)

    def _crear_tarjeta_actividad(self, parent, titulo, desc, icono, color, comando):
        card = ctk.CTkFrame(parent, fg_color="#0F192D", corner_radius=25, border_width=3, border_color=color)
        card.bind("<Button-1>", self._check_click_outside)
        
        # Eliminamos el icono y aumentamos los tamaños de fuente
        ctk.CTkLabel(card, text=titulo, font=(FONT_NAME, 32, "bold"), text_color=color).pack(pady=(35, 10))
        ctk.CTkLabel(card, text=desc, font=(FONT_NAME, 18), text_color="white", wraplength=280, justify="center").pack(pady=20, padx=30)
        
        ctk.CTkButton(
            card, 
            text="EJECUTAR NIVEL", 
            font=(FONT_NAME, 15, "bold"),
            fg_color=color, 
            text_color="#0A0F1E",
            hover_color="#005F5F" if color == "#00FFFF" else "#CC8E00",
            corner_radius=20,
            height=45,
            command=comando
        ).pack(pady=(10, 35))
        
        return card

    def _mostrar_selector_libros(self):
        self._limpiar_container()
        self.vista_actual = "meca"
        self.container.grid_columnconfigure((0, 1), weight=1)

        # Texto de instrucción
        ctk.CTkLabel(
            self.container,
            text="Elije el libro que mas te gusta para comenzar a Practicar",
            font=(FONT_NAME, 20, "bold"),
            text_color="#00FFFF"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        for i, (key, libro) in enumerate(LIBROS_MECANOGRAFIA.items()):
            fila, col = (i // 2) + 1, i % 2
            
            # Tarjeta de libro uniforme
            card = ctk.CTkFrame(
                self.container, 
                fg_color="#0F192D", 
                corner_radius=20, 
                border_width=2, 
                border_color="#00FFFF"
            )
            card.grid(row=fila, column=col, padx=15, pady=10, sticky="nsew")
            
            # Título en Azul Cian Brillante
            ctk.CTkLabel(
                card, 
                text=libro.titulo.upper(), 
                font=(FONT_NAME, 22, "bold"), 
                text_color="#00FFFF"
            ).pack(pady=(15, 5))
            
            # Descripción mejorada
            ctk.CTkLabel(
                card, 
                text=libro.descripcion, 
                font=(FONT_NAME, 15), 
                text_color="white", 
                wraplength=350, 
                justify="center"
            ).pack(pady=5, padx=20)
            
            ctk.CTkButton(
                card, 
                text="SELECCIONAR LIBRO", 
                font=(FONT_NAME, 14, "bold"),
                fg_color="#00FFFF", 
                text_color="#0A0F1E",
                hover_color="#005F5F",
                corner_radius=15,
                height=35,
                command=lambda k=key: self._lanzar_juego("mecanografia", k)
            ).pack(pady=(5, 15)) # Reducido margen superior para compactar

        self._crear_boton_atras_unificado()

    def _mostrar_selector_mouse(self):
        self._limpiar_container()
        self.vista_actual = "mouse"
        # Crear rejilla de niveles 1-20
        self.container.grid_columnconfigure((0,1,2,3,4), weight=1)

        # Texto de instrucción
        ctk.CTkLabel(
            self.container,
            text="Elige el nivel de dificultad para comenzar",
            font=(FONT_NAME, 24, "bold"),
            text_color="#FFB400"
        ).grid(row=0, column=0, columnspan=5, pady=(10, 5))

        # Texto de advertencia
        ctk.CTkLabel(
            self.container,
            text="!RECUERDA QUE LOS NIVELES ESTAN BASADOS EN LOS COLORES! LOS NIVELES MAS ALTOS SERAN MUCHO MAS DIFICIL",
            font=(FONT_NAME, 14, "bold"),
            text_color="#E74C3C"
        ).grid(row=1, column=0, columnspan=5, pady=(0, 20))

        for i in range(1, 21):
            # Lógica de colores estilo semáforo
            if i <= 4: # Niveles 1-4: Verde
                b_color, h_color = "#2ECC71", "#27AE60"
            elif i <= 8: # Niveles 5-8: Amarillo
                b_color, h_color = "#F1C40F", "#D4AC0D"
            elif i <= 12: # Niveles 9-12: Naranja
                b_color, h_color = "#E67E22", "#D35400"
            elif i <= 16: # Niveles 13-16: Rojo
                b_color, h_color = "#E74C3C", "#C0392B"
            else: # Niveles 17-20: Morado
                b_color, h_color = "#9B59B6", "#8E44AD"

            r, c = ((i-1)//5) + 2, (i-1)%5
            
            # Tarjetas de niveles mejoradas (Cyber Cards)
            card = ctk.CTkFrame(self.container, fg_color="#0F192D", border_width=2, border_color=b_color, corner_radius=15)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            
            ctk.CTkLabel(
                card, 
                text=f"LVL {i:02d}", 
                font=(FONT_NAME, 18, "bold"), 
                text_color="white"
            ).pack(pady=(15, 5))
            
            ctk.CTkButton(
                card,
                text="INICIAR",
                font=(FONT_NAME, 11, "bold"),
                fg_color=b_color,
                hover_color=h_color,
                text_color="#0A0F1E",
                height=30,
                width=80,
                corner_radius=10,
                command=lambda n=i: self._lanzar_juego("mouse", n)
            ).pack(pady=(0, 15))
            
        self._crear_boton_atras_unificado()

    def _mostrar_banner_curiosidades(self, fila_inicio, columnas):
        """Dibuja un banner con un dato curioso aleatorio."""
        banner = ctk.CTkFrame(self.container, fg_color="#0F192D", border_width=2, border_color="#39FF14", corner_radius=15)
        banner.grid(row=fila_inicio, column=0, columnspan=columnas, pady=20, padx=20, sticky="ew")
        
        dato = random.choice(DATOS_CURIOSOS_COMP)
        
        ctk.CTkLabel(
            banner,
            text=f"💡 ¿SABÍAS QUÉ? {dato.upper()}",
            font=(FONT_NAME, 14, "bold"),
            text_color="#39FF14",
            wraplength=800,
            justify="center"
        ).pack(pady=15, padx=20)

    def _crear_boton_atras_unificado(self):
        ctk.CTkButton(
            self, 
            text="ATRÁS", 
            command=self._mostrar_menu_principal, 
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            font=(FONT_NAME, 16, "bold"),
            width=200, 
            height=50,
            corner_radius=15
        ).pack(pady=20)

    def _lanzar_juego(self, tipo, parametro):
        """Lanza la lógica de Pygame en un hilo para no congelar la UI de Mundo Escolar."""
        def run():
            if tipo == "mecanografia":
                from modulos.Computacion.services.game_utils import TypingModule
                # Iniciamos en el capítulo 1 del libro seleccionado
                app = TypingModule(libro_id=parametro, capitulo_inicial=1)
                app.run()
            else:
                from modulos.Computacion.views.mouse_module import MouseModule
                app = MouseModule()
                app.dificultad = parametro
                app._reset_juego() # Iniciar directamente en el nivel
                app.run()
            
            # Al cerrar Pygame, actualizamos progreso
            GestorEstado().actualizar_progreso("Computación", 0.05)
            # Refrescar para cambiar el dato curioso al volver
            self.after(0, self._refrescar_vista)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def _refrescar_vista(self):
        if self.vista_actual == "meca": self._mostrar_selector_libros()
        elif self.vista_actual == "mouse": self._mostrar_selector_mouse()
        elif self.vista_actual == "menu": self._mostrar_menu_principal()

    def _limpiar_container(self):
        for w in self.container.winfo_children():
            w.destroy()
            
        # Resetear pesos de la rejilla para evitar que las vistas se estiren entre sí
        for i in range(10): 
            self.container.grid_columnconfigure(i, weight=0)
            self.container.grid_rowconfigure(i, weight=0)
            
        # Eliminar cualquier botón de ATRÁS existente para evitar la duplicación
        for w in self.winfo_children():
            if isinstance(w, ctk.CTkButton) and w.cget("text") == "ATRÁS":
                w.destroy()

    def _setup_logros_panel(self):
        """Configura el panel de logros lateral con temática tecnológica."""
        self.logros_frame = ctk.CTkScrollableFrame(
            self,
            width=380,
            height=500,
            fg_color="#0F192D",
            border_width=4,
            border_color="#00FFFF",
            label_text="🏆 REGISTRO DE LOGROS CYBER 🏆",
            label_font=(FONT_NAME, 14, "bold"),
            label_text_color="#00FFFF",
            label_fg_color="#0A0F1E",
            corner_radius=20,
        )

        # Definición de misiones para el panel
        sections = [
            ("⌨️ MECANOGRAFÍA", [
                ("computacion_principito", "El Principito"),
                ("computacion_don_quijote", "Don Quijote"),
                ("computacion_los_tres_cerditos", "Los 3 Cerditos"),
                ("computacion_pinocho", "Pinocho"),
                ("computacion_alicia_maravillas", "Alicia Maravillas"),
                ("computacion_liebre_tortuga", "Liebre y Tortuga")
            ], "#00FFFF"),
            ("🖱️ PRECISIÓN MOUSE", [(f"computacion_mouse_{i}", f"Precisión LVL {i:02d}") for i in range(1, 21)], "#FFB400")
        ]

        for sec_name, items, sec_color in sections:
            ctk.CTkLabel(self.logros_frame, text=sec_name, font=(FONT_NAME, 13, "bold"), text_color=sec_color).pack(pady=(15, 5))
            for lid, name in items:
                unlocked = self.gestor.tiene_logro(lid)
                
                # Estilo de cuadro bloqueado (gris) o desbloqueado (cyber)
                item = ctk.CTkFrame(
                    self.logros_frame, 
                    fg_color="#0A0F1E" if unlocked else "#2D2D2D", 
                    corner_radius=12, 
                    border_width=1, 
                    border_color="#00FFFF" if unlocked else "#444"
                )
                item.pack(fill="x", pady=4, padx=8)

                ctk.CTkLabel(item, text="✔️" if unlocked else "🔒", font=("Arial", 20), text_color="#39FF14" if unlocked else "#E74C3C").pack(side="left", padx=10)
                
                txt_status = name if unlocked else "BLOQUEADO"
                ctk.CTkLabel(
                    item, 
                    text=txt_status, 
                    font=(FONT_NAME, 11, "bold"), 
                    text_color="white" if unlocked else "#E74C3C",
                    justify="left"
                ).pack(side="left", pady=12)

    def toggle_logros(self):
        if self.logros_visible:
            self.logros_frame.place_forget()
        else:
            # Optimizacion: Solo creamos/refrescamos si es necesario
            if hasattr(self, "logros_frame") and self.logros_frame.winfo_exists():
                self.logros_frame.destroy()
            self._setup_logros_panel()
            self.logros_frame.place(relx=0.98, y=140, anchor="ne")
            self.logros_frame.lift()
        self.logros_visible = not self.logros_visible

    def _check_click_outside(self, event):
        if not self.logros_visible: return
        try:
            widget = self.winfo_containing(event.x_root, event.y_root)
            curr = widget
            while curr:
                if curr == self.logros_frame or curr == self.btn_logros: return
                curr = curr.master if hasattr(curr, 'master') else None
            self.toggle_logros()
        except: pass

def abrir_menu_computacion(_root=None):
    """Punto de entrada compatible con el sistema de navegación."""
    from core.module_factory import get_main_root
    root = get_main_root() or _root or ctk.CTk()
    # Si se lanza solo (fuera del main), cerrar al volver
    callback = lambda: sys.exit() if _root else None
    return crear_frame(root, callback)
