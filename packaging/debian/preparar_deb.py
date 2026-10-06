"""Preparación del paquete de instalación para ChromeOS/Linux."""

import os
import shutil

# Configuración
NOMBRE_APP = "mundo-escolar"
VERSION = "1.0.0"

# Obtener la ruta absoluta donde se encuentra este script para evitar errores de ruta
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CARPETA_PKG = os.path.join(BASE_PATH, f"{NOMBRE_APP}-pkg")
RUTA_CONTROL = os.path.join(BASE_PATH, "packaging", "debian", "control")

def crear_estructura():
    """Crea la estructura del paquete y copia los archivos requeridos para ChromeOS."""
    print("--- Iniciando preparación del paquete para ChromeOS ---")
    
    # 1. Crear rutas de Linux
    rutas = [
        os.path.join(CARPETA_PKG, "DEBIAN"),
        os.path.join(CARPETA_PKG, "usr/bin"),
        os.path.join(CARPETA_PKG, "usr/share/applications"),
        os.path.join(CARPETA_PKG, "usr/share", NOMBRE_APP),
        os.path.join(CARPETA_PKG, "usr/share", NOMBRE_APP, "lib")
    ]
    
    for ruta in rutas:
        os.makedirs(ruta, exist_ok=True)

    # Archivos de configuración requeridos
    archivos_config = ["mundo-escolar.desktop", "mundo-escolar.sh"]

    # Verificar que los archivos existan antes de intentar copiar
    for archivo in archivos_config:
        ruta_src = os.path.join(BASE_PATH, archivo)
        if not os.path.exists(ruta_src):
            print(f"\n[ERROR] No se encontró el archivo: {archivo}")
            print(f"Asegúrate de que esté en: {BASE_PATH}")
            return

    if not os.path.exists(RUTA_CONTROL):
        print(f"\n[ERROR] No se encontró el archivo de control: {RUTA_CONTROL}")
        return

    # 2. Copiar archivos de configuración
    shutil.copy(RUTA_CONTROL, os.path.join(CARPETA_PKG, "DEBIAN", "control"))
    shutil.copy(os.path.join(BASE_PATH, "mundo-escolar.desktop"), os.path.join(CARPETA_PKG, "usr/share/applications/"))
    
    # Copiar y dar permisos de ejecución al lanzador
    destino_sh = os.path.join(CARPETA_PKG, "usr/bin", NOMBRE_APP)
    shutil.copy(os.path.join(BASE_PATH, "mundo-escolar.sh"), destino_sh)

    # 3. Copiar todo tu código y assets
    items_a_ignorar = [os.path.basename(CARPETA_PKG), "preparar_deb.py", ".git", "__pycache__", "packaging"] + archivos_config
    
    for item in os.listdir(BASE_PATH):
        if item not in items_a_ignorar and not item.endswith('.pyc'):
            origen = os.path.join(BASE_PATH, item)
            destino = os.path.join(CARPETA_PKG, "usr/share", NOMBRE_APP, item)
            if os.path.isdir(origen):
                shutil.copytree(origen, destino, dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
            else:
                shutil.copy(origen, destino)

    print(f"\n[!] PASO FINAL REQUERIDO EN WINDOWS:")
    print(f"1. Ve a tu carpeta de Python (site-packages).")
    print(f"2. COPIA las siguientes carpetas a {CARPETA_PKG}/usr/share/{NOMBRE_APP}/lib/:")
    print(f"   - customtkinter")
    print(f"   - tkextrafont")
    print(f"\n[!] NOTA SOBRE PYGAME Y PILLOW:")
    print(f"No las copies manualmente. El archivo 'packaging/debian/control' le dirá a ChromeOS")
    print(f"que las instale automáticamente en su versión para Linux.")
    print("\n--- Estructura lista en la carpeta 'mundo-escolar-pkg' ---")

if __name__ == "__main__":
    crear_estructura()