from modulos.Robotica.robotica_dominio import (
    ComponenteRobot,
    ConstructorRobot,
    JuegoEmparejar,
    JuegoPartesRobot,
    MisionRobot,
    PreguntaParte,
    RobotProgramable,
    Tarjeta,
)


def test_juego_partes_robot_suma_punto_y_completa_al_acertar():
    juego = JuegoPartesRobot(
        [PreguntaParte("robot", "¿Qué detecta?", ["sensor"], "sensor", "Correcto")]
    )

    assert juego.verificar_respuesta("sensor") == (True, "Correcto")
    assert juego.puntaje == 1
    assert juego.completado is True


def test_juego_partes_robot_avanza_sin_punto_al_fallar():
    juego = JuegoPartesRobot(
        [PreguntaParte("robot", "¿Qué detecta?", ["sensor"], "sensor", "Pista")]
    )

    assert juego.verificar_respuesta("motor") == (False, "Pista")
    assert juego.puntaje == 0
    assert juego.completado is True


def test_juego_emparejar_completa_una_pareja_correcta():
    nombre = Tarjeta("sensor", "Sensor", "👁️", "sensor", "percibir")
    funcion = Tarjeta("percibir", "percibir", "🔎", "funcion", "")
    juego = JuegoEmparejar([nombre], [funcion])

    juego.seleccionar_nombre(nombre)
    assert juego.seleccionar_funcion(funcion) is True
    assert nombre.emparejada is True
    assert funcion.emparejada is True
    assert juego.completado is True


def test_juego_emparejar_falla_y_limpia_la_seleccion():
    nombre = Tarjeta("sensor", "Sensor", "👁️", "sensor", "percibir")
    funcion = Tarjeta("motor", "actuar", "⚙️", "funcion", "")
    juego = JuegoEmparejar([nombre], [funcion])
    juego.seleccionar_nombre(nombre)

    assert juego.seleccionar_funcion(funcion) is False
    assert juego.seleccionada_nombre is None
    assert juego.parejas_completadas == 0


def test_robot_programable_rechaza_limites_obstaculos_y_comandos_invalidos():
    robot = RobotProgramable((2, 2), obstaculos=[(0, 1)], meta=(1, 1))

    assert robot.mover("→") == (False, "¡Hay un obstáculo! No puedes pasar.")
    assert robot.mover("←") == (False, "Te saliste del mapa.")
    assert robot.mover("salta")[0] is False
    assert robot.pos == [0, 0]
    assert robot.historial == []


def test_robot_programable_alcanza_meta_y_bloquea_movimientos_posteriores():
    robot = RobotProgramable((2, 2), meta=(1, 1))

    assert robot.mover("↓")[0] is True
    assert robot.mover("→")[0] is True
    assert robot.exito is True
    assert robot.mover("↑")[0] is False


def test_robot_programable_deshacer_reproduce_la_ruta_restante():
    robot = RobotProgramable((3, 3), meta=(2, 2))
    robot.mover("→")
    robot.mover("↓")

    assert robot.deshacer() is True
    assert robot.pos == [0, 1]
    assert robot.historial == ["→"]
    assert robot.exito is False
    assert robot.deshacer() is True
    assert robot.pos == [0, 0]
    assert robot.deshacer() is False


def test_constructor_robot_verifica_mision_con_requisitos_y_componentes_base():
    sensor = ComponenteRobot("sensor", "Sensor", "👁️", "sensor", "percibir")
    actuador = ComponenteRobot("motor", "Motor", "⚙️", "actuador", "mover")
    constructor = ConstructorRobot(
        [sensor, actuador],
        MisionRobot("Explorar", "Explora el mapa", ["sensor"]),
    )

    assert constructor.agregar_componente(sensor) is True
    assert constructor.agregar_componente(actuador) is True
    assert constructor.verificar_mision() == (
        True,
        "¡Perfecto! Tu robot está listo para la misión.",
    )


def test_constructor_robot_rechaza_duplicados_y_exceso_de_componentes():
    componentes = [
        ComponenteRobot(str(i), f"Pieza {i}", "🔧", "extra", "apoyar")
        for i in range(6)
    ]
    constructor = ConstructorRobot(
        componentes,
        MisionRobot("Explorar", "Explora el mapa", []),
    )

    assert constructor.agregar_componente(componentes[0]) is True
    assert constructor.agregar_componente(componentes[0]) is False
    for componente in componentes[1:5]:
        assert constructor.agregar_componente(componente) is True
    assert constructor.agregar_componente(componentes[5]) is False
    assert len(constructor.seleccionados) == 5
    assert constructor.quitar_componente(componentes[0]) is None
    assert componentes[0] not in constructor.seleccionados
