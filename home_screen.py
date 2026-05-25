import pygame as pg
from class_collide_rect import HitBox
from scenez import *
from helper_pygame import *
#from globals import *


WIDTH, HEIGHT = 1280, 720

pg.display.init()
pg.display.set_caption("Redundant")
icon = pg.image.load("assets/goofy_revolver.png")
icon = pg.transform.rotate(icon, 45)
pg.display.set_icon(icon)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

def quit_game():
    global running
    running = False

def switch_scene(scene:Scenez):
    global current_scene
    current_scene = scene[0]

NightlyFuchsia = (72, 28, 43)
DebugGreen = (0, 100, 0)
color_theme = DebugGreen


lobby = Scenez(screen)
settings = Scenez(screen)




buttontest = Buttonz((WIDTH/2 - 100, HEIGHT/2 + 17.5), (200, 50), screen, True, "Back", (0, 0, 0), 30, 5, color_theme, switch_scene, [lobby])

settings.add_button(buttontest)



color_theme = NightlyFuchsia

background = Imagez(position=(0, 0), pathToImage="assets/may_background.png", isBackground=True)
button1 = Buttonz((WIDTH/2 - 100, HEIGHT/2 - 50), (200, 50), screen, True, "Start Game", (0, 0, 0), 30, 5, color_theme)
button2 = Buttonz((WIDTH/2 - 100, HEIGHT/2 + 17.5), (200, 50), screen, True, "Settings", (0, 0, 0), 30, 5, color_theme, switch_scene, [settings])
button3 = Buttonz((WIDTH/2 - 100, HEIGHT/2 + 85), (200, 50), screen, True, "Quit", (0, 0, 0), 30, 5, color_theme, quit_game)
title = "Redundant"
version = "alpha v0.1"
featured = "Abdul, Agmar, Kreatin"

lobby.add_image(background)
lobby.add_button(button1)
lobby.add_button(button2)
lobby.add_button(button3)
lobby.add_text(title, color_theme, WIDTH/2 , 100, 110, True)
lobby.add_text(version, color_theme,  1230, 700, 20, True)
lobby.add_text(featured, color_theme,  90, 700, 20, True)







mouse_HB = HitBox(((0, 0), (1, 1)))
MHB = mouse_HB



current_scene = lobby

while running:

    events[0] = pg.event.get()
    for event in events[0]:
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")


    mx, my = (pg.mouse.get_pos())
    mouse_HB.x = mx
    mouse_HB.y = my
    MHB_rect[0] = HitBox(((mx,my),(1, 1)))

    current_scene.draw_scene()


    pg.display.update()

    clock.tick(69)

pg.quit()