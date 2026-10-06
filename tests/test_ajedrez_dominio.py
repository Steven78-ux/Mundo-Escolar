from modulos.Ajedrez.domain.partida import Partida
from modulos.Ajedrez.domain.pieza import Pieza
from modulos.Ajedrez.domain.tablero_logico import (
    esta_atacada,
    es_movimiento_valido,
    obtener_pieza_en,
)


def test_peon_blanco_avanza_una_o_dos_casillas_desde_origen():
    peon = Pieza("peon", "blanco", 6, 4)

    assert es_movimiento_valido(peon, 5, 4, [peon]) is True
    assert es_movimiento_valido(peon, 4, 4, [peon]) is True


def test_peon_no_puede_saltar_una_pieza_al_avanzar_dos_casillas():
    peon = Pieza("peon", "blanco", 6, 4)
    obstaculo = Pieza("torre", "negro", 5, 4)

    assert es_movimiento_valido(peon, 4, 4, [peon, obstaculo]) is False


def test_alfil_no_puede_saltar_piezas():
    alfil = Pieza("alfil", "blanco", 4, 0)
    bloqueadora = Pieza("peon", "blanco", 3, 1)

    assert es_movimiento_valido(alfil, 2, 2, [alfil, bloqueadora]) is False


def test_caballo_puede_saltar_piezas_intermedias():
    caballo = Pieza("caballo", "blanco", 7, 1)
    bloqueadora = Pieza("peon", "blanco", 6, 1)

    assert es_movimiento_valido(caballo, 5, 2, [caballo, bloqueadora]) is True


def test_detecta_jaque_de_torre_en_columna_abierta():
    rey = Pieza("rey", "blanco", 7, 4)
    torre = Pieza("torre", "negro", 0, 4)

    assert esta_atacada(7, 4, "blanco", [rey, torre]) is True


def test_permite_enroque_corto_con_camino_libre():
    rey = Pieza("rey", "blanco", 7, 4)
    torre = Pieza("torre", "blanco", 7, 7)

    assert es_movimiento_valido(rey, 7, 6, [rey, torre]) is True


def test_rechaza_enroque_si_hay_una_pieza_en_el_camino():
    rey = Pieza("rey", "blanco", 7, 4)
    torre = Pieza("torre", "blanco", 7, 7)
    bloqueadora = Pieza("alfil", "blanco", 7, 5)

    assert es_movimiento_valido(rey, 7, 6, [rey, torre, bloqueadora]) is False


def test_partida_registra_y_deshace_un_avance_de_peon():
    partida = Partida()
    peon = obtener_pieza_en(partida.piezas, 6, 4)

    partida.registrar_movimiento(peon, 4, 4)

    assert (peon.fila, peon.col) == (4, 4)
    assert partida.turno == "negro"
    assert partida.en_passant_target == (5, 4)
    assert len(partida.historial) == 1

    partida.deshacer_movimiento()

    peon_restaurado = obtener_pieza_en(partida.piezas, 6, 4)
    assert peon_restaurado is not None
    assert partida.turno == "blanco"
    assert partida.en_passant_target is None
    assert partida.historial == []
