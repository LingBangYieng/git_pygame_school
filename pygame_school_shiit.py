import os
os.environ["SDL_VIDEODRIVER"] = "windows"
import pygame as pg
import numpy as np
import time
from entityz import *
from helper_pygame import *
from globals import *
from settings import *
from helper2 import *



#inits
pg.display.init()
pg.mixer.init()
pg.mouse.set_visible(False)


#loads
crosshair = pg.image.load(f"assets/goofy_crosshair.png")
static_player = pg.image.load(f"assets/player_gun_static.png")

#transform loads
crosshair = pg.transform.scale_by(crosshair, 4)
static_player = pg.transform.scale_by(static_player, GameScale/2)


#Audio
gunshot_sound = pg.mixer.Sound(f"assets/silenced_gunshot.mp3")
launch_missile = pg.mixer.Sound("assets/rocket_launch.mp3")
missile_explo = pg.mixer.Sound("assets/rocket_explosion.mp3")
# lobby_song = pg.mixer.music.load("assets/retrowave_song.mp3")

#transform Audio 
launch_missile.set_volume(0.1)
missile_explo.set_volume(0.1)
gunshot_sound.set_volume(0.1)
# pg.mixer.music.set_volume(0,125)
# pg.mixer.music.play(-1)




speed = 10
position_circle = pg.Vector2((WIDTH)/2, (HEIGHT)/2)
old_position_circle = pg.Vector2((WIDTH)/2, (HEIGHT)/2)
velocity = pg.Vector2((0, 0))
moving = False
sprinting= False
radius = 20
counter = 0
game_loop = True



#own Class init
player_walk = Animationz(numFrames=13, imageScale=GameScale)
mouse_HB = state.MHB = HitBox(((0, 0),(1, 1)))
entitySceneMain = EntityScenez()



state.entityScene = entitySceneMain




#debugs
enemy0 = Enemyz(position=(1000, 1000), path_to_image="assets/bombi_static.png", image_scale=GameScale)
item0 = Itemz(position=(500, 500), path_to_image_non_highlighted="assets/hk_416.png", image_scale=1.5)

entitySceneMain.add_enemy(enemy0)
entitySceneMain.add_item(item0)




#ideas
"grenade launch with size rescaling"





#commands
def spawn(entityType="enemy", position=(1000, 1000)):
    global entitySceneMain
    entity = None
    match entityType:
        case "enemy":
            entity = Enemyz(position=position, path_to_image="assets/bombi_static.png", image_scale=GameScale)
        case "item":
            entity = Itemz(position=position, path_to_image_non_highlighted="assets/goofy_revolver.png", image_scale=1.5, image_rotation=45)
    if entity is not None:
        for enemy in entitySceneMain.enemyList:
            if enemy.position == position:
                return
        entitySceneMain.add_enemy(entity)
        # isreali_ambient = pg.mixer.Sound("assets/israeli_ambient_quiet.mp3")
        # isreali_ambient.set_volume(0.05)
        # isreali_ambient.play()
        # print("hehe")






