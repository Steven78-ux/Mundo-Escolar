"""
Lógica de reglas pura del ajedrez.
"""


def esta_en_tablero(f, c):
    return 0 <= f < 8 and 0 <= c < 8


def obtener_pieza_en(piezas, f, c):
    return next((p for p in piezas if p.fila == f and p.col == c), None)


def es_movimiento_valido(pieza, n_f, n_c, piezas, en_passant_target=None):
    if not esta_en_tablero(n_f, n_c):
        return False

    df, dc = n_f - pieza.fila, n_c - pieza.col
    p_dest = obtener_pieza_en(piezas, n_f, n_c)
    if p_dest and p_dest.color == pieza.color:
        return False

    if pieza.tipo == "peon":
        dir = -1 if pieza.color == "blanco" else 1
        if dc == 0 and df == dir and not p_dest:
            return True
        if not pieza.ha_movido and dc == 0 and df == 2 * dir:
            if not obtener_pieza_en(piezas, pieza.fila + dir, pieza.col) and not p_dest:
                return True
        if abs(dc) == 1 and df == dir and p_dest:
            return True
        # Captura al paso
        if abs(dc) == 1 and df == dir and (n_f, n_c) == en_passant_target:
            return True
        return False

    if pieza.tipo == "caballo":
        return abs(df) * abs(dc) == 2

    if pieza.tipo == "alfil":
        if abs(df) != abs(dc):
            return False
        return camino_libre(pieza.fila, pieza.col, n_f, n_c, piezas)

    if pieza.tipo == "torre":
        if df != 0 and dc != 0:
            return False
        return camino_libre(pieza.fila, pieza.col, n_f, n_c, piezas)

    if pieza.tipo == "dama":
        if abs(df) != abs(dc) and df != 0 and dc != 0:
            return False
        return camino_libre(pieza.fila, pieza.col, n_f, n_c, piezas)

    if pieza.tipo == "rey":
        if abs(df) <= 1 and abs(dc) <= 1:
            return True

        # Enroque
        if not pieza.ha_movido and df == 0 and abs(dc) == 2:
            # El Rey debe estar en su casilla de origen para poder enrocar (e1 o e8)
            fila_inicio = 7 if pieza.color == "blanco" else 0
            if pieza.fila != fila_inicio or pieza.col != 4:
                return False
            col_torre = 7 if n_c == 6 else 0
            torre = obtener_pieza_en(piezas, pieza.fila, col_torre)
            if torre and torre.tipo == "torre" and not torre.ha_movido:
                # Verificar camino libre
                step = 1 if n_c == 6 else -1
                for c_check in range(pieza.col + step, col_torre, step):
                    if obtener_pieza_en(piezas, pieza.fila, c_check):
                        return False
                # Verificar que el rey no esté en jaque ni pase por casillas atacadas
                if esta_atacada(pieza.fila, pieza.col, pieza.color, piezas):
                    return False
                if esta_atacada(pieza.fila, pieza.col + step, pieza.color, piezas):
                    return False
                if esta_atacada(pieza.fila, pieza.col + 2 * step, pieza.color, piezas):
                    return False
                return True

    return False


def camino_libre(f1, c1, f2, c2, piezas):
    df = 0 if f2 == f1 else (1 if f2 > f1 else -1)
    dc = 0 if c2 == c1 else (1 if c2 > c1 else -1)
    f, c = f1 + df, c1 + dc
    while f != f2 or c != c2:
        if obtener_pieza_en(piezas, f, c):
            return False
        f, c = f + df, c + dc
    return True


def esta_atacada(f, c, color_defensor, piezas, en_passant_target=None):
    enemigo = "negro" if color_defensor == "blanco" else "blanco"
    for p in piezas:
        if p.color == enemigo and es_movimiento_valido(p, f, c, piezas, en_passant_target):
            return True
    return False


def obtener_movimientos_legales(pieza, piezas, en_passant_target=None):
    """
    Genera movimientos legales filtrando aquellos que dejan al rey en jaque.
    Optimizado para no revisar las 64 casillas innecesariamente.
    """
    pseudo_legales = []

    # Generación optimizada por tipo de pieza
    if pieza.tipo == "peon":
        dirs = [-1, -2] if pieza.color == "blanco" else [1, 2]
        for df in dirs:
            pseudo_legales.append((pieza.fila + df, pieza.col))
        for dc in [-1, 1]:
            pseudo_legales.append(
                (pieza.fila + (1 if pieza.color == "negro" else -1), pieza.col + dc)
            )
    elif pieza.tipo == "caballo":
        for df, dc in [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]:
            pseudo_legales.append((pieza.fila + df, pieza.col + dc))
    elif pieza.tipo in ["alfil", "torre", "dama", "rey"]:
        # Para piezas deslizantes y rey, revisamos rangos cercanos o líneas
        for f in range(8):
            for c in range(8):
                if abs(f - pieza.fila) <= 8 and abs(c - pieza.col) <= 8:
                    pseudo_legales.append((f, c))

    legales = []
    f_ori, c_ori = pieza.fila, pieza.col

    for f, c in pseudo_legales:
        if es_movimiento_valido(pieza, f, c, piezas, en_passant_target):
            # Simulación de movimiento
            p_cap = obtener_pieza_en(piezas, f, c)
            if p_cap:
                piezas.remove(p_cap)
            pieza.fila, pieza.col = f, c

            rey = next(
                (p for p in piezas if p.tipo == "rey" and p.color == pieza.color), None
            )

            # En el tutorial el rey puede no existir
            if rey is None or not esta_atacada(rey.fila, rey.col, pieza.color, piezas):
                legales.append((f, c))

            # Revertir simulación
            pieza.fila, pieza.col = f_ori, c_ori
            if p_cap:
                piezas.append(p_cap)

    return legales
