import os
os.environ["SDL_VIDEODRIVER"] = "windows"
import pygame as pg
import numpy as np
from entityz import *
from helper_pygame import *
from class_collide_rect import *

#from globals import *

game_loop = True



pg.display.init()
pg.mixer.init()



pg.mouse.set_visible(False)
# laser_data_list: list[Bullet] = []



# item0 = pg.image.load(f"assets/goofy_revolver_highlighted.png")
# item1 = pg.image.load(f"assets/goofy_katana_highlighted.png")
# entrance = pg.image.load(f"assets/goofy_entrance.png")
background = pg.image.load(f"assets/big_background.jpg")
static_laser = pg.image.load(f"assets/goofy_laser.png")
crosshair = pg.image.load(f"assets/goofy_crosshair.png")
static_player = pg.image.load(f"assets/player_gun_static.png")

player_walk = Animationz(numFrames=13, imageScale=scale_player)

crosshair = pg.transform.scale_by(crosshair, 4)
static_laser = pg.transform.scale_by(static_laser, 2)
# entrance = pg.transform.scale_by(entrance, 1)
static_player = pg.transform.scale_by(static_player, scale_player/2)
gunshot_sound = pg.mixer.Sound(f"assets/silenced_gunshot.mp3")
launch_missile = pg.mixer.Sound("assets/rocket_launch.mp3")
missile_explo = pg.mixer.Sound("assets/rocket_explosion.mp3")
launch_missile.set_volume(0.1)
missile_explo.set_volume(0.1)
gunshot_sound.set_volume(0.1)
# lobby_song = pg.mixer.music.load("assets/retrowave_song.mp3")
# pg.mixer.music.set_volume(0,125)
# pg.mixer.music.play(-1)
speed = 1 * size / 1
position_circle = pg.Vector2((width*size)/2, (height*size)/2)
old_position_circle = pg.Vector2((width*size)/2, (height*size)/2)
velocity = pg.Vector2((0, 0))
moving = False
sprinting= False
radius = 20
counter = 0


mouse_HB = MHB_rect[0] = HitBox(((0, 0),(1, 1)))

entitySceneMain = EntityScenez()
entityScenes[0] = entitySceneMain


item0 = Itemz(position=(500, 500), path_to_image_non_highlighted="assets/hk_416.png", image_scale=1.5)

enemy0 = Enemyz(position=(1000, 1000), path_to_image="assets/bombi_static.png", image_scale=scale_player)
# enemy1 = Enemyz(position=(500, 1000), path_to_image="assets/middled_player2.png", image_scale=scale_player)
# for i in range(10):
#     entitySceneMain.add_enemy(Enemyz(position=(i*10, 1000), path_to_image="assets/middled_player2.png", image_scale=scale_player))
entitySceneMain.add_enemy(enemy0)
# entitySceneMain.add_enemy(enemy1)
entitySceneMain.add_item(item0)



def spawn(entityType="enemy", position=(1000, 1000)):
    global entitySceneMain
    entity = None
    match entityType:
        case "enemy":
            entity = Enemyz(position=position, path_to_image="assets/bombi_static.png", image_scale=scale_player)
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
        print("hehe")

