import json

import pygame as pg

import constantes as c
from aliados import Turret
from enemigos import Enemigo
from nivel import Nivel

# iniciar pygame
pg.init()

# reloj
clock = pg.time.Clock()

# crear la ventana de juego
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.PANEL_LATERAL, c.SCREEN_HEGHT))
pg.display.set_caption("Tower Defence")

# cargar imagenes
# niveles
nivel0 = pg.image.load('../niveles/nivel0.png').convert_alpha()

# imagenes de turretas individuales para el mouse
cursor_torreta = pg.image.load('../assets/anticuerpos.png').convert_alpha()

# enemigos
imagen_enemigo = pg.image.load("../assets/enemigo1.png").convert_alpha()

# cargar datos del archivo .json para el nivel
with open("../niveles/camino_nivel0.tmj") as file:
    datos_nivel = json.load(file)


def crear_torreta(mousepos):
    mouse_fila = mousepos[0] // c.TILE_SIZE
    mouse_col = mousepos[1] // c.TILE_SIZE
    # calcular el numeros de casillas secuenciales
    num_casilla_mouse = (mouse_col * c.COLUMNAS) + mouse_fila
    # verificar que la casilla sea terreno plano
    if nivel.tile_map[num_casilla_mouse] == 205:
        #verificar que la casilla donde se colocara la togit rreta este vacia
        casilla_esta_libre = True
        for torreta in grupo_torreta:
            if (mouse_fila, mouse_col) == (torreta.fila, torreta.columna):
                casilla_esta_libre = False
        if casilla_esta_libre:
            torreta = Turret(cursor_torreta, mouse_fila, mouse_col)
            grupo_torreta.add(torreta)


# crear nivel
nivel = Nivel(datos_nivel, nivel0)
nivel.pocesar_datos()

# crear grupo
grupo_enemigo = pg.sprite.Group()
grupo_torreta = pg.sprite.Group()

enemigo = Enemigo(nivel.waypoints, imagen_enemigo)
grupo_enemigo.add(enemigo)

# game loop
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey")

    # dibujar nivel
    nivel.dibujar(screen)

    # dibujar camino de los enemigos
    # pg.draw.lines(screen, "grey0", False, nivel.waypoints)

    # actualizar grupos
    grupo_enemigo.update()

    # dibujar grupos
    grupo_enemigo.draw(screen)
    grupo_torreta.draw(screen)

    # eventos
    for event in pg.event.get():
        # cerrar el juego
        if event.type == pg.QUIT:
            run = False

        # clics
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEGHT:
                crear_torreta(mouse_pos)

    # actualizar la pantalla
    pg.display.flip()

pg.quit()
