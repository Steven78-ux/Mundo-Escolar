"""Historia por capitulos y fragmentos para mecanografia."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import unicodedata

# =============================================================================
# ESTRUCTURAS DE DATOS
# =============================================================================

@dataclass(frozen=True)
class CapituloMecanografia:
    numero: int
    titulo: str
    fragmentos: list[str]


@dataclass(frozen=True)
class LibroMecanografia:
    id_libro: str
    titulo: str
    descripcion: str
    capitulos: list[CapituloMecanografia]


@lru_cache(maxsize=128)
def _texto_para_primaria(texto: str) -> str:
    """Reduce signos complejos para facilitar mecanografia infantil."""
    tabla = str.maketrans("", "", ".,;:!?¿¡()\"'-")
    texto_limpio = texto.translate(tabla)
    # Preserva la ñ porque es una letra clave en espanol.
    texto_protegido = texto_limpio.replace("ñ", "__ENIE_MIN__").replace("Ñ", "__ENIE_MAY__")
    texto_sin_tildes = unicodedata.normalize("NFD", texto_protegido)
    texto_sin_tildes = "".join(c for c in texto_sin_tildes if unicodedata.category(c) != "Mn")
    texto_restaurado = texto_sin_tildes.replace("__ENIE_MIN__", "ñ").replace("__ENIE_MAY__", "Ñ")
    texto_ascii_simple = texto_restaurado.replace("ü", "u").replace("Ü", "U")
    return " ".join(texto_ascii_simple.split())


def _capitulos_para_primaria(capitulos: list[CapituloMecanografia]) -> list[CapituloMecanografia]:
    capitulos_limpios: list[CapituloMecanografia] = []
    for capitulo in capitulos:
        fragmentos_limpios = [_texto_para_primaria(fragmento) for fragmento in capitulo.fragmentos]
        capitulos_limpios.append(
            CapituloMecanografia(
                numero=capitulo.numero,
                titulo=capitulo.titulo,
                fragmentos=fragmentos_limpios,
            )
        )
    return capitulos_limpios

# =============================================================================
# DEFINICIÓN DE LIBROS (CONTENIDO)
# =============================================================================

CAPITULOS_PRINCIPITO: list[CapituloMecanografia] = [
    CapituloMecanografia(
        numero=1,
        titulo="El dibujo del sombrero",
        fragmentos=[
            "Cuando tenia seis años vi una boa que se tragaba una fiera",
            "Dibuje una boa cerrada pero los adultos vieron un sombrero",
            "Luego dibuje el interior para que pudieran entender mi idea",
            "Comprendi que los adultos no tienen mucha imaginacion",
        ],
    ),
    CapituloMecanografia(
        numero=2,
        titulo="Averia en el Sahara",
        fragmentos=[
            "Me converti en piloto y viaje por todo el mundo en mi avion",
            "Un dia tuve una averia en medio del desierto del Sahara",
            "Estaba solo y cansado cuando escuche una voz muy pequeña",
            "Por favor dibujame un cordero me dijo un niño extraño",
        ],
    ),
    CapituloMecanografia(
        numero=3,
        titulo="El pequeño visitante",
        fragmentos=[
            "Aquel niño era el Principito y venia de un planeta muy lejano",
            "Su hogar era el asteroide B-612 que era apenas como una casa",
            "Me conto que alli tenia tres volcanes y una rosa muy hermosa",
            "El cuidaba su planeta cada dia arrancando los malos baobabs",
        ],
    ),
    CapituloMecanografia(
        numero=4,
        titulo="Peligro de Baobabs",
        fragmentos=[
            "Visito un planeta donde un Rey queria mandar a todo el mundo",
            "Luego conocio a un hombre vanidoso que solo buscaba aplausos",
            "Que extrañas son las personas grandes pensaba el Principito",
            "El buscaba amigos pero ellos solo pensaban en si mismos",
        ],
    ),
    CapituloMecanografia(
        numero=5,
        titulo="Los tres volcanes",
        fragmentos=[
            "En su planeta habia dos volcanes activos y uno apagado",
            "El Principito los deshollinaba cada mañana con mucho cuidado",
            "Incluso el volcan apagado recibia limpieza por si acaso",
            "Mantenia su pequeño mundo en orden con mucha disciplina",
        ],
    ),
    CapituloMecanografia(
        numero=6,
        titulo="La Rosa orgullosa",
        fragmentos=[
            "Un dia nacio una flor muy bella y un poco vanidosa",
            "Ella pedia agua y un biombo para protegerse del viento",
            "El Principito la amaba pero no comprendia sus palabras",
            "Decidio viajar para aprender lo que no sabia del amor",
        ],
    ),
    CapituloMecanografia(
        numero=7,
        titulo="El Rey mandon",
        fragmentos=[
            "Llego al primer planeta donde vivia un rey solitario",
            "El rey creia que todos los demas eran sus subditos",
            "Mandaba al sol a ponerse pero solo cuando era la hora",
            "Las personas grandes son muy extrañas penso el niño",
        ],
    ),
    CapituloMecanografia(
        numero=8,
        titulo="El hombre de negocios",
        fragmentos=[
            "En otro planeta un hombre contaba todas las estrellas",
            "El creia que por contarlas era el dueño de todo el cielo",
            "Yo poseo una flor y la cuido cada dia dijo el Principito",
            "Tu no eres util para las estrellas le dijo el niño",
        ],
    ),
    CapituloMecanografia(
        numero=9,
        titulo="El fiel Farolero",
        fragmentos=[
            "Llego a un planeta que giraba muy rapido cada minuto",
            "Un hombre encendia y apagaba su farol sin descansar",
            "Este hombre piensa en algo mas que en si mismo",
            "Al Principito le gusto su sentido del deber y constancia",
        ],
    ),
    CapituloMecanografia(
        numero=10,
        titulo="El gran Geografo",
        fragmentos=[
            "Conocio a un sabio que escribia libros sobre montañas",
            "Pero el sabio nunca salia de su oficina para verlas",
            "Le recomendo visitar el planeta Tierra por su fama",
            "El Principito partio pensando en su rosa efimera",
        ],
    ),
    CapituloMecanografia(
        numero=11,
        titulo="Llegada a la Tierra",
        fragmentos=[
            "El septimo planeta fue la Tierra un lugar inmenso",
            "Caminó por el desierto y hablo con una serpiente",
            "Buscaba a los hombres pero solo encontraba arena",
            "Sintio un poco de soledad en aquel lugar tan grande",
        ],
    ),
    CapituloMecanografia(
        numero=12,
        titulo="El eco de la montaña",
        fragmentos=[
            "Subio a una montaña alta y grito hola con fuerza",
            "El eco respondio hola hola hola varias veces seguidas",
            "Que planeta tan seco y sin originalidad penso el niño",
            "Extrañaba su casa donde su rosa hablaba primero",
        ],
    ),
    CapituloMecanografia(
        numero=13,
        titulo="El jardin de rosas",
        fragmentos=[
            "Encontro un jardin con cinco mil rosas iguales",
            "Se sintio triste al creer que su rosa no era unica",
            "Pero entonces aparecio un zorro bajo un manzano",
            "El zorro le pidio que lo domesticara para ser amigos",
        ],
    ),
    CapituloMecanografia(
        numero=14,
        titulo="El secreto del Zorro",
        fragmentos=[
            "Domesticar significa crear lazos y ser especiales",
            "Solo se ve bien con el corazon decia el nuevo amigo",
            "Lo esencial es siempre invisible a los ojos humanos",
            "Eres responsable para siempre de lo que has domesticado",
        ],
    ),
    CapituloMecanografia(
        numero=15,
        titulo="Regreso a las estrellas",
        fragmentos=[
            "El Principito debia volver para cuidar a su rosa",
            "Me dijo que al mirar el cielo escucharia su risa",
            "Un destello amarillo toco su tobillo y el niño cayo",
            "Ahora el cuida su planeta y yo miro las estrellas",
        ],
    ),
]


CAPITULOS_DON_QUIJOTE: list[CapituloMecanografia] = [
    CapituloMecanografia(
        numero=1,
        titulo="Alonso el Caballero",
        fragmentos=[
            "En un lugar de la Mancha vivia un hombre que amaba leer",
            "Leia tantos libros de caballeria que un dia perdio el juicio",
            "Decidio ser un caballero andante y llamarse Don Quijote",
            "Limpio sus viejas armas y preparo a su caballo Rocinante",
        ],
    ),
    CapituloMecanografia(
        numero=2,
        titulo="Sancho el Escudero",
        fragmentos=[
            "Nuestro caballero necesitaba un escudero que lo acompañara",
            "Convencio a un labrador vecino llamado Sancho Panza",
            "Le prometio que un dia seria el gobernador de una isla",
            "Sancho subio a su burro y juntos salieron a buscar aventuras",
        ],
    ),
    CapituloMecanografia(
        numero=3,
        titulo="Molinos o Gigantes",
        fragmentos=[
            "Vieron a lo lejos treinta o cuarenta gigantes muy grandes",
            "Son molinos de viento decia Sancho con mucha preocupacion",
            "Don Quijote ataco con su lanza pero el viento lo derribo",
            "Asi fue como aprendieron que la imaginacion es muy poderosa",
        ],
    ),
    CapituloMecanografia(
        numero=4,
        titulo="El Yelmo dorado",
        fragmentos=[
            "Vieron a un barbero con una bacia dorada en la cabeza",
            "¡Es el famoso yelmo del rey Mambrino! grito Don Quijote",
            "El barbero huyo asustado y dejo su bacia en el camino",
            "Nuestro heroe lucia su nuevo casco con muchisimo orgullo",
        ],
    ),
    CapituloMecanografia(
        numero=5,
        titulo="La Dulcinea ideal",
        fragmentos=[
            "Todo caballero necesita una dama a quien dedicar sus triunfos",
            "Penso en una aldeana llamada Aldonza con mucha ternura",
            "La llamo Dulcinea del Toboso la mas bella del mundo",
            "Ella seria la luz que guiaria sus valientes aventuras",
        ],
    ),
    CapituloMecanografia(
        numero=6,
        titulo="La Venta del Castillo",
        fragmentos=[
            "Llegaron a una posada que el loco hidalgo vio como castillo",
            "El ventero divertido acepto seguir el juego al caballero",
            "Veló sus armas toda la noche junto a un pozo de agua",
            "Fue nombrado caballero en una ceremonia muy graciosa",
        ],
    ),
    CapituloMecanografia(
        numero=7,
        titulo="Los Galeotes libres",
        fragmentos=[
            "Encontraron a unos presos que iban camino a las galeras",
            "Don Quijote decidio liberarlos creyendo que era justicia",
            "Sancho le advirtio que eran malhechores pero no escucho",
            "Al final los presos le lanzaron piedras y huyeron rapido",
        ],
    ),
    CapituloMecanografia(
        numero=8,
        titulo="Sierra Morena",
        fragmentos=[
            "Se escondieron en las montañas para evitar a la justicia",
            "Sancho cuidaba del asno mientras el amo hacia locuras",
            "Escribio una carta de amor para su amada Dulcinea",
            "Sancho debia llevar el mensaje hasta el lejano Toboso",
        ],
    ),
    CapituloMecanografia(
        numero=9,
        titulo="La batalla de cueros",
        fragmentos=[
            "Don Quijote lucho en sueños contra gigantes invisibles",
            "Eran en realidad cueros de vino tinto de la posada",
            "El suelo se lleno de vino y el ventero se enfado mucho",
            "Sancho buscaba la cabeza del gigante entre los charcos",
        ],
    ),
    CapituloMecanografia(
        numero=10,
        titulo="El Caballero de Espejos",
        fragmentos=[
            "Un extraño caballero desafio a Don Quijote en el campo",
            "Llevaba una armadura llena de espejos que brillaban",
            "Nuestro heroe gano el duelo con valentia y destreza",
            "Resulto ser un amigo que queria llevarlo de vuelta",
        ],
    ),
    CapituloMecanografia(
        numero=11,
        titulo="La aventura de Leones",
        fragmentos=[
            "Un carro llevaba leones reales para el gran rey",
            "Don Quijote ordeno abrir la jaula para luchar con ellos",
            "El leon le dio la espalda y se volvio a dormir tranquilo",
            "El hidalgo se sintio el hombre mas valiente del mundo",
        ],
    ),
    CapituloMecanografia(
        numero=12,
        titulo="Cueva de Montesinos",
        fragmentos=[
            "Bajo con una cuerda a una cueva muy profunda y oscura",
            "Dijo haber visto palacios y caballeros encantados alli",
            "Sancho no creia nada pero escuchaba con mucho respeto",
            "La realidad y los sueños se mezclaban en su cabeza",
        ],
    ),
    CapituloMecanografia(
        numero=13,
        titulo="El vuelo de Clavileño",
        fragmentos=[
            "Subieron a un caballo de madera llamado Clavileño",
            "Les dijeron que volarian por el aire hasta el cielo",
            "Con los ojos vendados sintieron el viento y el fuego",
            "Fue una broma de unos duques pero ellos fueron felices",
        ],
    ),
    CapituloMecanografia(
        numero=14,
        titulo="Sancho Gobernador",
        fragmentos=[
            "Sancho cumplio su sueño de gobernar una pequeña insula",
            "Dio consejos sabios y demostro tener un buen corazon",
            "Pero prefirio volver con su amigo que vivir con lujos",
            "Mas vale pan con amor que pollo con dolor decia el sabio",
        ],
    ),
    CapituloMecanografia(
        numero=15,
        titulo="Regreso de la leyenda",
        fragmentos=[
            "Finalmente recupero el juicio y volvio a ser Alonso",
            "Pidio perdon a Sancho por haberlo llevado a aventuras",
            "Pero Sancho le pedia mas historias de caballeros andantes",
            "Murio en paz dejando el recuerdo de sus nobles ideales",
        ],
    ),
]

CAPITULOS_TRES_CERDITOS: list[CapituloMecanografia] = [
    CapituloMecanografia(
        numero=1,
        titulo="Hermanos en el bosque",
        fragmentos=[
            "Tres cerditos vivian felices y jugaban todo el dia",
            "Decidieron construir sus propias casas en el bosque",
            "El menor hizo su casa de paja para terminar rapido",
            "El mediano uso madera porque era un poco mas fuerte",
        ],
    ),
    CapituloMecanografia(
        numero=2,
        titulo="El plan de trabajo",
        fragmentos=[
            "El hermano mayor era muy trabajador y muy paciente",
            "El decidio construir una casa con ladrillos rojos",
            "Sus hermanos se burlaban porque el trabajaba mucho",
            "Pronto verian que el esfuerzo vale mucho la pena",
        ],
    ),
    CapituloMecanografia(
        numero=3,
        titulo="El Lobo hambriento",
        fragmentos=[
            "Un lobo hambriento llego a la casa de paja del menor",
            "¡Soplare y soplaré y tu casa derribaré! grito el lobo",
            "La paja volo por los aires y el cerdito salio corriendo",
            "Se refugio en la casa de madera de su hermano mediano",
        ],
    ),
    CapituloMecanografia(
        numero=4,
        titulo="Tablas y clavos",
        fragmentos=[
            "El lobo soplo con todas sus fuerzas la casa de madera",
            "Las tablas crujieron y la casa se rompio en mil pedazos",
            "Los dos cerditos corrieron rapido a la casa de ladrillo",
            "Por suerte el hermano mayor les abrio la puerta a tiempo",
        ],
    ),
    CapituloMecanografia(
        numero=5,
        titulo="Ladrillos resistentes",
        fragmentos=[
            "El lobo soplo y resoplo pero la casa de ladrillo resistio",
            "Decidio entrar por la chimenea pero cayo en agua caliente",
            "El lobo salio disparado y nunca mas volvio al bosque",
            "Los hermanos aprendieron que el trabajo bien hecho es mejor",
        ],
    ),
    CapituloMecanografia(
        numero=6,
        titulo="El mercado de paja",
        fragmentos=[
            "El cerdito pequeño compro paja a un buen hombre",
            "Cargaba los fardos con mucha prisa para ir a jugar",
            "La paja era dorada y olia a campo y a sol",
            "Un refugio rapido seria suficiente para descansar hoy",
        ],
    ),
    CapituloMecanografia(
        numero=7,
        titulo="El mercado de leña",
        fragmentos=[
            "El hermano mediano busco troncos en el gran mercado",
            "La madera era fuerte pero dificil de martillar fuerte",
            "Puso ventanas de cristal para ver a los pajaros volar",
            "Se sentia muy seguro bajo su nuevo techo de roble",
        ],
    ),
    CapituloMecanografia(
        numero=8,
        titulo="El mercado de cemento",
        fragmentos=[
            "El hermano mayor busco la mejor arena y cemento gris",
            "Mezclaba con fuerza mientras sus hermanos descansaban ya",
            "Cada ladrillo era un paso hacia una seguridad eterna",
            "No importa el cansancio si el resultado es perfecto",
        ],
    ),
    CapituloMecanografia(
        numero=9,
        titulo="La orquesta del bosque",
        fragmentos=[
            "Los cerditos tocaban flauta y violin por las tardes",
            "Cantaban canciones sobre la libertad y la alegria pura",
            "El lobo escuchaba la musica desde su cueva oscura",
            "Esperaba el momento para arruinar su bonita fiesta",
        ],
    ),
    CapituloMecanografia(
        numero=10,
        titulo="Huellas sospechosas",
        fragmentos=[
            "Encontraron huellas grandes y afiladas cerca del rio",
            "El lobo habia estado observando sus nuevas construcciones",
            "El hermano mayor reforzo los cerrojos de su puerta",
            "Debemos estar listos para cualquier sorpresa les advirtio",
        ],
    ),
    CapituloMecanografia(
        numero=11,
        titulo="El soplido magico",
        fragmentos=[
            "El lobo tenia un pulmon gigante y soplaba muy fuerte",
            "Entrenaba cada dia para derribar cualquier obstaculo hoy",
            "La casa de paja no tuvo oportunidad ante tal viento",
            "Pobres cerditos que solo querian jugar sin esforzarse",
        ],
    ),
    CapituloMecanografia(
        numero=12,
        titulo="Refugio compartido",
        fragmentos=[
            "Ahora los tres hermanos vivian en la casa de ladrillo",
            "Compartian la comida y el calor de la chimenea encendida",
            "Aprendieron que la union hace la fuerza en momentos malos",
            "Vigilaban por la ventana mientras el lobo merodeaba fuera",
        ],
    ),
    CapituloMecanografia(
        numero=13,
        titulo="La astucia del Lobo",
        fragmentos=[
            "El lobo se disfrazó de oveja para intentar engañarlos",
            "Hablaba con voz suave pidiendo entrar para dormir ya",
            "Pero sus orejas picudas lo delataron ante los hermanos",
            "No podras engañarnos mas lobo malvado gritaron todos",
        ],
    ),
    CapituloMecanografia(
        numero=14,
        titulo="Olla de agua caliente",
        fragmentos=[
            "Prepararon el fuego cuando oyeron pasos en el tejado",
            "El lobo bajo por el conducto pensando en su cena",
            "Al caer al agua grito y salto por la chimenea de nuevo",
            "Se fue corriendo hacia el lago para enfriar su cola",
        ],
    ),
    CapituloMecanografia(
        numero=15,
        titulo="Final feliz en el bosque",
        fragmentos=[
            "Los cerditos vivieron felices y siempre unidos al fin",
            "Ayudaron a otros animales a construir casas de ladrillo",
            "El lobo se volvio vegetariano y nunca mas molesto",
            "El esfuerzo y el trabajo traen la paz verdadera",
        ],
    ),
]

CAPITULOS_PINOCHO: list[CapituloMecanografia] = [
    CapituloMecanografia(
        numero=1,
        titulo="El deseo de Gepeto",
        fragmentos=[
            "Gepeto era un carpintero que tallo un muñeco de madera",
            "Un hada magica aparecio y le dio vida propia a Pinocho",
            "Pinocho abrio los ojos y comenzo a hablar con mucha alegria",
            "Debes ser un niño bueno y obediente le dijo el hada azul",
        ],
    ),
    CapituloMecanografia(
        numero=2,
        titulo="La escuela olvidada",
        fragmentos=[
            "Gepeto vendio su abrigo para comprar libros para Pinocho",
            "Nuestro amigo salio feliz camino a su primer dia de clases",
            "Pero un zorro astuto y un gato lo engañaron en el sendero",
            "Pinocho olvido su promesa y se fue a ver un espectaculo",
        ],
    ),
    CapituloMecanografia(
        numero=3,
        titulo="Nariz y mentiras",
        fragmentos=[
            "Pinocho conto una mentira y su nariz comenzo a crecer",
            "Cada vez que mentia su nariz se hacia mas y mas larga",
            "El hada le enseño que la verdad es siempre el mejor camino",
            "Prometio no volver a engañar a su querido papa Gepeto",
        ],
    ),
    CapituloMecanografia(
        numero=4,
        titulo="La gran Ballena",
        fragmentos=[
            "Gepeto salio al mar a buscar a su hijo y una ballena lo trago",
            "Pinocho nado con valentia y logro entrar al gran animal",
            "Alli encontro a su papa y juntos planearon un gran escape",
            "Hicieron una fogata y el animal los lanzo afuera con un estornudo",
        ],
    ),
    CapituloMecanografia(
        numero=5,
        titulo="Transformacion real",
        fragmentos=[
            "Pinocho demostro ser valiente y amar mucho a su papa",
            "Por su buen corazon el hada lo convirtio en niño de verdad",
            "Gepeto lloró de alegria al abrazar a su hijo de carne y hueso",
            "Desde entonces vivieron felices y siempre dijeron la verdad",
        ],
    ),
    CapituloMecanografia(
        numero=6,
        titulo="El grillo Pepe",
        fragmentos=[
            "Un pequeño grillo con sombrero era su voz de conciencia",
            "Le daba consejos para no meterse en lios peligrosos hoy",
            "Pinocho a veces lo escuchaba y otras veces se olvidaba",
            "Ser responsable es dificil para un muñeco de madera pura",
        ],
    ),
    CapituloMecanografia(
        numero=7,
        titulo="El Teatro de Titeres",
        fragmentos=[
            "Entro a un teatro donde los titeres bailaban con hilos",
            "El dueño era un hombre rudo que lo encerro en una jaula",
            "Pinocho lloraba pensando en su pobre papa solo en casa",
            "El hada lo rescato pero le advirtio sobre la obediencia",
        ],
    ),
    CapituloMecanografia(
        numero=8,
        titulo="El Zorro y el Gato",
        fragmentos=[
            "Dos pillos le dijeron que podia plantar monedas de oro",
            "Le prometieron que creceria un arbol lleno de riquezas",
            "Pinocho les creyo y enterro su dinero en la tierra roja",
            "Pronto aprendio que el dinero se gana trabajando mucho",
        ],
    ),
    CapituloMecanografia(
        numero=9,
        titulo="Campo de Milagros",
        fragmentos=[
            "Espero toda la noche a que el arbol magico creciera",
            "Pero al despertar los malvados se habian llevado todo",
            "Se sintio muy tonto por confiar en desconocidos extraños",
            "El grillo le dijo que no hay caminos cortos al exito",
        ],
    ),
    CapituloMecanografia(
        numero=10,
        titulo="Pais de Juguetes",
        fragmentos=[
            "Se subio a un carro lleno de niños que solo querian jugar",
            "Iban a un lugar donde no habia libros ni maestros pesados",
            "Comian dulces y corrian por todas partes sin parar nunca",
            "Parecia el paraiso pero habia una trampa muy oculta",
        ],
    ),
    CapituloMecanografia(
        numero=11,
        titulo="Orejas de Burro",
        fragmentos=[
            "Un dia noto que sus orejas eran largas y peludas ya",
            "A todos los niños perezosos les pasaba lo mismo alli",
            "Comenzo a rebuznar en lugar de hablar con sus amigos",
            "Era el castigo por no querer estudiar y ser un vago",
        ],
    ),
    CapituloMecanografia(
        numero=12,
        titulo="Escape del Circo",
        fragmentos=[
            "Lo llevaron a un circo para hacer piruetas muy dificiles",
            "Pinocho se lastimo una pierna y lo lanzaron al mar azul",
            "Al tocar el agua magica volvio a ser un muñeco normal",
            "Comenzo a nadar con fuerza para buscar a su buen padre",
        ],
    ),
    CapituloMecanografia(
        numero=13,
        titulo="Dentro del Monstruo",
        fragmentos=[
            "Una ballena gigante abrio su boca y se trago al muñeco",
            "En la oscuridad del estomago encontro una pequeña luz",
            "Era Gepeto en su bote comiendo peces para sobrevivir",
            "Papa e hijo se abrazaron con lagrimas de mucha emocion",
        ],
    ),
    CapituloMecanografia(
        numero=14,
        titulo="Estornudo de Libertad",
        fragmentos=[
            "Hicieron una hoguera para que la ballena estornudara fuerte",
            "El humo la hizo picar y los lanzo fuera con mucha potencia",
            "Pinocho nado cargando a su anciano padre en la espalda",
            "Llegaron a la costa sanos y salvos tras el gran esfuerzo",
        ],
    ),
    CapituloMecanografia(
        numero=15,
        titulo="Un corazon de verdad",
        fragmentos=[
            "Cuido a Gepeto enfermo trabajando duro en el campo cada dia",
            "Demostro que un muñeco puede tener sentimientos muy nobles",
            "El hada azul aparecio y cumplio el sueño de su vida hoy",
            "Ahora es un niño de verdad que siempre dice la verdad",
        ],
    ),
]

CAPITULOS_ALICIA: list[CapituloMecanografia] = [
    CapituloMecanografia(1, "El conejo blanco", ["Alicia vio un conejo con chaleco y reloj de bolsillo", "Siguio al animal hasta una madriguera muy profunda", "Cayo por un tunel lleno de estantes y mapas raros", "Asi comenzo su viaje al Pais de las Maravillas"]),
    CapituloMecanografia(2, "Bebe esto", ["Encontro una botella con una etiqueta que decia bebeme", "Al beber el liquido Alicia se hizo muy pequeña", "Luego comio un pastel que la hizo crecer muchisimo", "Que cosas tan extrañas suceden hoy penso la niña"]),
    CapituloMecanografia(3, "El Gato de Cheshire", ["Vio a un gato que sonreia sentado en una rama", "El gato desaparecia dejando solo su gran sonrisa", "Todos aqui estamos locos le dijo el minino azul", "Alicia busco el camino hacia la casa de la liebre"]),
    CapituloMecanografia(4, "Merienda de locos", ["El Sombrerero y la Liebre tomaban te sin parar", "Hacian acertijos sin respuesta y movian las tazas", "Alicia se canso de tantas tonterias y se marcho", "Encontro una puerta dorada que llevaba al jardin"]),
    CapituloMecanografia(5, "La Reina de Corazones", ["Los soldados eran cartas que pintaban rosas rojas", "La Reina grito que le corten la cabeza a todos", "Alicia no tenia miedo porque eran solo naipes", "Al final desperto de su sueño bajo el arbol"]),
]

CAPITULOS_LIEBRE_TORTUGA: list[CapituloMecanografia] = [
    CapituloMecanografia(1, "El reto veloz", ["La liebre se burlaba de la tortuga por ser lenta", "Te apuesto una carrera le dijo la tortuga segura", "Todos los animales del bosque fueron a mirar", "La liebre acepto el reto riendo con muchas ganas"]),
    CapituloMecanografia(2, "La gran salida", ["El zorro dio la señal y la carrera comenzo ya", "La liebre salio disparada como una flecha veloz", "La tortuga caminaba paso a paso sin detenerse", "La meta estaba muy lejos pero ella tenia fe"]),
    CapituloMecanografia(3, "La siesta confiada", ["La liebre iba tan adelantada que decidio dormir", "Bajo un arbol fresco se quedo profundamente frita", "Pensaba que tenia tiempo de sobra para ganar hoy", "Mientras tanto la tortuga seguia avanzando lento"]),
    CapituloMecanografia(4, "Esfuerzo constante", ["El sol bajaba y la tortuga ya casi llegaba", "No se detuvo ni un segundo a descansar un poco", "Los animales gritaban animando a la gran valiente", "La liebre seguia soñando sin saber lo que pasaba"]),
    CapituloMecanografia(5, "Leccion aprendida", ["La liebre desperto y corrio con todas sus fuerzas", "Pero la tortuga ya habia cruzado la linea final", "La constancia siempre vence a la arrogancia loca", "Despacio se llega lejos le recordaron a la liebre"]),
]


LIBROS_MECANOGRAFIA: dict[str, LibroMecanografia] = {
    "el_principito": LibroMecanografia(
        id_libro="el_principito",
        titulo="El Principito",
        descripcion="Viaja por las estrellas y descubre el valor de la amistad en esta historia clásica.",
        capitulos=_capitulos_para_primaria(CAPITULOS_PRINCIPITO),
    ),
    "don_quijote": LibroMecanografia(
        id_libro="don_quijote",
        titulo="Don Quijote de la Mancha",
        descripcion="Acompaña al ingenioso hidalgo en sus locas aventuras contra gigantes y molinos.",
        capitulos=_capitulos_para_primaria(CAPITULOS_DON_QUIJOTE),
    ),
    "los_tres_cerditos": LibroMecanografia(
        id_libro="los_tres_cerditos",
        titulo="Los Tres Cerditos",
        descripcion="Aprende que la constancia y el trabajo duro siempre rinden frutos.",
        capitulos=_capitulos_para_primaria(CAPITULOS_TRES_CERDITOS),
    ),
    "pinocho": LibroMecanografia(
        id_libro="pinocho",
        titulo="Pinocho",
        descripcion="Descubre el camino hacia la verdad y la honestidad con el muñeco de madera más famoso.",
        capitulos=_capitulos_para_primaria(CAPITULOS_PINOCHO),
    ),
    "alicia_maravillas": LibroMecanografia(
        id_libro="alicia_maravillas",
        titulo="Alicia en el País de las Maravillas",
        descripcion="Sigue al conejo blanco hacia un mundo de fantasía y lógica disparatada.",
        capitulos=_capitulos_para_primaria(CAPITULOS_ALICIA),
    ),
    "liebre_tortuga": LibroMecanografia(
        id_libro="liebre_tortuga",
        titulo="La Liebre y la Tortuga",
        descripcion="Una carrera épica que enseña que la constancia siempre gana a la prisa.",
        capitulos=_capitulos_para_primaria(CAPITULOS_LIEBRE_TORTUGA),
    ),
}
