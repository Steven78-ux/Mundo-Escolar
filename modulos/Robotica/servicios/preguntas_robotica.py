"""Datos educativos para las misiones de Robótica."""
import random
from ..robotica_dominio import PreguntaParte, Tarjeta, ComponenteRobot, MisionRobot


def obtener_preguntas_parte_robot():
    return [
        # =================================================================
        # BLOQUE 1: LAS 12 PREGUNTAS ANTERIORES (CALIBRADAS)
        # =================================================================
        PreguntaParte(
            imagen="👀",
            pregunta="¿Qué usa el robot para 'ver' si hay una pared enfrente y no chocarse?",
            opciones=["Sensor ultrasónico (ojitos mágicos)", "Motor", "Rueda", "Batería"],
            respuesta_correcta="Sensor ultrasónico (ojitos mágicos)",
            explicacion="¡Es como el radar de los murciélagos! Lanza un sonido invisible para saber qué hay cerca.",
        ),
        PreguntaParte(
            imagen="💪",
            pregunta="¿Cuál de estas partes funciona como los 'músculos' del robot para que pueda moverse?",
            opciones=["Sensor de luz", "Motor", "Cámara", "Micrófono"],
            respuesta_correcta="Motor",
            explicacion="Los motores hacen girar las ruedas y mover los brazos. ¡Sin ellos, el robot sería una estatua!",
        ),
        PreguntaParte(
            imagen="👂",
            pregunta="Si quieres que tu robot responda cuando le aplaudes, ¿qué necesita para escucharte?",
            opciones=["Un altavoz", "Un micrófono", "Una luz LED", "Una batería"],
            respuesta_correcta="Un micrófono",
            explicacion="El micrófono funciona exactamente como sus oídos: atrapa los sonidos del aire.",
        ),
        PreguntaParte(
            imagen="🧠",
            pregunta="¿Cuál es el verdadero 'cerebro' del robot, donde guarda sus ideas y órdenes?",
            opciones=["El cerebro electrónico (Controlador)", "La batería", "La rueda", "El cable"],
            respuesta_correcta="El cerebro electrónico (Controlador)",
            explicacion="Es un chip pequeño donde vive el código. Él piensa y le dice a las demás partes qué hacer.",
        ),
        PreguntaParte(
            imagen="🔋",
            pregunta="El robot tiene hambre y necesita energía para funcionar, ¿cuál es su comida?",
            opciones=["Un plato de galletas", "La batería", "Una rueda de repuesto", "Un tornillo"],
            respuesta_correcta="La batería",
            explicacion="La batería guarda la electricidad. ¡Es la que le da la fuerza para encenderse y jugar!",
        ),
        PreguntaParte(
            imagen="🚨",
            pregunta="¿Qué parte usa el robot para brillar en la oscuridad o avisar con colores que está feliz?",
            opciones=["Una rueda", "Luces LED", "Un micrófono", "Un motor"],
            respuesta_correcta="Luces LED",
            explicacion="Las luces LED son como pequeños bombillos de colores que usa para comunicarse o iluminar.",
        ),
        PreguntaParte(
            imagen="👣",
            pregunta="Si el robot quiere avanzar por el suelo de tu habitación, ¿qué necesita en sus pies?",
            opciones=["Ruedas u orugas", "Una pantalla", "Un cable de computadora", "Un botón"],
            respuesta_correcta="Ruedas u orugas",
            explicacion="Las ruedas le permiten rodar por todos lados, ¡así como tu bicicleta o tu carrito de juguete!",
        ),
        PreguntaParte(
            imagen="📟",
            pregunta="¿Qué parte usa un robot para mostrarte dibujitos, caras felices o números?",
            opciones=["La batería", "La pantalla", "El motor", "El sensor de sonido"],
            respuesta_correcta="La pantalla",
            explicacion="En la pantalla puedes ver lo que el robot está pensando o sintiendo, ¡como un emoticón!",
        ),
        PreguntaParte(
            imagen="🗣️",
            pregunta="Tu robot quiere saludarte y decirte '¡Hola, amigo!'. ¿A través de qué parte sale su voz?",
            opciones=["Del micrófono", "Del altavoz (parlante)", "De la rueda", "De la batería"],
            respuesta_correcta="Del altavoz (parlante)",
            explicacion="El altavoz funciona como la boca del robot. Convierte la electricidad en sonidos y palabras.",
        ),
        PreguntaParte(
            imagen="☀️",
            pregunta="¿Qué tipo de sensor usa el robot para saber si es de día, de noche o si encendiste la luz?",
            opciones=["Sensor de luz", "Sensor de saltos", "Rueda", "Batería"],
            respuesta_correcta="Sensor de luz",
            explicacion="Este sensor siente la claridad de la habitación. ¡Sabe perfectamente cuándo apagas la luz!",
        ),
        PreguntaParte(
            imagen="🤝",
            pregunta="Si un robot quiere recoger un juguete del suelo, ¿qué necesita usar?",
            opciones=["Una pinza o garra", "Una luz LED", "Un micrófono", "Una pantalla"],
            respuesta_correcta="Una pinza o garra",
            explicacion="Las garras mecánicas hacen el trabajo de nuestras manos: se abren y cierran para agarrar cosas.",
        ),
        PreguntaParte(
            imagen="🔌",
            pregunta="¿Qué usamos para conectar el robot a la computadora y pasarle las instrucciones del juego?",
            opciones=["Un cable de datos (USB)", "Un trozo de cuerda", "Una batería", "Un motor"],
            respuesta_correcta="Un cable de datos (USB)",
            explicacion="El cable es como un puente por donde viaja la información desde la computadora hasta su cerebro.",
        ),

        # =================================================================
        # BLOQUE 2: NUEVAS PREGUNTAS (Para llegar a 20 y ampliar conceptos)
        # =================================================================
        PreguntaParte(
            imagen="💥",
            pregunta="¿Qué sensor usa el robot para saber si chocó contra algo, funcionando como su sentido del tacto?",
            opciones=["Sensor de choque (Botón pulsador)", "Sensor de mentiras", "Pantalla", "Altavoz"],
            respuesta_correcta="Sensor de choque (Botón pulsador)",
            explicacion="Es como un botón. Cuando el robot choca, el botón se hunde y el cerebro se entera del golpe.",
        ),
        PreguntaParte(
            imagen="🎨",
            pregunta="Si queremos que el robot siga una línea negra dibujada en el suelo, ¿qué sensor debe usar?",
            opciones=["Sensor de color o líneas", "Sensor de temperatura", "Un motor", "Una antena"],
            respuesta_correcta="Sensor de color o líneas",
            explicacion="Este sensor mira hacia el suelo y distingue los colores. ¡Le avisa al robot si se está saliendo del camino!",
        ),
        PreguntaParte(
            imagen="🐢",
            pregunta="¿Qué es el 'esqueleto' o cuerpo de plástico y metal donde se atornillan todas las piezas del robot?",
            opciones=["El Chasis (o base)", "La batería", "El código", "Las gomas"],
            respuesta_correcta="El Chasis (o base)",
            explicacion="El chasis es el cuerpo del robot. Sostiene los motores, las ruedas y el cerebro en su sitio.",
        ),
        PreguntaParte(
            imagen="🧠",
            pregunta="¿Cómo se le llama a la lista de pasos ordenados que le damos al robot para que sepa qué hacer?",
            opciones=["Programa o Código", "Historieta", "Control remoto", "Batería"],
            respuesta_correcta="Programa o Código",
            explicacion="Los robots no saben hacer nada solos. El programa es la lista de tareas que nosotros les escribimos.",
        ),
        PreguntaParte(
            imagen="🧱",
            pregunta="¿De qué se encargan los cables de colores que van conectados dentro del robot?",
            opciones=["Llevar la electricidad y los mensajes", "Adornar el robot", "Amarrar las ruedas", "Apagar los motores"],
            respuesta_correcta="Llevar la electricidad y los mensajes",
            explicacion="Los cables son como las venas y los nervios de nuestro cuerpo: llevan energía e información a cada pieza.",
        ),
        PreguntaParte(
            imagen="🛑",
            pregunta="¿Qué pasa si le quitamos la batería a un robot mientras está caminando?",
            opciones=["Se apaga de inmediato", "Camina más rápido", "Se pone a cantar", "Guarda sus juguetes"],
            respuesta_correcta="Se apaga de inmediato",
            explicacion="Sin batería no hay electricidad. Es como apagar la luz de la habitación: todo se detiene.",
        ),
        PreguntaParte(
            imagen="🛠️",
            pregunta="¿Quién es la persona que inventa, diseña y construye a los robots?",
            opciones=["Un ingeniero o ingeniera en robótica", "Un astronauta", "Un doctor", "Un mago"],
            respuesta_correcta="Un ingeniero o ingeniera en robótica",
            explicacion="¡Así es! Usando la ciencia, la imaginación y la tecnología, crean robots para ayudarnos en el mundo.",
        ),
        PreguntaParte(
            imagen="🔄",
            pregunta="Si queremos que el robot dé una vuelta completa sobre su propio eje, ¿qué comando debemos programar?",
            opciones=["Girar", "Avanzar", "Detenerse", "Encender luces"],
            respuesta_correcta="Girar",
            explicacion="El comando 'Girar' hace que un motor vaya hacia adelante y el otro hacia atrás, ¡haciéndolo dar vueltas!",
        ),
    ]

