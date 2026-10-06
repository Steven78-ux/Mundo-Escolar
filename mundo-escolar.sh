#!/bin/bash
cd /usr/share/mundo-escolar

# Verificar si tkextrafont está instalado, si no, intentar instalarlo
python3 -c "import tkextrafont" 2>/dev/null || pip3 install tkextrafont --user

# Ejecutar la aplicación
python3 main.py
