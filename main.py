"""
Mundo Escolar - Menú Principal (Refactorizado)
Módulos embebidos en panel, logros, tema unificado y diseño responsive.
"""

import sys
import os
import logging
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import customtkinter as ctk
from PIL import Image
from tkextrafont import Font

# -------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"sesion_{datetime.now():%Y%m%d}.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mundo_escolar")
logger.info("Aplicación iniciada")

# Añadir carpeta de librerías locales para compatibilidad en Linux/ChromeOS
LIB_DIR = os.path.join(BASE_DIR, "lib")
if os.path.exists(LIB_DIR):
    sys.path.insert(0, LIB_DIR)

from core.gestor_estado import GestorEstado
from core.module_factory import ModuleFactory, set_main_root
from core.logros_config import LOGROS
from core import theme

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "imagenes")

# Re-exportar para compatibilidad con código que importa desde main
COLORS = theme.COLORS
DEFAULT_COLORS = dict(COLORS)
COLORS.setdefault("border", "#2A7ACC")  # Color de borde por defecto
DEFAULT_COLORS.setdefault("border", "#2A7ACC")
FONT_NAME = theme.FONT_NAME
FONTS = theme.FONTS

# -------------------------------------------------------------
# ESTADO DE VISTA Y CARGA
# -------------------------------------------------------------
vista_actual = None
_loading_module = False
_tarjetas_deshabilitadas = False
perfil_frame_ref = None

# -------------------------------------------------------------
# CONFIGURACIÓN DE TEMAS POR MÓDULO (Inmersión)
# -------------------------------------------------------------
MODULO_THEMES = {
    "lectura_escritura": {
        "bg": "#FDF5E6",       # Papel antiguo
        "sidebar": "#FEF9E7",  # Crema cálido
        "border": "#8D6E63",   # Marrón tinta
        "text": "#5D4037",     # Texto café
        "hover": "#D7CCC8"     # Hover suave
    },
    "ajedrez": {
        "bg": "#2C3E50",       # Azul profundo
        "sidebar": "#34495E",  # Gris azulado
        "border": "#1ABC9C",   # Verde esmeralda (Ajedrez táctico)
        "text": "#ECF0F1",     # Blanco nube
        "hover": "#16A085"
    },
    "computacion": {
        "bg": "#0A0F1E",       # Cyber Dark
        "sidebar": "#0F192D",  # Tech Blue
        "border": "#00FFFF",   # Cyan neón
        "text": "#00FFFF",     # Texto neón
        "hover": "#005F5F"
    },
    "robotica": {
        "bg": "#0A0E1A",       # Azul Media Noche
        "sidebar": "#151B2D",  # Azul noche Sidebar
        "border": "#00E5FF",   # Cian Brillante Diamante
        "text": "#E0F7FA",     # Texto Cian Claro
        "hover": "#006064"     # Hover Cian Oscuro
    },
    "dibujo": {
        "bg": "#E3F2FD",       # Celeste Creativo
        "sidebar": "#BBDEFB",  # Azul Pastel
        "border": "#1976D2",   # Azul Artístico
        "text": "#0D47A1",     # Contraste profundo
        "hover": "#90CAF9"     # Azul selección
    }
}

# -------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------
image_cache = {}

def get_asset(nombre, size=None):
    """Carga una imagen y devuelve CTkImage."""
    path = os.path.join(ASSETS_DIR, nombre)
    if not os.path.exists(path):
        path = os.path.join(ASSETS_DIR, nombre.lower())
    key = (path, size)
    if key in image_cache:
        return image_cache[key]

    # Búsqueda robusta para Linux (ignora mayúsculas/minúsculas si el archivo no existe)
    if not os.path.exists(path):
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path).lower()
        if os.path.exists(dir_name):
            for f in os.listdir(dir_name):
                if f.lower() == base_name:
                    path = os.path.join(dir_name, f)
                    break

    if not os.path.exists(path):
        logger.error("No se encontró el recurso requerido: %s", path)
        return None

    imagen = Image.open(path)
    asset = ctk.CTkImage(light_image=imagen, size=size) if size else ctk.CTkImage(light_image=imagen, size=imagen.size)
    image_cache[key] = asset
    return asset


def obtener_tamano_ventana():
    ancho = root.winfo_width()
    alto = root.winfo_height()
    if ancho <= 1 or alto <= 1:
        ancho = root.winfo_screenwidth()
        alto = root.winfo_screenheight()
    return ancho, alto


def obtener_ancho_sidebar(expandido=True):
    ancho, _ = obtener_tamano_ventana()
    if expandido:
        return max(180, min(240, int(ancho * 0.12)))
    return max(60, min(90, int(ancho * 0.05)))


def actualizar_fuentes_responsivas():
    """Recalcula fuentes según el tamaño actual de la ventana."""
    global FONTS
    ancho, _ = obtener_tamano_ventana()
    theme.FONTS = theme.fuentes_responsivas(ancho)
    FONTS = theme.FONTS

