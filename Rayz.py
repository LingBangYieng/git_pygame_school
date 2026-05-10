import pygame as pg
import numpy as np

class Rayz:

    def __init__(self):
        pass


def move(dotx, doty,speed):
    # global dotx, doty


    keys = pg.key.get_pressed()

    if keys[pg.K_LSHIFT]:
        speed *= 2

    if keys[pg.K_w]:
        doty += - speed
    if keys[pg.K_a]:
        dotx += - speed
    if keys[pg.K_s]:
        doty += speed
    if keys[pg.K_d]:
        dotx +=  speed
    
    return dotx, doty






pg.display.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
running = True
pg.mouse.set_visible(False)


visual_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],                
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]


dotx, doty = 550,550
field_size = 100
speed = 5
pg.font.init()
font = pg.font.Font(None, 20)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False



    screen.fill("black")

    for row in range(len(visual_grid)):
        for col in range(len(visual_grid[row])):
            if visual_grid[row][col] == 1:
                pg.draw.rect(screen, (100, 100, 100), (col*field_size, row*field_size, field_size, field_size), field_size)
            pg.draw.rect(screen, "light grey", (col*field_size, row*field_size, field_size, field_size), 1)


    pg.draw.circle(screen, "blue", (dotx, doty), 15)
    pg.draw.circle(screen, "green", pg.mouse.get_pos(), 10)
    pg.draw.line(screen, "red", (dotx, doty), pg.mouse.get_pos(), 1)

    mx,my = pg.mouse.get_pos()
    vertical_points = []
    horizontal_points = []

    
    dotx, doty = move(dotx, doty, speed)
    m = 1000
    if abs(dotx - mx) > 0.001:
        m = (doty - my) / (dotx - mx)

    
    #Help Plus
    if mx > dotx: plus_x = 1
    else: plus_x = -1
    if my > doty: plus_y = 1
    else: plus_y = -1

    c_dotx = (dotx//field_size) + (mx > dotx)
    c_doty = (doty//field_size) + (my > doty)


    shoot_range = 200
    shoot_range2 = shoot_range**2


    for i in range(shoot_range//field_size+1):

        #edges
        edge_x = (c_dotx + plus_x * i) * field_size
        edge_y = (c_doty + plus_y * i) * field_size

        #Deltas
        dx = edge_x - dotx 
        dy = edge_y - doty 

        #ca<lc
        x_Y = doty + m * dx
        if abs(m) > 1e-6: y_X = dotx + dy / m
        else: y_X = dotx + dy * 1000

        pg.draw.circle(screen, "yellow", (edge_x, x_Y), 5)
        vertical_points.append((edge_x, x_Y,"v"))

        pg.draw.circle(screen, "yellow", (y_X, edge_y), 5)
        horizontal_points.append((y_X, edge_y,"h"))



    points = vertical_points + horizontal_points
    

    
    res = []
    for x,y,type in points:
        exactness = 100
        if type == "h":
            y_p = y + field_size/exactness
            y_n = y - field_size/exactness
            res.append((x,y_p))
            res.append((x,y_n))
        else:
            x_p = x + field_size/exactness
            x_n = x - field_size/exactness
            res.append((x_p, y))
            res.append((x_n, y))
    points = res





    res = []
    for x,y in points:
        dist = (x-dotx)**2+(y-doty)**2
        if dist <= shoot_range2:
            res.append((x,y,dist))
    points = res

    points = sorted(points, key=lambda p: p[2])

    
    c=0
    for x, y, _ in points:
        c+=1
        pg.draw.circle(screen, "orange", (x, y), 3)
        num = font.render(f"{c}", True, (255,255,255))
        screen.blit(num, (x,y-10))

    
    for x, y, _ in points:
        pg.draw.circle(screen, "blue", (x, y), 3)
        try:
            if visual_grid[int(y) // field_size][int(x) // field_size] != 0:
                pg.draw.rect(screen, "green", ((x // field_size)*field_size, (y // field_size)*field_size, field_size, field_size), field_size)
                pg.draw.circle(screen, "red", (x, y), 1)
                break
        except Exception as e:
            print(e)
            pass
    
    pg.draw.circle(screen, "red", (dotx, doty), shoot_range, 1)




    
    # length_x = abs(round(field_size//field_size) - round(pg.mouse.get_pos()[0]//field_size))
    # length_y = abs(round(900//field_size) - round(pg.mouse.get_pos()[1]//field_size))
    # length = length_x + length_y

    # print(length)

    pg.display.update()
    clock.tick(60)
pg.quit()