import os
os.environ["SDL_VIDEODRIVER"] = "windows"
import pygame as pg
import numpy as np
# import time
from entityz import *
from helper_pygame import *
from helper2 import *
from hostageGame import miniGame
from inGameSettingsFunc import GoEscMenu
from GameOverScreen import GameOverSCreen
from thanksForPlaying import goTYScene


def pss(mapName:str = "main"):
    def switchToHostageGame():
        miniGame()

    #inits
    pg.display.init()
    pg.mixer.init()
    pg.mouse.set_visible(True)


    #loads
    crosshair = pg.image.load(f"assets/goofy_crosshair.png")
    static_player = pg.image.load(f"assets/player_gun_static.png")
    hostage_red = pg.image.load(f"assets/hostage_highlighted_red.png")
    hostage_green = pg.image.load(f"assets/hostage_highlighted_green.png")
    bullet_green = pg.image.load(f"assets/bullet_inv_green.png")

    #transform loads
    crosshair = pg.transform.scale_by(crosshair, 4)
    static_player = pg.transform.scale_by(static_player, s.GameScale/2)
    hostage_red = pg.transform.scale_by(hostage_red, s.GameScale/2)
    hostage_green = pg.transform.scale_by(hostage_green, s.GameScale/2)



    #Audio
    gunshot_sound = pg.mixer.Sound(f"assets/silenced_gunshot.mp3")
    launch_missile = pg.mixer.Sound("assets/rocket_launch.mp3")
    missile_explo = pg.mixer.Sound("assets/rocket_explosion.mp3")
    # lobby_song = pg.mixer.music.load("assets/retrowave_song.mp3")

    #transform Audio 
    launch_missile.set_volume(0.1 * s.SFX_VOLUME)
    missile_explo.set_volume(0.1 * s.SFX_VOLUME)
    gunshot_sound.set_volume(0.1 * s.SFX_VOLUME)
    # pg.mixer.music.set_volume(0,125)
    # pg.mixer.music.play(-1)




    speed = 10
    position_circle = pg.Vector2((s.WIDTH)/2, (s.HEIGHT)/2)
    old_position_circle = pg.Vector2((s.WIDTH)/2, (s.HEIGHT)/2)
    velocity = pg.Vector2((0, 0))
    moving = False
    sprinting= False
    radius = 20
    state.game_loop = True
    alpha = 0
    state.bulletsInInv = 5

    
    #!!Externalize background ahs to be given by homescreen (level like)


    HB_layer = upscale_grid(bitmap(mapName))
    # HB_layer = bitmap()

    state.HB_layer = HB_layer

    background = pg.image.load(f"saves/{mapName}_as.png")
    background = pg.transform.scale_by(background, s.GameScale)

    HB_layerHBs = getHitBox_HBLayer(mapName)

    #own Class init
    # player_walk = Animationz(numFrames=13, imageScale=s.GameScale)
    mouse_HB = state.MHB_rect = HitBox(((0, 0),(1, 1)))
    entitySceneMain = EntityScenez()



    state.entityScene = entitySceneMain




    #debugs
    # enemy0 = Enemyz(position=(1000, 1000), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    # item0 = Itemz(position=(500, 500), path_to_image_non_highlighted="assets/hk_416.png", image_scale=1.5)
    hostage0 = Hostage(position=tuple(e*4 for e in(415, 160)), path_to_image_non_highlighted="assets/hostage.png", image_scale=s.GameScale, instruction=switchToHostageGame)
    hostage1 = Hostage(position=tuple(e*4 for e in(2284, 141)), path_to_image_non_highlighted="assets/hostage.png", image_scale=s.GameScale, instruction=switchToHostageGame)
    hostage2 = Hostage(position=tuple(e*4 for e in(1693, 304)), path_to_image_non_highlighted="assets/hostage.png", image_scale=s.GameScale, instruction=switchToHostageGame)
    hostage3 = Hostage(position=tuple(e*4 for e in(63, 1011)), path_to_image_non_highlighted="assets/hostage.png", image_scale=s.GameScale, instruction=switchToHostageGame)
    hostage4 = Hostage(position=tuple(e*4 for e in(1914, 911)), path_to_image_non_highlighted="assets/hostage.png", image_scale=s.GameScale, instruction=switchToHostageGame)

    enemy0 = Enemyz(position=tuple(e*4 for e in(565, 201)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy1 = Enemyz(position=tuple(e*4 for e in(907, 205)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy2 = Enemyz(position=tuple(e*4 for e in(144, 683)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy3 = Enemyz(position=tuple(e*4 for e in(285, 1185)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy4 = Enemyz(position=tuple(e*4 for e in(643, 1206)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy5 = Enemyz(position=tuple(e*4 for e in(1395, 346)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy6 = Enemyz(position=tuple(e*4 for e in(1988, 155)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy7 = Enemyz(position=tuple(e*4 for e in(2396, 396)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy8 = Enemyz(position=tuple(e*4 for e in(1577, 622)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy9 = Enemyz(position=tuple(e*4 for e in(2298, 980)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy10 = Enemyz(position=tuple(e*4 for e in(2375, 1285)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy11 = Enemyz(position=tuple(e*4 for e in(1922, 1272)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy12 = Enemyz(position=tuple(e*4 for e in(962, 1148)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy13 = Enemyz(position=tuple(e*4 for e in(1485, 1272)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    enemy14 = Enemyz(position=tuple(e*4 for e in(348, 403)), path_to_image="assets/bombi_static.png", image_scale=s.GameScale)



    entitySceneMain.add_hostage(hostage0)
    entitySceneMain.add_hostage(hostage1)
    entitySceneMain.add_hostage(hostage2)
    entitySceneMain.add_hostage(hostage3)
    entitySceneMain.add_hostage(hostage4)

    entitySceneMain.add_enemy(enemy0)
    entitySceneMain.add_enemy(enemy1)
    entitySceneMain.add_enemy(enemy2)
    entitySceneMain.add_enemy(enemy3)
    entitySceneMain.add_enemy(enemy4)
    entitySceneMain.add_enemy(enemy5)
    entitySceneMain.add_enemy(enemy6)
    entitySceneMain.add_enemy(enemy7)
    entitySceneMain.add_enemy(enemy8)
    entitySceneMain.add_enemy(enemy9)
    entitySceneMain.add_enemy(enemy10)
    entitySceneMain.add_enemy(enemy11)
    entitySceneMain.add_enemy(enemy12)
    entitySceneMain.add_enemy(enemy13)
    entitySceneMain.add_enemy(enemy14)





    #ideas
    "grenade launch with size rescaling"
    




    #commands
    # def spawn(entityType="enemy", position=(1000, 1000)):
    #     nonlocal entitySceneMain
    #     entity = None
    #     match entityType:
    #         case "enemy":
    #             entity = Enemyz(position=position, path_to_image="assets/bombi_static.png", image_scale=s.GameScale)
    #         case "item":
    #             entity = Itemz(position=position, path_to_image_non_highlighted="assets/goofy_revolver.png", image_scale=1.5, image_rotation=45)
    #     if entity is not None:
    #         for enemy in entitySceneMain.enemyList:
    #             if enemy.position == position:
    #                 return
    #         entitySceneMain.add_enemy(entity)
            # isreali_ambient = pg.mixer.Sound("assets/israeli_ambient_quiet.mp3")
            # isreali_ambient.set_volume(0.05)
            # isreali_ambient.play()
            # print("hehe")






    def move(position_circle,speed):
        nonlocal alpha, moving, old_position_circle, sprinting, velocity


        keys = pg.key.get_pressed()

        if keys[pg.K_LSHIFT]:
            speed *= 2
            sprinting = True
        if keys[pg.K_w]:
            velocity[1] += - speed
        if keys[pg.K_a]:
            velocity[0] += - speed
        if keys[pg.K_s]:
            velocity[1] += speed
        if keys[pg.K_d]:
            velocity[0] +=  speed


        position_circle[0] += velocity.x
        position_circle[1] += velocity.y

        velocity.xy = 0, 0 
        
        vwp.topleft = (position_circle[0] - s.WIDTH/2, position_circle[1] - s.HEIGHT/2)



        mouse_pos = (pg.mouse.get_pos()[0] - s.WIDTH // 2, pg.mouse.get_pos()[1] - s.HEIGHT // 2)
        alpha = np.degrees(np.arctan2(-mouse_pos[1], mouse_pos[0]))
        

        moving = position_circle != old_position_circle

        state.playerPos = position_circle 










    fov = np.deg2rad(s.fov_degr)


    clock = pg.time.Clock()
    # (46, 150, 172)

    shootCooldown = 0


    class BottleNeck:
        def checkN(gg, das):
            pass
    


    # hintTextSize = 25
    # hintFont = pg.font.Font(None, hintTextSize)

    # HintText1 = "@@@@@@@@@@@@@@@@Find the Hostage and Rescue it!"

    # # Lines = HintText1.split("\n")
    # currentDisplayText = ""
    # currentRender = hintFont.render(currentDisplayText, False, "white")
    # displayedRender = currentRender
    # started = None

    # renders = []
    # prevIndex = -1
    # def drawHintText(delay: int=7):
    #     nonlocal started, currentDisplayText, hintFont, hintTextSize, currentRender, prevIndex, renders, displayedRender
    #     if started is None:
    #         started = state.counter



    #     index = (state.counter-started)//delay

        
    #     if index > len(HintText1)*1.1:
    #         currentDisplayText = ""
    #         renders = []
    #         return


    #     invalid = (index < 0 or index >= len(HintText1))
    #     if index != prevIndex and not invalid:    
    #         letter = HintText1[index]
    #         # print(letter)
    #         if letter == "\n":
    #             renders.append(currentRender)
    #             currentDisplayText = ""
    #         elif letter == "@":
    #             pass
    #         else:
    #             currentDisplayText = currentDisplayText + letter

    #         currentRender = hintFont.render(currentDisplayText, False, "white")
    #         displayedRender = currentRender
    #         if index%2==0:
    #             displayedRender = hintFont.render(currentDisplayText+" _ ", False, "white")

    #         prevIndex = index

   

    #     maxW = currentRender.get_size()[0] if len(renders)==0 else max(max([r.get_size()[0] for r in renders]),currentRender.get_size()[0])

    #     HintArea = pg.Surface((maxW+20,200+10), pg.SRCALPHA)
    #     HintArea.fill((0,0,0,255))
    #     screen.blit(HintArea, ((s.WIDTH-maxW-20)/2, s.HEIGHT*0.9-10))  

    #     for i in range(len(renders)):
    #         dispRend = renders[i]
    #         screen.blit(dispRend, ((s.WIDTH-dispRend.get_size()[0])/2, s.HEIGHT*0.9+i*hintTextSize*1.1))
    #     screen.blit(displayedRender, ((s.WIDTH-maxW)/2, s.HEIGHT*0.9+len(renders)*hintTextSize*1.1))
















    
    while state.game_loop:
        # clock.tick(s.MAX_FPS)
        clock.tick(s.MAX_FPS)

        D.add("FPS", clock.get_fps(), avg=20)

        P = BottleNeck()

        state.events = pg.event.get()
        keys = pg.key.get_pressed()

        mouse_position = pg.mouse.get_pos()

        #Escape
        for event in state.events:
            if event.type == pg.QUIT:
                state.game_loop = False
            
            if keys[pg.K_SPACE]:
                # enemy0.alive = True
                # spawn(position=(mx,my))
                pass

            if keys[pg.K_f]:
                s.MAX_FPS = 1
            if keys[pg.K_g]:
                s.MAX_FPS = 69

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    GoEscMenu()
            





        screen.fill(tuple(e+100 for e in (0, 0, 0)))  
        vis.overlay.fill((0, 0, 0, 240)) 

        screen.blit(background, wtsc((0,0), ))

        P.checkN("pastbackgrnd")

        move(position_circle, speed)



        
        #calc VTA
        radAlpha = np.deg2rad(-alpha)
        LTheta = radAlpha + fov/2
        RTheta = radAlpha - fov/2
        baseAngles = []
        hits = checkBases(LTheta, RTheta, s.WIDTH/4 * 3, HB_layer, precision=256)


        P.checkN("pastshadow")

        #cache Player ANimationz
        if moving:
            state.animDict["player_walk"].play_looped(position=position_circle, rotation=alpha)
        else:
            state.animDict["player_walk"].isActive = False


        #bullet calc
        shootCooldown -= 1
        for event in state.events: 
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and shootCooldown<=0 and state.bulletsInInv>0:  # Left mouse button
                    laser = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/bullet_new.png", image_scale=2, bullet_speed=35, lifetime=200)
                    entitySceneMain.add_friendlyBulletList(laser)
                    gunshot_sound.play()
                    shootCooldown = s.MAX_FPS/10
                    state.bulletsInInv -= 1 
                # if event.button == 3:
                #     rockety = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/rockety.png", image_scale=2, bullet_speed=15, lifetime=600, remote_control=True, isDiag=True, explosive=True, explosionRadius=75, isAnimated=True, damage=2000)
                #     entitySceneMain.add_friendlyBulletList(rockety)
                #     launch_missile.play()
        
        
        P.checkN("past bullets")

        #calc static player angle
        mx, my = screen_to_world_coords_rare_use(mouse_position, )
        mouse_HB.x = mx
        mouse_HB.y = my
        frame = pg.transform.rotate(static_player, alpha - 90)
        frame_rect = frame.get_rect(center = position_circle) 
        frame_rect.center = wtsc(position_circle, )
        
        if not moving:
            screen.blit(frame, frame_rect)   
        state.playerHB = HitBox(rect=((e-37.5 for e in(position_circle)), (75, 75)))
        # state.playerHB.show_HB()


        P.checkN("past playerlogf")

        #draw Corpses
        if state.CorpseList:
            for corpseImage, pos in state.CorpseList:
                screen.blit(corpseImage, tuple(e-32 * s.GameScale/1.5 for e in wtsc(pos, )))
        
        if len(state.CorpseList) > 10: #corps cap
            state.CorpseList.pop(0)
                    

        P.checkN("past coprs")

        #draw all Animations
        for anim in state.allAnimsList:
            if not anim.alive: 
                state.allAnimsList.remove(anim)
                anim.revive() #amimdict support - required for repeating (non looping) animationsz
            else: anim.update()


            
        P.checkN("past anims")


        #avoid clipping logic
        for HBs in HB_layerHBs:
            # HBs.show_HB()
            pushvec = HBs.get_push_vector(state.playerHB)
            velocity[0] -= pushvec[0]
            velocity[1] -= pushvec[1]
        

        for enemy in entitySceneMain.enemyList:
            for HBs in HB_layerHBs:
                pushvec = HBs.get_push_vector(enemy.hitbox)
                enemy.extra = (enemy.extra[0] - pushvec[0],enemy.extra[1] - pushvec[1])
            
            # for enemy2 in entitySceneMain.enemyList:
            #     if enemy != enemy2:
            #         pushvec = enemy2.hitbox.get_push_vector(enemy.hitbox)
            #         enemy.extra = (enemy.extra[0] - pushvec[0]*0.5,enemy.extra[1] - pushvec[1]*0.5)
                

        for bullet in entitySceneMain.friendlyBulletList:
            for HBs in HB_layerHBs:
                if bullet.hitbox.check_collision(HBs):
                    bullet.die()


                
        P.checkN("past HBs colls")



        # if keys[pg.K_RIGHT]:
        #     entitySceneMain.saveToFile()
        # if keys[pg.K_LEFT]:
        #     entitySceneMain.loadFromFile()
        #     # for en in entitySceneMain.enemyList:
        #     #     en.extra = (25, 0)"



            


        #draws the entity scene
        entitySceneMain.draw_EntityScene()
        P.checkN("past enemey pathfind and bvlit")



        #blit VTA
        screenHits = []
        for hit in hits:
            screenHits.append(wtsc(hit))

        pg.draw.polygon(vis.overlay, (0, 0, 0, 150), screenHits)
        pg.draw.circle(vis.overlay, (0, 0, 0, 150), wtsc(state.playerPos), 40)


        for enemy in entitySceneMain.enemyList:
            pg.draw.circle(vis.overlay, (10, 0, 0, 150), wtsc(enemy.position), 200)
        for enemy in entitySceneMain.enemyList:
            if enemy.lit:
                pg.draw.circle(vis.overlay, (150, 0, 0, 30), wtsc(enemy.position), state.counter%8*10+20)

        # screen.blit(blur_surface(vis.overlay, 0.2), (0, 0))
        # screen.blit()
        screen.blit(vis.overlay, (0, 0))
        

        # print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                

        P.checkN("past shadow blit")

        old_position_circle = position_circle.copy()

        hostageCounter = 0
        for i in range(len(entitySceneMain.hostageList)):
            hostage = entitySceneMain.hostageList[i]

            if hostage.hostageSaved:
                screen.blit(hostage_green, (s.WIDTH * (0.01 + i * 0.04), s.HEIGHT * 0.90))
                hostageCounter += 1
            else:
                screen.blit(hostage_red, (s.WIDTH * (0.01 + i * 0.04), s.HEIGHT * 0.90))

            if hostageCounter == len(entitySceneMain.hostageList):
                goTYScene()
            
            D.add("hostages", hostageCounter)
            D.add("length hostage list", len(entitySceneMain.hostageList))


        for i in range(state.bulletsInInv):
            screen.blit(bullet_green, (s.WIDTH * (0.875 + i * 0.02), s.HEIGHT * 0.925))
        

        screen.blit(crosshair, (mouse_position[0] - 16,mouse_position[1] - 16))

        if state.gameOver:
            GameOverSCreen()


        D.add("count", state.counter)
        state.counter += 1

        # drawHintText()
        D.add("mousPos", pg.mouse.get_pos())


        D.draw()
        pg.display.update()


    pg.quit()


                
if __name__ == "__main__":
    pss("main")






