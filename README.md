# Mundo Escolar

Aplicación educativa de escritorio que reúne cinco módulos interactivos en una interfaz común. El menú principal permite seleccionar una actividad y consultar perfiles, progreso y logros. Las vistas de los módulos se cargan en el panel de la aplicación a través de un punto de entrada compartido.

## Módulos

| Módulo | Punto de entrada registrado |
|---|---|
| Lectura y Escritura | `modulos/Lenguaje/lenguaje_menu.py` |
| Ajedrez | `modulos/Ajedrez/main_ajedrez.py` |
| Computación | `modulos/Computacion/computacion_menu.py` |
| Robótica | `modulos/Robotica/robotica_menu.py` |
| Dibujo | `modulos/Dibujo/vistas/app/paint_app.py` |

## Requisitos e instalación

El proyecto usa Python, CustomTkinter, Pillow, `tkextrafont` y Pygame. Ajedrez y Computación tienen archivos de dependencias adicionales. Para instalar:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-ajedrez.txt
python -m pip install -r requirements-computacion.txt
```

Los requisitos opcionales de cada módulo pueden omitirse si no se va a utilizar ese módulo.

## Motor de Ajedrez (Stockfish)

El módulo de Ajedrez usa [Stockfish](https://stockfishchess.org/) como motor de IA. Sus binarios no están incluidos en el repositorio por su tamaño (aproximadamente 220 MB).

Descarga el binario correspondiente a tu sistema desde [stockfishchess.org/download](https://stockfishchess.org/download/):

- **Linux / ChromeOS:** `stockfish-ubuntu-x86-64`
- **Windows:** `stockfish-windows-x86-64`

Colócalo en la ruta correspondiente:

- **Linux:** `modulos/Ajedrez/assets/stockfish linux/stockfish`
- **Windows:** `modulos/Ajedrez/assets/stockfish/stockfish.exe`

Para verificar que el módulo puede cargarse, ejecuta desde la raíz del proyecto:

```bash
python -c "from modulos.Ajedrez.services.motor_ia import *; print('OK')"
```

En Linux, asegúrate también de que el binario tenga permisos de ejecución:

```bash
chmod +x "modulos/Ajedrez/assets/stockfish linux/stockfish"
```

## Ejecución

```bash
python main.py
```

En Linux o ChromeOS también se incluye `mundo-escolar.sh`.

## Arquitectura

El proyecto sigue una arquitectura por capas con un estilo hub-and-spoke: `main.py` crea la interfaz principal y coordina la navegación; `core/module_factory.py` registra los módulos e importa su código cuando se seleccionan; cada módulo aporta una vista `crear_frame(parent, on_back_callback)`. `core/module_manager.py` gestiona la vista activa y el atajo Escape.

`core/gestor_estado.py` centraliza el estado del usuario en archivos JSON bajo `core/data/usuarios/`. `core/theme.py` contiene estilos compartidos y `core/logros_config.py` define los tipos y requisitos de logros.

```text
.
├── core/           # Estado, tema, logros y gestión/fábrica de módulos
├── modulos/        # Lenguaje, Ajedrez, Computación, Robótica y Dibujo
├── assets/         # Recursos de la interfaz principal
├── tests/          # Pruebas de contrato y de lógica de dominio
├── docs/           # Arquitectura, métricas, validación y estándares
├── legacy/         # Código conservado fuera del flujo activo
├── main.py
└── requirements*.txt
```

Para el detalle de capas, estado inicial y flujo de carga, consulta [docs/architecture.md](docs/architecture.md).

## Tests

Instala las dependencias de desarrollo y ejecuta las pruebas:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

El workflow de GitHub Actions ejecuta los tests en Ubuntu con Python 3.11.

## Contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para las instrucciones de cambios y módulos, y [CONTRIBUTORS.md](CONTRIBUTORS.md) para los créditos del equipo.

## Documentación adicional

- [Métricas de ingeniería](docs/metrics.md)
- [Validación en campo](docs/field-validation.md)
- [Estándares y metodología](docs/standards.md)
- [Auditoría de rutas](docs/audit-rutas.md)

## Licencia

El proyecto incluye la licencia MIT en [LICENSE](LICENSE).
