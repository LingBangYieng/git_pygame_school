import pygame as pg
import random as r
from helper_pygame import state

pg.init()
screen = pg.display.set_mode((1000, 1000))
mask = pg.Surface((1000, 1000), pg.SRCALPHA)
clock = pg.time.Clock()
running = True

enemy = pg.image.load("assets/hostageKeeper.jpg")
enemy = pg.transform.scale_by(enemy, 0.5)

CenterCross = pg.Vector2(500, 500)

posAim = pg.Vector2(100, 100)

counter = 0

randVec, randStrength = None, None

# def checkCircleCollision(pos1, r1, pos2, r2):
    
#     pass

def getCHPos():
    mousePos = pg.Vector2(pg.mouse.get_pos())
    CenterCross = pg.Vector2(state.WIDTH/2, state.HEIGHT/2)

    if counter % 180 == 0:
        x = r.choice([r.randint(0, state.WIDTH/5 * 2), r.randint(state.WIDTH - state.WIDTH/5 * 3, state.WIDTH)])
        y = r.choice([r.randint(0, state.HEIGHT/5 * 2), r.randint(state.HEIGHT - state.HEIGHT/5 * 3, state.HEIGHT)])

        randVec = pg.Vector2(x, y) - CenterCross
        randStrength = r.uniform(0.01, 0.02)

    if randVec and randStrength:
        posAim += (randVec * randStrength)       

    ctm = CenterToMouse = mousePos - CenterCross
    ctm *= 0.02


    posAim += ctm

    return posAim



while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    screen.fill((100, 100, 100))
    mask.fill((0, 0, 0, 255))
    screen.blit(enemy, (0, 0))

    mousePos = pg.Vector2(pg.mouse.get_pos())




    pg.draw.circle(screen, "red", posAim, 350, 3)
    pg.draw.circle(screen, "red", posAim, 250, 3)
    pg.draw.circle(screen, "red", posAim, 150, 3)
    pg.draw.circle(screen, "red", posAim, 50, 3)
    pg.draw.line(screen, "red", pg.Vector2(350, 0) + posAim, pg.Vector2(-350, 0) + posAim, 3)
    pg.draw.line(screen, "red", pg.Vector2(0, 350) + posAim, pg.Vector2(0, -350) + posAim, 3)


    # pg.draw.line(screen, "purple", CenterCross, mousePos, 5)
    # pg.draw.line(screen, "orange", CenterCross, posAim, 5)



    if counter % 180 == 0:
        x = r.choice([r.randint(0, 400), r.randint(600, 1000)])
        y = r.choice([r.randint(0, 400), r.randint(600, 1000)])

        randVec = pg.Vector2(x, y) - CenterCross
        randStrength = r.uniform(0.01, 0.02)
        # randStrength = 0.01

    if randVec and randStrength:
        posAim += (randVec * randStrength)


    ctm = CenterToMouse = mousePos - CenterCross
    ctm *= 0.02


    posAim += ctm

    # posAim = getCHPos()


    pg.draw.circle(screen, "green", posAim, 10)

    pg.draw.circle(mask, (0, 0, 0, 0), posAim, 350)

    # screen.blit(mask, (0, 0))

    print(counter)

    pg.display.flip()
    counter += 1
    clock.tick(60) 

pg.quit()