def aplicar_tema_interfaz(tema_id):
    """Cambia dinámicamente los colores de la UI para que coincidan con el módulo."""
    if tema_id == "default":
        bg_color = DEFAULT_COLORS["bg"]
        sb_color = DEFAULT_COLORS["sidebar"]
        brd_color = DEFAULT_COLORS.get("border", "#4DA3FF")
        txt_color = DEFAULT_COLORS.get("text_dark", "black")
        hov_color = DEFAULT_COLORS["sidebar_hover"]
        brd_width = 1
        root.configure(cursor="arrow")
    else:
        # Temas inmersivos para los módulos
        t = MODULO_THEMES.get(tema_id, MODULO_THEMES["lectura_escritura"])
        bg_color = t["bg"]
        sb_color = t["sidebar"]
        brd_color = t["border"]
        txt_color = t["text"]
        hov_color = t["hover"]
        brd_width = 3 # Marco más definido para módulos
        
        # Especial para dibujo: Cursor de lápiz
        if tema_id == "dibujo":
            root.configure(cursor="pencil")
        else:
            root.configure(cursor="arrow")

    # Actualizamos el diccionario global con el tema activo
    COLORS["bg"] = bg_color
    COLORS["border"] = brd_color
    COLORS["hover"] = hov_color
    COLORS["text"] = txt_color
    COLORS["sidebar"] = sb_color

    # Restaurar el tema base completo cuando volvemos a inicio
    if tema_id == "default":
        COLORS.update({
            "sidebar": DEFAULT_COLORS["sidebar"],
            "sidebar_hover": DEFAULT_COLORS["sidebar_hover"],
            "text_dark": DEFAULT_COLORS["text_dark"],
            "white": DEFAULT_COLORS["white"],
            "progress_fill": DEFAULT_COLORS["progress_fill"],
            "progress_bg": DEFAULT_COLORS["progress_bg"],
            "locked": DEFAULT_COLORS["locked"],
            "success": DEFAULT_COLORS["success"],
            "danger": DEFAULT_COLORS["danger"],
            "warning": DEFAULT_COLORS["warning"],
        })

    # Forzamos el color de fondo en la raíz de forma absoluta (base Tk y CTk)
    # Esto elimina cualquier rastro del color del módulo anterior.
    root.configure(fg_color=bg_color)
    root.config(bg=bg_color)
    
    sidebar.configure(fg_color=sb_color, border_color=brd_color, border_width=brd_width)
    principal.configure(fg_color=bg_color)
    lbl_titulo_sidebar.configure(text_color=txt_color)
    
    # Actualizar colores de los botones y mantener el resaltado si existe
    for btn in botones_menu.values():
        btn.configure(text_color=txt_color, hover_color=hov_color)
        if btn.cget("fg_color") != "transparent":
            btn.configure(fg_color=hov_color)

    btn_toggle.configure(text_color=txt_color, hover_color=hov_color)
    btn_salir.configure(text_color="white") # El botón de salir mantiene su contraste por seguridad

def marcar_boton_activo(nombre):
    """Aplica un recuadro de selección al botón del menú lateral activo."""
    for texto, btn in botones_menu.items():
        if texto == nombre:
            # Usamos el color de hover para crear el 'recuadro' de selección
            btn.configure(fg_color=btn.cget("hover_color"))
        else:
            btn.configure(fg_color="transparent")

def _dibujar_perfil_usuario():
    """Dibuja un indicador de perfil en la esquina superior derecha del panel principal."""
    global perfil_frame_ref
    gestor = GestorEstado()
    nombre = getattr(gestor, "usuario_actual", "Explorador")

    # Manejo de nombres largos: Si el nombre es muy largo, lo truncamos para no romper el diseño
    nombre_display = str(nombre).upper()
    if len(nombre_display) > 15:
        nombre_display = nombre_display[:12] + "..."

    # Reemplazamos el frame anterior si existe
    try:
        if perfil_frame_ref and perfil_frame_ref.winfo_exists():
            perfil_frame_ref.destroy()
    except Exception:
        pass

    perfil_frame = ctk.CTkFrame(
        principal,
        fg_color=COLORS["sidebar"],
        corner_radius=25,
        border_width=3,
        border_color=COLORS.get("border", "white")
    )
    perfil_frame.place(relx=0.995, y=20, anchor="ne")

    lbl = ctk.CTkLabel(
        perfil_frame,
        text=f"👤  {nombre_display}",
        font=(FONT_NAME, 14, "bold"),
        text_color="white"
    )
    lbl.pack(side="left", padx=(15, 0), pady=10)

    # Dropdown para seleccionar usuario existente
    def obtener_usuarios_disponibles():
        diru = GestorEstado().dir_usuarios
        usuarios = []
        try:
            for f in os.listdir(diru):
                if f.lower().endswith(".json"):
                    usuarios.append(os.path.splitext(f)[0])
        except Exception:
            pass
        if "Invitado" not in usuarios:
            usuarios.insert(0, "Invitado")
        return usuarios

    def on_usuario_seleccionado(value):
        if not value:
            return
        GestorEstado().inicializar_usuario(value)
        logger.info("Usuario cargado: %s", value)
        _dibujar_perfil_usuario()
        vista_inicio()

    usuarios = obtener_usuarios_disponibles()
    try:
        color_sidebar = COLORS["sidebar"]
        # Estilo mejorado y unificado con la temática del software
        option = ctk.CTkOptionMenu(
            perfil_frame, 
            values=usuarios, 
            command=on_usuario_seleccionado,
            fg_color=color_sidebar,      # Igualamos al fondo para eliminar el efecto de "bloque comprimido"
            button_color=color_sidebar,  # El botón base es invisible
            button_hover_color=color_sidebar, # Eliminamos el efecto de hover en el botón
            dropdown_fg_color=color_sidebar,
            dropdown_hover_color=COLORS.get("hover", COLORS["sidebar_hover"]), # Mantenemos hover estándar solo en la lista
            dropdown_text_color="white",
            text_color="white",          # Hacemos visible la flechita
            font=(FONT_NAME, 13, "bold"),
            dynamic_resizing=False,
            corner_radius=15,
            width=35,                    # Ancho ajustado para mostrar la flecha con mejor espacio
            height=38
        )
        option.set(nombre if nombre in usuarios else (usuarios[0] if usuarios else "Invitado"))
        option.pack(side="right", padx=(0, 10), pady=8)
    except Exception:
        # Fallback: si CTkOptionMenu no está disponible, no romper la UI
        pass

    perfil_frame_ref = perfil_frame

