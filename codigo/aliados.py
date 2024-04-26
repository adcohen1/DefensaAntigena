import pygame as pg

import constantes as c


class Turret(pg.sprite.Sprite):
    def __init__(self, imagen, fila, columna):
        pg.sprite.Sprite.__init__(self)
        self.fila = fila
        self.columna = columna
        # calcular coordenada del centro
        self.x = (self.fila + 0.5) * c.TILE_SIZE
        self.y = (self.columna + 0.5) * c.TILE_SIZE
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
