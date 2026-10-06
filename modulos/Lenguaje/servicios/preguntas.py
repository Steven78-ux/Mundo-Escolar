"""Provee listas de preguntas para cada juego."""

from ..dominio.juegos import (
    PreguntaSonido,
    PalabraConstruible,
    PreguntaEspejo,
    PalabraEscrita,
    PreguntaRima,
    PalabraDesordenada,
    PreguntaLectura,
    Sopa,
)


# ------------------------------------------------------------
# Detective de Sonidos (nivel 1) – ampliado
# ------------------------------------------------------------
def obtener_preguntas_detective():
    return [
        PreguntaSonido("A", "🍎", ["🍎", "🐶", "🐱"], "🍎"),
        PreguntaSonido("B", "🎈", ["🎈", "⭐", "🚗"], "🎈"),
        PreguntaSonido("C", "🏠", ["🏠", "☀️", "🌙"], "🏠"),
        PreguntaSonido("D", "🍩", ["🐬", "🍩", "🚪"], "🍩"),
        PreguntaSonido("E", "🐘", ["🐘", "🧸", "✏️"], "🐘"),
        PreguntaSonido("F", "🌸", ["🌸", "🔥", "🐸"], "🌸"),
        PreguntaSonido("G", "🎸", ["🐱", "🧤", "🎸"], "🎸"),
        PreguntaSonido("L", "🍋", ["🦁", "📚", "🍋"], "🍋"),
        PreguntaSonido("M", "🧸", ["🧸", "🐵", "🌙"], "🧸"),
        PreguntaSonido("P", "🍐", ["⚽", "🍐", "🐧"], "🍐"),
        PreguntaSonido("S", "🍓", ["🐍", "☀️", "🍓"], "🍓"),
        PreguntaSonido("T", "🍅", ["🐢", "🍅", "🎺"], "🍅"),
    ]


# ------------------------------------------------------------
# Constructor de Palabras (nivel 2) – más palabras y sílabas
# ------------------------------------------------------------
def obtener_palabras_constructor():
    return [
        PalabraConstruible("🦆", "PATO", ["PA", "TO"]),
        PalabraConstruible("☀️", "SOL", ["SOL"]),
        PalabraConstruible("🌙", "LUNA", ["LU", "NA"]),
        PalabraConstruible("🐸", "SAPO", ["SA", "PO"]),
        PalabraConstruible("🏠", "CASA", ["CA", "SA"]),
        PalabraConstruible("🐕", "PERRO", ["PE", "RRO"]),
        PalabraConstruible("🐈", "GATO", ["GA", "TO"]),
        PalabraConstruible("🐟", "PEZ", ["PEZ"]),
        PalabraConstruible("🌳", "ARBOL", ["AR", "BOL"]),
        PalabraConstruible("🐘", "ELEFANTE", ["E", "LE", "FAN", "TE"]),
        PalabraConstruible("🦋", "MARIPOSA", ["MA", "RI", "PO", "SA"]),
        PalabraConstruible("🐒", "MONO", ["MO", "NO"]),
        PalabraConstruible("🦁", "LEON", ["LE", "ON"]),
        PalabraConstruible(
            "🦩",
            "FLAMENCO",
            (["FLA", "MEN", "CO"]),
        ),  # O usar otra de estructura simple
        PalabraConstruible("🐄", "VACA", ["VA", "CA"]),
        PalabraConstruible("🐺", "LOBO", ["LO", "BO"]),
        PalabraConstruible("🐁", "RATON", ["RA", "TON"]),
        PalabraConstruible(
            "🍎", "MANZANA", ["MAN", "ZA", "NA"]
        ),  # (Esta va en 3, abajo pongo más sencillas)
        PalabraConstruible("🍕", "PIZZA", ["PI", "ZZA"]),
        PalabraConstruible("🪑", "SILLA", ["SI", "LLA"]),
        PalabraConstruible("🧸", "OSITO", ["O", "SI", "TO"]),  # 3 sílabas
        PalabraConstruible("🧸", "OSO", ["O", "SO"]),
        PalabraConstruible("🍇", "UVA", ["U", "VA"]),
        PalabraConstruible("🍌", "PLATANO", ["PLA", "TA", "NO"]),  # 3 sílabas
        PalabraConstruible("🐄", "VACA", ["VA", "CA"]),
        PalabraConstruible("🐺", "LOBO", ["LO", "BO"]),
        PalabraConstruible("🐻", "OSO", ["O", "SO"]),
        PalabraConstruible("🍇", "UVA", ["U", "VA"]),
        PalabraConstruible("🪑", "SILLA", ["SI", "LLA"]),
        PalabraConstruible("🍍", "PIÑA", ["PI", "ÑA"]),
        PalabraConstruible("🎈", "GLOBO", ["GLO", "BO"]),
        PalabraConstruible("🥛", "LECHE", ["LE", "CHE"]),
        PalabraConstruible("🔑", "LLAVE", ["LLA", "VE"]),
        PalabraConstruible("🦛", "HIPOPOTAMO", ["HI", "PO", "PO", "TA", "MO"]),
        PalabraConstruible("🦖", "DINOSAURIO", ["DI", "NO", "SAU", "RIO"]),
        PalabraConstruible("🛩️", "HELICOPTERO", ["HE", "LI", "COP", "TE", "RO"]),
        PalabraConstruible("💻", "COMPUTADORA", ["COM", "PU", "TA", "DO", "RA"]),
        PalabraConstruible(
            "🍉", "SANDIA", ["SAN", "DI", "A"]
        ),  # 3 sílabas pero con hiato
        PalabraConstruible("🦘", "CANGURO", ["CAN", "GU", "RO"]),  # 3 sílabas compleja
        PalabraConstruible("🚲", "BICICLETA", ["BI", "CI", "CLE", "TA"]),
    ]


