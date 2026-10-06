"""Dominio del módulo domain."""

import random
from .partida import Partida
from ..views.pieza_animada import PiezaAnimada
from .tablero_logico import obtener_pieza_en
from ..views.Flecha import Flecha


# This class `PartidaTutorial` likely inherits from a class named `Partida` and may contain specific
# functionality related to tutorial gameplay.
class PartidaTutorial(Partida):
    def __init__(self, section_id, sub_id, parent_ventana):
        super().__init__(minutos=99, bando_elegido="blanco", contra_ia=False)
        self.parent_ventana = parent_ventana

    def registrar_movimiento(self, p, f_dest, c_dest, uci_ia="", promocion="dama"):
        turno_previo = self.turno
        super().registrar_movimiento(p, f_dest, c_dest, uci_ia, promocion)
        self.turno = turno_previo

    def cargar_escenario(self, sid, subid):
        self.piezas = []
        self.en_passant_target = None
        self.historial = []
        step = self.parent_ventana.level_step
        self.parent_ventana.circulos_tacticos.clear()
        self.parent_ventana.flechas_tacticos.clear()
        self.parent_ventana.reiniciar_contadores()

        if sid == "1":
            self._cargar_movimientos(subid)
        elif sid == "2":
            self._cargar_capturas(subid)
        elif sid == "3":
            self._cargar_especiales(subid, step)
        elif sid == "4":
            self._cargar_jaque(subid, step)
        elif sid == "5":
            self._cargar_reglas(subid, step)

    def _cargar_movimientos(self, subid):
        if subid == "peon":
            self.parent_ventana.task_goal = 4
            self.piezas.append(PiezaAnimada("peon", "blanco", 6, 4))
        else:
            self.parent_ventana.task_goal = 5
            pos = {
                "caballo": (7, 1),
                "alfil": (7, 2),
                "torre": (7, 0),
                "dama": (7, 3),
                "rey": (7, 4),
            }
            f, c = pos.get(subid, (4, 4))
            self.piezas.append(PiezaAnimada(subid, "blanco", f, c))

    def _cargar_capturas(self, subid):
        self.parent_ventana.task_goal = 3
        if subid == "peon":
            # Posiciones optimizadas (a2, d2, g2) para evitar ambigüedad en las capturas
            # Cada peón tiene ahora un único objetivo directo.
            for c in [0, 3, 6]:
                self.piezas.append(PiezaAnimada("peon", "blanco", 6, c))
            self.piezas.extend(
                [
                    PiezaAnimada("torre", "negro", 5, 1),   # b3 (Objetivo de a2)
                    PiezaAnimada("caballo", "negro", 5, 4), # e3 (Objetivo de d2)
                    PiezaAnimada("alfil", "negro", 5, 7),   # h3 (Objetivo de g2)
                ]
            )
            # Añadimos flechas tácticas como pistas visuales para el niño
            tam = self.parent_ventana.vista.tam_cuadro
            self.parent_ventana.flechas_tacticos.extend([
                Flecha((6, 0), (5, 1), (0, 255, 0), tam_cuadro=tam),
                Flecha((6, 3), (5, 4), (0, 255, 0), tam_cuadro=tam),
                Flecha((6, 6), (5, 7), (0, 255, 0), tam_cuadro=tam)
            ])
        else:
            self.piezas.append(PiezaAnimada(subid, "blanco", 7, 3))
            if subid == "alfil":
                white_squares = [
                    (f, c)
                    for f in range(1, 6)
                    for c in range(8)
                    if (f + c) % 2 == 0
                ]
                random.shuffle(white_squares)
                for rf, rc in white_squares[:3]:
                    self.piezas.append(PiezaAnimada("peon", "negro", rf, rc))
            else:
                for _ in range(3):
                    rf, rc = random.randint(1, 5), random.randint(0, 7)
                    self.piezas.append(PiezaAnimada("peon", "negro", rf, rc))

    def _cargar_especiales(self, subid, step):
        if subid == "enroque":
            self.parent_ventana.task_goal = 1
            # Peones defensivos para realismo
            if step in [0, 2, 3]:  # Escenario Corto
                for c in [5, 6, 7]:
                    self.piezas.append(PiezaAnimada("peon", "blanco", 6, c))
            elif step in [1, 4, 5]:  # Escenario Largo
                for c in [0, 1, 2]:
                    self.piezas.append(PiezaAnimada("peon", "blanco", 6, c))

            if step == 0:  # Enroque Corto
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 7),
                    ]
                )
            elif step == 1:  # Enroque Largo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 0),
                    ]
                )
            elif step == 2:  # Bloquear Corto
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 7),
                        PiezaAnimada("alfil", "negro", 2, 0),
                        PiezaAnimada("caballo", "blanco", 5, 2),
                    ]
                )
            elif step == 3:  # Capturar Corto
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 7),
                        PiezaAnimada("alfil", "negro", 2, 0),
                        PiezaAnimada("dama", "blanco", 1, 0),
                    ]
                )
            elif step == 4:  # Bloquear Largo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 0),
                        PiezaAnimada("alfil", "negro", 3, 7),
                        PiezaAnimada("alfil", "blanco", 0, 0),
                    ]
                )
            elif step == 5:  # Capturar Largo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "blanco", 7, 0),
                        PiezaAnimada("alfil", "negro", 3, 7),
                        PiezaAnimada("caballo", "blanco", 2, 6),
                    ]
                )
        elif subid == "promocion":
            self.parent_ventana.task_goal = 4
            for c in [1, 3, 5, 7]:
                self.piezas.append(PiezaAnimada("peon", "blanco", 1, c))
        elif subid == "paso":
            self.parent_ventana.task_goal = 3
            for i in range(3):
                p = PiezaAnimada("peon", "blanco", 4, [1, 3, 5][i])
                p.ha_movido = True
                self.piezas.append(p)
                self.piezas.append(PiezaAnimada("peon", "negro", 1, [0, 2, 6][i]))

    def _cargar_jaque(self, subid, step):
        if subid == "jaque":
            if step == 0:  # Escapar de Torre
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "negro", 0, 4),
                    ]
                )
            elif step == 1:  # Escapar de Alfil
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 7),
                        PiezaAnimada("alfil", "negro", 0, 0),
                    ]
                )
            elif step == 2:  # Escapar de Dama
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 4, 4),
                        PiezaAnimada("dama", "negro", 4, 0),
                    ]
                )
            elif step == 3:  # Bloquear Torre
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "negro", 0, 4),
                        PiezaAnimada("alfil", "blanco", 6, 2),
                    ]
                )
            elif step == 4:  # Bloquear Dama
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 7),
                        PiezaAnimada("dama", "negro", 3, 3),
                        PiezaAnimada("alfil", "blanco", 5, 7),
                    ]
                )
            elif step == 5:  # Bloquear con Caballo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 0, 0),
                        PiezaAnimada("torre", "negro", 0, 7),
                        PiezaAnimada("caballo", "blanco", 2, 1),
                    ]
                )
            elif step == 6:  # Capturar Caballo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 6),
                        PiezaAnimada("caballo", "negro", 5, 5),
                        PiezaAnimada("dama", "blanco", 7, 3),
                    ]
                )
            elif step == 7:  # Capturar Torre con Rey
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 7, 4),
                        PiezaAnimada("torre", "negro", 6, 4),
                    ]
                )
            elif step == 8:  # Capturar Alfil
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "blanco", 0, 7),
                        PiezaAnimada("alfil", "negro", 5, 2),
                        PiezaAnimada("alfil", "blanco", 7, 4),
                    ]
                )
        else:  # Jaque Mate
            if step == 0:  # Pasillo
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "negro", 0, 4),
                        PiezaAnimada("peon", "negro", 1, 3),
                        PiezaAnimada("peon", "negro", 1, 4),
                        PiezaAnimada("peon", "negro", 1, 5),
                        PiezaAnimada("torre", "blanco", 5, 0),
                    ]
                )
            elif step == 1:  # Pastor Style
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "negro", 0, 4),
                        PiezaAnimada("peon", "negro", 1, 5),
                        PiezaAnimada("dama", "blanco", 2, 6),
                        PiezaAnimada("alfil", "blanco", 4, 2),
                    ]
                )
            elif step == 2:  # Dos torres
                self.piezas.extend(
                    [
                        PiezaAnimada("rey", "negro", 0, 0),
                        PiezaAnimada("torre", "blanco", 1, 7),
                        PiezaAnimada("torre", "blanco", 5, 1),
                    ]
                )

    def _cargar_reglas(self, subid, step):
        if subid == "ahogado":
            self.piezas.extend(
                [
                    PiezaAnimada("rey", "blanco", 7, 7),
                    PiezaAnimada("torre", "blanco", 7, 5),
                    PiezaAnimada("alfil", "blanco", 7, 4),
                    PiezaAnimada("peon", "blanco", 6, 3),
                    PiezaAnimada("peon", "blanco", 6, 5),
                    PiezaAnimada("peon", "blanco", 6, 7),
                    PiezaAnimada("peon", "negro", 5, 3),
                    PiezaAnimada("peon", "negro", 5, 5),
                    PiezaAnimada("peon", "negro", 5, 7),
                    PiezaAnimada("dama", "negro", 3, 6),
                    PiezaAnimada("rey", "negro", 0, 0),
                ]
            )
        elif subid == "tablas":
            self.piezas.extend(
                [
                    PiezaAnimada("rey", "blanco", 5, 4),
                    PiezaAnimada("rey", "negro", 0, 2),
                ]
            )
        elif subid == "clavada":
            self.parent_ventana.task_goal = 1
            self._cargar_escenario_clavada(step)
        elif subid == "insuficiencia_material":
            self.piezas.extend(
                [
                    PiezaAnimada("rey", "blanco", 6, 3),
                    PiezaAnimada("caballo", "blanco", 5, 5),
                    PiezaAnimada("rey", "negro", 1, 4),
                ]
            )

    def _cargar_escenario_clavada(self, _):
        # Cargar todas las piezas en posición inicial
        self._colocar_piezas_iniciales()

        # Ajustes Blancas
        for f, c in [(6, 3), (6, 4), (7, 1), (7, 6)]:
            pieza = obtener_pieza_en(self.piezas, f, c)
            if pieza:
                self.piezas.remove(pieza)

        self.piezas.extend(
            [
                PiezaAnimada("peon", "blanco", 4, 3),  # d4
                PiezaAnimada("peon", "blanco", 5, 4),  # e3
                PiezaAnimada("caballo", "blanco", 5, 5),  # f3
                PiezaAnimada("caballo", "blanco", 5, 2),  # c3
            ]
        )

        # Ajustes Negras
        for f, c in [(1, 3), (1, 4), (0, 6), (0, 5)]:
            pieza = obtener_pieza_en(self.piezas, f, c)
            if pieza:
                self.piezas.remove(pieza)

        self.piezas.extend(
            [
                PiezaAnimada("peon", "negro", 3, 3),  # d5
                PiezaAnimada("peon", "negro", 2, 4),  # e6
                PiezaAnimada("caballo", "negro", 2, 5),  # f6
                PiezaAnimada("alfil", "negro", 4, 1),  # b4
            ]
        )