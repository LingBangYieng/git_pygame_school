import os
os.environ["SDL_VIDEODRIVER"] = "windows"
import pygame as pg
import numpy as np
from entityz import *
from helper_pygame import *
from class_collide_rect import *

from globals import *

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
static_player = pg.image.load(f"assets/middled_player.png")

player_walk = Animationz(numFrames=13, imageScale=scale_player)

crosshair = pg.transform.scale_by(crosshair, 4)
static_laser = pg.transform.scale_by(static_laser, 2)
# entrance = pg.transform.scale_by(entrance, 1)
static_player = pg.transform.scale_by(static_player, scale_player)
laser_sound = pg.mixer.Sound(f"assets/goofy_laser.mp3")
launch_missile = pg.mixer.Sound("assets/rocket_launch.mp3")
missile_explo = pg.mixer.Sound("assets/rocket_explosion.mp3")
launch_missile.set_volume(0.1)
missile_explo.set_volume(0.1)
laser_sound.set_volume(0.1)
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


mouse_HB = HitBox(((0, 0),(1, 1)))




enemy = pg.image.load(f"assets/middled_player2.png")
enemy = pg.transform.scale_by(enemy, scale_player)
enemy_pos = (1000, 1000)
enemy_alive = True

laser_data_list = []


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
    if mouse_pos[1] < 0:
        alpha = (np.acos(mouse_pos[0]/ np.linalg.norm(np.array(mouse_pos)))) * 180 / np.pi
    else:
        alpha = -(np.acos(mouse_pos[0]/ np.linalg.norm(np.array(mouse_pos)))) * 180 / np.pi

    moving = position_circle != old_position_circle

    return position_circle


import time
animation_speed = 0.2  
frame_index = 0

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
            enemy_alive = True

        if keys[pg.K_f]:
            fps = 2
        if keys[pg.K_g]:
            fps = 69

    screen.fill((0, 0, 0))  
    screen.blit(background, world_to_screen_coords((0,0), view_field_xy_position))

    move(position_circle, speed)


    if sprinting:
        animation_speed = 0.3
        sprinting = not sprinting
    else:
        animation_speed = 0.2

    if moving:
        player_walk.play_looped(position=position_circle, rotation=alpha)
    else:
        frame = static_player



    for event in events: 
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 or keys[pg.K_f]:  # Left mouse button
                laser_data_list.append(Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/goofy_laser.png", image_scale=2, bullet_speed=25, lifetime=200))
                laser_sound.play()
            if event.button == 3:
                laser_data_list.append(Bulletz(position=position_circle, hitbox=HitBox(((0, 0), (5, 5))), path_to_image="assets/rockety.png", image_scale=2, bullet_speed=15, lifetime=600, remote_control=True, isDiag=True))
                launch_missile.play()


    clean_list = [e for e in laser_data_list]


    for i in range(len(laser_data_list)):
        laser_data = laser_data_list[i]
        if not laser_data.alive:
            clean_list.pop(i)

    laser_data_list = clean_list

    laser_data = None

    for i in range(len(laser_data_list)):
        laser_data = laser_data_list[i]
        laser_data.draw()


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
    # player_HB.show_HB()

    screen.blit(crosshair, (mouse_position[0] - 16, mouse_position[1] - 16))


    # screen.blit(item0, (world_to_screen_coords((500,500), view_field_xy_position)))
    # item0_HB = HitBox(((500,500), item0.get_size()))

    # screen.blit(item1, (world_to_screen_coords((400,400), view_field_xy_position)))
    # screen.blit(entrance, (world_to_screen_coords((600,600), view_field_xy_position)))

    item0 = Itemz(position=(500, 500), path_to_image_non_highlighted="assets/goofy_revolver.png", image_scale=1.5, image_rotation=45)


    enemy_rect = enemy.get_rect(center=enemy_pos)
    enemy_HB = HitBox(((e-37.5 for e in enemy_pos), (75, 75)))

    if enemy_alive:
        screen.blit(enemy, world_to_screen_coords(enemy_rect, vwp))
        # enemy_HB.show_HB()

    if laser_data is not None:
        if enemy_HB.check_collision(laser_data.hitbox): 
            # enemy_HB.show_HB(color=(0, 255, 0))
            explosion = Animationz(pathToSpriteSheet="assets/may_explosion.png", numFrames=6, imageScale=4, animationSpeed=0.3)
            missile_explo.play()
            enemy_alive = False
            laser_data.alive = False

    if enemy_HB is not None:
        if enemy_alive == False:
                explosion.play((enemy_HB.x + enemy_HB.w/2, enemy_HB.y + enemy_HB.h/2))
            
    item0.draw()
    item0.hitbox.show_HB()

    mouse_HB.show_HB()

    old_position_circle = position_circle.copy()
    pg.display.update()



                








