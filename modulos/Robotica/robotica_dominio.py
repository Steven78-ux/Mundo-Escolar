"""Lógica de dominio para el módulo de Robótica (versión infantil)."""
from dataclasses import dataclass
from typing import List, Optional, Tuple
import random


# ----------------------------------------------
# Misión 1: Partes del robot (preguntas)
# ----------------------------------------------
@dataclass
class PreguntaParte:
    imagen: str
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    explicacion: str


class JuegoPartesRobot:
    def __init__(self, preguntas: List[PreguntaParte]):
        self.preguntas = preguntas[:]
        random.shuffle(self.preguntas)
        self.indice = 0
        self.puntaje = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.preguntas)

    def pregunta_actual(self) -> Optional[PreguntaParte]:
        if self.completado:
            return None
        return self.preguntas[self.indice]

    def verificar_respuesta(self, respuesta: str) -> Tuple[bool, str]:
        """Retorna (acertó, explicación)."""
        actual = self.pregunta_actual()
        if not actual:
            return False, ""
        acerto = respuesta == actual.respuesta_correcta
        if acerto:
            self.puntaje += 1
        self.indice += 1
        return acerto, actual.explicacion


# ----------------------------------------------
# Misión 2: Emparejar parte con función
# ----------------------------------------------
@dataclass
class Tarjeta:
    id: str
    nombre: str
    icono: str
    tipo: str
    funcion: str
    emparejada: bool = False


class JuegoEmparejar:
    def __init__(self, tarjetas_nombre: List[Tarjeta], tarjetas_funcion: List[Tarjeta]):
        self.tarjetas_nombre = tarjetas_nombre[:]
        self.tarjetas_funcion = tarjetas_funcion[:]
        random.shuffle(self.tarjetas_nombre)
        random.shuffle(self.tarjetas_funcion)
        self.seleccionada_nombre: Optional[Tarjeta] = None
        self.parejas_completadas = 0
        self.total_parejas = len(tarjetas_nombre)

    def seleccionar_nombre(self, tarjeta: Tarjeta) -> None:
        """Selecciona o cambia el componente activo."""
        if tarjeta.emparejada:
            return
        if self.seleccionada_nombre == tarjeta:
            self.seleccionada_nombre = None
        else:
            self.seleccionada_nombre = tarjeta

    def seleccionar_funcion(self, tarjeta_funcion: Tarjeta) -> Optional[bool]:
        """Retorna True si pareja correcta, False si no, None si aún no hay selección."""
        if tarjeta_funcion.emparejada or self.seleccionada_nombre is None:
            return None
        if self.seleccionada_nombre.funcion == tarjeta_funcion.nombre:
            self.seleccionada_nombre.emparejada = True
            tarjeta_funcion.emparejada = True
            self.parejas_completadas += 1
            self.seleccionada_nombre = None
            return True
        self.seleccionada_nombre = None
        return False

    @property
    def completado(self) -> bool:
        return self.parejas_completadas >= self.total_parejas


# ----------------------------------------------
# Misión 3: Construye tu robot para una misión
# ----------------------------------------------
@dataclass
class ComponenteRobot:
    id: str
    nombre: str
    icono: str
    tipo: str
    utilidad: str


@dataclass
class MisionRobot:
    nombre: str
    descripcion: str
    requisitos: List[str]


class ConstructorRobot:
    def __init__(self, componentes_disponibles: List[ComponenteRobot], mision: MisionRobot):
        self.componentes = componentes_disponibles[:]
        self.mision = mision
        self.seleccionados: List[ComponenteRobot] = []
        self.mensaje_feedback = ""

    def agregar_componente(self, comp: ComponenteRobot) -> bool:
        if comp in self.seleccionados:
            self.mensaje_feedback = "Ya añadiste esta pieza."
            return False
        if len(self.seleccionados) >= 5:
            self.mensaje_feedback = "Solo puedes añadir hasta 5 componentes."
            return False
        self.seleccionados.append(comp)
        self.mensaje_feedback = f"¡{comp.nombre} añadido!"
        return True

    def quitar_componente(self, comp: ComponenteRobot):
        if comp in self.seleccionados:
            self.seleccionados.remove(comp)
            self.mensaje_feedback = f"Has quitado {comp.nombre}."

    def verificar_mision(self) -> Tuple[bool, str]:
        tipos_seleccionados = [c.tipo for c in self.seleccionados]
        for req in self.mision.requisitos:
            if req not in tipos_seleccionados:
                return False, f"Falta un componente de tipo «{req}». Revisa la misión."
        if "sensor" not in tipos_seleccionados:
            return False, "Tu robot necesita al menos un sensor para percibir el entorno."
        if "actuador" not in tipos_seleccionados:
            return False, "Tu robot necesita al menos un actuador (motor, rueda, brazo) para actuar."
        return True, "¡Perfecto! Tu robot está listo para la misión."


# ----------------------------------------------
# Misión 3 (parte 2): Programación con flechas
# ----------------------------------------------
class RobotProgramable:
    def __init__(
        self,
        tamano_mapa: Tuple[int, int] = (5, 5),
        obstaculos: Optional[List[Tuple[int, int]]] = None,
        meta: Tuple[int, int] = (4, 4),
    ):
        self.filas, self.columnas = tamano_mapa
        self.obstaculos = set(obstaculos) if obstaculos else set()
        self.meta = meta
        self.pos = [0, 0]
        self.historial: List[str] = []
        self.exito = False

    def reiniciar(self):
        self.pos = [0, 0]
        self.historial.clear()
        self.exito = False

    def mover(self, direccion: str) -> Tuple[bool, str]:
        if self.exito:
            return False, "Ya alcanzaste la meta. Reinicia para otro intento."
        f, c = self.pos
        if direccion == "↑":
            f -= 1
        elif direccion == "↓":
            f += 1
        elif direccion == "←":
            c -= 1
        elif direccion == "→":
            c += 1
        else:
            return False, "Comando no válido."

        if not (0 <= f < self.filas and 0 <= c < self.columnas):
            return False, "Te saliste del mapa."
        if (f, c) in self.obstaculos:
            return False, "¡Hay un obstáculo! No puedes pasar."

        self.pos = [f, c]
        self.historial.append(direccion)
        if (f, c) == self.meta:
            self.exito = True
            return True, "¡Llegaste a la meta! ¡Misión cumplida!"
        return True, ""

    def deshacer(self) -> bool:
        if not self.historial:
            return False
        self.historial.pop()
        self.pos = [0, 0]
        self.exito = False
        for d in self.historial:
            if d == "↑":
                self.pos[0] -= 1
            elif d == "↓":
                self.pos[0] += 1
            elif d == "←":
                self.pos[1] -= 1
            elif d == "→":
                self.pos[1] += 1
        return True
