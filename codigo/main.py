import json
import random

import pygame as pg

import constantes as c
from View.Buttons import Button
from aliados import Turret
from enemigos import Enemigo
from nivel import Nivel

# iniciar pygame
pg.init()

# reloj
clock = pg.time.Clock()

# crear la ventana de juego
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.PANEL_LATERAL, c.SCREEN_HEGHT))
pg.display.set_caption('Defensa Antigena')

# variables del juego
colocando_torretas = False
torreta_seleccionada = None
lvl = '1'

# cargar imagenes
# niveles
nivel0 = pg.image.load('../assets/niveles/Nivel' + lvl + '.png').convert_alpha()

# cargar hoja de animacion
hoja_torreta1 = pg.image.load('../assets/torretas/Torreta1.png').convert_alpha()

# tienda
tienda = pg.image.load('../assets/tienda/Tienda' + lvl + '.png').convert_alpha()

# imagenes de turretas individuales para el mouse
cursor_torreta = pg.image.load('../assets/comprar1.png').convert_alpha()

# enemigos
imagen_enemigo = pg.image.load('../assets/enemigo1.png').convert_alpha()

# botones
buy_turret_image = pg.image.load('../assets/comprar1.jpeg').convert_alpha()
cancel_image = pg.image.load('../assets/boton_cancelar.png').convert_alpha()

# cargar datos del archivo .json para el nivel

with open('../niveles/Nivel' + lvl + '.json') as file:
    datos_nivel = json.load(file)


def crear_torreta(mousepos):
    mouse_fila = mousepos[0] // c.TILE_SIZE
    mouse_col = mousepos[1] // c.TILE_SIZE
    # calcular el numeros de casillas secuenciales
    num_casilla_mouse = (mouse_col * c.COLUMNAS) + mouse_fila
    # verificar que la casilla sea terreno plano
    if nivel.tile_map[num_casilla_mouse] == 205:
        # verificar que la casilla donde se colocara la togit rreta este vacia
        casilla_esta_libre = True
        for torreta in grupo_torreta:
            if (mouse_fila, mouse_col) == (torreta.fila, torreta.columna):
                casilla_esta_libre = False
        if casilla_esta_libre:
            torreta = Turret(hoja_torreta1, mouse_fila, mouse_col)
            grupo_torreta.add(torreta)


def selecionar_torreta(mousepos):
    mouse_fila = mousepos[0] // c.TILE_SIZE
    mouse_col = mousepos[1] // c.TILE_SIZE
    for torreta in grupo_torreta:
        if (mouse_fila, mouse_col) == (torreta.fila, torreta.columna):
            return torreta


def quitar_seleccion():
    for t in grupo_torreta:
        t.seleccionado = False


# crear nivel
nivel = Nivel(datos_nivel, nivel0)
nivel.pocesar_datos()

# crear grupo
grupo_enemigo = pg.sprite.Group()
grupo_torreta = pg.sprite.Group()

ruta = random.randint(0, 1)
enemigo = Enemigo(nivel.waypoints[ruta], imagen_enemigo)
grupo_enemigo.add(enemigo)

buy_button = Button(c.SCREEN_WIDTH + 27, 302, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 315, 196, cancel_image, True)

# game loop
run = True
while run:

    clock.tick(c.FPS)

    '''        ╔═══════════════════════════╗
               ║   ZONA DE ACTUALIZACIÓN   ║
               ╚═══════════════════════════╝        '''

    # actualizar grupos
    grupo_enemigo.update()
    grupo_torreta.update(grupo_enemigo)

    # resaltar torreta seleccionada
    if torreta_seleccionada:
        torreta_seleccionada.seleccionado = True

    '''        ╔═══════════════════════════╗
               ║     ZONA DE DIBUJADO      ║
               ╚═══════════════════════════╝        '''

    screen.fill('cyan')

    # dibujar nivel
    nivel.dibujar(screen)
    screen.blit(tienda, (1500, 0))

    # dibujar grupos
    grupo_enemigo.draw(screen)
    for t in grupo_torreta:
        t.draw(screen)
    #grupo_torreta.draw(screen)

    # dibujar botones
    if buy_button.draw(screen):
        colocando_torretas = True

    if colocando_torretas:
        # mostrar torreta en el cursor
        cursor_rect = cursor_torreta.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos

        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_torreta, cursor_rect)

        # dibujar el boton de cancelar
        if cancel_button.draw(screen):
            colocando_torretas = False

    '''        ╔═══════════════════════════╗
               ║          EVENTOS          ║
               ╚═══════════════════════════╝        '''

    for event in pg.event.get():
        # cerrar el juego
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            run = False

        # clics
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            # verificar que el mouse este dentro del mapa
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEGHT:
                torreta_seleccionada = None
                quitar_seleccion()
                if colocando_torretas:
                    crear_torreta(mouse_pos)
                else:
                    torreta_seleccionada = selecionar_torreta(mouse_pos)

    # actualizar la pantalla
    pg.display.flip()

pg.quit()
