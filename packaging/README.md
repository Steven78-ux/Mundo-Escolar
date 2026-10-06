# Empaquetado Debian

## Construir el paquete

Desde la raíz del repositorio, en Debian o en otra distribución Linux con las
herramientas requeridas, ejecuta:

```sh
python3 preparar_deb.py
fakeroot dpkg-deb --build mundo-escolar-pkg packaging/mundo-escolar_1.0.0_all.deb
```

El primer comando prepara el árbol `mundo-escolar-pkg/` con la estructura de
archivos del paquete. El segundo genera
`packaging/mundo-escolar_1.0.0_all.deb`. Si el script solicita dependencias
locales que no se encuentran en Debian, sigue las instrucciones que muestra
antes de construir el paquete.

## Requisitos

- `dpkg-deb`, para construir el archivo `.deb`.
- `fakeroot`, para ejecutar la construcción con permisos de root simulados.
- Python 3, para ejecutar `preparar_deb.py`.

## Archivos

- `README.md`: estas instrucciones para construir el paquete.
- `debian/control`: metadatos del paquete, como versión, mantenedor,
  dependencias y descripción. `preparar_deb.py` lo copia a
  `mundo-escolar-pkg/DEBIAN/control`.
- `mundo-escolar_1.0.0_all.deb`: artefacto generado; no se versiona.
