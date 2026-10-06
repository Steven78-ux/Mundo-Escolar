"""Herramientas de administración para el profesor (limpieza de datos locales)."""

import os

import customtkinter as ctk
from tkinter import messagebox
from core.gestor_estado import GestorEstado
from core.theme import FONT_NAME, COLORS


class AdminTools(ctk.CTkToplevel):
    """Panel administrativo con diseño profesional para la gestión de datos de alumnos."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Panel de Administración — Mundo Escolar")
        self.attributes("-fullscreen", True)
        # Fondo oscuro profundo (Estilo Dashboard Profesional)
        self.configure(fg_color="#0F172A") 
        self.transient(parent)
        self.grab_set()
        self.focus_force()

        self.usuario_seleccionado = None
        self.widgets_usuarios = {}

        # Contenedor Principal (Tarjeta Central)
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#1E293B", 
            corner_radius=25, 
            border_width=2, 
            border_color="#334155"
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

        # --- Encabezado ---
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", padx=50, pady=(45, 25))
        
        ctk.CTkLabel(
            header,
            text="🔐 PANEL DE CONTROL DOCENTE",
            font=(FONT_NAME, 34, "bold"),
            text_color="#F8FAFC",
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="Herramientas de Gestión de Usuarios y Progreso",
            font=(FONT_NAME, 14),
            text_color="#64748B",
        ).pack(side="right", pady=(15, 0))

        # Separador Estilizado
        ctk.CTkFrame(self.main_frame, height=2, fg_color="#334155").pack(fill="x", padx=50)

        # --- Cuerpo del Panel ---
        body = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=50, pady=30)

        # Columna Izquierda: Lista de Estudiantes
        left_col = ctk.CTkFrame(body, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 30))

        ctk.CTkLabel(
            left_col,
            text="ALUMNOS REGISTRADOS EN EL SISTEMA",
            font=(FONT_NAME, 13, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(0, 10))

        self.scroll_lista = ctk.CTkScrollableFrame(
            left_col, 
            fg_color="#0F172A", 
            border_width=1, 
            border_color="#334155",
            scrollbar_button_color="#334155",
            corner_radius=15
        )
        self.scroll_lista.pack(fill="both", expand=True)

        # Columna Derecha: Acciones
        right_col = ctk.CTkFrame(body, fg_color="transparent", width=280)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)

        btn_style = {"font": (FONT_NAME, 14, "bold"), "height": 52, "corner_radius": 15}

        self.btn_refrescar = ctk.CTkButton(
            right_col,
            text="🔄 Actualizar Lista",
            fg_color="#334155",
            hover_color="#475569",
            command=self._cargar_usuarios_lista,
            **btn_style
        )
        self.btn_refrescar.pack(fill="x", pady=(0, 15))

        self.btn_eliminar = ctk.CTkButton(
            right_col,
            text="👤 Eliminar Alumno",
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self._eliminar_usuario_seleccionado,
            **btn_style
        )
        self.btn_eliminar.pack(fill="x", pady=(0, 15))

        self.btn_borrar_todo = ctk.CTkButton(
            right_col,
            text="🗑️ BORRAR TODOS LOS PROGRESOS",
            fg_color="#7F1D1D",
            hover_color="#991B1B",
            command=self._confirmar_y_borrar_todo,
            **btn_style
        )
        self.btn_borrar_todo.pack(fill="x")

        # Footer: Atajos e Información
        footer = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=50, pady=35)
        
        ctk.CTkLabel(
            footer,
            text="Acceso exclusivo para docentes. Atajo rápido: Ctrl+Shift+A",
            font=(FONT_NAME, 12),
            text_color="#475569"
        ).pack(side="left")

        ctk.CTkButton(
            footer,
            text="VOLVER AL SOFTWARE",
            font=(FONT_NAME, 13, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#475569",
            text_color="#F8FAFC",
            hover_color="#334155",
            width=180,
            height=40,
            command=self.destroy
        ).pack(side="right")

        self._cargar_usuarios_lista()

    def _confirmar_y_borrar_todo(self):
        if not messagebox.askyesno(
            "Confirmar",
            "¿Borrar todos los archivos de progreso de estudiantes?\n"
            "Esta acción no se puede deshacer.",
            parent=self,
        ):
            return

        gestor = GestorEstado()
        carpeta = gestor.dir_usuarios
        nombre_control = "ultima_limpieza.json"
        borrados = 0
        try:
            if os.path.isdir(carpeta):
                for nombre in os.listdir(carpeta):
                    if not nombre.lower().endswith(".json") or nombre == nombre_control:
                        continue
                    ruta = os.path.join(carpeta, nombre)
                    try:
                        os.remove(ruta)
                        borrados += 1
                    except OSError:
                        pass
        except OSError:
            messagebox.showerror(
                "Error",
                f"No se pudo acceder a la carpeta de datos:\n{carpeta}",
                parent=self,
            )
            return

        gestor.inicializar_usuario("Invitado")
        gestor.reset()

        messagebox.showinfo(
            "Listo",
            f"Se eliminaron {borrados} archivo(s). Estado actual: Invitado (limpio).",
            parent=self,
        )

    def _cargar_usuarios_lista(self):
        """Carga los alumnos dinámicamente en el panel de scroll."""
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()
        
        self.usuario_seleccionado = None
        self.widgets_usuarios = {}
        
        gestor = GestorEstado()
        carpeta = gestor.dir_usuarios
        try:
            archivos = sorted([f for f in os.listdir(carpeta) if f.lower().endswith('.json')])
        except Exception:
            archivos = []

        if not archivos:
            ctk.CTkLabel(self.scroll_lista, text="No hay perfiles de alumnos registrados.", text_color="#64748B", font=(FONT_NAME, 14, "italic")).pack(pady=40)
            return

        for f in archivos:
            nombre = os.path.splitext(f)[0]
            
            btn = ctk.CTkButton(
                self.scroll_lista,
                text=f"  👤  {nombre}",
                anchor="w",
                fg_color="transparent",
                text_color="#E2E8F0",
                hover_color="#334155",
                font=(FONT_NAME, 15),
                height=48,
                corner_radius=10,
                command=lambda n=nombre: self._seleccionar_usuario(n)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.widgets_usuarios[nombre] = btn

    def _seleccionar_usuario(self, nombre):
        # Resetear estilos de todos los botones
        for btn in self.widgets_usuarios.values():
            btn.configure(fg_color="transparent", text_color="#E2E8F0")
        
        # Resaltar el seleccionado
        self.usuario_seleccionado = nombre
        self.widgets_usuarios[nombre].configure(fg_color="#3B82F6", text_color="white")

    def _eliminar_usuario_seleccionado(self):
        if not self.usuario_seleccionado:
            messagebox.showwarning("Atención", "Por favor, seleccione un alumno de la lista.", parent=self)
            return

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al alumno '{self.usuario_seleccionado}'?\nEste proceso borrará todo su progreso de forma permanente.", parent=self):
            return

        gestor = GestorEstado()
        ruta = os.path.join(gestor.dir_usuarios, f"{self.usuario_seleccionado}.json")
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
        except Exception:
            messagebox.showerror("Error", "No se pudo acceder al archivo del alumno.", parent=self)
            return

        # Reestablecer estado si era el alumno activo
        if getattr(gestor, 'usuario_actual', None) == self.usuario_seleccionado:
            gestor.inicializar_usuario('Invitado')
            gestor.reset()

        self._cargar_usuarios_lista()
        messagebox.showinfo("Proceso Completado", f"El perfil del alumno '{self.usuario_seleccionado}' ha sido eliminado.", parent=self)
