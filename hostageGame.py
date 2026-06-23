import pygame as pg
import random as r
from helper_pygame import s, state, DebugScreen, screen
from class_collide_rect import HitBox

import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

def miniGame():

    pg.init()
    screen = pg.display.set_mode((8 * 128, 8 * 128))
    mask = pg.Surface((8 * 128, 8 * 128), pg.SRCALPHA)
    clock = pg.time.Clock()
    running = True

    enemy = pg.image.load("assets/hostageSituation1.png")
    enemy = pg.transform.scale_by(enemy, 8)

    CenterCross = pg.Vector2(512, 512)

    posAim = pg.Vector2(512, 512)

    counter = 0

    # posGoal = pg.Vector2(500, 250)

    goalHB = HitBox(((650-180/2, 400-180/2), (180, 180)))

    antiGoalHB = HitBox(((300-180/2, 600-180/2), (180, 180)))

    randVec, randStrength = None, None

    # def ocheckScreenExit(position):
    #     if position[0] < 0:
    #         return 1,-1
    #     if position[0] > s.WIDTH:
    #         return -1,0
    #     if position[1] < 0:
    #         return 0,1
    #     if position[1] > s.HEIGHT:
    #         return 0,-1
        
    #     return 1,1
    
    # def checkScreenExit(position):
    #     if position[0] < 0:
    #         return 1,-1
    #     if position[0] > s.WIDTH:
    #         return 1,-1
    #     if position[1] < 0:
    #         return -1,1
    #     if position[1] > s.HEIGHT:
    #         return -1,1
        
    #     return 1,1
    

    # checkCircleCollision(pos1, r1, pos2, r2):
        
    #     pass

    # def getCHPos():
    #     mousePos = pg.Vector2(pg.mouse.get_pos())
    #     CenterCross = pg.Vector2(s.WIDTH/2, s.HEIGHT/2)

    #     if counter % 180 == 0:
    #         x = r.choice([r.randint(0, s.WIDTH/5 * 2), r.randint(s.WIDTH - s.WIDTH/5 * 3, s.WIDTH)])
    #         y = r.choice([r.randint(0, s.HEIGHT/5 * 2), r.randint(s.HEIGHT - s.HEIGHT/5 * 3, s.HEIGHT)])

    #         randVec = pg.Vector2(x, y) - CenterCross
    #         randStrength = r.uniform(0.01, 0.02)

    #     if randVec and randStrength:
    #         posAim += (randVec * randStrength)       

    #     ctm = CenterToMouse = mousePos - CenterCross
    #     ctm *= 0.02


    #     posAim += ctm

    #     return posAim
    Q = DebugScreen()

    while running:
        Q.add("fps", clock.get_fps())

        keys = pg.key.get_pressed()


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if goalHB.check_collision(HitBox((tuple(posAim),(1,1)))) or keys[pg.K_SPACE]:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return
            
            if antiGoalHB.check_collision(HitBox((tuple(posAim),(1,1)))):
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        state.gameOver = True
                        return
                

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






        # if checkScreenExit(posAim):

        if counter % 180 == 0:
            x = r.choice([r.randint(0, int(1028*0.4)), r.randint(int(1028*0.6), 1028)])
            y = r.choice([r.randint(0, int(1028*0.4)), r.randint(int(1028*0.6), 1028)])


            randVec = pg.Vector2(x, y) - CenterCross
            randStrength = r.uniform(0.01, 0.02)

            shub = (randVec * randStrength)
            
        if shub:
            posAim += shub
            shub *= 0.999
        
        
        # if not checkScreenExit(posAim):
        #     posAim = pg.Vector2(100, 100)


        ctm = CenterToMouse = mousePos - CenterCross
        ctm *= 0.02


        posAim += ctm

        # posAim = getCHPos()


        # pg.draw.circle(screen, "green", posAim, 10)

        pg.draw.circle(mask, (0, 0, 0, 0), posAim, 350)

        goalHB.show_HB()
        antiGoalHB.show_HB()


        screen.blit(mask, (0, 0))
        # pg.draw.line(screen, "orange", posAim, mousePos, 5)


        # print(counter)
        Q.draw()
        pg.display.flip()
        counter += 1
        clock.tick(69)

    pg.quit()




                
if __name__ == "__main__":
    miniGame()