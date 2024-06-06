import json
import pathlib
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
torreta_seleccionada: Turret = None
lvl = 4

# cargar imagenes
# niveles
nivel0 = pg.image.load('../assets/niveles/Nivel' + str(lvl) + '.png').convert_alpha()

# cargar hoja de animacion
dir_torretas: pathlib.Path = pathlib.Path('../assets/torretas')
frames_torretas = [pg.image.load('../assets/torretas/FramesNeutrofilo.png').convert_alpha(),
                   pg.image.load('../assets/torretas/FramesLinfocitosB.png').convert_alpha(),
                   pg.image.load('../assets/torretas/FramesLinfocitosT.png').convert_alpha(),
                   pg.image.load('../assets/torretas/FramesMacrofagos.png').convert_alpha(),
                   pg.image.load('../assets/torretas/FramesNaturalKiller.png').convert_alpha()]

# tienda
tienda = pg.image.load('../assets/tienda/Tienda' + str(lvl) + '.png').convert_alpha()

# imagenes de turretas individuales para el mouse
cursor_neutrofilo = pg.image.load('../assets/comprar1.png').convert_alpha()

# enemigos
imagen_enemigo = pg.image.load('../assets/enemigo1.png').convert_alpha()

# botones
img_neutrofilo = pg.image.load('../assets/iconos/IconoNeutrofilo.png').convert_alpha()
img_linfo_b = pg.image.load('../assets/iconos/IconoLifocitoB.png').convert_alpha()
img_linfo_t = pg.image.load('../assets/iconos/IconoLinfocitoT.png').convert_alpha()
img_macrofago = pg.image.load('../assets/iconos/IconoMacrofago.png').convert_alpha()
img_natural_killer = pg.image.load('../assets/iconos/IconoNaturalKiller.png').convert_alpha()
cancel_image = pg.image.load('../assets/boton_cancelar.png').convert_alpha()

# cargar datos del archivo .json para el nivel
with open('../niveles/Nivel' + str(lvl) + '.json') as file:
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
            torreta = Turret(frames_torretas, mouse_fila, mouse_col)
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

# crear botones
boton_neutrofilo = Button(c.SCREEN_WIDTH + 27, 302, img_neutrofilo, True)
boton_linfo_b = Button(c.SCREEN_WIDTH + 27, 402, img_linfo_b, True)
boton_linfo_t = Button(c.SCREEN_WIDTH + 27, 502, img_linfo_t, True)
boton_macrofago = Button(c.SCREEN_WIDTH + 27, 602, img_macrofago, True)
boton_natural_killer = Button(c.SCREEN_WIDTH + 27, 702, img_natural_killer, True)
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
    # grupo_torreta.draw(screen)

    # dibujar botones
    if boton_neutrofilo.draw(screen):
        colocando_torretas = True

    if colocando_torretas:
        # mostrar torreta en el cursor
        cursor_rect = cursor_neutrofilo.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos

        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_neutrofilo, cursor_rect)

        # dibujar el boton de cancelar
        if cancel_button.draw(screen):
            colocando_torretas = False

    if lvl > 1:
        if boton_linfo_b.draw(screen):
            if torreta_seleccionada and torreta_seleccionada.nivel_mejora == 1:
                torreta_seleccionada.mejorar()

    if lvl > 1:
        if boton_linfo_t.draw(screen):
            if torreta_seleccionada and torreta_seleccionada.nivel_mejora == 2:
                torreta_seleccionada.mejorar()

    if lvl > 2:
        if boton_macrofago.draw(screen):
            if torreta_seleccionada and torreta_seleccionada.nivel_mejora == 3:
                torreta_seleccionada.mejorar()

    if lvl > 3:
        if boton_natural_killer.draw(screen):
            if torreta_seleccionada and torreta_seleccionada.nivel_mejora == 4:
                torreta_seleccionada.mejorar()

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
