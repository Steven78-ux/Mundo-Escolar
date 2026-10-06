from modulos.Lenguaje.dominio.juegos import (
    CarreraLetras,
    ConstructorPalabras,
    DetectiveSonidos,
    EscribePalabra,
    LeeEncuentra,
    OrdenaLetras,
    PalabraConstruible,
    PalabraDesordenada,
    PalabraEscrita,
    PreguntaEspejo,
    PreguntaLectura,
    PreguntaRima,
    PreguntaSonido,
    Rimas,
    Sopa,
    SopaLetras,
)


def test_detective_sonidos_no_avanza_con_respuesta_incorrecta():
    juego = DetectiveSonidos([PreguntaSonido("a", "a", ["sol", "ala"], "ala")])

    assert juego.verificar("sol") is False
    assert juego.indice == 0
    assert juego.completado is False


def test_detective_sonidos_completa_con_respuesta_correcta():
    juego = DetectiveSonidos([PreguntaSonido("a", "a", ["sol", "ala"], "ala")])

    assert juego.verificar("ala") is True
    assert juego.completado is True
    assert juego.pregunta_actual() is None
    assert juego.verificar("ala") is False


def test_constructor_palabras_reinicia_una_silaba_incorrecta():
    palabra = PalabraConstruible("🏠", "casa", ["ca", "sa"])
    juego = ConstructorPalabras([palabra], [])

    assert juego.agregar_silaba("pa") == (False, "")
    assert juego.palabra_formada == ""
    assert juego.agregar_silaba("ca") == (True, "parcial")


def test_constructor_palabras_avanza_al_completar_la_palabra():
    juego = ConstructorPalabras(
        [PalabraConstruible("🌙", "luna", ["lu", "na"])], []
    )

    assert juego.agregar_silaba("lu") == (True, "parcial")
    assert juego.agregar_silaba("na") == (True, "completada")
    assert juego.completado is True
    assert juego.palabra_actual() is None


def test_sopa_letras_completa_al_seleccionar_todas_las_posiciones():
    sopa = Sopa("sol", [["s", "o", "l"]], [(0, 0), (0, 1), (0, 2)])
    juego = SopaLetras([sopa])

    assert juego.intentar_posicion(0, 0) == (True, False)
    assert juego.intentar_posicion(0, 1) == (True, False)
    assert juego.intentar_posicion(0, 2) == (True, True)
    assert juego.completado is True


def test_sopa_letras_borra_seleccion_tras_posicion_incorrecta():
    sopa = Sopa("sol", [["s", "o", "l"]], [(0, 0), (0, 1), (0, 2)])
    juego = SopaLetras([sopa])

    assert juego.intentar_posicion(0, 0) == (True, False)
    assert juego.intentar_posicion(1, 0) == (False, False)
    assert juego.seleccion_actual == []


def test_carrera_letras_avanza_con_respuesta_correcta_y_rechaza_tras_finalizar():
    juego = CarreraLetras([PreguntaEspejo("casa", "casa", True)])

    assert juego.verificar(True) is True
    assert juego.completado is True
    assert juego.verificar(True) is False


def test_carrera_letras_consume_pregunta_con_respuesta_incorrecta():
    juego = CarreraLetras([PreguntaEspejo("casa", "caza", False)])

    assert juego.verificar(True) is False
    assert juego.completado is True


def test_escribe_palabra_acepta_mayusculas_y_espacios():
    juego = EscribePalabra([PalabraEscrita("🍎", "manzana", "m")])

    assert juego.verificar_escritura(" MANZANA ") is True
    assert juego.completado is True


def test_escribe_palabra_rechaza_respuesta_incorrecta_y_lista_vacia():
    juego = EscribePalabra([PalabraEscrita("🍎", "manzana", "m")])
    vacio = EscribePalabra([])

    assert juego.verificar_escritura("pera") is False
    assert juego.indice == 0
    assert vacio.verificar_escritura("manzana") is False
    assert vacio.palabra_actual() is None


def test_rimas_normaliza_espacios_y_mayusculas():
    juego = Rimas([PreguntaRima("canción", ["balón"], " BALÓN ")])

    assert juego.verificar("balón") is True
    assert juego.completado is True


def test_rimas_no_avanza_con_respuesta_incorrecta_ni_sin_preguntas():
    juego = Rimas([PreguntaRima("canción", ["balón"], "balón")])
    vacio = Rimas([])

    assert juego.verificar("melón") is False
    assert juego.indice == 0
    assert vacio.verificar("balón") is False


def test_ordena_letras_acepta_respuesta_sin_distinguir_mayusculas():
    juego = OrdenaLetras([PalabraDesordenada("🐈", "gato", ["t", "a", "g", "o"])])

    assert juego.verificar("GATO") is True
    assert juego.completado is True


def test_ordena_letras_rechaza_respuesta_y_cubre_lista_vacia():
    juego = OrdenaLetras([PalabraDesordenada("🐈", "gato", ["t", "a", "g", "o"])])
    vacio = OrdenaLetras([])

    assert juego.verificar("perro") is False
    assert juego.indice == 0
    assert vacio.verificar("gato") is False
    assert vacio.palabra_actual() is None


def test_lee_encuentra_avanza_solo_con_opcion_exacta():
    juego = LeeEncuentra([PreguntaLectura("El sol brilla", ["sol"], "sol")])

    assert juego.verificar("sol") is True
    assert juego.completado is True


def test_lee_encuentra_no_avanza_con_respuesta_incorrecta_o_sin_preguntas():
    juego = LeeEncuentra([PreguntaLectura("El sol brilla", ["sol"], "sol")])
    vacio = LeeEncuentra([])

    assert juego.verificar("luna") is False
    assert juego.indice == 0
    assert vacio.verificar("sol") is False
    assert vacio.pregunta_actual() is None
