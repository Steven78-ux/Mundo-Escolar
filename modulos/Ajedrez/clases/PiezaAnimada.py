import pygame
import os


class PiezaAnimada:
    def __init__(self, nombre, color, fila, col, tam_cuadro):
        self.nombre = nombre
        self.color = color
        self.fila = fila
        self.col = col
        self.tam_cuadro = tam_cuadro
        self.ha_movido = False

        # --- AJUSTE DE TAMAÑO (80% de la casilla) ---
        self.factor_escala = 0.80
        self.tam_pieza = int(self.tam_cuadro * self.factor_escala)
        self.margen = (self.tam_cuadro - self.tam_pieza) // 2

        # --- Posición visual para la animación ---
        self.x = col * tam_cuadro
        self.y = fila * tam_cuadro

        # Velocidad de la animación
        self.velocidad_animacion = 0.30

        self.imagen = None
        self.cargar_imagen()

    def dibujar(self, pantalla):
        """Calcula el movimiento fluido y dibuja la pieza limpia (sin sombra)."""
        # El destino es la coordenada del cuadro
        destino_x = self.col * self.tam_cuadro
        destino_y = self.fila * self.tam_cuadro

        # Suavizado de movimiento (Interpolación)
        diff_x = destino_x - self.x
        diff_y = destino_y - self.y

        if abs(diff_x) < 0.5:
            self.x = destino_x
        else:
            self.x += diff_x * self.velocidad_animacion

        if abs(diff_y) < 0.5:
            self.y = destino_y
        else:
            self.y += diff_y * self.velocidad_animacion

        if self.imagen:
            # --- DIBUJO DE LA PIEZA ---
            # Dibujamos directamente la imagen centrada con el margen
            pantalla.blit(self.imagen, (self.x + self.margen, self.y + self.margen))

    def cargar_imagen(self):
        """Carga la imagen y la escala al tamaño reducido."""
        try:
            dir_clases = os.path.dirname(os.path.abspath(__file__))
            ruta_raiz = os.path.dirname(dir_clases)
            ruta_carpeta = os.path.join(ruta_raiz, "assets", "piezas_animadas")

            color_normalizado = (
                "blanco" if self.color in ["blanco", "blanca"] else "negro"
            )
            nombre_base = f"{self.nombre}_{color_normalizado}"

            ruta_png = os.path.join(ruta_carpeta, f"{nombre_base}.png")
            ruta_jpg = os.path.join(ruta_carpeta, f"{nombre_base}.jpg")

            if os.path.exists(ruta_png):
                ruta_final = ruta_png
            elif os.path.exists(ruta_jpg):
                ruta_final = ruta_jpg
            else:
                raise FileNotFoundError(f"No se encontró {nombre_base}")

            imagen_temp = pygame.image.load(ruta_final).convert_alpha()

            if ruta_final.endswith(".jpg"):
                imagen_temp.set_colorkey((255, 255, 255))

            self.imagen = pygame.transform.smoothscale(
                imagen_temp, (self.tam_pieza, self.tam_pieza)
            )

        except Exception as e:
            print(f"Error cargando {self.nombre}_{self.color}: {e}")
            self.imagen = pygame.Surface((self.tam_pieza, self.tam_pieza))
            self.imagen.fill((255, 0, 255))

    def __getstate__(self):
        state = self.__dict__.copy()
        state["imagen"] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.cargar_imagen()