def _evaluar_logro_desbloqueado(logro, materias, completadas, gestor):
    """Determina si un logro está desbloqueado (porcentaje, acción o general)."""
    if gestor.tiene_logro(logro["id"]):
        return True
    tipo = logro.get("tipo", "porcentaje")
    if tipo == "accion":
        return False
    if tipo == "general":
        link = logro["link"]
        if "3" in link:
            return completadas >= 3
        return completadas >= len(materias) and len(materias) > 0
    return materias.get(logro["link"], 0) >= logro["req"]


# -------------------------------------------------------------
# CONFIGURACIÓN DE LA INTERFAZ PRINCIPAL
# -------------------------------------------------------------
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Mundo Escolar")

root.attributes("-fullscreen", True)
root.update()
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.configure(fg_color=COLORS["bg"])

set_main_root(root)

# Verificación automática de limpieza semanal de JSON de logros.
try:
    GestorEstado().limpiar_si_es_necesario()
except Exception:
    logger.exception("Error en limpieza de archivos JSON")

# -------------------------------------------------------------
# DIÁLOGO INICIAL DE USUARIO
# -------------------------------------------------------------
class VentanaUsuarioCustom(ctk.CTkToplevel):
    def __init__(self, master, titulo, mensaje, show_cancel=True):
        super().__init__(master)
        self.overrideredirect(True) # Quitar barra de Windows
        self.geometry("550x320")
        self.configure(fg_color="white") # Fondo blanco para camuflar las esquinas rectangulares
        self.resultado = None
        
      
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (550 // 2)
        y = (screen_h // 2) - (320 // 2)
        self.geometry(f"550x320+{x}+{y}")

        # Contenedor principal con borde temático
        main_frame = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], border_width=6, border_color="white", corner_radius=30)
        main_frame.pack(fill="both", expand=True)

        # Marco para el título (encerrado para que no flote)
        title_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=15)
        title_frame.pack(pady=(25, 10), padx=40, fill="x")

        ctk.CTkLabel(title_frame, text="🚀 ¡NUEVA AVENTURA! 🚀", font=(FONT_NAME, 24, "bold"), text_color=COLORS["sidebar"]).pack(pady=10)
        ctk.CTkLabel(main_frame, text=mensaje, font=(FONT_NAME, 18), text_color="white").pack(pady=5)
        
        self.entrada = ctk.CTkEntry(main_frame, width=320, height=45, font=(FONT_NAME, 20), corner_radius=15, border_color="white", justify="center", fg_color="#F0F7FF")
        self.entrada.pack(pady=15)
        if self.entrada.winfo_exists():
            try:
                self.entrada.focus_set()
            except Exception:
                pass

        btn = ctk.CTkButton(main_frame, text="¡VAMOS A JUGAR!", font=(FONT_NAME, 18, "bold"), fg_color="#2ECC71", hover_color="#27AE60", corner_radius=20, height=50, command=self._confirmar)
        btn.pack(pady=(10, 5))

        # Botón Cancelar (solo si se permite) debajo del botón principal
        if show_cancel:
            btn_cancelar = ctk.CTkButton(main_frame, text="CANCELAR", font=(FONT_NAME, 14, "bold"), width=180, height=35, fg_color="#D5DBDB", text_color="#566573", hover_color="#ABB2B9", corner_radius=15, command=self.destroy)
            btn_cancelar.pack(pady=(0, 10))
        
        self.bind("<Return>", lambda e: self._confirmar())
        self.lift()
        self.grab_set()

    def _confirmar(self):
        val = self.entrada.get().strip() or "INVITADO"
        self.resultado = val
        self.destroy()

def solicitar_usuario(can_cancel=False):
    dialogo = VentanaUsuarioCustom(root, "Bienvenido", "Escribe tu nombre para comenzar:", show_cancel=can_cancel)
    root.wait_window(dialogo)
    nombre = dialogo.resultado
    
    gestor = GestorEstado()
    if nombre:
        gestor = GestorEstado()
        gestor.inicializar_usuario(nombre)
        logger.info("Usuario cargado: %s", nombre)