def move(position_circle,speed):
    global alpha, moving, old_position_circle, sprinting, velocity


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
    
    vwp.topleft = (position_circle[0] - WIDTH/2, position_circle[1] - HEIGHT/2)



    mouse_pos = (pg.mouse.get_pos()[0] - WIDTH // 2, pg.mouse.get_pos()[1] - HEIGHT // 2)
    alpha = np.degrees(np.arctan2(-mouse_pos[1], mouse_pos[0]))
    

    moving = position_circle != old_position_circle

    state.playerPos = position_circle 



#!!Externalize background ahs to be given by homescreen (level like)


HB_layer = upscale_grid(bitmap())
# HB_layer = bitmap()

state.HB_layer = HB_layer

background = pg.image.load(f"saves/test_as.png")
background = pg.transform.scale_by(background, GameScale)

HB_layerHBs = getHitBox_HBLayer()







fov = np.deg2rad(fov_degr)


clock = pg.time.Clock()
# (46, 150, 172)

shootCooldown = 0


class BottleNeck:
    def checkN(gg, das):
        pass

while game_loop:
    clock.tick(MAX_FPS)

    P = BottleNeck()

    state.events = pg.event.get()
    keys = pg.key.get_pressed()

    mouse_position = pg.mouse.get_pos()

    #Escape
    for event in state.events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            game_loop = False
        
        if keys[pg.K_SPACE]:
            # enemy0.alive = True
            spawn(position=(mx,my))

        if keys[pg.K_f]:
            MAX_FPS = 1
        if keys[pg.K_g]:
            MAX_FPS = 69




    screen.fill(tuple(e+100 for e in (0, 0, 0)))  
    overlay.fill((0, 0, 0, 240)) 

    screen.blit(background, wtsc((0,0), ))

    P.checkN("pastbackgrnd")

    move(position_circle, speed)



    
    #calc VTA
    radAlpha = np.deg2rad(-alpha)
    LTheta = radAlpha + fov/2
    RTheta = radAlpha - fov/2
    baseAngles = []
    hits = checkBases(LTheta, RTheta, 1400, HB_layer)


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
            if event.button == 1 and shootCooldown<=0:  # Left mouse button
                laser = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/bullet_new.png", image_scale=2, bullet_speed=35, lifetime=200)
                entitySceneMain.add_friendlyBulletList(laser)
                gunshot_sound.play()
                shootCooldown = MAX_FPS/10
            if event.button == 3:
                rockety = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/rockety.png", image_scale=2, bullet_speed=15, lifetime=600, remote_control=True, isDiag=True, explosive=True, explosionRadius=75, isAnimated=True)
                entitySceneMain.add_friendlyBulletList(rockety)
                launch_missile.play()
    
    
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
    player_HB = HitBox(rect=((e-37.5 for e in(position_circle)), (75, 75)))
    player_HB.show_HB()


    P.checkN("past playerlogf")

    #draw Corpses
    if state.CorpseList:
        for corpseImage, pos in state.CorpseList:
            screen.blit(corpseImage, tuple(e-32 * GameScale/1.5 for e in wtsc(pos, )))
    
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
        HBs.show_HB()
        pushvec = HBs.get_push_vector(player_HB)
        velocity[0] -= pushvec[0]
        velocity[1] -= pushvec[1]
    

    for enemy in entitySceneMain.enemyList:
        for HBs in HB_layerHBs:
            pushvec = HBs.get_push_vector(enemy.hitbox)
            enemy.extra = (enemy.extra[0] - pushvec[0],enemy.extra[1] - pushvec[1])
        
        for enemy2 in entitySceneMain.enemyList:
            if enemy != enemy2:
                pushvec = enemy2.hitbox.get_push_vector(enemy.hitbox)
                enemy.extra = (enemy.extra[0] - pushvec[0]*0.5,enemy.extra[1] - pushvec[1]*0.5)
            

            
    P.checkN("past HBs colls")



    # if keys[pg.K_RIGHT]:
    #     for en in entitySceneMain.enemyList:
    #         en.extra = (25, 0)



        


    #draws the entity scene
    entitySceneMain.draw_EntityScene()
    P.checkN("past enemey pathfind and bvlit")

    screen.blit(crosshair, (mouse_position[0] - 16,mouse_position[1] - 16))


    #blit VTA
    screenHits = []
    for hit in hits:
        screenHits.append(wtsc(hit,))

    pg.draw.polygon(overlay, (0, 0, 0, 150), screenHits)
    pg.draw.circle(overlay, (0, 0, 0, 150), wtsc(state.playerPos, ), 40)

    for enemy in entitySceneMain.enemyList:
        pg.draw.circle(overlay, (10, 0, 0, 150), wtsc(enemy.position, ), 200)
    for enemy in entitySceneMain.enemyList:
        pg.draw.circle(overlay, (150, 0, 0, 30), wtsc(enemy.position, ), counter%8*10+20)

    screen.blit(blur_surface(overlay, 0.2), (0, 0))
    screen.blit(overlay, (0, 0))
    


    P.checkN("past shadow blit")

    old_position_circle = position_circle.copy()



    counter += 1
    pg.display.update()


pg.quit()


                