def obtener_tarjetas_emparejar():
    nombres = [
        # --- BLOQUE ORIGINAL (1 a 6) ---
        Tarjeta("n1", "Sensor de luz", "☀️", "sensor", "Siente la claridad o la oscuridad"),
        Tarjeta("n2", "Sensor de distancia", "📏", "sensor", "Mide qué tan cerca hay un obstáculo"),
        Tarjeta("n3", "Motor mecánico", "⚙️", "actuador", "Hace girar las ruedas para avanzar"),
        Tarjeta("n4", "Brazo robótico", "🦾", "actuador", "Se estira para agarrar y mover objetos"),
        Tarjeta("n5", "Micrófono", "🎤", "sensor", "Escucha los sonidos del ambiente"),
        Tarjeta("n6", "Altavoz", "🔊", "actuador", "Habla o reproduce sonidos y música"),
        
        # --- SEGUNDO BLOQUE (7 a 12) ---
        Tarjeta("n7", "Cerebro (Controlador)", "🧠", "cerebro", "Guarda el código y da las órdenes"),
        Tarjeta("n8", "Batería", "🔋", "energia", "Le da energía eléctrica al robot"),
        Tarjeta("n9", "Luces LED", "🚨", "actuador", "Brillan con colores divertidos"),
        Tarjeta("n10", "Sensor de choque", "💥", "sensor", "Avisa al cerebro si el robot se golpeó"),
        Tarjeta("n11", "Pantalla", "📟", "actuador", "Muestra dibujitos y caras felices"),
        Tarjeta("n12", "Cable de datos", "🔌", "conexion", "Conecta el robot a la computadora"),

        # --- NUEVO BLOQUE DE EXPANSIÓN (13 a 24) ---
        Tarjeta("n13", "Sensor de temperatura", "🌡️", "sensor", "Siente si hace frío o calor en la habitación"),
        Tarjeta("n14", "Panel solar", "🛰️", "energia", "Atrapa los rayos del sol para cargarse"),
        Tarjeta("n15", "Servomotor", "🤖", "actuador", "Mueve piezas con mucha precisión (como un cuello)"),
        Tarjeta("n16", "Sensor de equilibrio", "🤸", "sensor", "Avisa al robot si se está cayendo o inclinando"),
        Tarjeta("n17", "Hélices", "🛸", "actuador", "Giran súper rápido para que un robot dron vuele"),
        Tarjeta("n18", "Interruptor", "🔘", "control", "Un botón para encender o apagar por completo el robot"),
        Tarjeta("n19", "Cámara de video", "📷", "sensor", "Toma fotos y reconoce los colores de los juguetes"),
        Tarjeta("n20", "Sensor de humedad", "💧", "sensor", "Siente si el suelo o la tierra están mojados"),
        Tarjeta("n21", "Imán electrónico", "🧲", "actuador", "Se activa para pegar y cargar objetos de metal"),
        Tarjeta("n22", "Bucle (Repetir)", "🔄", "logica", "Una orden que hace que el robot repita una acción"),
        Tarjeta("n23", "Estructura (Chasis)", "🐢", "fisico", "El esqueleto de metal que sostiene todas las piezas"),
        Tarjeta("n24", "Antena Wi-Fi", "📡", "conexion", "Le permite hablar con otros robots a la distancia"),
    ]
    
    funciones = [
        # --- BLOQUE ORIGINAL (1 a 6) ---
        Tarjeta("f1", "Siente la claridad o la oscuridad", "🌑", "funcion", "Sensor de luz"),
        Tarjeta("f2", "Mide qué tan cerca hay un obstáculo", "🚧", "funcion", "Sensor de distancia"),
        Tarjeta("f3", "Hace girar las ruedas para avanzar", "🏃", "funcion", "Motor mecánico"),
        Tarjeta("f4", "Se estira para agarrar y mover objetos", "✋", "funcion", "Brazo robótico"),
        Tarjeta("f5", "Escucha los sonidos del ambiente", "👂", "funcion", "Micrófono"),
        Tarjeta("f6", "Habla o reproduce sonidos y música", "📢", "funcion", "Altavoz"),
        
        # --- SEGUNDO BLOQUE (7 a 12) ---
        Tarjeta("f7", "Guarda el código y da las órdenes", "💡", "funcion", "Cerebro (Controlador)"),
        Tarjeta("f8", "Le da energía eléctrica al robot", "⚡", "funcion", "Batería"),
        Tarjeta("f9", "Brillan con colores divertidos", "✨", "funcion", "Luces LED"),
        Tarjeta("f10", "Avisa al cerebro si el robot se golpeó", "HN", "funcion", "Sensor de choque"), # Nota: Usabas "🤕", se mantiene similar pedagógicamente
        Tarjeta("f11", "Muestra dibujitos y caras felices", "😊", "funcion", "Pantalla"),
        Tarjeta("f12", "Conecta el robot a la computadora", "💻", "funcion", "Cable de datos"),

        # --- NUEVO BLOQUE DE EXPANSIÓN (13 a 24) ---
        Tarjeta("f13", "Siente si hace frío o calor en la habitación", "❄️", "funcion", "Sensor de temperatura"),
        Tarjeta("f14", "Atrapa los rayos del sol para cargarse", "☀️", "funcion", "Panel solar"),
        Tarjeta("f15", "Mueve piezas con mucha precisión (como un cuello)", "🎯", "funcion", "Servomotor"),
        Tarjeta("f16", "Avisa al robot si se está cayendo o inclinando", "🛹", "funcion", "Sensor de equilibrio"),
        Tarjeta("f17", "Giran súper rápido para que un robot dron vuele", "🪶", "funcion", "Hélices"),
        Tarjeta("f18", "Un botón para encender o apagar por completo el robot", "🛑", "funcion", "Interruptor"),
        Tarjeta("f19", "Toma fotos y reconoce los colores de los juguetes", "🖼️", "funcion", "Cámara de video"),
        Tarjeta("f20", "Siente si el suelo o la tierra están mojados", "🌱", "funcion", "Sensor de humedad"),
        Tarjeta("f21", "Se activa para pegar y cargar objetos de metal", "🏗️", "funcion", "Imán electrónico"),
        Tarjeta("f22", "Una orden que hace que el robot repita una acción", "🔁", "funcion", "Bucle (Repetir)"),
        Tarjeta("f23", "El esqueleto de metal que sostiene todas las piezas", "🦴", "funcion", "Estructura (Chasis)"),
        Tarjeta("f24", "Le permite hablar con otros robots a la distancia", "💬", "funcion", "Antena Wi-Fi"),
    ]
    
    return nombres, funciones