solicitar_usuario(can_cancel=False)


class VentanaSalirCustom(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(True) # Quitar barra de Windows
        self.geometry("550x420")
        self.configure(fg_color="white") # Fondo blanco para camuflar las esquinas rectangulares
        
        # Centrar manualmente
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (550 // 2)
        y = (screen_h // 2) - (420 // 2)
        self.geometry(f"550x420+{x}+{y}")

        # Contenedor principal con borde
        main_frame = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], border_width=6, border_color="white", corner_radius=30)
        main_frame.pack(fill="both", expand=True)

        # Marco para el título (encerrado para que no flote)
        title_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=15)
        title_frame.pack(pady=(25, 10), padx=40, fill="x")

        ctk.CTkLabel(title_frame, text="👋 ¡ADIÓS EXPLORADOR!", font=(FONT_NAME, 24, "bold"), text_color=COLORS["sidebar"]).pack(pady=10)
        ctk.CTkLabel(main_frame, text="¿Ya te vas?\n¡Vuelve pronto para seguir jugando y aprendiendo!", font=(FONT_NAME, 18), text_color="white", justify="center").pack(pady=5)
        
        # Mensaje de auto-guardado
        ctk.CTkLabel(
            main_frame, 
            text="¡SE GUARDARÁN AUTOMÁTICAMENTE TODOS TUS LOGROS Y TU PROGRESO!", 
            font=(FONT_NAME, 14, "bold"), 
            text_color="white", 
            justify="center",
            wraplength=480 # Mantiene el texto dentro de los márgenes de la ventana (550px)
        ).pack(pady=(20, 0)) # Separamos del texto superior sin empujar los botones

        # Contenedor para botones
        self.frame_botones = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.frame_botones.pack(fill="both", expand=True, padx=20, pady=10)

        # Botón para quedarse (Grande y fácil de clickear)
        self.btn_no = ctk.CTkButton(
            self.frame_botones, 
            text="🚀 ¡NO, QUIERO SEGUIR!", 
            font=(FONT_NAME, 18, "bold"),
            fg_color="#2ECC71", 
            hover_color="#27AE60",
            corner_radius=25, 
            height=70, 
            command=self.destroy
        )
        self.btn_no.place(relx=0.5, rely=0.35, anchor="center", relwidth=0.9)

        # Botón para salir (El travieso que esquiva)
        self.btn_si = ctk.CTkButton(
            self.frame_botones, 
            text="Sí, salir", 
            font=(FONT_NAME, 12, "bold"),
            fg_color=COLORS["danger"], # Cambiado a Rojo para indicar salida/peligro
            text_color="white",        # Blanco para mejor contraste sobre rojo
            hover_color="#C0392B",     # Rojo oscuro al pasar el ratón
            corner_radius=15, 
            width=100,
            height=35, 
            command=cerrar_aplicacion
        )
        self.btn_si.place(relx=0.5, rely=0.8, anchor="center")
        
        # Bind del evento para esquivar
        self.btn_si.bind("<Enter>", self._esquivar)
        self.lift()
        self.grab_set()

    def _move_btn_si(self, nx, ny):
        if self.btn_si.winfo_exists():
            try:
                self.btn_si.place(relx=nx, rely=ny, anchor="center")
            except Exception:
                pass

    def _esquivar(self, event):
        """Mueve el botón SÍ con saltos pequeños para que sea entretenido, no imposible."""
        info = self.btn_si.place_info()
        try:
            relx = float(info.get("relx", 0.5))
            rely = float(info.get("rely", 0.75))
        except (TypeError, ValueError):
            relx, rely = 0.5, 0.75

        dx = random.uniform(-0.15, 0.15)
        dy = random.uniform(-0.1, 0.1)
        nx = min(max(relx + dx, 0.2), 0.8)
        ny = min(max(rely + dy, 0.65), 0.9) # Limitar a la zona inferior segura

        self.after(150, lambda: self._move_btn_si(nx, ny))


# -------------------------------------------------------------
# LANZAMIENTO DE MATERIAS (panel embebido)
# -------------------------------------------------------------
def launch_subject(subject_id):
    """Carga el módulo dentro del panel principal (sin ventanas nuevas)."""
    global vista_actual, _loading_module

    if _loading_module:
        return

    _loading_module = True
    logger.info("Módulo abierto: %s", subject_id)
    try:
        limpiar_panel()
        aplicar_tema_interfaz(subject_id)

        # Ocultar temporalmente el botón de Salir para evitar clicks accidentales
        try:
            if btn_salir and btn_salir.winfo_ismapped():
                btn_salir.pack_forget()
        except Exception:
            pass

        modulo_frame = ModuleFactory.get_module_frame(subject_id, principal, vista_inicio)
        if modulo_frame:
            global vista_actual
            vista_actual = modulo_frame
            modulo_frame.pack(fill="both", expand=True)

            config = ModuleFactory.SUBJECTS.get(subject_id, {})
            materia_real = config.get("nombre", "")
            if materia_real:
                GestorEstado().actualizar_progreso(materia_real, 0.05)
        else:
            messagebox.showerror(
                "Módulo no disponible",
                f"No se pudo cargar: {subject_id}",
                parent=root,
            )
    finally:
        root.after(500, _liberar_carga_modulo)


