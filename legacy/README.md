# Codigo legacy

Esta carpeta conserva interfaces antiguas que no forman parte del flujo activo
de la aplicacion. Se mantienen solo como referencia para una posible migracion
manual; no deben importarse desde el codigo principal.

- `dibujo_menu.py`: menu antiguo de Dibujo. `ModuleFactory` carga actualmente
  `modulos.Dibujo.vistas.app.paint_app.crear_frame`.
- `ui_helpers.py`: antigua barra de navegacion (`crear_navbar`), sin usos en el
  proyecto.

No se borraron para preservar su implementacion, pero cualquier funcionalidad
nueva debe integrarse en la arquitectura activa, no depender de estos archivos.