def obtener_componentes_construccion():
    return [
        ComponenteRobot("c1", "Sensor de luz", "☀️", "sensor", "Detecta si hay luz"),
        ComponenteRobot("c2", "Sensor de distancia", "📏", "sensor", "Evita chocar"),
        ComponenteRobot("c3", "Ruedas con motor", "🛞", "actuador", "Para moverse"),
        ComponenteRobot("c4", "Brazo robótico", "🦾", "actuador", "Para agarrar cosas"),
        ComponenteRobot("c5", "Altavoz", "🔊", "actuador", "Para hablar o sonar"),
        ComponenteRobot("c6", "Batería", "🔋", "estructura", "Da energía a todo"),
        ComponenteRobot("c7", "Controlador", "🧠", "estructura", "El cerebro del robot"),
    ]


def obtener_mision_ejemplo():
    return MisionRobot(
        nombre="Robot explorador",
        descripcion=(
            "Tu robot debe explorar una cueva oscura. "
            "Necesita ver en la oscuridad, evitar obstáculos y moverse."
        ),
        requisitos=["sensor", "actuador", "estructura"],
    )


def _existe_camino(rows, cols, start, meta, obstaculos):
    """Verifica si existe un camino desde el inicio a la meta usando BFS."""
    queue = [start]
    visitados = {start}
    while queue:
        curr_r, curr_c = queue.pop(0)
        if (curr_r, curr_c) == meta:
            return True
        # Movimientos posibles: Arriba, Abajo, Izquierda, Derecha
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                (nr, nc) not in obstaculos and (nr, nc) not in visitados):
                visitados.add((nr, nc))
                queue.append((nr, nc))
    return False


