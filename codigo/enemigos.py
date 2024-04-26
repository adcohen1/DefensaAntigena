import math

import pygame as pg
from pygame.math import Vector2


class Enemigo(pg.sprite.Sprite):
    def __init__(self, waypoints, imagen):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.velocidad = 2
        self.angulo = 0
        self.imagen_original = imagen
        self.image = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.mover()
        self.rotar()

    def mover(self):
        # definir a punto objetivo
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movimiento = self.target - self.pos
        else:
            # El enemigo ha llegado al final del camino
            self.kill()

        # calcular la distancia al objetivo
        dist = self.movimiento.length()
        # verificar si la distancia restante es mayor que la velocidad del enemigo
        if dist >= self.velocidad:
            self.pos += self.movimiento.normalize() * self.velocidad
        else:
            if dist != 0:
                self.pos += self.movimiento.normalize() * dist
            self.target_waypoint += 1

    def rotar(self):
        # Calsular la distancia al siguiente punto objetivo
        dist = self.target - self.pos

        # Usar la distancia para calcular el angulo
        self.angulo = math.degrees(math.atan2(-dist[1], dist[0]))

        # Rotar la imagen y actualizar el rectangulo
        self.image = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
