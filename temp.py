from scenez import *
from globals import *
import pygame as pg


main = Scenez(widgets=[
    Containerz(tuple(e//2 - screen.get_width()//12 for e in screen.get_size()), (screen.get_width()//6, screen.get_width()//6), visible=False, widgets=[
        Buttonz((0, 0), (screen.get_width()//6, screen.get_width()//18), visible=True, widget=Textz((0,0), "F", text_color=(255, 255, 255), three_d=False, anchor="center")),
        Buttonz((0, (screen.get_width()//2 - screen.get_width()//12)//6), (screen.get_width()//6, screen.get_width()//18), visible=True, widget=Textz((0,0), "F", text_color=(255, 255, 255), three_d=False, anchor="center"))])
    ])





pg.init()
clock = pg.time.Clock()
running = True

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    
    screen.fill("black")

    main.draw()


    pg.display.flip()

    clock.tick(69)

pg.quit()

