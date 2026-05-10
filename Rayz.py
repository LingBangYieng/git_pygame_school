import pygame as pg
import numpy as np


def check_boundaries(row: int, col: int, array: list[list]):
    if row < len(array) and col < len(array[0]) and row >= 0 and col >= 0:
        return True
    return False

# def cast_ray(start_position:tuple, end_position:tuple, length:int, exactness: int, field_size: int, array: list[list]):


#     start = start_position
#     x0 = start[0]
#     y0 = start[1]

#     end = end_position
#     x1 = end[0]
#     y1 = end[1]

#     vertical_points = []
#     horizontal_points = []

#     exactness = exactness
#     length = length
#     length2= length * length

#     m = 1000
#     if abs(x0 - x1) > 0.001:
#         m = (y0 - y1) / (x0 - x1)

#     #direction_check
#     if x1 > x0: plus_x = 1
#     else: plus_x = -1
#     if y1 > y0: plus_y = 1
#     else: plus_y = -1

#     #get first chunk edge
#     c_x = (x0//field_size) + (x1 > x0)
#     c_y = (y0//field_size) + (y1 > y0)

#     for i in range(length//field_size+1):  

#         #get second chunk edge, direction applied
#         edge_x = (c_x + plus_x * i) * field_size
#         edge_y = (c_y + plus_y * i) * field_size

#         #get distance from start to direfctional chunk line
#         dx = edge_x - x0 
#         dy = edge_y - y0

#         #get missing side vertical
#         c_distance_y = y0 + m * dx
#         #get missing side horizontal
#         if abs(m) > 1e-6: c_distance_x = x0 + dy / m
#         else: c_distance_x = x0 + dy * 1000

#         # pg.draw.circle(screen, "yellow", (edge_x, c_distance_y), 5)
#         vertical_points.append((edge_x, c_distance_y,"v"))

#         # pg.draw.circle(screen, "yellow", (c_distance_x, edge_y), 5)
#         horizontal_points.append((c_distance_x, edge_y,"h"))

#         points = vertical_points + horizontal_points

    
    
#     res = []
#     for x,y,type in points:
#         #get checkpoint
#         if type == "h":
#             y_p = y + field_size/exactness
#             y_n = y - field_size/exactness
#             res.append((x,y_p))
#             res.append((x,y_n))
#         else:
#             x_p = x + field_size/exactness
#             x_n = x - field_size/exactness
#             res.append((x_p, y))
#             res.append((x_n, y))
#     points = res

#     res = []
#     for x,y in points:
#         dist = (x-x0)**2+(y-y0)**2
#         if dist <= length2:
#             res.append((x,y,dist))
#     points = res

#     points = sorted(points, key=lambda p: p[2])

#     # c=0
#     # for x, y, _ in points:
#     #     c+=1
#     #     pg.draw.circle(screen, "orange", (x, y), 3)
#     #     num = font.render(f"{c}", True, (255,255,255))
#     #     screen.blit(num, (x,y-10))

    
#     for x, y, distance in points:
#         # pg.draw.circle(screen, "blue", (x, y), 3)
#         row, col = int(y/field_size), int(x/field_size)
#         if check_boundaries(row, col, array):
#             if array[row][col] != 0:
#                 # pg.draw.rect(screen, "green", ((x // field_size)*field_size, (y // field_size)*field_size, field_size, field_size), field_size)
#                 # pg.draw.circle(screen, "red", (x, y), 1)
#                 return ((row, col), (x, y), distance)
#     return None



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





# print(cast_ray((500, 100), (1000, 100), 1000, 100, 100, visual_grid))




def move(dotx, doty,speed):

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



def check_boundaries(row, col, array):
    if row < len(array) and col < len(array[0]) and row >= 0 and col >= 0:
        return True
    return False






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
            pg.draw.rect(screen, "grey", (col*field_size, row*field_size, field_size, field_size), 1)


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
        row, col = int(y/field_size), int(x/field_size)
        if check_boundaries(row, col, visual_grid):
            if visual_grid[row][col] != 0:
                pg.draw.rect(screen, "green", ((x // field_size)*field_size, (y // field_size)*field_size, field_size, field_size), field_size)
                pg.draw.circle(screen, "red", (x, y), 1)
                break
    
    pg.draw.circle(screen, "red", (dotx, doty), shoot_range, 1)

    pg.display.update()
    clock.tick(60)
pg.quit()