def _liberar_carga_modulo():
    global _loading_module, _tarjetas_deshabilitadas
    _loading_module = False
    _tarjetas_deshabilitadas = False


def mostrar_boton_salir():
    """Asegura que el botón Salir esté visible en la barra lateral."""
    try:
        if btn_salir and not btn_salir.winfo_ismapped():
            btn_salir.pack(side="bottom", fill="x", padx=10, pady=30)
    except Exception:
        pass


# -------------------------------------------------------------
# LIMPIEZA Y VISTAS DEL PANEL
# -------------------------------------------------------------
def limpiar_panel():
    global vista_actual
    if vista_actual is not None:
        try:
            vista_actual.destroy()
        except Exception:
            pass
        vista_actual = None

    for widget in principal.winfo_children():
        widget.destroy()


def vista_inicio():
    limpiar_panel()
    marcar_boton_activo("Inicio")
    aplicar_tema_interfaz("default")
    _dibujar_perfil_usuario()
    # Mostrar de nuevo el botón Salir cuando estemos en el inicio
    mostrar_boton_salir()
    actualizar_fuentes_responsivas()

    ancho, alto = obtener_tamano_ventana()
    tam_logo = (
        max(280, min(420, int(ancho * 0.22))),
        max(90, min(180, int(alto * 0.13))),
    )
    # Aumentar tamaño de tarjeta (50% más grande para mejor visibilidad y proporción)
    base_tam = theme.tamano_tarjeta(ancho, alto)
    tam_tarjeta = (int(base_tam[0] * 1.5), int(base_tam[1] * 1.5))
    card_padding_x = max(18, int(ancho * 0.015))
    card_padding_y = max(28, int(alto * 0.035))

    img_logo = get_asset("imagenes/logo.png", size=tam_logo)
    ctk.CTkLabel(principal, image=img_logo, text="", fg_color="transparent").pack(
        pady=(max(24, int(alto * 0.035)), max(14, int(alto * 0.025)))
    )

    contenedor = ctk.CTkFrame(principal, fg_color="transparent")
    contenedor.pack(expand=True, fill="both")
    # Usamos 6 columnas para permitir el centrado de los 2 módulos inferiores (Pirámide invertida)
    for i in range(6):
        contenedor.grid_columnconfigure(i, weight=1)
    for i in range(2):
        contenedor.grid_rowconfigure(i, weight=1)

    orden = ["lectura_escritura", "ajedrez", "computacion", "robotica", "dibujo"]
    descripciones = {
        "lectura_escritura": "¡CONVIÉRTETE EN EL MAESTRO DE LAS HISTORIAS Y LAS LETRAS! ✍️📜",
        "ajedrez": "¡DESAFÍA TU MENTE Y CONQUISTA EL TABLERO COMO UN CAMPEÓN! ♟️🏆",
        "computacion": "¡DOMINA LA TECNOLOGÍA Y VIAJA AL CORAZÓN DEL CÓDIGO! 💻⚡",
        "robotica": "¡CONSTRUYE, PROGRAMA Y DA VIDA A TU PROPIO ROBOT! 🦾",
        "dibujo": "¡DA VIDA A TU IMAGINACIÓN Y CREA MUNDOS DE COLORES! 🎨✨"
    }
    posiciones = {
        "lectura_escritura": (0, 0, 2), # fila, col, span
        "ajedrez": (0, 2, 2),
        "computacion": (0, 4, 2),
        "robotica": (1, 1, 2),
        "dibujo": (1, 3, 2),
    }

    for subject_id in orden:
        if subject_id not in ModuleFactory.SUBJECTS:
            continue
        cfg = ModuleFactory.SUBJECTS[subject_id]
        fila, col, span = posiciones[subject_id]
        crear_tarjeta(
            contenedor,
            descripciones.get(subject_id, cfg["nombre"]),
            cfg["imagen"],
            fila,
            col,
            tam_tarjeta,
            card_padding_x,
            card_padding_y,
            comando=lambda sid=subject_id: launch_subject(sid),
            columnspan=span,
        )


def crear_tarjeta(parent, texto, img_name, fila, columna, size, padx, pady, comando=None, columnspan=1):
    img_normal = get_asset(img_name, size=size)
    contenedor = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=25)
    contenedor.grid(row=fila, column=columna, columnspan=columnspan, padx=padx, pady=pady, sticky="n")

    def animar_entrada(y=40):
        if not contenedor.winfo_exists():
            return
        if y > 20:
            contenedor.grid_configure(pady=y - 2)
            root.after(10, lambda: animar_entrada(y - 2))

    root.after(100, animar_entrada)

    lbl = ctk.CTkLabel(
        contenedor, image=img_normal, text="", cursor="hand2", fg_color="transparent"
    )
    lbl.pack(padx=12, pady=(12, 8))

    ctk.CTkLabel(
        contenedor,
        text=texto,
        font=FONTS["botones"],
        text_color=COLORS["text_dark"],
        anchor="center",
        wraplength=size[0] - 20,
    ).pack(pady=(0, 12), padx=10)

    def on_enter(_e):
        contenedor.configure(fg_color=COLORS["sidebar"])

    def on_leave(_e):
        contenedor.configure(fg_color="transparent")

    def on_click(_e):
        global _tarjetas_deshabilitadas
        if _loading_module or _tarjetas_deshabilitadas:
            return
        _tarjetas_deshabilitadas = True
        if comando:
            comando()

    lbl.bind("<Enter>", on_enter)
    lbl.bind("<Leave>", on_leave)
    lbl.bind("<Button-1>", on_click)


