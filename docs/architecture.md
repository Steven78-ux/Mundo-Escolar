# Arquitectura del Sistema

## Visión general

Mundo Escolar utiliza una arquitectura hub-and-spoke: `main.py` es el hub que construye la ventana principal, el menú y el panel de contenido; los cinco módulos educativos son spokes seleccionables. El catálogo `ModuleFactory.SUBJECTS` relaciona cada identificador con la ruta importable de su punto de entrada. Cuando se selecciona una materia, la fábrica importa ese módulo y solicita su vista para incrustarla en el panel.

Las piezas compartidas incluyen `GestorEstado` para el progreso y los logros persistidos, `core.theme` para los estilos comunes y `ModuleManager` para registrar la vista activa y gestionar su cierre con Escape. Los módulos consultan o actualizan el estado compartido mientras conservan sus propias vistas y lógica educativa. La composición verificada en código es:

```text
main.py (hub / ventana principal)
  ├── ModuleFactory ── importa y crea la vista del módulo seleccionado
  ├── GestorEstado ─── progreso y logros del usuario
  ├── core.theme ───── estilos compartidos
  └── módulos (spokes)
       ├── Lectura y Escritura
       ├── Ajedrez
       ├── Computación
       ├── Robótica
       └── Dibujo
```

## Diagrama de capas

```text
Presentación
  main.py, tema compartido y vistas de los cinco módulos
                  │
                  ├── invoca lógica de módulos y administra la navegación
                  ▼
Dominio
  reglas y modelos educativos/juegos; configuración de logros
                  │
                  ├── estado consultado y actualizado por GestorEstado
                  ▼
Persistencia
  GestorEstado ── archivos JSON en core/data/usuarios/
```

Las capas no son paquetes completamente aislados: los puntos de entrada de los módulos conectan sus vistas con el estado compartido, y `main.py` contiene tanto composición de interfaz como evaluación visual de logros.

## Capa de Presentación

- **Tecnología:** Python con CustomTkinter (sobre Tkinter), Pillow para imágenes y `tkextrafont` para fuentes.
- **Archivos principales:**
  - `main.py`
  - `core/module_factory.py`
  - `core/module_manager.py`
  - `core/theme.py`
  - `modulos/Lenguaje/lenguaje_menu.py`
  - `modulos/Ajedrez/main_ajedrez.py`
  - `modulos/Computacion/computacion_menu.py`
  - `modulos/Robotica/robotica_menu.py`
  - `modulos/Dibujo/vistas/app/paint_app.py`
- **Responsabilidad:** construir la ventana, el menú, vistas y temas; cargar el módulo escogido en el panel principal; facilitar navegación de regreso y cierre de la vista activa.

## Capa de Dominio

Los siguientes archivos de lógica/configuración no importan Tkinter directamente:

- `core/logros_config.py`
- `modulos/Ajedrez/domain/partida.py`
- `modulos/Ajedrez/domain/partida_tutorial.py`
- `modulos/Ajedrez/domain/pieza.py`
- `modulos/Ajedrez/domain/tablero_logico.py`
- `modulos/Computacion/domain/base_module.py`
- `modulos/Computacion/domain/texts.py`
- `modulos/Lenguaje/dominio/juegos.py`
- `modulos/Robotica/robotica_dominio.py`

Estos archivos definen reglas y datos de juegos, preguntas, piezas, partidas y logros. `core/gestor_estado.py` también evita importar Tkinter, pero se describe en Persistencia por su responsabilidad de guardar y cargar estado. La implementación de dominio de Dibujo está integrada en `modulos/Dibujo/vistas/app/paint_app.py`; no se encontró un paquete separado de dominio para ese módulo.

## Capa de Persistencia

`GestorEstado` centraliza el acceso a los datos de usuario y tiene una única instancia mediante `__new__` (Singleton). Carga y guarda JSON directamente con la biblioteca estándar `json` en `core/data/usuarios/`, usando un nombre de archivo saneado basado en el usuario. Su responsabilidad es similar a un repositorio de estado; el código no define una interfaz formal o repositorio genérico separado.

- **Formato:** JSON UTF-8.
- **Archivo de usuario:** `core/data/usuarios/<nombre_seguro>.json`.
- **Archivo de control de limpieza:** `core/data/usuarios/ultima_limpieza.json`.
- **Esquema inicial (`_estado_default`):**

```json
{
  "materias": {
    "Lectura y Escritura": 0.0,
    "Ajedrez": 0.0,
    "Computación": 0.0,
    "Robotica": 0.0,
    "Dibujo": 0.0
  },
  "logros_obtenidos": [],
  "robotica": {
    "misiones_completadas": 0,
    "monedas": 0,
    "niveles_completados": [],
    "dificultad": "basico"
  }
}
```

## Patrón ModuleFactory

`ModuleFactory.SUBJECTS` es el registro de los identificadores y rutas de importación. `get_module_frame(subject_id, parent, on_back_callback)`:

1. Busca la configuración del identificador; si no existe, devuelve `None`.
2. Importa la ruta configurada con `importlib.import_module()` y obtiene el callable indicado (actualmente `crear_frame`). Si la importación o el atributo falla, registra la excepción y devuelve `None`.
3. Invoca el callable con el padre y el callback de regreso.
4. Si recibe una vista, almacena el callback, enlaza Escape con el retorno y la registra en `ModuleManager`.
5. Devuelve la vista. Si ocurre una excepción durante su creación o configuración, la registra y devuelve `None`.

La importación bajo demanda evita cargar la implementación del módulo hasta que se solicita (lazy loading). El registro desacopla la selección de materia de la ruta concreta de importación y permite agregar una entrada para ampliar la oferta (beneficio alineado con OCP); no elimina la necesidad de actualizar otras interfaces que presenten los módulos.

## Sistema de logros

`core/logros_config.py` define los registros con `id`, nombre, descripción, tipo, enlace, requisito y color. El código utiliza tres tipos:

| Tipo | Condición observada |
|---|---|
| `porcentaje` | `GestorEstado.actualizar_progreso` incrementa el porcentaje de una materia (con tope 1.0) y `_sincronizar_logros_porcentaje` registra los logros de esa materia cuyo requisito se alcanza. |
| `accion` | La actividad correspondiente registra el identificador mediante `GestorEstado.desbloquear_logro`; la vista de logros solo lo muestra como desbloqueado si ya está registrado. |
| `general` | La evaluación de la vista de logros considera desbloqueado `general_3` al tener al menos tres materias con progreso de 0.99 o superior, y `general_todas` al alcanzar todas las materias. Esta evaluación se realiza en `main.py`. |

Los logros registrados se guardan en `logros_obtenidos` como una lista JSON; en memoria se manejan como conjunto.

## Contrato de módulos

```python
def crear_frame(parent, on_back_callback) -> CTkFrame
```

Los cinco módulos de `ModuleFactory.SUBJECTS` tienen una función `crear_frame(parent, on_back_callback)` en la ruta registrada:

| Identificador | Archivo |
|---|---|
| `lectura_escritura` | `modulos/Lenguaje/lenguaje_menu.py` |
| `ajedrez` | `modulos/Ajedrez/main_ajedrez.py` |
| `computacion` | `modulos/Computacion/computacion_menu.py` |
| `robotica` | `modulos/Robotica/robotica_menu.py` |
| `dibujo` | `modulos/Dibujo/vistas/app/paint_app.py` |

Cada función crea y devuelve una vista `CTkFrame` compatible con el panel. Las funciones no declaran anotaciones de tipo en el código revisado; la firma anterior expresa el contrato esperado por `ModuleFactory`.
