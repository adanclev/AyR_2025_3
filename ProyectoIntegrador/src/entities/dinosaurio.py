from ProyectoIntegrador.src.settings import SUELO_Y, ANCHO_DINO, ALTO_DINO, COLOR_DINO
import pygame as pg

class Dinosaurio:
    def __init__(self, alto=ALTO_DINO, ancho=ANCHO_DINO, color=COLOR_DINO, modelo=None):
        self.x = 50
        self.y = SUELO_Y
        self.alto = alto
        self.ancho = ancho
        self.color = color
        self.vel_y = 0
        self.saltando = False
        self.vivo = True
        self.score = 0
        self.rect = pg.Rect(self.x, self.y - self.alto, self.ancho, self.alto)

    def update(self):
        if not self.vivo: return

        # Física
        self.vel_y += 0.8
        self.y += self.vel_y
        if self.y >= SUELO_Y:
            self.y = SUELO_Y
            self.vel_y = 0
            self.saltando = False
        self.rect.y = self.y - self.alto

        self.score += 1

        '''# Pensar
        self.pensar(obstaculos, vel_mundo)'''

    '''def pensar(self, obstaculos, vel_mundo):
        # Buscar obstáculo siguiente
        obs_siguiente = None
        for obs in obstaculos:
            if obs.rect.right > self.rect.left:
                obs_siguiente = obs
                break

        if obs_siguiente:
            # Las 6 variables para la Red Neuronal
            inputs = [
                (SUELO_Y - self.y) / 100.0,  # x1
                (obs_siguiente.rect.x - self.rect.right) / 800.0,  # x2
                obs_siguiente.rect.width / 100.0,  # x3
                obs_siguiente.rect.height / 100.0,  # x4
                self.vel_y / 20.0,  # x5
                vel_mundo / 20.0  # x6
            ]

            # Usar Keras para decidir
            decision = predecir_accion(self.cerebro, inputs)

            if decision >= UMBRAL_SALTO and not self.saltando:
                self.saltar()'''

    def saltar(self):
        if not   self.saltando:
            self.vel_y = -15
            self.saltando = True

    def dibujar(self, screen):
        if self.vivo:
            pg.draw.rect(screen, self.color, self.rect)