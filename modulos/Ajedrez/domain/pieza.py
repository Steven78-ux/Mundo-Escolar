"""Dominio del módulo domain."""

class Pieza:
    """Representación lógica de una pieza de ajedrez."""

    def __init__(self, tipo, color, fila, col):
        self.tipo = tipo  # 'peon', 'torre', 'caballo', 'alfil', 'dama', 'rey'
        self.color = color  # 'blanco', 'negro'
        self.fila = fila
        self.col = col
        self.ha_movido = False

    def __repr__(self):
        return f"{self.color[:1].upper()}{self.tipo[:2]} ({self.fila},{self.col})"