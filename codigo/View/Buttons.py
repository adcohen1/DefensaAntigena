import pygame as pg


class Button:
    def __init__(self, x, y, image, single_click) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.seleccionado = False
        self.single_click = single_click

    def draw(self, surface):
        accion = False

        # obtener la posicion del mouse
        pos = pg.mouse.get_pos()

        # verificar seleccion
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.seleccionado:
                accion = True

                # si el boton es de un solo click, entonces se cambia el esta de seleccionado a True
                if self.single_click:
                    self.seleccionado = True

        if pg.mouse.get_pressed()[0] == 0:
            self.seleccionado = False

        # dibujar boton en la pantalla
        surface.blit(self.image, self.rect)

        return accion
