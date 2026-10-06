"""Prueba rápida del módulo de mecanografía para depuración local."""

from modulos.Computacion.services.game_utils import TypingModule

mod = TypingModule(libro_id='el_principito', capitulo_inicial=1)
text = mod.texto_objetivo
print('text:', repr(text))
print('len', len(text))
for idx, ch in enumerate(text):
    if idx == 2:
        mod._procesar_tecla('x')
        print('mistake 1', idx, mod.posicion_actual, mod.en_error, mod.errores_locales)
        mod._procesar_tecla(text[idx])
        print('correct after mistake', idx, mod.posicion_actual, mod.en_error, mod.errores_locales)
    else:
        mod._procesar_tecla(ch)
print('final pos', mod.posicion_actual, 'resultado', mod.resultado_final, 'errores', mod.errores_locales)
