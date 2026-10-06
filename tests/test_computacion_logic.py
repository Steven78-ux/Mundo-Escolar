from modulos.Computacion.services.logic_utils import (
    ComboManager,
    ResultadoMecanografia,
    VisualFeedbackManager,
)


def test_combo_otorga_hitos_y_bonus_en_diez_aciertos():
    combo = ComboManager()

    for _ in range(4):
        combo.registrar_acierto(10)
    assert combo.registrar_acierto(10) == (12, 5, True)

    for _ in range(4):
        combo.registrar_acierto(10)
    assert combo.registrar_acierto(10) == (114, 10, True)
    assert combo.max_combo == 10


def test_fallo_reinicia_combo_y_limita_puntaje_minimo_a_cero():
    combo = ComboManager()
    combo.registrar_acierto(20)

    assert combo.registrar_fallo(50) == 50
    assert combo.combo == 0
    assert combo.puntos_totales == 0
    assert combo.max_combo == 1


def test_rango_de_recompensa_depende_del_combo():
    combo = ComboManager()
    assert combo.obtener_rango_recompensa() == (255, 255, 255)

    for _ in range(10):
        combo.registrar_acierto(1)
    assert combo.obtener_rango_recompensa() == (255, 215, 0)


def test_feedback_guarda_efecto_sin_necesitar_una_pantalla():
    feedback = VisualFeedbackManager()

    feedback.agregar("¡Bien!", 20, 30, (0, 255, 0), fuente="fuente")

    assert feedback.efectos == [
        {
            "t": "¡Bien!",
            "x": 20,
            "y": 30,
            "c": (0, 255, 0),
            "v": 1.0,
            "f": "fuente",
            "grande": False,
        }
    ]


def test_resultado_mecanografia_calcula_puntaje_wpm_y_nota():
    resultado = ResultadoMecanografia(aciertos=50, errores=2, segundos=60)

    assert resultado.puntaje == 490
    assert resultado.wpm == 10
    assert resultado.nota == 76


def test_resultado_mecanografia_limita_nota_y_maneja_cero_intentos():
    vacio = ResultadoMecanografia(aciertos=0, errores=0, segundos=0)
    perfecto = ResultadoMecanografia(aciertos=100, errores=0, segundos=1)
    con_muchos_errores = ResultadoMecanografia(
        aciertos=0, errores=100, segundos=60
    )

    assert vacio.wpm == 0
    assert vacio.nota == 1
    assert perfecto.nota == 100
    assert con_muchos_errores.nota == 1