# grenade launch with size rescaling





 
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

    # velocity.xy *= 0.99 #icy
    velocity.xy = 0, 0 
    
    view_field_xy_position.topleft = (position_circle[0] - width*size/2, position_circle[1] - height*size/2)



    mouse_pos = (pg.mouse.get_pos()[0] - width*size//2, pg.mouse.get_pos()[1] - height*size//2)
    alpha = None
    save_mouse_pos = tuple(0.001 if abs(p)<0.001 else p for p in mouse_pos)
    if save_mouse_pos[1] < 0:
        alpha = (np.acos(save_mouse_pos[0]/ np.linalg.norm(np.array(save_mouse_pos)))) * 180 / np.pi
    else:
        alpha = -(np.acos(save_mouse_pos[0]/ np.linalg.norm(np.array(save_mouse_pos)))) * 180 / np.pi
    

    moving = position_circle != old_position_circle

    playerPos[0] = position_circle 




from helper2 import *

HB_layer = upscale_grid(bitmap())

state["HB_layer"] = HB_layer

background = pg.image.load(f"saves/test_as.png")
background = pg.transform.scale_by(background, scale_player)






clock = pg.time.Clock()
# (46, 150, 172)
fps = 69
while game_loop:
    events = pg.event.get()
    clock.tick(fps)
    # pygame.QUIT event means the user clicked X to close your window
    mouse_position = pg.mouse.get_pos()
    keys = pg.key.get_pressed()
    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            game_loop = False
        
        if keys[pg.K_SPACE]:
            # enemy0.alive = True
            spawn(position=(mx,my))

        if keys[pg.K_f]:
            fps = 5
        if keys[pg.K_g]:
            fps = 69



    screen.fill(tuple(e for e in (0, 0, 0)))  
    screen.blit(background, world_to_screen_coords((0,0), vwp))

    move(position_circle, speed)



    # for row in range(len(HB_layer)):
    #     for col in range(len(HB_layer[0])):
    #         if HB_layer[row][col]:
    #             pg.draw.rect(screen, "white", (world_to_screen_coords((col*CellSize, row*CellSize), vwp),(CellSize, CellSize)))


    if moving:
        animDict["player_walk"].play_looped(position=position_circle, rotation=alpha)
    else:
        animDict["player_walk"].isActive = False


    for event in events: 
        if event.type == pg.MOUSEBUTTONDOWN:
            # if event.button == 1:  # Left mouse button
            #     laser = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/bullet_new.png", image_scale=2, bullet_speed=35, lifetime=200)
            #     entitySceneMain.add_friendlyBulletList(laser)
            #     gunshot_sound.play()
            if event.button == 3:
                rockety = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/rockety.png", image_scale=2, bullet_speed=15, lifetime=600, remote_control=True, isDiag=True, explosive=True, explosionRadius=75, isAnimated=True)
                entitySceneMain.add_friendlyBulletList(rockety)
                launch_missile.play()
    
    if pg.mouse.get_pressed()[0] and counter % 4 == 0:
        laser = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/bullet_new.png", image_scale=2, bullet_speed=35, lifetime=200)
        entitySceneMain.add_friendlyBulletList(laser)
        gunshot_sound.play()
    
    # if pg.mouse.get_pressed()[1] and counter % 1 == 0:
    #     rockety = Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/rockety.png", image_scale=2, bullet_speed=15, lifetime=600, remote_control=True, isDiag=True, explosive=True, explosionRadius=75, isAnimated=True)
    #     entitySceneMain.add_friendlyBulletList(rockety)
    #     launch_missile.play()

    mx, my = screen_to_world_coords_rare_use(pg.mouse.get_pos(), vwp)
    mouse_HB.x = mx
    mouse_HB.y = my
    frame = pg.transform.rotate(static_player, alpha - 90)
    frame_rect = frame.get_rect(center = position_circle) 
    frame_rect.center = world_to_screen_coords(position_circle, vwp)
    
    if not moving:
        screen.blit(frame, frame_rect)   
    player_HB = HitBox(rect=((e-37.5 for e in(position_circle)), (75, 75)))
    # pg.draw.rect(screen, "red", (world_to_screen_coords((position_circle), view_field_xy_position)[0] - 50, world_to_screen_coords((position_circle), view_field_xy_position)[1] - 50, 100, 100), 3)
    player_HB.show_HB()

    mouse_HB.show_HB()



    pg.draw.circle(screen, "red", world_to_screen_coords((0, 0), vwp), 5)
    # print(playerPos[0])

    if CorpseList:
        for corpseImage, pos in CorpseList:
            screen.blit(corpseImage, tuple(e-32 for e in world_to_screen_coords(pos, vwp)))

    # print(len(allAnimsList))
    for anim in allAnimsList:
        if not anim.alive: 
            allAnimsList.remove(anim)
            anim.revive() #amimdict support - required for repeating (non looping) animationsz
        else: anim.update()

    entitySceneMain.draw_EntityScene()

    screen.blit(crosshair, (mouse_position[0] - 16, mouse_position[1] - 16))



    old_position_circle = position_circle.copy()
    pg.display.update()

    print(len(entitySceneMain.enemyList))

    counter += 1
    print(counter)
pg.quit()


                








