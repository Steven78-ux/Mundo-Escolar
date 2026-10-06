# Auditoría de rutas

Al revisar archivos Python del proyecto no se encontraron rutas absolutas de máquina (`C:\...`, `/home/...`, `/Users/...` o `/tmp/...`).

Se encontraron rutas relativas y separadores de sistema de archivos escritos como cadenas. La mayoría se combinan con `os.path.join` y se anclan a `__file__` o a `BASE_DIR`, por lo que no dependen del directorio de trabajo actual; aun así, pueden migrarse a `pathlib.Path` para hacer explícitos los límites y la composición de rutas.

| Archivo y línea | Hallazgo | Reemplazo sugerido |
|---|---|---|
| `core/module_factory.py:32,40,48,56,69` | Metadatos de imagen expresados como `imagenes/<materia>.png`; se resuelven después desde `ASSETS_DIR` en `main.py`. | Guardar rutas relativas como `Path("imagenes") / "<materia>.png"` y convertir a `str` si la API de interfaz lo requiere. |
| `main.py:624` | Nombre relativo `imagenes/logo.png` pasado a `get_asset`, que lo ancla a `ASSETS_DIR`. | Resolverlo con `Path(ASSETS_DIR) / "imagenes" / "logo.png"` o adaptar `get_asset` para recibir `Path`. |
| `modulos/Robotica/servicios/audio.py:19` | Segmentos de ruta `..` y `assets/sonidos/lenguaje` combinados con `os.path.join` desde `__file__`. | Usar `Path(__file__).resolve().parent / ".." / ".." / "assets" / "sonidos" / "lenguaje"` y normalizar con `.resolve()`. |
| `modulos/Lenguaje/servicios/audio.py:56,58-63` | Rutas de assets se construyen con segmentos relativos `..` y nombres de carpetas en cadenas. | Construir las rutas con `Path` desde el directorio del módulo/servicio. |
| `preparar_deb.py:43,46,55` | Las cadenas destino incluyen separadores `/` dentro de argumentos de `os.path.join` (`usr/share/applications/`, `usr/share`, `usr/bin`). | Componer cada segmento con `Path` y `shutil.copy`/`copytree` usando esos objetos. |

Las cadenas con `/` usadas para representar notación ajedrecística (por ejemplo, filas FEN) son datos del dominio, no rutas de archivos, y no se consideran hallazgos de rutas.
