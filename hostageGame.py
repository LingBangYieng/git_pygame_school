import pygame as pg
import random as r

pg.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
running = True

Center = pg.Vector2(500, 500)

posAim = pg.Vector2(100, 100)

counter = 0

randVec, randStrength = None, None

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    screen.fill((100, 100, 100))

    mousePos = pg.Vector2(pg.mouse.get_pos())


    pg.draw.circle(screen, "red", Center, 350, 3)
    pg.draw.circle(screen, "red", Center, 250, 3)
    pg.draw.circle(screen, "red", Center, 150, 3)
    pg.draw.circle(screen, "red", Center, 50, 3)
    pg.draw.line(screen, "red", (500, 0), (500, 1000), 3)
    pg.draw.line(screen, "red", (0, 500), (1000, 500), 3)


    pg.draw.line(screen, "purple", Center, mousePos, 5)
    pg.draw.line(screen, "orange", Center, posAim, 5)



    if counter % 180 == 0:
        x = r.choice([r.randint(0, 400), r.randint(600, 1000)])
        y = r.choice([r.randint(0, 400), r.randint(600, 1000)])

        randVec = pg.Vector2(x, y) - Center
        randStrength = r.uniform(0.01, 0.02)
        # randStrength = 0.01

    if randVec and randStrength:
        posAim += (randVec * randStrength)


    ctm = CenterToMouse = mousePos - Center
    ctm *= 0.02


    posAim += ctm



    pg.draw.circle(screen, "green", posAim, 10)

    print(counter)

    pg.display.flip()
    counter += 1
    clock.tick(60) 

pg.quit()