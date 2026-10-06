"""Servicios del módulo services."""

import pygame
from dataclasses import dataclass

class VisualFeedbackManager:
    def __init__(self):
        self.efectos = []

    def agregar(self, texto, x, y, color, fuente, grande=False):
        self.efectos.append(
            {
                "t": texto,
                "x": x,
                "y": y,
                "c": color,
                "v": 1.0,
                "f": fuente,
                "grande": grande,
            }
        )

    def actualizar_y_dibujar(self, pantalla):
        for ef in self.efectos[:]:
            s = ef["f"].render(ef["t"], True, ef["c"]).convert_alpha()
            s.set_alpha(int(255 * ef["v"]))
            pantalla.blit(s, (ef["x"] - s.get_width() // 2, ef["y"]))
            ef["y"] -= 2
            ef["v"] -= 0.03
            if ef["v"] <= 0:
                self.efectos.remove(ef)


class ComboManager:
    def __init__(self):
        self.combo = 0
        self.max_combo = 0
        self.puntos_totales = 0

    def registrar_acierto(self, puntos_base):
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        multiplicador = 1 + (self.combo // 5) * 0.2
        puntos_ganados = int(puntos_base * multiplicador)
        if self.combo > 0 and self.combo % 10 == 0:
            puntos_ganados += 100
        self.puntos_totales += puntos_ganados
        es_hito = self.combo > 0 and self.combo % 5 == 0
        return puntos_ganados, self.combo, es_hito

    def registrar_fallo(self, penalizacion=5):
        self.combo = 0
        self.puntos_totales = max(0, self.puntos_totales - penalizacion)
        return penalizacion

    def obtener_rango_recompensa(self):
        if self.combo < 5:
            return (255, 255, 255)
        if self.combo < 10:
            return (77, 163, 255)
        if self.combo < 20:
            return (255, 215, 0)
        return (255, 69, 0)


@dataclass
class ResultadoMecanografia:
    aciertos: int
    errores: int
    segundos: float

    @property
    def puntaje(self) -> int:
        return (self.aciertos * 10) - (self.errores * 5)

    @property
    def wpm(self) -> float:
        minutos = max(self.segundos / 60.0, 1e-6)
        palabras = self.aciertos / 5.0
        return palabras / minutos

    @property
    def nota(self) -> int:
        total_intentos = self.aciertos + self.errores
        precision = (self.aciertos / total_intentos) if total_intentos > 0 else 0
        meta_ppm = 25.0
        factor_velocidad = min(1.0, self.wpm / meta_ppm)
        puntaje_bruto = (precision * 70) + (factor_velocidad * 30)
        return max(1, min(100, int(puntaje_bruto - (self.errores * 1.5))))