# distractores adicionales
DISTRACTORES = [
    "MA",
    "RE",
    "CI",
    "RA",
    "LO",
    "NA",
    "PA",
    "SA",
    "TE",
    "PE",
    "RO",
    "LI",
    "TU",
    "BA",
    "DA",
    "BO",
    "DO",
    "PO",
    "QO",
    "PU",
    "QU",
    "VA",  # Para competir con VACA/BOLA
    "VE",
    "VI",
    "ZA",  # Para competir con MANZANA/CASA
    "ZO",
    "CE",
    "SE",
    "SO",
    "AL",  # Distractor de LA
    "EL",  # Distractor de LE
    "OL",  # Distractor de LO
    "AN",  # Distractor de NA
    "EN",  # Distractor de NE
    "AR",  # Distractor de RA
    "OR",  # Distractor de RO
    "ES",  # Distractor de SE
    "TRA",
    "BRA",
    "CRA",
    "PLA",
    "BLA",
    "CLE",
    "PLO",
    "RRA",  # Para ver si diferencia R de RR
]


# ------------------------------------------------------------
# Carrera de Letras (nivel 3) – muchas confusiones típicas
# ------------------------------------------------------------
def obtener_preguntas_carrera():
    return [
        PreguntaEspejo("pala", "pala", True),
        PreguntaEspejo("sopa", "sopa", True),
        PreguntaEspejo("pelo", "pelo", True),
        PreguntaEspejo("gato", "gato", True),
        PreguntaEspejo("ratón", "ratón", True),
        PreguntaEspejo("libro", "libro", True),
        PreguntaEspejo("luna", "luna", True),
        PreguntaEspejo("sol", "sol", True),
        PreguntaEspejo("agua", "agua", True),
        PreguntaEspejo("piña", "piña", True),
        PreguntaEspejo("tren", "tren", True),
        PreguntaEspejo("avión", "avión", True),
        # Nuevas verdaderas añadidas para equilibrar:
        PreguntaEspejo("bota", "bota", True),
        PreguntaEspejo("dedo", "dedo", True),
        PreguntaEspejo("vaca", "vaca", True),
        PreguntaEspejo("vino", "vino", True),
        PreguntaEspejo("mano", "mano", True),
        PreguntaEspejo("casa", "casa", True),
        PreguntaEspejo("dado", "dado", True),
        PreguntaEspejo("fuego", "fuego", True),
        PreguntaEspejo("zapato", "zapato", True),
        PreguntaEspejo("chocolate", "chocolate", True),
        PreguntaEspejo("plato", "plato", True),

        # --- BLOQUE 2: PAREJAS DIFERENTES (23 False) ---
        # Confusiones de espejo (b, d, p, q)
        PreguntaEspejo("bota", "dota", False),
        PreguntaEspejo("dedo", "bedo", False),
        PreguntaEspejo("pato", "qato", False),
        PreguntaEspejo("dado", "babo", False),
        PreguntaEspejo("boda", "doba", False),
        PreguntaEspejo("pavo", "qavo", False),
        PreguntaEspejo("gota", "qota", False),
        # Confusiones ortográficas (b/v, c/z, ll/y, H muda)
        PreguntaEspejo("baca", "vaca", False),
        PreguntaEspejo("vino", "bino", False),
        PreguntaEspejo("casa", "caza", False),
        PreguntaEspejo("llave", "yave", False),
        PreguntaEspejo("huevo", "uevo", False),
        PreguntaEspejo("hoja", "oja", False),
        PreguntaEspejo("helado", "elado", False),
        PreguntaEspejo("zapato", "sapato", False),
        PreguntaEspejo("bote", "vote", False),
        # Confusiones fonológicas cercanas (m/n, g/c, p/d, f/t)
        PreguntaEspejo("niño", "miño", False),
        PreguntaEspejo("goma", "coma", False),
        PreguntaEspejo("foca", "toca", False),
        PreguntaEspejo("pato", "pado", False),
        # Inversiones de sílabas o letras
        PreguntaEspejo("tarta", "trata", False),
        PreguntaEspejo("plato", "palto", False),
        PreguntaEspejo("blusa", "bulsa", False),
    ]


