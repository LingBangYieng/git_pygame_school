import pygame as pg
import numpy as np

game_loop = True

    
# pg.init()
pg.display.init()

size = 8
width, height = 200, 100
screen = pg.display.set_mode((width*size, height*size))
pos_circle_x, pos_circle_y = 0, height
speed = 0.1 * size
position_circle = pg.Vector2((width*size)/2, (height*size)/2)
radius = 20
alpha = 180
amount_circles = 3



def move(position_circle,speed):

    keys = pg.key.get_pressed()


    if keys[pg.K_LSHIFT]:
        speed *= 1.5
    if keys[pg.K_w]:
        position_circle[1] = position_circle[1] - speed
    if keys[pg.K_a]:
        position_circle[0] = position_circle[0] - speed
    if keys[pg.K_s]:
        position_circle[1] = position_circle[1] + speed
    if keys[pg.K_d]:
        position_circle[0] = position_circle[0] + speed
    
    
    return position_circle



while game_loop:

    # pygame.QUIT event means the user clicked X to close your window
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            game_loop = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                amount_circles += 1
            if event.key == pg.K_u:
                amount_circles = max(1, amount_circles - 1)       
        

    screen.fill((0,0,0))

    radian = (np.pi / 180) * alpha
    offset = 2 * np.pi / amount_circles
    for i in range(amount_circles):

        xy_rotate = radius * 3 * np.cos(radian + offset * i), radius * 3 * np.sin(radian + offset * i)
        pg.draw.circle(screen, (255, 0, 0), ( position_circle + xy_rotate), radius/2)

    
   
    alpha += 0.05


    pg.draw.circle(screen, (46, 150, 172), (position_circle), radius)
    move(position_circle, speed)


    pg.display.update()