def vista_progreso():
    limpiar_panel()
    marcar_boton_activo("Progreso")
    aplicar_tema_interfaz("default")
    actualizar_fuentes_responsivas()
    gestor = GestorEstado()
    nombre_usuario = getattr(gestor, "usuario_actual", "Explorador")
    materias = gestor.get_materias()
    promedio = sum(materias.values()) / len(materias) if materias else 0
    ancho, alto = obtener_tamano_ventana()
    padding_x = max(30, int(ancho * 0.035))
    padding_y = max(15, int(alto * 0.02))

    header = ctk.CTkFrame(principal, fg_color="transparent")
    header.pack(fill="x", padx=padding_x, pady=(max(30, int(alto * 0.03)), max(15, int(alto * 0.02))))
    ctk.CTkLabel(
        header,
        text=f"FELICIDADES ESTE ES UN FANTASTICO PROGRESO\n✨ {str(nombre_usuario).upper()} ✨",
        font=FONTS["subtitulo"],
        text_color=COLORS["text_dark"],
        justify="center"
    ).pack()
    global_pb = ctk.CTkProgressBar(
        header,
        progress_color=COLORS["gold"],
        fg_color=COLORS["progress_bg"],
        height=25,
        corner_radius=12,
    )
    global_pb.set(promedio)
    global_pb.pack(fill="x", pady=10)
    ctk.CTkLabel(
        header,
        text=f"Completado {int(promedio * 100)}% del Mundo Escolar",
        font=FONTS["pequeno"],
    ).pack()

    contenedor = ctk.CTkFrame(principal, fg_color="transparent")
    contenedor.pack(fill="both", expand=True, padx=padding_x, pady=padding_y)
    contenedor.grid_columnconfigure(0, weight=1)

    iconos = {cfg["nombre"]: cfg["icono"] for cfg in ModuleFactory.SUBJECTS.values()}

    def animar_barra(barra, label, objetivo, actual=0):
        # Verificar si el widget aún existe para evitar errores al cambiar de vista
        if not barra.winfo_exists() or not label.winfo_exists():
            return
        if actual <= objetivo:
            barra.set(actual)
            label.configure(text=f"{int(actual * 100)}%")
            root.after(20, lambda: animar_barra(barra, label, objetivo, actual + 0.04))

    materia_items = list(materias.items())
    def render_item(idx=0):
        if not contenedor.winfo_exists():
            return
        if idx >= len(materia_items): return
        nombre, valor = materia_items[idx]
        f = ctk.CTkFrame(
            contenedor,
            fg_color=COLORS["white"],
            corner_radius=25,
            border_width=2,
            border_color=COLORS["sidebar"],
        )
        f.pack(fill="x", pady=12, padx=5)
        ctk.CTkLabel(
            f,
            text=f"{iconos.get(nombre, '⭐')} {nombre}",
            font=FONTS["botones"],
            text_color="#333",
        ).pack(side="left", padx=25)
        lbl_pct = ctk.CTkLabel(
            f, text="0%", font=FONTS["subtitulo"], text_color=COLORS["sidebar"]
        )
        lbl_pct.pack(side="right", padx=25)
        pb = ctk.CTkProgressBar(
            f,
            progress_color=COLORS["gold"],
            fg_color="#E0E0E0",
            height=22,
            corner_radius=12,
            border_width=1,
            border_color="#CCC"
        )
        pb.set(0)
        pb.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        animar_barra(pb, lbl_pct, valor)
        root.after(30, lambda: render_item(idx + 1))

    render_item()


