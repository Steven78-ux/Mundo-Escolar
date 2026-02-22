import chess
import chess.engine


class BotAjedrez:
    def __init__(self, ruta_motor, color="negro"):
        self.color = color
        try:
            # Importante: Asegúrate de que la ruta termine en .exe en Windows
            self.engine = chess.engine.SimpleEngine.popen_uci(ruta_motor)
        except Exception as e:
            print(f"No se pudo cargar Stockfish: {e}")
            self.engine = None

    def transformar_a_chess_board(self, juego):
        """Convierte las piezas de Pygame a un objeto chess.Board"""
        board = chess.Board()
        board.clear_board()

        # Mapeo de nombres de tus piezas a constantes de la librería chess
        mapeo_piezas = {
            "peon": chess.PAWN,
            "torre": chess.ROOK,
            "caballo": chess.KNIGHT,
            "alfil": chess.BISHOP,
            "dama": chess.QUEEN,
            "rey": chess.KING,
        }

        for p in juego.piezas:
            color = chess.WHITE if p.color == "blanco" else chess.BLACK
            tipo = mapeo_piezas.get(p.nombre)
            if tipo:
                # Convertir coordenadas (fila 0 en Pygame es 7 en chess.Board)
                casilla = chess.square(p.col, 7 - p.fila)
                board.set_piece_at(casilla, chess.Piece(tipo, color))

        # Sincronizar el turno
        board.turn = chess.WHITE if juego.turno == "blanco" else chess.BLACK

        # Nota: Para enroques y peón al paso avanzados, se requeriría
        # sincronizar board.castling_rights y board.ep_square si fuera necesario.
        return board

    def seleccionar_movimiento(self, juego, tiempo_limite=1.0):
        """Recibe la instancia de la clase Juego y devuelve el movimiento elegido"""
        if not self.engine:
            return None

        # 1. Convertimos tu juego actual a un tablero lógico
        board_logico = self.transformar_a_chess_board(juego)

        try:
            # 2. Stockfish analiza el tablero lógico
            resultado = self.engine.play(
                board_logico, chess.engine.Limit(time=tiempo_limite)
            )
            movimiento = resultado.move

            # 3. Traducimos el movimiento de vuelta a tu sistema (fila, col)
            # movimiento.from_square y to_square devuelven índices 0-63
            f_orig = 7 - chess.square_rank(movimiento.from_square)
            c_orig = chess.square_file(movimiento.from_square)
            f_dest = 7 - chess.square_rank(movimiento.to_square)
            c_dest = chess.square_file(movimiento.to_square)

            # Buscamos la pieza en tu lista de Pygame que está en el origen
            pieza_a_mover = next(
                (p for p in juego.piezas if p.fila == f_orig and p.col == c_orig), None
            )

            if pieza_a_mover:
                return pieza_a_mover, f_dest, c_dest

        except Exception as e:
            print(f"Error durante el análisis del motor: {e}")

        return None

    def __del__(self):
        """Cerrar el motor cuando se destruya el bot"""
        if self.engine:
            self.engine.quit()