# ------------------------------------------------------------
# Escribe la Palabra (nivel 4) – más palabras y pistas
# ------------------------------------------------------------
def obtener_palabras_escribe():
    return [
        PalabraEscrita("🐱", "GATO", "G"),
        PalabraEscrita("🏠", "CASA", "C"),
        PalabraEscrita("🐶", "PERRO", "P"),
        PalabraEscrita("🌳", "ARBOL", "A"),
        PalabraEscrita("🐸", "SAPO", "S"),
        PalabraEscrita("☀️", "SOL", "S"),
        PalabraEscrita("🌙", "LUNA", "L"),
        PalabraEscrita("🐘", "ELEFANTE", "E"),
        PalabraEscrita("🐟", "PEZ", "P"),
        PalabraEscrita("🚗", "AUTO", "A"),
        PalabraEscrita("📚", "LIBRO", "L"),
        PalabraEscrita("🍎", "MANZANA", "M"),
        PalabraEscrita("🍞", "PAN", "P"),
        PalabraEscrita("👁️", "OJO", "O"),
        PalabraEscrita("🗺️", "MAPA", "M"),
        PalabraEscrita("🦆", "PATO", "P"),
        PalabraEscrita("🐮", "VACA", "V"),
        PalabraEscrita("🍇", "UVA", "U"),
        PalabraEscrita("🐻", "OSO", "O"),
        PalabraEscrita("🦁", "LEON", "L"),
        PalabraEscrita("🐺", "LOBO", "L"),
        PalabraEscrita("🔑", "LLAVE", "LL"), # Puedes darle "LL" o solo "L" según prefieras
        PalabraEscrita("🐀", "RATON", "R"),
        PalabraEscrita("🎈", "GLOBO", "G"),
        PalabraEscrita("🥛", "LECHE", "L"),
        PalabraEscrita("🐒", "MONO", "M"),
        PalabraEscrita("🪑", "SILLA", "S"),
        PalabraEscrita("⚓", "ANCLA", "A"),
        PalabraEscrita("🥔", "PAPA", "P"),
        PalabraEscrita("🍍", "PIÑA", "P"),
        PalabraEscrita("🥕", "ZANAHORIA", "Z"), # (Esta es más larga, ideal para reto)
        PalabraEscrita("🚀", "COHETE", "C"),     # ¡Buena para evaluar la 'H' intermedia!
        PalabraEscrita("🍅", "TOMATE", "T"),
        PalabraEscrita("🎒", "MOCHILA", "M"),
        PalabraEscrita("🍌", "PLATANO", "P"),
        PalabraEscrita("🎸", "GUITARRA", "G"),   # Reto con la 'GU' y la 'RR'
        PalabraEscrita("🎻", "VIOLIN", "V"),
        PalabraEscrita("🚲", "BICICLETA", "B"),
        PalabraEscrita("🦋", "MARIPOSA", "M"),
    ]