def obtener_obstaculos_por_dificultad(dificultad: str, personalizado=None):
    """Genera obstáculos dinámicamente asegurando que siempre haya un camino a la meta."""
    if personalizado:
        rows, cols, num_obstaculos = personalizado
    elif dificultad == "basico":
        rows, cols, num_obstaculos = 6, 6, 6
    elif dificultad == "intermedio":
        rows, cols, num_obstaculos = 10, 10, 25
    elif dificultad == "experto":
        rows, cols, num_obstaculos = 15, 15, 60
    else:
        rows, cols, num_obstaculos = 6, 6, 6

    start = (0, 0)
    meta = (rows - 1, cols - 1)
    obstaculos = set()
    
    # Intentar colocar obstáculos aleatorios validando el camino
    intentos_maximos = num_obstaculos * 15
    intentos = 0
    
    while len(obstaculos) < num_obstaculos and intentos < intentos_maximos:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        pos = (r, c)
        
        # No poner obstáculos en inicio, meta o si ya existe uno ahí
        if pos != start and pos != meta and pos not in obstaculos:
            obstaculos.add(pos)
            # Verificar si el camino sigue siendo posible tras añadir este muro
            if not _existe_camino(rows, cols, start, meta, obstaculos):
                obstaculos.remove(pos)
        intentos += 1
        
    return list(obstaculos)