def vista_logros():
    limpiar_panel()
    marcar_boton_activo("Logros")
    aplicar_tema_interfaz("default")
    actualizar_fuentes_responsivas()
    ancho, alto = obtener_tamano_ventana()
    gestor = GestorEstado()
    nombre_usuario = getattr(gestor, "usuario_actual", "Explorador")

    # --- Pantalla de Carga Estilizada ---
    loading_frame = ctk.CTkFrame(principal, fg_color="transparent")
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        loading_frame,
        text="CARGANDO TUS LOGROS",
        font=(FONT_NAME, 32, "bold"),
        text_color=COLORS["text_dark"]
    ).pack()

    ctk.CTkLabel(
        loading_frame,
        text="POR FAVOR ESPERA",
        font=(FONT_NAME, 18),
        text_color=COLORS["text_dark"]
    ).pack(pady=10)

    # Barra de progreso para indicar que el sistema está trabajando
    loading_bar = ctk.CTkProgressBar(
        loading_frame,
        width=350,
        height=15,
        corner_radius=10,
        progress_color=COLORS.get("progress_fill", "#4DA3FF"),
        fg_color=COLORS.get("progress_bg", "#E0E0E0")
    )
    loading_bar.set(0)
    loading_bar.pack(pady=15)

    scroll = ctk.CTkScrollableFrame(principal, fg_color="transparent")
    for i in range(4):
        scroll.grid_columnconfigure(i, weight=1)

    ctk.CTkLabel(
        scroll,
        text=f"IMPRESIONANTE ESTOS SON TUS LOGROS DESBLOQUEADOS\n🏆 {str(nombre_usuario).upper()} 🏆",
        text_color=COLORS["text_dark"],
        font=FONTS["subtitulo"],
        justify="center",
        wraplength=max(400, int(ancho * 0.7))
    ).grid(row=0, column=0, columnspan=4, pady=30)

    materias = gestor.get_materias()
    completadas = sum(1 for v in materias.values() if v >= 0.99)

    def render_logros_batch(idx=0, fila=1, col=0):
        if not scroll.winfo_exists():
            return

        # Actualizar el progreso de la barra visualmente
        if loading_frame.winfo_exists() and loading_bar.winfo_exists():
            progreso = idx / len(LOGROS) if len(LOGROS) > 0 else 0
            loading_bar.set(progreso)

        if idx >= len(LOGROS):
            # Finalizado: Quitamos la carga y mostramos el scroll completo
            if loading_frame.winfo_exists():
                loading_frame.destroy()
            scroll.pack(fill="both", expand=True, padx=max(15, int(ancho * 0.01)), pady=max(15, int(alto * 0.02)))
            return
        
        logro = LOGROS[idx]
        desbloqueado = _evaluar_logro_desbloqueado(logro, materias, completadas, gestor)
        color = logro["color"] if desbloqueado else COLORS["locked"]

        card = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["white"],
            corner_radius=20,
            border_width=2,
            border_color=logro["color"] if desbloqueado else "#F0F0F0",
        )
        card.grid(row=fila, column=col, padx=15, pady=12, sticky="nsew")

        insignia = ctk.CTkFrame(card, fg_color=color, width=45, height=45, corner_radius=22)
        insignia.pack(pady=(15, 5))
        insignia.pack_propagate(False)
        ctk.CTkLabel(
            insignia,
            text="🏆" if desbloqueado else "🔒",
            text_color="white",
            font=("Arial", 18),
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text=logro["nombre"],
            font=FONTS["tarjetas"],
            text_color="#333" if desbloqueado else "#999",
        ).pack()
        ctk.CTkLabel(
            card,
            text=logro["desc"],
            font=FONTS["pequeno"],
            text_color="#888",
            wraplength=max(120, int(ancho * 0.06)),
        ).pack(pady=2, padx=10)

        if logro["tipo"] == "accion":
            estado = "✨ ¡CONSEGUIDO!" if desbloqueado else "Completa la actividad"
        elif logro["tipo"] == "general":
            estado = "✨ ¡CONSEGUIDO!" if desbloqueado else "Sigue explorando"
        else:
            estado = (
                "✨ ¡CONSEGUIDO!"
                if desbloqueado
                else f"NECESITAS: {int(logro['req'] * 100)}%"
            )
        ctk.CTkLabel(
            card,
            text=estado,
            font=FONTS["pequeno"],
            text_color=color if desbloqueado else "#BBB",
        ).pack(pady=(2, 10))

        idx += 1
        col += 1
        if col > 3:
            col = 0
            fila += 1
        
        # Renderizamos rápido en segundo plano mientras está oculto
        root.after(20, lambda: render_logros_batch(idx, fila, col))

    render_logros_batch()

def confirmar_salida():
    VentanaSalirCustom(root)


def cerrar_aplicacion():
    logger.info("Aplicación cerrada")
    root.quit()


root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)


def ajustar_sidebar():
    ancho = obtener_ancho_sidebar(sidebar_expandido)
    sidebar.configure(width=ancho)
    if sidebar_expandido:
        expanded_width = max(130, ancho - 30)
        for btn in botones_menu.values():
            btn.configure(width=expanded_width)
        btn_nuevo_usuario.configure(width=expanded_width)
        btn_salir.configure(width=expanded_width)
    else:
        for btn in botones_menu.values():
            btn.configure(width=40)
        btn_nuevo_usuario.configure(width=40)
        btn_salir.configure(width=40)


_resize_after_id = None

def _on_resize(_event=None):
    """Reajusta fuentes al cambiar el tamaño de la ventana."""
    global _resize_after_id
    if _resize_after_id:
        root.after_cancel(_resize_after_id)
    _resize_after_id = root.after(120, _handle_redimension)


def _handle_redimension():
    global _resize_after_id
    _resize_after_id = None
    if principal.winfo_children():
        actualizar_fuentes_responsivas()
        ajustar_sidebar()
        # Actualizar el margen de seguridad para que el contenido no sea tapado al redimensionar
        ancho_sb_max = obtener_ancho_sidebar(True)
        principal.pack_configure(padx=(ancho_sb_max, 0))