# ------------------------------------------------------------
# Rimas Divertidas (nivel 5)
# ------------------------------------------------------------
def obtener_rimas():
    return [
        # --- Las tuyas corregidas (1 rima + 1 distractor) ---
        PreguntaRima("GATO", ["PATO", "PERRO"], "PATO"),        # Rima con -ATO
        PreguntaRima("SOL", ["GOL", "PAN"], "GOL"),            # Rima con -OL
        PreguntaRima("LUNA", ["CUNA", "LOMA"], "CUNA"),         # Rima con -UNA
        PreguntaRima("PEZ", ["DIEZ", "SOL"], "DIEZ"),          # Rima con -EZ (Cambié VEZ/REZ por DIEZ)
        PreguntaRima("OSO", ["FOSO", "SOPA"], "FOSO"),          # Rima con -OSO (Cambié POZO por fonética)
        PreguntaRima("RATÓN", ["BOTÓN", "PERRO"], "BOTÓN"),     # Rima con -ÓN
        PreguntaRima("CAMPANA", ["MANZANA", "CAMA"], "MANZANA"),# Rima con -ANA
        PreguntaRima("ANILLO", ["MARTILLO", "SILLA"], "MARTILLO"), # Rima con -ILLO
        PreguntaRima("FLOR", ["AMOR", "FLAN"], "AMOR"),         # Rima con -OR
        PreguntaRima("HELADO", ["PESCADO", "PELO"], "PESCADO"), # Rima con -ADO
        PreguntaRima("PALETA", ["MALETA", "PELOTA"], "MALETA"), # Rima con -ETA (¡Corregido!)
        PreguntaRima("AVIÓN", ["CAMIÓN", "AUTO"], "CAMIÓN"),    # Rima con -ÓN
        PreguntaRima("CAMA", ["RAMA", "CASA"], "RAMA"),         # Rima con -AMA
        PreguntaRima("CASA", ["MASA", "CARRO"], "MASA"),        # Rima con -ASA
        PreguntaRima("ESPEJO", ["CONEJO", "OJO"], "CONEJO"),    # Rima con -EJO
        PreguntaRima("QUESO", ["HUESO", "MESA"], "HUESO"),      # Rima con -ESO

        # --- Nuevas Incorporaciones (Para ampliar el juego) ---
        PreguntaRima("BOTA", ["GOTA", "BOCA"], "GOTA"),         # Rima con -OTA
        PreguntaRima("PIÑA", ["NIÑA", "PEÑA"], "NIÑA"),         # Rima con -IÑA
        PreguntaRima("ZAPATO", ["PATO", "ZANAHORIA"], "PATO"),  # Rima con -ATO
        PreguntaRima("TREN", ["CIEN", "TREPADOR"], "CIEN"),    # Rima con -EN
        PreguntaRima("FOCA", ["BOCA", "FUEGO"], "BOCA"),        # Rima con -OCA
        PreguntaRima("VENTANA", ["IGUANA", "VIENTO"], "IGUANA"),# Rima con -ANA
        PreguntaRima("TORO", ["LORO", "TORRE"], "LORO"),        # Rima con -ORO
        PreguntaRima("PLÁTANO", ["PÁNTANO", "PLATO"], "PÁNTANO"),# Rima con -ÁTANO (Reto largo)
        PreguntaRima("CEPILLO", ["CASTILLO", "PELO"], "CASTILLO"),# Rima con -ILLO
        PreguntaRima("SOPA", ["ROPA", "SACO"], "ROPA"),         # Rima con -OPA
        PreguntaRima("BALLENA", ["SIRENA", "BARCO"], "SIRENA"), # Rima con -ENA
        PreguntaRima("COHETE", ["RODETE", "COCHE"], "RODETE"),  # Rima con -ETE
        PreguntaRima("CHUPETE", ["JUGUETE", "LECHE"], "JUGUETE"),# Rima con -ETE
        PreguntaRima("LOBO", ["GLOBO", "LUNA"], "GLOBO"),       # Rima con -OBO
    ]


# ------------------------------------------------------------
# Ordena las Letras (nivel 6)
# ------------------------------------------------------------
def obtener_ordenar_letras():
    return [
        PalabraDesordenada("🐱", "GATO", ["A", "T", "G", "O"]),
        PalabraDesordenada("🏠", "CASA", ["S", "A", "C", "A"]),
        PalabraDesordenada("🐶", "PERRO", ["R", "O", "E", "P", "R"]),
        PalabraDesordenada("☀️", "SOL", ["O", "L", "S"]),
        PalabraDesordenada("🐸", "SAPO", ["P", "S", "O", "A"]),
        PalabraDesordenada("🐘", "ELEFANTE", ["E", "T", "L", "E", "A", "F", "N", "E"]),
        PalabraDesordenada("🚗", "AUTO", ["U", "A", "O", "T"]),
        PalabraDesordenada("🐟", "PEZ", ["E", "P", "Z"]),
        PalabraDesordenada("🍞", "PAN", ["N", "P", "A"]),
        PalabraDesordenada("👁️", "OJO", ["J", "O", "O"]),
        PalabraDesordenada("🌙", "LUNA", ["N", "U", "A", "L"]),
        PalabraDesordenada("🦆", "PATO", ["T", "P", "O", "A"]),
        PalabraDesordenada("🐄", "VACA", ["C", "A", "V", "A"]),
        PalabraDesordenada("🐻", "OSO", ["S", "O", "O"]),
        PalabraDesordenada("🗺️", "MAPA", ["P", "A", "M", "A"]),
        PalabraDesordenada("🦁", "LEON", ["O", "L", "N", "E"]),
        PalabraDesordenada("🍇", "UVA", ["V", "A", "U"]),
        PalabraDesordenada("🌳", "ARBOL", ["L", "B", "A", "O", "R"]),
        PalabraDesordenada("📚", "LIBRO", ["R", "L", "O", "I", "B"]),
        PalabraDesordenada("🐺", "LOBO", ["B", "O", "L", "O"]),  # (Esta es de 4, pero es buen distractor de letras repetidas)
        PalabraDesordenada("🔑", "LLAVE", ["V", "L", "E", "A", "L"]), # Se separan las dos L
        PalabraDesordenada("🐀", "RATON", ["O", "R", "N", "A", "T"]),
        PalabraDesordenada("🎈", "GLOBO", ["O", "G", "O", "L", "B"]),
        PalabraDesordenada("🥛", "LECHE", ["H", "L", "C", "E", "E"]),
        PalabraDesordenada("🐒", "MONO", ["N", "O", "M", "O"]),   # (De 4 letras, ideal para este bloque)
        PalabraDesordenada("🪑", "SILLA", ["L", "S", "A", "I", "L"]),
        PalabraDesordenada("⚓", "BARCO", ["C", "B", "O", "R", "A"]),
        PalabraDesordenada("🍎", "MANZANA", ["N", "A", "Z", "M", "A", "A", "N"]),
        PalabraDesordenada("🚀", "COHETE", ["E", "C", "H", "O", "T", "E"]),
        PalabraDesordenada("🍅", "TOMATE", ["T", "O", "A", "M", "E", "T"]),
        PalabraDesordenada("🎒", "MOCHILA", ["L", "M", "H", "O", "A", "C", "I"]),
        PalabraDesordenada("🍌", "PLATANO", ["A", "P", "T", "L", "O", "A", "N"]),
        PalabraDesordenada("🦖", "DINOSAURIO", ["I", "D", "N", "S", "U", "A", "R", "O", "I", "O"]),
        PalabraDesordenada("🎸", "GUITARRA", ["G", "U", "I", "T", "A", "R", "A"]),
        PalabraDesordenada("🎻", "VIOLIN", ["N", "I", "O", "I", "L", "V"]),
        PalabraDesordenada("🚲", "BICICLETA", ["B", "C", "I", "T", "E", "L", "A", "I", "C"]),
        PalabraDesordenada("🦋", "MARIPOSA", ["S", "M", "A", "O", "R", "A", "P", "I"]),
    ]


