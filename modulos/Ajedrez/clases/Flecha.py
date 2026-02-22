import pygame
import math


class Flecha:
    def __init__(self, fila_inicio, col_inicio, fila_fin, col_fin, color, tam_cuadro):
        # --- Lógica de Tablero (Indispensable para comparaciones) ---
        self.inicio_tablero = (fila_inicio, col_inicio)
        self.fin_tablero = (fila_fin, col_fin)

        # Usamos el color pero aseguramos que tenga un valor Alpha (Transparencia)
        # Si el color viene como (R, G, B), le añadimos 160 de opacidad
        if len(color) == 3:
            self.color = (*color, 160)
        else:
            self.color = color

        self.tam_cuadro = tam_cuadro

        # Coordenadas de píxeles centradas para el dibujo
        self.inicio = pygame.Vector2(
            col_inicio * tam_cuadro + tam_cuadro // 2,
            fila_inicio * tam_cuadro + tam_cuadro // 2,
        )
        self.fin = pygame.Vector2(
            col_fin * tam_cuadro + tam_cuadro // 2,
            fila_fin * tam_cuadro + tam_cuadro // 2,
        )

    def __eq__(self, otra):
        """Permite comparar si dos flechas son iguales lógicamente por posición"""
        if not isinstance(otra, Flecha):
            return False
        # No comparamos el color aquí para que un clic derecho
        # pueda borrar la flecha sin importar el color actual seleccionado.
        return (
            self.inicio_tablero == otra.inicio_tablero
            and self.fin_tablero == otra.fin_tablero
        )

    def dibujar(self, superficie):
        # 1. Configuración de estilo
        ancho_cuerpo = 12
        radio_punta = 22  # Tamaño de la cabeza de la flecha

        # 2. Crear una superficie temporal transparente del tamaño de la pantalla
        temp_surface = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)

        # 3. Calcular dirección y ángulos
        direccion = self.fin - self.inicio
        if direccion.length() == 0:
            return  # Evitar error si el inicio y fin son iguales

        angulo = math.atan2(-direccion.y, direccion.x)

        # Acortamos un poco el cuerpo para que no sobresalga de la punta
        fin_cuerpo = self.fin - direccion.normalize() * (radio_punta * 0.8)

        # 4. Dibujar el cuerpo (Línea gruesa)
        pygame.draw.line(
            temp_surface, self.color, self.inicio, fin_cuerpo, ancho_cuerpo
        )

        # 5. Dibujar la punta (Triángulo estilizado)
        punto1 = self.fin  # La punta misma

        # Las dos esquinas de la base del triángulo
        offset_angulo = math.radians(150)  # Apertura de la punta
        punto2 = (
            self.fin
            + pygame.Vector2(
                math.cos(angulo + offset_angulo), -math.sin(angulo + offset_angulo)
            )
            * radio_punta
        )

        punto3 = (
            self.fin
            + pygame.Vector2(
                math.cos(angulo - offset_angulo), -math.sin(angulo - offset_angulo)
            )
            * radio_punta
        )

        pygame.draw.polygon(temp_surface, self.color, [punto1, punto2, punto3])

        # 6. Transferir la flecha transparente a la pantalla principal
        superficie.blit(temp_surface, (0, 0))
