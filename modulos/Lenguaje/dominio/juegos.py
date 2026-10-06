"""
Lógica de dominio para los juegos de Lenguaje.
No depende de ninguna librería gráfica.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import random


# ----------------------------------------------------------------------
# Detective de Sonidos
# ----------------------------------------------------------------------
@dataclass
class PreguntaSonido:
    letra: str
    sonido: str
    opciones: List[str]
    correcta: str


class DetectiveSonidos:
    def __init__(self, preguntas: List[PreguntaSonido]):
        self.preguntas = preguntas[:]
        random.shuffle(self.preguntas)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.preguntas)

    def pregunta_actual(self) -> Optional[PreguntaSonido]:
        if self.completado:
            return None
        return self.preguntas[self.indice]

    def verificar(self, opcion_elegida: str) -> bool:
        actual = self.pregunta_actual()
        if actual is None:
            return False
        if opcion_elegida == actual.correcta:
            self.indice += 1
            return True
        return False


# ----------------------------------------------------------------------
# Constructor de Palabras
# ----------------------------------------------------------------------
@dataclass
class PalabraConstruible:
    imagen: str  # emoji
    palabra: str
    silabas: List[str]


class ConstructorPalabras:
    def __init__(self, palabras: List[PalabraConstruible], distractores: List[str]):
        self.palabras = palabras[:]
        random.shuffle(self.palabras)
        self.distractores = distractores[:]
        self.indice = 0
        self.palabra_formada = ""

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.palabras)

    def palabra_actual(self) -> Optional[PalabraConstruible]:
        if self.completado:
            return None
        return self.palabras[self.indice]

    def agregar_silaba(self, silaba: str) -> Tuple[bool, str]:
        """
        Retorna (es_correcto_hasta_ahora, mensaje).
        Si la palabra se completa correctamente, avanza al siguiente ítem.
        """
        actual = self.palabra_actual()
        if actual is None:
            return False, ""

        self.palabra_formada += silaba
        if not actual.palabra.startswith(self.palabra_formada):
            self.palabra_formada = ""
            return False, ""
        if self.palabra_formada == actual.palabra:
            self.indice += 1
            self.palabra_formada = ""
            return True, "completada"
        return True, "parcial"


# ----------------------------------------------------------------------
# Carrera de Letras (Espejo)
# ----------------------------------------------------------------------
@dataclass
class PreguntaEspejo:
    original: str
    muestra: str
    es_igual: bool


class CarreraLetras:
    def __init__(self, preguntas: List[PreguntaEspejo]):
        self.preguntas = preguntas[:]
        random.shuffle(self.preguntas)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.preguntas)

    def pregunta_actual(self) -> Optional[PreguntaEspejo]:
        if self.completado:
            return None
        return self.preguntas[self.indice]

    def verificar(self, respuesta_es_igual: bool) -> bool:
        actual = self.pregunta_actual()
        if actual is None:
            return False
        if respuesta_es_igual == actual.es_igual:
            self.indice += 1
            return True
        self.indice += 1
        return False


# ----------------------------------------------------------------------
# Escribe la Palabra (NUEVO)
# ----------------------------------------------------------------------
@dataclass
class PalabraEscrita:
    imagen: str  # emoji
    palabra: str
    pista: str  # primera letra, por ejemplo


class EscribePalabra:
    def __init__(self, palabras: List[PalabraEscrita]):
        self.palabras = palabras[:]
        random.shuffle(self.palabras)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.palabras)

    def palabra_actual(self) -> Optional[PalabraEscrita]:
        if self.completado:
            return None
        return self.palabras[self.indice]

    def verificar_escritura(self, texto: str) -> bool:
        actual = self.palabra_actual()
        if actual is None:
            return False
        if texto.strip().upper() == actual.palabra.upper():
            self.indice += 1
            return True
        return False


# ----------------------------------------------------------------------
# Rimas Divertidas (Nivel 5)
# ----------------------------------------------------------------------
@dataclass
class PreguntaRima:
    palabra: str
    opciones: List[str]
    correcta: str


class Rimas:
    def __init__(self, preguntas: List[PreguntaRima]):
        self.preguntas = preguntas[:]
        random.shuffle(self.preguntas)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.preguntas)

    def pregunta_actual(self) -> Optional[PreguntaRima]:
        if self.completado:
            return None
        return self.preguntas[self.indice]

    def verificar(self, opcion: str) -> bool:
        actual = self.pregunta_actual()
        if actual and opcion.strip().upper() == actual.correcta.strip().upper():
            self.indice += 1
            return True
        return False


# ----------------------------------------------------------------------
# Ordena las Letras (Nivel 6)
# ----------------------------------------------------------------------
@dataclass
class PalabraDesordenada:
    imagen: str  # emoji
    palabra: str
    letras: List[str]  # desordenadas


class OrdenaLetras:
    def __init__(self, palabras: List[PalabraDesordenada]):
        self.palabras = palabras[:]
        random.shuffle(self.palabras)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.palabras)

    def palabra_actual(self) -> Optional[PalabraDesordenada]:
        if self.completado:
            return None
        return self.palabras[self.indice]

    def verificar(self, respuesta: str) -> bool:
        actual = self.palabra_actual()
        if actual is None:
            return False
        if respuesta.upper() == actual.palabra.upper():
            self.indice += 1
            return True
        return False


# ----------------------------------------------------------------------
# Lee y Encuentra (Nivel 7)
# ----------------------------------------------------------------------
@dataclass
class PreguntaLectura:
    frase: str
    opciones: List[str]
    correcta: str


class LeeEncuentra:
    def __init__(self, preguntas: List[PreguntaLectura]):
        self.preguntas = preguntas[:]
        random.shuffle(self.preguntas)
        self.indice = 0

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.preguntas)

    def pregunta_actual(self) -> Optional[PreguntaLectura]:
        if self.completado:
            return None
        return self.preguntas[self.indice]

    def verificar(self, opcion: str) -> bool:
        actual = self.pregunta_actual()
        if actual and opcion == actual.correcta:
            self.indice += 1
            return True
        return False


# ----------------------------------------------------------------------
# Sopa de Letras (Nivel 8)
# ----------------------------------------------------------------------
@dataclass
class Sopa:
    palabra: str
    tablero: List[List[str]]
    posicion: List[tuple]


class SopaLetras:
    def __init__(self, sopas: List[Sopa]):
        self.sopas = sopas[:]
        random.shuffle(self.sopas)
        self.indice = 0
        self.seleccion_actual = []

    @property
    def completado(self) -> bool:
        return self.indice >= len(self.sopas)

    def sopa_actual(self) -> Optional[Sopa]:
        if self.completado:
            return None
        return self.sopas[self.indice]

    def intentar_posicion(self, fila: int, columna: int) -> Tuple[bool, bool]:
        actual = self.sopa_actual()
        if actual is None:
            return False, False

        if (fila, columna) in actual.posicion:
            if (fila, columna) not in self.seleccion_actual:
                self.seleccion_actual.append((fila, columna))

            completa = len(self.seleccion_actual) == len(actual.posicion)
            if completa:
                self.indice += 1
                self.seleccion_actual = []
            return True, completa

        self.seleccion_actual = []
        return False, False
