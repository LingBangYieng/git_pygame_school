import pygame as pg
from class_collide_rect import HitBox
from scenez import *
from helper_pygame import *
from globals import *


WIDTH, HEIGHT = 1280, 720

pg.display.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

NightlyFuchsia = (72, 28, 43)
DebugGreen = (0, 1, 0)
color_theme = NightlyFuchsia

button1 = Buttonz((WIDTH/2 - 100, HEIGHT/2 - 50), (200, 50), screen, True, "Start Game", (0, 0, 0), 30, 5, color_theme)
button2 = Buttonz((WIDTH/2 - 100, HEIGHT/2 + 17.5), (200, 50), screen, True, "Settings", (0, 0, 0), 30, 5, color_theme)
button3 = Buttonz((WIDTH/2 - 100, HEIGHT/2 + 85), (200, 50), screen, True, "Quit", (0, 0, 0), 30, 5, color_theme)

title = "Redundant"
version = "alpha v0.1"
featured = "Abdul, Agmar, Kreatin"

lobby = Scenez(screen)


lobby.add_button(button1)
lobby.add_button(button2)
lobby.add_button(button3)

lobby.add_text(title, color_theme, WIDTH/2 , 100, 110, True)
lobby.add_text(version, color_theme,  1230, 700, 20, True)
lobby.add_text(featured, color_theme,  90, 700, 20, True)


mouse_HB = HitBox(((0, 0), (1, 1)))
MHB = mouse_HB
background = pg.image.load("assets/may_background.png")
image_scale_fac = max(WIDTH/background.get_width(), HEIGHT/background.get_height())
background = pg.transform.scale_by(background, image_scale_fac)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")



    mx, my = (pg.mouse.get_pos())
    mouse_HB.x = mx
    mouse_HB.y = my
    MHB_rect[0] = ((mx,my),(1, 1))

    screen.blit(background, (0, 0))
    lobby.draw_scene()


    pg.display.flip()

    clock.tick(69)

pg.quit()