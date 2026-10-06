"""Servicios del módulo services."""

import os
import chess
import chess.engine
import random
import platform
import stat


class MotorIA:
    """Wrapper humanizado de Stockfish para niños."""

    def __init__(self, nivel="Hierro"):
        # Detección del sistema operativo
        self.sistema = platform.system()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if self.sistema == "Windows":
            print("SISTEMA: Detectado Windows. Usaremos el motor .exe")
            folder_name = "stockfish"
            filename = "stockfish-windows-x86-64.exe"
        else:
            print(f"SISTEMA: Detectado {self.sistema} (ChromeOS Flex/Linux). Usaremos el motor de Linux.")
            folder_name = "stockfish linux"
            filename = "stockfish-ubuntu-x86-64-avx2"

        self.ruta = os.path.abspath(os.path.join(base_dir, "assets", folder_name, filename))
        self.engine = None

        self.niveles = {
            "Hierro": {"skill": 2, "error": 0.25},
            "Bronce": {"skill": 5, "error": 0.20},
            "Plata": {"skill": 8, "error": 0.15},
            "Oro": {"skill": 11, "error": 0.10},
            "Diamante": {"skill": 14, "error": 0.05},
            "Maestro": {"skill": 17, "error": 0.02},
            "Gran Maestro": {"skill": 20, "error": 0.01},
            "Élite": {"skill": 20, "error": 0.0},
            "Galáctico": {"skill": 20, "error": 0.0},
            "Estelar": {"skill": 20, "error": 0.0},
            "Solar": {"skill": 20, "error": 0.0},
            "Místico": {"skill": 20, "error": 0.0},
            "Dios de la IA": {"skill": 20, "error": 0.0},
        }

        self.nivel_nombre = nivel if isinstance(nivel, str) else "Hierro"
        self.nivel_nombre = self.nivel_nombre if self.nivel_nombre in self.niveles else "Hierro"

        # Verificación preventiva para evitar que el programa se cierre sin explicación
        if not os.path.exists(self.ruta):
            print(f"ADVERTENCIA: No se encontró el motor en {self.ruta}. La IA jugará al azar.")
            self.ruta = None
        elif self.sistema != "Windows":
            try:
                st = os.stat(self.ruta)
                os.chmod(self.ruta, st.st_mode | stat.S_IEXEC)
            except Exception as e:
                print(f"SISTEMA: No se pudo auto-asignar permisos a {self.ruta}: {e}")

        if self.ruta:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.ruta)
                self.engine.configure({"Threads": 1})
                self.engine.configure({"Hash": 16})
                self.engine.configure({"Skill Level": self.niveles[self.nivel_nombre]["skill"]})
            except Exception as e:
                print(f"ADVERTENCIA: No se pudo iniciar el motor Stockfish ({e}). La IA jugará al azar.")
                self.engine = None

    def obtener_mejor_jugada(self, fen, nivel_nombre):
        config = self.niveles.get(nivel_nombre, self.niveles["Hierro"])
        board = chess.Board(fen)

        if random.random() < config["error"] or not self.engine:
            return random.choice(list(board.legal_moves))

        try:
            pensamiento = 0.05
            if nivel_nombre == "Dios de la IA":
                pensamiento = 1.5
            elif nivel_nombre in ["Místico", "Solar", "Estelar"]:
                pensamiento = 0.3
            elif nivel_nombre in ["Galáctico", "Élite"]:
                pensamiento = 0.15

            result = self.engine.play(board, chess.engine.Limit(time=pensamiento))
            return result.move
        except Exception as e:
            print(f"Error al pedir jugada a Stockfish: {e}")
            return random.choice(list(board.legal_moves))

    def close(self):
        if self.engine:
            try:
                self.engine.quit()
            except Exception:
                pass
            self.engine = None