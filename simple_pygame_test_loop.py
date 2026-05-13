import pygame as pg
from Buttons import Buttonz
from class_collide_rect import HitBox
from scenez import Scenez


pg.display.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True


button1 = Buttonz((1280//2 - 100, 720//2 - 50), 200, 50, screen, True, "Start Game", (0, 0, 0), 30, 10, (100, 50, 30))
button2 = Buttonz((1280//2 - 100, 720//2 + 17.5), 200, 50, screen, True, "Settings", (0, 0, 0), 30, 10, (100, 50, 30))
button3 = Buttonz((1280//2 - 100, 720//2 + 85), 200, 50, screen, True, "Quit", (0, 0, 0), 30, 10, (100, 50, 30))

title = "Redundant"
version = "alpha v0.1"
featured = "Abdul, Agmar, Kreatin"

lobby = Scenez(screen)


lobby.add_button(button1)
lobby.add_button(button2)
lobby.add_button(button3)

lobby.add_text(title, (100, 50, 30), 1280//2 , 100, 75, True)
lobby.add_text(version, (100, 50, 30),  1230, 700, 20, True)
lobby.add_text(featured, (100, 50, 30),  80, 700, 20, True)



mouse_HB = HitBox(0, 0, 1, 1)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")



    mx, my = pg.mouse.get_pos()
    mouse_HB.x = mx
    mouse_HB.y = my

    lobby.draw_scene()


    pg.display.flip()

    clock.tick(60)

pg.quit()