# -------------------------------------------------------------
# CONSTRUCCIÓN DEL SIDEBAR
# -------------------------------------------------------------
principal = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
# Reservamos el espacio del sidebar expandido de forma estática para evitar solapamientos y saltos
ancho_sb_reserva = obtener_ancho_sidebar(True)
principal.pack(expand=True, fill="both", padx=(ancho_sb_reserva, 0))

sidebar = ctk.CTkFrame(
    root,
    fg_color=COLORS["sidebar"],
    width=obtener_ancho_sidebar(True),
    corner_radius=0,
    border_width=1,
    border_color="#2A7ACC",
)
# Usamos place para que la barra lateral sea un "overlay" y no desplace el contenido principal al colapsar
sidebar.place(x=0, y=0, relheight=1)
sidebar.pack_propagate(False)
sidebar.lift() # Aseguramos que la barra esté siempre por encima del contenido

sidebar_expandido = True


def toggle_sidebar():
    global sidebar_expandido
    if sidebar_expandido:
        ancho = obtener_ancho_sidebar(False)
        sidebar.configure(width=ancho)
        for btn in botones_menu.values():
            btn.configure(text=btn._icono, width=40)
        btn_nuevo_usuario.configure(text="👤", width=40)
        btn_salir.configure(text="❌", width=40)
        btn_toggle.configure(text="▶")
        lbl_titulo_sidebar.pack_forget() # Ocultar el título cuando la barra se contrae
        sidebar_expandido = False
    else:
        ancho = obtener_ancho_sidebar(True)
        sidebar.configure(width=ancho)
        expanded_width = max(130, ancho - 30)
        for texto, btn in botones_menu.items():
            # Evitar error con el botón de Usuario que no está en la lista 'menus' inicial
            icono = getattr(btn, "_icono", "")
            btn.configure(text=f"  {icono}  {texto}", width=expanded_width)
        btn_nuevo_usuario.configure(text="  👤  Usuario", width=expanded_width)
        btn_salir.configure(text="  ❌  Salir", width=expanded_width)
        btn_toggle.configure(text="◀")
        lbl_titulo_sidebar.pack(pady=(0, 20), after=btn_toggle) # Volver a mostrar el título al expandir
        sidebar_expandido = True


btn_toggle = ctk.CTkButton(
    sidebar,
    text="🏠",
    width=40,
    fg_color="transparent",
    hover_color=COLORS["sidebar_hover"],
    command=vista_inicio,
)
btn_toggle.pack(pady=(10, 20), anchor="e", padx=10)

lbl_titulo_sidebar = ctk.CTkLabel(
    sidebar, text="Mundo Escolar", text_color="white", font=(FONT_NAME, 18, "bold")
)
lbl_titulo_sidebar.pack(pady=(0, 20))

menus = [
    ("Inicio", "🏠", vista_inicio),
    ("Progreso", "📈", vista_progreso),
    ("Logros", "🏆", vista_logros),
]

botones_menu = {}
for texto, icono, comando in menus:
    btn = ctk.CTkButton(
        sidebar,
        text=f"  {icono}  {texto}",
        command=comando,
        fg_color="transparent",
        text_color="white",
        hover_color=COLORS["sidebar_hover"],
        font=FONTS["botones"],
        anchor="w",
        height=50,
        corner_radius=10,
    )
    btn._icono = icono
    btn.pack(fill="x", padx=10, pady=5)
    botones_menu[texto] = btn

btn_nuevo_usuario = ctk.CTkButton(
    sidebar,
    text=" 👤   Usuario",
    command=lambda: [reset_and_prompt(), marcar_boton_activo("Usuario")],
    fg_color="transparent",
    text_color="white",
    hover_color=COLORS["sidebar_hover"],
    font=FONTS["botones"],
    anchor="w",
    height=35,
    corner_radius=10,
)
btn_nuevo_usuario._icono = "👤"
btn_nuevo_usuario.pack(fill="x", padx=10, pady=5)
botones_menu["Usuario"] = btn_nuevo_usuario


def reset_and_prompt():
    # Al ser desde el botón lateral, permitimos cancelar
    dialogo = VentanaUsuarioCustom(root, "Nueva Aventura", "Escribe tu nombre para el nuevo perfil:", show_cancel=True)
    root.wait_window(dialogo)
    if dialogo.resultado:
        GestorEstado().reset()
        GestorEstado().inicializar_usuario(dialogo.resultado)
        logger.info("Usuario cargado: %s", dialogo.resultado)
        vista_inicio()


btn_salir = ctk.CTkButton(
    sidebar,
    text="  ❌  Salir",
    command=confirmar_salida,
    fg_color=COLORS["danger"],
    hover_color="#C0392B",
    font=FONTS["botones"],
    anchor="w",
    height=50,
    corner_radius=10,
)
btn_salir.pack(side="bottom", fill="x", padx=10, pady=30)

# -------------------------------------------------------------
# PANEL PRINCIPAL Y ARRANQUE
# -------------------------------------------------------------
root.bind("<Configure>", _on_resize)

vista_inicio()


def abrir_admin(event=None):
    from core.admin_tools import AdminTools

    AdminTools(root)


root.bind("<Control-Shift-A>", abrir_admin)

root.mainloop()