# ------------------------------------------------------------
# Lee y Encuentra (nivel 7)
# ------------------------------------------------------------
def obtener_frases_lectura():
    return [
        # --- CORREGIDAS: Mismo género en los distractores ---
        PreguntaLectura("El 🐱 toma leche", ["🐱", "🐶", "🦁"], "🐱"),         # Todos masculinos (gato, perro, león)
        PreguntaLectura("El 🚗 es rojo", ["🚲", "🚗", "✈️"], "🚗"),             # Auto, camión 🚚, tren 🚂 (Mejor cambiar bicicleta/avión por masculinos: coche, camión, tren)
        PreguntaLectura("La 🐢 nada en el agua", ["🐢", "🐋", "🐸"], "🐢"),     # ¡Corregido! Tortuga, ballena, rana (Todas femeninas)
        PreguntaLectura("La 🌙 sale de noche", ["☀️", "🌙", "⭐"], "🌙"),        # Luna, estrella, nube ☁️ (Cambié Sol por Nube para mantener femenino)
        PreguntaLectura("El 📚 está sobre la mesa", ["📚", "✏️", "🎒"], "📚"),   # Libro, lápiz, cuaderno 📓 (Cambié mochila por cuaderno)
        PreguntaLectura("La 🍎 es roja", ["🍌", "🍎", "🍇"], "🍎"),             # Manzana, banana, fresa 🍓 (Cambié uva por fresa)
        PreguntaLectura("El 🐕 ladra fuerte", ["🐕", "🐈", "🦁"], "🐕"),        # Perro, gato, león (Todos masculinos)
        PreguntaLectura("El 🐵 come una banana", ["🐘", "🐵", "🦒"], "🐵"),     # Mono, elefante, cocodrilo 🐊 (Cambié jirafa por masculino)
        PreguntaLectura("El 🐦 vuela por el aire", ["🐟", "🐸", "🐦"], "🐦"),   # Pájaro, pez, sapo (Todos masculinos)
        PreguntaLectura("La 🐝 hace miel dulce", ["🦋", "🐜", "🐝"], "🐝"),     # Abeja, mariposa, hormiga (Todas femeninas)
        PreguntaLectura("El 🐰 salta en el pasto", ["🐢", "🐰", "🐌"], "🐰"),   # Conejo, sapo 🐸, ratón 🐀 (Cambié tortuga y caracol por masculinos)
        PreguntaLectura("El 🦁 es el rey del bosque", ["🦊", "🐻", "🦁"], "🦁"), # León, zorro, oso (Todos masculinos)
        PreguntaLectura("El ☀️ brilla en el día", ["☀️", "🔥", "⚡"], "☀️"),       # Sol, fuego, rayo (Todos masculinos)
        PreguntaLectura("La 🌸 huele muy rico", ["🌱", "🌸", "🌿"], "🌸"),       # Flor, rosa 🌹, planta 🪴 (Cambié árbol y hoja)
        PreguntaLectura("El 🌳 tiene muchas hojas", ["🌳", "🌵", "🌻"], "🌳"),   # Árbol, cactus, girasol (Todos masculinos)
        PreguntaLectura("La ❄️ es fría como el hielo", ["🔥", "🌧️", "❄️"], "❄️"), # Nieve, lluvia, fogata 🪵
        PreguntaLectura("El 🔥 calienta la fogata", ["💧", "🔥", "🌬️"], "🔥"),   # Fuego, viento, río 🌊 (Cambié agua por río)
        PreguntaLectura("Uso el ✏️ para escribir", ["✏️", "🎒", "🪑"], "✏️"),    # Lápiz, pincel 🖌️, color 🖍️ (Cambié mochila y silla)
        PreguntaLectura("El 🍦 es de fresa", ["🍕", "🍿", "🍦"], "🍦"),         # Helado, chocolate 🍫, caramelo 🍬 (Cambié pizza y pop-corn)
        PreguntaLectura("La 🥛 está en el vaso", ["🥛", "🍎", "🍪"], "🥛"),     # Leche, sopa 🥣, agua 💧 (Cambié manzana y galleta)
        PreguntaLectura("La 👑 es del rey", ["🎩", "👑", "🧢"], "👑"),          # Corona, gorra, peluca 🧑‍🦱 (Cambié sombrero por femeninos)
        PreguntaLectura("El 🎈 vuela muy alto", ["🚗", "🎈", "🔑"], "🎈"),      # Globo, avión ✈️, pájaro 🐦 (Cambié auto y llave)
        PreguntaLectura("Me pongo el 👟 en el pie", ["🧦", "👕", "👟"], "👟"),   # Zapato, calcetín 🧦, pantalón 👖 (Cambié camiseta)

        # --- NUEVAS INCORPORACIONES (Ampliación del banco de preguntas) ---
        PreguntaLectura("La 🐔 pone un huevo", ["🐔", "🦆", "🦉"], "🐔"),       # Gallina, pata, lechuza
        PreguntaLectura("El 🧀 es de color amarillo", ["🧀", "🍞", "🥩"], "🧀"),# Queso, pan, filete
        PreguntaLectura("La ⛵ navega por el mar", ["⛵", "🛶", "⚓"], "⛵"),     # Barca, canoa, balsa
        PreguntaLectura("El ⏰ suena por la mañana", ["⏰", "📱", "📻"], "⏰"),  # Reloj, teléfono, radio
        PreguntaLectura("La 🧥 me quita el frío", ["🧥", "camisa", "falda"], "🧥"), # Chaqueta, camisa, falda (Puedes usar texto si prefieres)
        PreguntaLectura("El 🤡 trabaja en el circo", ["🤡", "🧙‍♂️", "👨‍🚒"], "🤡"),  # Payaso, mago, bombero
        PreguntaLectura("La 🕷️ teje su telaraña", ["🕷️", "hormiga", "mosca"], "🕷️"), # Araña
        PreguntaLectura("El 🌽 crece en la planta", ["🌽", "tomate", "plátano"], "🌽"), # Maíz / Choclo
        PreguntaLectura("La 🥖 es crujiente y rica", ["🥖", "galleta", "tarta"], "🥖"), # Barra de pan / Flauta
        PreguntaLectura("El 🦷 se cayó ayer", ["🦷", "ojo", "pelo"], "🦷"),      # Diente
    ]


