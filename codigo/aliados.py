import math

import pygame as pg

import constantes as c
from datos_torretas import DATOS_TORRETAS


class Turret(pg.sprite.Sprite):
    def __init__(self, hojas_sprites, fila, columna):
        pg.sprite.Sprite.__init__(self)
        self.nivel_mejora = 1
        self.rango = DATOS_TORRETAS[self.nivel_mejora - 1].get('rango')
        self.cooldown = DATOS_TORRETAS[self.nivel_mejora - 1].get('cooldown')
        self.ultimo_disparo = pg.time.get_ticks()
        self.seleccionado = False
        self.objetivo = None

        # posicion
        self.fila = fila
        self.columna = columna

        # calcular coordenada del centro
        self.x = (self.fila + 0.5) * c.TILE_SIZE
        self.y = (self.columna + 0.5) * c.TILE_SIZE

        # varibles de animacion
        self.hojas_sprites = hojas_sprites
        self.lista_animacion = self.cargar_imagenes(self.hojas_sprites[self.nivel_mejora - 1])
        self.indice_frame = 0
        self.tiempo_actualizacion = pg.time.get_ticks()

        # actualizar imagen
        self.angulo = 270
        self.imagen_original = self.lista_animacion[self.indice_frame]
        self.imagen = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

        # mostrar rango
        self.range_image = pg.Surface((self.rango * 2, self.rango * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'grey100', (self.rango, self.rango), self.rango)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def fijar_objetivo(self, grupo_enemigo):
        # seleccionar un eneigo para atacar
        x_dist = 0
        y_dist = 0

        # verificar que el enemigo este dentro del rango
        for enemigo in grupo_enemigo:
            x_dist = enemigo.pos[0] - self.x
            y_dist = enemigo.pos[1] - self.y
            distacia = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if distacia < self.rango:
                self.objetivo = enemigo
                self.angulo = math.degrees(math.atan2(-y_dist, x_dist))

    def cargar_imagenes(self, hoja_sprites):
        # extraer las imagenes de la hoja de sprites
        size = hoja_sprites.get_height()
        lista_animacion = []
        for i in range(c.FRAMES_ANIM):
            temp_img = hoja_sprites.subsurface(i * size, 0, size, size)
            lista_animacion.append(temp_img)
        return lista_animacion

    def update(self, grupo_enemigo):
        # verificar que la torreta tenga oobjetivo para disparar
        if self.objetivo:
            self.reproducir_animacion()
        else:
            # localizar objetivo

            if pg.time.get_ticks() - self.ultimo_disparo > self.cooldown:
                self.fijar_objetivo(grupo_enemigo)

    def reproducir_animacion(self):
        # actualizar imagenes
        self.imagen_original = self.lista_animacion[self.indice_frame]

        if pg.time.get_ticks() - self.tiempo_actualizacion > c.DELAY_ANIM:
            self.tiempo_actualizacion = pg.time.get_ticks()
            self.indice_frame += 1
            if self.indice_frame >= len(self.lista_animacion):
                self.indice_frame = 0

                self.ultimo_disparo = pg.time.get_ticks()
                self.objetivo = None

    def mejorar(self):
        self.nivel_mejora += 1

        self.rango = DATOS_TORRETAS[self.nivel_mejora - 1].get('rango')
        self.cooldown = DATOS_TORRETAS[self.nivel_mejora - 1].get('cooldown')
        self.lista_animacion = self.cargar_imagenes(self.hojas_sprites[self.nivel_mejora - 1])
        self.imagen_original = self.lista_animacion[self.indice_frame]

        # actualizar rango mostrado
        self.range_image = pg.Surface((self.rango * 2, self.rango * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'grey100', (self.rango, self.rango), self.rango)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.imagen = pg.transform.rotate(self.imagen_original, self.angulo - 270)
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(self.imagen, self.rect)
        if self.seleccionado:
            surface.blit(self.range_image, self.range_rect)