def obtener_datos_curiosos_robotica():
    """Lista de 30 datos curiosos sobre robótica para el banner del menú."""
    return [
        "🤖 ¿Sabías que? El primer robot de la historia fue una paloma mecánica que volaba con vapor hace más de 2000 años.",
        "🚀 Tip de ingeniería: Los sensores ultrasónicos usan eco, exactamente igual que los delfines en el océano.",
        "🛰️ Dato curioso: El robot Curiosity en Marte tiene el tamaño de un coche pequeño y su propia cuenta de Twitter.",
        "🤖 ¿Sabías que? La palabra 'robot' viene de una obra de teatro checa y significa 'trabajo forzado'.",
        "⚡ Tip de energía: Las baterías de litio son las mismas que usa tu tablet, ¡pero mucho más grandes!",
        "🌊 Robótica marina: Existen robots con forma de pez que ayudan a limpiar la contaminación de los océanos.",
        "🧠 Inteligencia Artificial: Los robots pueden aprender a reconocer caras usando miles de fotos como ejemplos.",
        "🕷️ Bio-robótica: Algunos ingenieros crean robots que caminan por las paredes inspirados en las patas de las arañas.",
        "🏥 Robots médicos: Hay robots cirujanos que pueden coser una uva sin romperle la piel. ¡Qué precisión!",
        "🐜 Micro-robots: Se están diseñando robots tan pequeños como hormigas para explorar lugares difíciles.",
        "🌕 Exploración lunar: El primer robot en la Luna se llamó Lunokhod 1 y era como un laboratorio con ruedas.",
        "🛰️ Satélites: Los satélites que orbitan la Tierra son robots que nos dan GPS e internet.",
        "🦾 Prótesis: Las manos robóticas modernas pueden ser controladas por la mente de las personas.",
        "🚗 Autos autónomos: Son robots gigantes con ruedas que usan cámaras y láseres para conducir solos.",
        "🤖 Compañeros: En algunos hospitales, robots amigables ayudan a los niños a sentirse mejor.",
        "🧹 Robots domésticos: Tu aspiradora inteligente es un robot que mapea tu casa para no chocar.",
        "Rex Dino-robots: Los animatrónicos de las películas son robots complejos cubiertos de piel falsa.",
        "⚙️ Engranajes: Usar un engranaje grande con uno pequeño puede darte mucha fuerza o mucha velocidad.",
        "🌡️ Sensores: Un termistor es un sensor que cambia su resistencia cuando cambia la temperatura.",
        "📡 Antenas: Los robots espaciales usan antenas gigantes para enviar fotos desde otros planetas.",
        "🔋 Paneles solares: Los robots espaciales obtienen su energía transformando la luz del sol en electricidad.",
        "📐 Algoritmos: Un algoritmo es como una receta de cocina, pero con pasos para que el robot los siga.",
        "🐍 Robots serpiente: Estos robots pueden entrar por tuberías y grietas para rescatar personas.",
        "🐝 Enjambres: A veces muchos robots pequeños trabajan juntos como un enjambre de abejas.",
        "📦 Logística: En los almacenes de internet, cientos de robots mueven cajas para que tus juguetes lleguen rápido.",
        "🎨 Arte robótico: Hay robots que pueden pintar cuadros hermosos siguiendo el ritmo de la música.",
        "🚒 Bomberos: Existen robots que pueden entrar al fuego para apagar incendios sin peligro.",
        "🛸 Drones: Los drones son robots voladores que usan giroscopios para mantenerse equilibrados.",
        "🧩 Modularidad: Muchos robots modernos se arman como piezas de LEGO para cambiar sus funciones.",
        "🤖 Futuro: ¡Tú podrías ser quien diseñe el próximo gran robot que ayude a salvar el planeta!"
    ]