# ------------------------------------------------------------
# Sopa de Letras (nivel 8)
# ------------------------------------------------------------
def obtener_sopas():
    return [
        # =================================================================
        # DIFICULTAD FÁCIL (4x4, 5x5, 6x6)
        # =================================================================
        Sopa(
            "SOL",
            [
                ["A", "B", "S", "D"],
                ["E", "F", "O", "H"],
                ["I", "J", "L", "K"],
                ["M", "N", "Ñ", "P"],
            ],
            [(0, 2), (1, 2), (2, 2)], # Vertical
        ),
        Sopa(
            "LUNA",
            [
                ["L", "X", "Y", "Z"],
                ["U", "A", "B", "C"],
                ["N", "D", "E", "F"],
                ["A", "G", "H", "I"],
            ],
            [(0, 0), (1, 0), (2, 0), (3, 0)], # Vertical
        ),
        Sopa(
            "CASA",
            [
                ["C", "D", "E", "F"],
                ["A", "G", "H", "I"],
                ["S", "J", "K", "L"],
                ["A", "M", "N", "Ñ"],
            ],
            [(0, 0), (1, 0), (2, 0), (3, 0)], # Vertical
        ),
        Sopa(
            "GATO",
            [
                ["P", "G", "A", "T", "O"],
                ["X", "A", "L", "K", "J"],
                ["Q", "T", "Z", "M", "N"],
                ["W", "O", "B", "V", "C"],
                ["E", "R", "Y", "U", "I"],
            ],
            [(0, 1), (0, 2), (0, 3), (0, 4)], # Horizontal
        ),
        Sopa(
            "PANA",
            [
                ["P", "A", "N", "A", "X"],
                ["B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K"],
                ["L", "M", "N", "O", "P"],
                ["Q", "R", "S", "T", "U"],
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3)], # Horizontal
        ),
        Sopa(
            "MESA",
            [
                ["X", "Y", "Z", "W", "V"],
                ["A", "M", "E", "S", "A"],
                ["B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K"],
                ["L", "M", "N", "O", "P"],
            ],
            [(1, 1), (1, 2), (1, 3), (1, 4)], # Horizontal
        ),
        Sopa(
            "PERRO",
            [
                ["M", "L", "K", "J", "H", "G"],
                ["A", "B", "C", "D", "E", "F"],
                ["P", "E", "R", "R", "O", "X"],
                ["Q", "W", "E", "R", "T", "Y"],
                ["U", "I", "O", "P", "A", "S"],
                ["D", "F", "G", "H", "J", "K"]
            ],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)], # Horizontal
        ),
        Sopa(
            "BARCO",
            [
                ["F", "B", "X", "Z", "Q", "W"],
                ["G", "A", "R", "T", "Y", "U"],
                ["H", "R", "O", "P", "S", "D"],
                ["J", "C", "K", "L", "M", "N"],
                ["K", "O", "B", "V", "C", "X"],
                ["L", "Z", "A", "S", "D", "F"]
            ],
            [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)], # Vertical
        ),
        Sopa(
            "LLAVE",
            [
                ["L", "A", "B", "C", "D", "E"],
                ["L", "X", "Y", "Z", "W", "V"],
                ["A", "P", "Q", "R", "S", "T"],
                ["V", "M", "N", "Ñ", "O", "P"],
                ["E", "F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O", "P"]
            ],
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], # Vertical
        ),

        # =================================================================
        # DIFICULTAD MEDIA (7x7, 8x8, 9x9)
        # =================================================================
        Sopa(
            "TORTUGA",
            [
                ["A", "S", "D", "F", "G", "H", "J"],
                ["K", "L", "Z", "X", "C", "V", "B"],
                ["N", "M", "Q", "W", "E", "R", "T"],
                ["Y", "U", "I", "O", "P", "A", "S"],
                ["T", "O", "R", "T", "U", "G", "A"],
                ["D", "F", "G", "H", "J", "K", "L"],
                ["P", "O", "I", "U", "Y", "T", "R"]
            ],
            [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], # Horizontal
        ),
        Sopa(
            "ESCUELA",
            [
                ["Q", "W", "E", "R", "T", "Y", "U"],
                ["I", "O", "P", "A", "S", "D", "F"],
                ["G", "H", "J", "K", "L", "Z", "X"],
                ["E", "S", "C", "U", "E", "L", "A"],
                ["C", "V", "B", "N", "M", "Q", "W"],
                ["E", "R", "T", "Y", "U", "I", "O"],
                ["P", "A", "S", "D", "F", "G", "H"]
            ],
            [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], # Horizontal
        ),
        Sopa(
            "PLÁTANO",
            [
                ["P", "L", "A", "T", "A", "N", "O"],
                ["B", "N", "M", "Q", "W", "E", "R"],
                ["V", "C", "X", "Z", "L", "K", "J"],
                ["G", "F", "D", "S", "A", "P", "O"],
                ["U", "I", "O", "P", "L", "K", "J"],
                ["R", "E", "W", "Q", "A", "S", "D"],
                ["Z", "X", "C", "V", "B", "N", "M"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)], # Horizontal
        ),
        Sopa(
            "PELOTA",
            [
                ["A", "B", "C", "D", "E", "F", "G", "X"],
                ["H", "I", "J", "K", "L", "M", "N", "Y"],
                ["O", "P", "E", "L", "O", "T", "A", "Z"],
                ["P", "Q", "R", "S", "T", "U", "V", "W"],
                ["W", "X", "Y", "Z", "A", "B", "C", "D"],
                ["D", "E", "F", "G", "H", "I", "J", "K"],
                ["K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z"]
            ],
            [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], # Horizontal
        ),
        Sopa(
            "MARIPOSA",
            [
                ["Z", "X", "C", "V", "B", "N", "M", "Q"],
                ["M", "A", "R", "I", "P", "O", "S", "A"],
                ["W", "E", "R", "T", "Y", "U", "I", "O"],
                ["P", "A", "S", "D", "F", "G", "H", "J"],
                ["K", "L", "Z", "X", "C", "V", "B", "N"],
                ["M", "Q", "W", "E", "R", "T", "Y", "U"],
                ["I", "O", "P", "A", "S", "D", "F", "G"],
                ["H", "J", "K", "L", "M", "N", "O", "P"]
            ],
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)], # Horizontal
        ),
        Sopa(
            "MOCHILA",
            [
                ["M", "A", "S", "D", "F", "G", "H", "J"],
                ["O", "Z", "X", "C", "V", "B", "N", "M"],
                ["C", "H", "Q", "W", "E", "R", "T", "Y"], # Corregido: Separados 'C' y 'H'
                ["H", "I", "O", "P", "A", "S", "D", "F"],
                ["I", "G", "H", "J", "K", "L", "Z", "X"],
                ["L", "C", "V", "B", "N", "M", "Q", "W"],
                ["L", "W", "E", "R", "T", "Y", "U", "I"],
                ["A", "P", "A", "S", "D", "F", "G", "H"]
            ],
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1)], # Sigue la ruta vertical y gira en la A
        ),
        Sopa(
            "ELEFANTE",
            [
                ["Q", "W", "E", "R", "E", "T", "Y", "U", "I"],
                ["O", "P", "A", "S", "L", "D", "F", "G", "H"],
                ["J", "K", "L", "Z", "E", "X", "C", "V", "B"],
                ["N", "M", "Q", "W", "F", "E", "R", "T", "Y"],
                ["U", "I", "O", "P", "A", "A", "S", "D", "F"],
                ["G", "H", "J", "K", "N", "L", "Z", "X", "C"],
                ["V", "B", "N", "M", "T", "Q", "W", "E", "R"],
                ["T", "Y", "U", "I", "E", "O", "P", "A", "S"],
                ["D", "F", "G", "H", "J", "K", "L", "Z", "X"]
            ],
            [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)], # Vertical
        ),
        Sopa(
            "GUITARRA",
            [
                ["G", "U", "I", "T", "A", "R", "R", "A", "X"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O", "P", "Q", "R", "S"],
                ["T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
                ["C", "D", "E", "F", "G", "H", "I", "J", "K"],
                ["L", "M", "N", "O", "P", "Q", "R", "S", "T"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], # Horizontal
        ),
        Sopa(
            "PANADERÍA",
            [
                ["X", "Y", "Z", "W", "V", "U", "T", "S", "R"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["P", "A", "N", "A", "D", "E", "R", "I", "A"],
                ["J", "K", "L", "M", "N", "Ñ", "O", "P", "Q"],
                ["R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["J", "K", "L", "M", "N", "Ñ", "O", "P", "Q"],
                ["R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            ],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)], # Horizontal
        ),

        # =================================================================
        # DIFICULTAD DIFÍCIL (10x10, 11x11, 12x12)
        # =================================================================
        Sopa(
            "DINOSAURIO",
            [
                ["P", "L", "K", "J", "H", "G", "F", "D", "S", "A"],
                ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Z"],
                ["X", "C", "V", "B", "N", "M", "Q", "W", "E", "R"],
                ["T", "Y", "U", "I", "O", "P", "A", "S", "D", "F"],
                ["D", "I", "N", "O", "S", "A", "U", "R", "I", "O"],
                ["G", "H", "J", "K", "L", "Z", "X", "C", "V", "B"],
                ["N", "M", "Q", "W", "E", "R", "T", "Y", "U", "I"],
                ["O", "P", "A", "S", "D", "F", "G", "H", "J", "K"],
                ["L", "Z", "X", "C", "V", "B", "N", "M", "Q", "W"]
            ],
            [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9)], # Horizontal
        ),
        Sopa(
            "ZANAHORIA",
            [
                ["Z", "A", "N", "A", "H", "O", "R", "I", "A", "X"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
                ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                ["O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
                ["I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
                ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)], # Horizontal
        ),
        Sopa(
            "BOMBEROS",
            [
                ["B", "O", "M", "B", "E", "R", "O", "S", "X", "Y"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
                ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                ["O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
                ["I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
                ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)], # Horizontal ("BOMBEROS")
        ),
        Sopa(
            "COMPUTADORA",
            [
                ["C", "O", "M", "P", "U", "T", "A", "D", "O", "R", "A"],
                ["X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
                ["I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"],
                ["T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
                ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                ["L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"],
                ["W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G"],
                ["H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)], # Horizontal
        ),
        Sopa(
            "CHIMPANANCE",
            [
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                ["L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U"],
                ["V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
                ["C", "H", "I", "M", "P", "A", "N", "C", "E", "X", "Y"],
                ["G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P"],
                ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                ["M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V"],
                ["W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G"],
                ["H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"]
            ],
            [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)], # Horizontal ("CHIMPANC")
        ),
        Sopa(
            "HERRAMIENTA",
            [
                ["H", "E", "R", "R", "A", "M", "I", "E", "N", "T", "A"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                ["L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U"],
                ["V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P"],
                ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                ["M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V"],
                ["W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G"],
                ["H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)], # Horizontal
        ),
        Sopa(
            "CONSTRUCCIÓN",
            [
                ["C", "O", "N", "S", "T", "R", "U", "C", "C", "I", "O", "N"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                ["M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W"],
                ["X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q"],
                ["R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"],
                ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"],
                ["N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"]
            ],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)], # Horizontal
        ),
        Sopa(
            "REFRIGERADOR",
            [
                ["X", "Y", "Z", "W", "V", "U", "T", "S", "R", "Q", "P", "O"],
                ["R", "E", "F", "R", "I", "G", "E", "R", "A", "D", "O", "R"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                ["M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W"],
                ["X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q"],
                ["R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"],
                ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
            ],
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11)], # Horizontal
        ),
        Sopa(
            "ENCICLOPEDIA",
            [
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                ["M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W"],
                ["X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
                ["J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q"],
                ["R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C"],
                ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"],
                ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"],
                ["N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                ["E", "N", "C", "I", "C", "L", "O", "P", "E", "D", "I", "A"]
            ],
            [(11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11)], # Horizontal
        ),
    ]