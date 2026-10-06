# Cómo contribuir

## Añadir un nuevo módulo educativo

1. Crea un paquete bajo `modulos/` y elige su ruta Python de entrada. La ruta no tiene que llamarse `main_<modulo>.py`; debe coincidir exactamente con `import_path` en el registro.
2. Expón una función `crear_frame(parent, on_back_callback)` que cree y devuelva una vista `CTkFrame` compatible con el panel principal.
3. Registra el identificador y la ruta de importación en `core/module_factory.py` → `ModuleFactory.SUBJECTS`.
4. Añade la materia al estado inicial de `core/gestor_estado.py` → `_estado_default()`.
5. Añade una entrada de tema en `MODULO_THEMES` de `main.py`.
6. Añade el identificador y su posición/descripción en `vista_inicio()` de `main.py`; las tarjetas se generan a partir del orden y la configuración del menú.
7. Define los logros aplicables en `core/logros_config.py` y conecta los logros por acción si corresponde.
8. Añade los recursos de tarjeta bajo `assets/imagenes/` y referencia su nombre en el registro.
9. Añade pruebas de dominio y/o de contrato en `tests/`, sin iniciar una interfaz gráfica para probar lógica pura.

## Flujo de trabajo

```bash
git checkout -b feature/mi-modulo
git commit -m "feat: añadir módulo X"
git push origin feature/mi-modulo
```

Después, abre un Pull Request hacia `main`.

## Estilo

- Sigue PEP 8 y las convenciones de los archivos relacionados.
- El contrato `crear_frame(parent, on_back_callback)` es obligatorio para los módulos registrados.
- No rompas los tests existentes; ejecuta `pytest tests/ -v` antes de enviar el cambio.
