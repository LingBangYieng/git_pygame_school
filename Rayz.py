import pygame as pg
import numpy as np

class Rayz:

    def __init__(self):
        pass


pg.display.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
running = True
pg.mouse.set_visible(False)

visual_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],                
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


dotx, doty = 550,550
field_size = 100


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False



    screen.fill("black")

    for row in range(len(visual_grid)):
        for col in range(len(visual_grid[row])):
            if visual_grid[row][col] == 1:
                pg.draw.rect(screen, (field_size, field_size, field_size), (col*field_size, row*field_size, field_size, field_size), field_size)
            pg.draw.rect(screen, "light grey", (col*field_size, row*field_size, field_size, field_size), 1)


    pg.draw.circle(screen, "blue", (dotx, doty), 15)
    pg.draw.circle(screen, "green", pg.mouse.get_pos(), 15)
    pg.draw.line(screen, "red", (dotx, doty), pg.mouse.get_pos(), 1)

    mx,my = pg.mouse.get_pos()
    for i in range(5):
        m = 1000
        if abs(dotx - pg.mouse.get_pos()[0]) > 0.001:
            m = (doty - pg.mouse.get_pos()[1]) / (dotx - pg.mouse.get_pos()[0])

        c_dotx = (dotx//field_size)
        c_doty = (doty//field_size)

        #Help Plus
        if mx > dotx: plus_x = 1
        else: plus_x = -1
        if my > doty: plus_y = 1
        else: plus_y = -1

        #edges
        edge_x = (c_dotx + plus_x * i) * field_size
        edge_y = (c_doty + plus_y * i) * field_size

        #Deltas
        dx = edge_x - dotx 
        dy = edge_y - doty 

        #ca<lc
        x_Y = doty + m * dx
        if m > 1e-6: y_X = dotx + dy / m
        else: y_X = dotx + dy * 1000

        pg.draw.circle(screen, "yellow", (edge_x, x_Y), 5)
        pg.draw.circle(screen, "yellow", (y_X, edge_y), 5)

        # pg.draw.line(screen, "yellow", (field_size, 900), (yx,yy), 1)



    # length_x = abs(round(field_size//field_size) - round(pg.mouse.get_pos()[0]//field_size))
    # length_y = abs(round(900//field_size) - round(pg.mouse.get_pos()[1]//field_size))
    # length = length_x + length_y

    # print(length)

    pg.display.update()
    clock.tick(60)
pg.quit()