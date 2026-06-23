# Example file showing a basic pygame "game loop"
import pygame as pg
import numpy as np
from helper_pygame import cast_ray

# pygame setup
pg.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
running = True





visual_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],                
               [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 1, 0, 0, 0, 0, 0, 1, 1, 0], 
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

field_size = 100

baseAngles = []


def blur_surface(surface, scale_factor=0.25):
    w, h = surface.get_size()
    
    # shrink
    small = pg.transform.smoothscale(
        surface,
        (int(w * scale_factor), int(h * scale_factor))
    )
    
    # scale back up
    blurred = pg.transform.smoothscale(small, (w, h))
    
    return blurred

# def oangleCreate(l, r, c="black"):
#     global pos0, LTheta, RTheta
#     localFovHalf = (l - r)/2

#     baseAngles.append(l-localFovHalf)

#     pg.draw.line(screen, c, pos0, np.array([1000*np.cos(l-localFovHalf), 1000*np.sin(l-localFovHalf)])+pos0, 1)
    
#     if localFovHalf < np.deg2rad(12):
#         return
    
#     if l == LTheta:
#         pg.draw.line(screen, "green", pos0, np.array([1000*np.cos(l), 1000*np.sin(l)])+pos0, 5)    

#     if r == RTheta:
#         pg.draw.line(screen, "green", pos0, np.array([1000*np.cos(r), 1000*np.sin(r)])+pos0, 5)

#     # time.sleep(0.1)
#     # pg.display.update()

#     angleCreate(l, l-localFovHalf, "blue")
#     angleCreate(r+localFovHalf, r, "red")


def move(dot, speed=10):

    dotx, doty = dot

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
    
    return np.array([dotx, doty])


def angleCreate(l, r, c="black"):
    global baseAngles
    baseAngles = np.linspace(l,r,512)

hits = []
def checkBases():
    global baseAngles, LTheta, RTheta, hits
    hits = []

    _, LHit, _ = cast_ray(pos0, np.array([1000*np.cos(LTheta), 1000*np.sin(LTheta)])+pos0, 1000, 100, field_size=field_size, array=visual_grid)
    if not LHit: LHit = (np.array([1000*np.cos(LTheta), 1000*np.sin(LTheta)])+pos0)
    _, RHit, _ = cast_ray(pos0, np.array([1000*np.cos(RTheta), 1000*np.sin(RTheta)])+pos0, 1000, 100, field_size=field_size, array=visual_grid)
    if not RHit: RHit = (np.array([1000*np.cos(RTheta), 1000*np.sin(RTheta)])+pos0)


    # print(len(baseAngles))
    hits.append(pos0)
    hits.append(LHit)
    for phi in baseAngles:
        _,hit,_ = cast_ray(pos0, np.array([1000*np.cos(phi), 1000*np.sin(phi)])+pos0, 1000, 100, field_size=field_size, array=visual_grid)
        if not hit: hit = (np.array([1000*np.cos(phi), 1000*np.sin(phi)])+pos0)
        hits.append(hit)
        # if hit:
            
        #     pg.draw.circle(screen, "red", hit, 5)
    hits.append(RHit)


pos0 =  np.array([500, 500])
mousPos = np.array([0, 0])

fov_degr = 90*0.5
fov = np.deg2rad(fov_degr)



while running:
    events = pg.event.get()
    keys = pg.key.get_pressed()
    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            running = False

   
    screen.fill("purple")
    vis.overlay = pg.Surface((1000, 1000), pg.SRCALPHA)
    vis.overlay.fill((0, 0, 0, 240))  # semi-transparent dark vis.overlay

    for row in range(len(visual_grid)):
        for col in range(len(visual_grid[row])):
            if visual_grid[row][col] == 1:
                pg.draw.rect(screen, (100, 100, 100), (col*field_size, row*field_size, field_size, field_size), field_size)
            pg.draw.rect(screen, "grey", (col*field_size, row*field_size, field_size, field_size), 1)

    pos0 = move(pos0)

    mx, my = pg.mouse.get_pos()
    mousPos = np.array([mx, my])


    dx, dy = tuple(mousPos - pos0)

    alpha = np.atan2(dy, dx)

    LTheta = alpha + fov/2
    RTheta = alpha - fov/2
    baseAngles = []
    angleCreate(LTheta, RTheta)
    # print(baseAngles)

    
    checkBases()

    # pg.draw.polygon(screen, "black", hits)

    pg.draw.polygon(vis.overlay, (0, 0, 0, 0), hits)
    # pg.draw.circle(vis.overlay, (0, 0, 0, 0), pos0, 30)

    screen.blit(blur_surface(vis.overlay, 0.2), (0, 0))

    pg.draw.circle(screen, "red", pos0, 3)


    pg.display.update()

    clock.tick(60)

pg.quit()