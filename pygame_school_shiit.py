import os
os.environ["SDL_VIDEODRIVER"] = "windows"
import pygame as pg
import numpy as np
from helper_pygame import spritesheet_cutter_2d, Bullet


game_loop = True



pg.display.init()
pg.mixer.init()


size = 12
scale_player = 4
width, height = 200, 100
screen = pg.display.set_mode((width*size, height*size))
pg.mouse.set_visible(False)
laser_data_list = []



background = pg.image.load(f"assets/big_background.jpg")
item0 = pg.image.load(f"assets/goofy_revolver.png")
item1 = pg.image.load(f"assets/goofy_katana.png")
entrance = pg.image.load(f"assets/goofy_entrance.png")
static_laser = pg.image.load(f"assets/goofy_laser.png")
crosshair = pg.image.load(f"assets/goofy_crosshair.png")
static_player = pg.image.load(f"assets/middled_player.png")
sprite_sheet_player_walking = pg.image.load(f"assets/goofy_player_walk_forward.png")
frame_width_player_walking = 32
frame_height_player_walking = 32
num_frames_player_walking = 13
frames_player_walking = spritesheet_cutter_2d(frame_width_player_walking, frame_height_player_walking, num_frames_player_walking, sprite_sheet_player_walking)
crosshair = pg.transform.scale_by(crosshair, 4)
static_laser = pg.transform.scale_by(static_laser, 2)
entrance = pg.transform.scale_by(entrance, 1)
static_player = pg.transform.scale_by(static_player, scale_player)
laser_sound = pg.mixer.Sound(f"assets/goofy_laser.mp3")
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
view_field_xy_position = pg.Rect(0, 0, width*size, height*size)



# grenade launch with size rescaling

def world_to_screen_coords(world_coords_object):
    
    screen_coords = world_coords_object[0] - view_field_xy_position.topleft[0], world_coords_object[1] - view_field_xy_position.topleft[1]
    return screen_coords



 
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

    return position_circle, view_field_xy_position



animation_speed = 0.2  
frame_index = 0

clock = pg.time.Clock()
# (46, 150, 172)
print("gamne loop")
while game_loop:


    events = pg.event.get()

    clock.tick(69)
    # pygame.QUIT event means the user clicked X to close your window
    mouse_position = pg.mouse.get_pos()
    keys = pg.key.get_pressed()
    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            game_loop = False




    move(position_circle, speed)

    if sprinting:
        animation_speed = 0.3
        sprinting = not sprinting
    else:
        animation_speed = 0.2

    if moving:
        frame_index += animation_speed
        
        if frame_index >= len(frames_player_walking):
            frame_index = 0

        frame = frames_player_walking[int(frame_index)]
        frame = pg.transform.scale_by(frame, scale_player)


    else:
        frame = static_player
   

    player = pg.transform.rotate(frame, alpha - 90)
    player_rect = player.get_rect(center = (width*size//2, height*size//2)) 
    player_sprite_rect = pg.Rect(0,0, 32*scale_player,32*scale_player)
    player_sprite_rect.center = (width*size//2, height*size//2)




    screen.fill((0, 0, 0))  
    screen.blit(background, world_to_screen_coords((0,0)))

   

    for event in events: 
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 or keys[pg.K_f]:  # Left mouse button
                laser_data_list.append(Bullet(25, static_laser, (position_circle[0], position_circle[1]), alpha))
                laser_sound.play()
                # laser_data_list.append((mouse_position[0] + position_circle[0] - width*size/2, mouse_position[1] + position_circle[1] - height*size/2, alpha))
        elif keys[pg.K_r]:
                laser_data_list.append(Bullet(25, static_laser, (position_circle[0], position_circle[1]), alpha))
                laser_sound.play()


    for laser_data in laser_data_list:
        laser = pg.transform.rotate(laser_data.sprite, laser_data.alpha - 90)
        laser_rect = laser.get_rect(center = (laser_data.position[0] + 16, laser_data.position[1] + 16))  # 16 --> bullet sprite size
        laser_data.move()
        screen.blit(laser, world_to_screen_coords(laser_data.position))
        if abs(laser_data.position[0]) >= width * size * 2 or abs(laser_data.position[1]) >= height * size * 2 or len(laser_data_list) > 100:
            laser_data_list.pop(0)

    
    

    screen.blit(player, player_rect)   
    screen.blit(item0, (world_to_screen_coords((500,500))))
    screen.blit(item1, (world_to_screen_coords((400,400))))
    screen.blit(entrance, (world_to_screen_coords((600,600))))
    
    screen.blit(crosshair, (mouse_position[0] - 16, mouse_position[1] - 16))



    old_position_circle = position_circle.copy()
    pg.display.update()





