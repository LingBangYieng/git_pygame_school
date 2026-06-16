import pygame as pg
from pathlib import Path
# from helper_pygame import image_color_shifter
import tkinter as tk
import numpy as np
from PIL import Image
from helper_pygame import *
def image_color_shifter(path_to_image: str, color_shift: str, name: str, strength: int = 0.25) -> str:       # adds a color shift (white'll look greenish or other color'ish) to an image

    possible_color_shifts = {               # dict that stores color tuples (rgb) keys are strings that are given in argumentss
        "white":  (255, 255, 255),
        "red":    (255, 0, 0),
        "yellow": (255, 255, 0),
        "green":  (0, 255, 0),
        "cyan":   (0, 255, 255),
        "blue":   (0, 0, 255),
        "purple": (255, 0, 255),
        "black":  (0, 0, 0),
        "best":   (46, 150, 172)
    }


    if color_shift in possible_color_shifts:      # iterates over list and finds corresponding tuple for key (string given in args)
        color_shift_tuple = possible_color_shifts[color_shift]  # dict syntax set a variable to dict(key-->(color_shift))
        
    else:   
        raise ValueError(
        f"Invalid color_shift '{color_shift}'. "
        f"Must be one of: {list(possible_color_shifts.keys())}"     # if that isnt true the key doesnt exist --> function cant work, returns error
        )           

    original_image = Image.open(path_to_image)  # loads the image for later edits

    img_array = np.array(original_image)    # converts the original image into an np.array (matrix conatining tuples)

    img_array = np.array(original_image, dtype=np.float32)  # sets the value in the rgb tuples to be higher than uint8 (8 bits) --> allows for better adjustements in color to not overflow the uint 8 --> (setting it to its max (255))

    for row in range(len(img_array)):
        for col in range(len(img_array[row])):      # iterates through image matrix

            img_array[row, col, 0] += (1 - strength) + color_shift_tuple[0] * strength  # applies at row, col and index of tuple the effect which is calculated through / blends the pixel toward the target color based on strength (higher strength = stronger tint)
            img_array[row, col, 1] += (1 - strength) + color_shift_tuple[1] * strength
            img_array[row, col, 2] += (1 - strength) + color_shift_tuple[2] * strength

    img_array = np.clip(img_array, 0, 255).astype(np.uint8) # turns it back into uint8 to be valid for rgb tuples
    new_img = Image.fromarray(img_array)    # opposite to np.array --> converts np.array into an image
    new_img.save(f"assets/color_shifted/{name}_image.png")  # saves to image to given path / folder
    path_to_new_img = f"assets/color_shifted/{name}_image.png"  # saves the exact saving location in variable
    return path_to_new_img  # return path string for later pygame use


pg.font.init()
pg.display.init()     

def update_map_builder_sprites():

    for i, file in enumerate(library_folder.iterdir()):
        if file.suffix == ".png":
            image = pg.image.load(f"assets/map_builder_sprites/{file.stem}.png")
            for i in range(0, 4):
                timage = pg.transform.rotate(image, i*90)
                pg.image.save(timage, f"assets/map_builder_sprites_rotated/{i*90}_{file.stem}_image.png")
                sprite_dict[f"assets/map_builder_sprites_rotated/{i*90}_{file.stem}_image.png"] = timage = pg.transform.scale_by(pg.image.load(f"assets/map_builder_sprites_rotated/{i*90}_{file.stem}_image.png"), zoom)
                

def update_color_shifted():

    for i, file in enumerate(library_folder.iterdir()):
        if file.suffix == ".png":
            string_current_shift = image_color_shifter(f"assets/map_builder_sprites/{file.stem}.png", "blue", file.stem, 0.5)
            image = pg.image.load(string_current_shift)
            image = pg.transform.scale_by(image, zoom*3/4)
            print(string_current_shift)
            for i in range(0, 4):
                timage = pg.transform.rotate(image, i*90)
                pg.image.save(timage, f"assets/color_shifted/{i*90}_{file.stem}_image.png")


def save_save_grid(visual_grid, filename="temp_save", saveImg=False):
    save_grid = [[[(tup[1],tup[2]) if isinstance(tup, tuple) else 0 for tup in row ] for row in layer] for layer in visual_grid]
    with open(f"saves/{filename}.map", "w") as f:
        f.write(f"{save_grid}")
    if saveImg:
        pg.image.save(screen, f"saves/{filename}_as.png")

def tup_to_sprite(tup):
    rotation, current_sprite_name = tup
    sprite = pg.image.load(f"assets/map_builder_sprites_rotated/{rotation}_{current_sprite_name}_image.png")
    return pg.transform.scale_by(sprite, zoom)


def load_save_grid(filename):
    save_grid = None
    with open(f"saves/{filename}.map", "r") as f:
        save_grid = eval(f.read())
    visual_grid = [[[(tup_to_sprite(tup), tup[0], tup[1]) if isinstance(tup, tuple) else 0 for tup in row ] for row in layer] for layer in save_grid]
    return visual_grid











def in_menu_func(events):
 
    global current_sprite, in_menu, ignore_next_click, old_current_sprite, scroll_displacement, current_sprite_name

    sprite_text_positions = {}

    #scroll
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 4:
                scroll_displacement += 35
            if event.button == 5:
                scroll_displacement -= 35



    for i, file in enumerate(library_folder.iterdir()):

        #DRAW Text,Icon,Box
        text = font.render(f"{file.stem}", True, (255, 255, 255))

        x = (state.WIDTH - text.get_width()) // 2
        y = state.HEIGHT // 10 + 60 * (i) + scroll_displacement
        w = text.get_width()
        h = text.get_height()

        
        screen.blit(text, (x, y))
        current_sprite_library = pg.image.load(f"assets/map_builder_sprites/{file.stem}.png")
        screen.blit(current_sprite_library, (x + 10 + w, y))
        w_curr, h_curr = current_sprite_library.get_size()

        x_hit_rect = x - 10 
        y_hit_rect = y - 10 
        w_hit_rect = w + 30 + w_curr
        h_hit_rect = h_curr + 20

        pg.draw.rect(screen, (0, 0, 0), (x_hit_rect , y_hit_rect, w_hit_rect, h_hit_rect), 2)
        screen.blit(crosshair, (mouse_pos[0] - 8, mouse_pos[1] - 8))
        #end DRAW Text,Icon,Box



        sprite_text_positions[file.stem] = (x_hit_rect, y_hit_rect, w_hit_rect, h_hit_rect)

        m_x, m_y = mouse_pos #global

        for name, (x, y, w, h) in sprite_text_positions.items():

            if x <= m_x <= x + w and y <= m_y <= y + h:
                
                for event in events:

                    if event.type == pg.MOUSEBUTTONDOWN:

                        if event.button == 1:

                            current_sprite_name = name
                            current_sprite = pg.image.load(f"assets/map_builder_sprites/{name}.png")
                            current_sprite = pg.transform.scale_by(current_sprite, zoom)
                            in_menu = False
                            ignore_next_click = True

                            print(f"clicked on: {name}")


        

        print(scroll_displacement)
                        







game_loop = True
size = 1
state.WIDTH, state.HEIGHT = 2560, 1440
screen = pg.display.set_mode((state.WIDTH, state.HEIGHT))  
fade = pg.Surface((state.WIDTH, state.HEIGHT))
fade.fill((0,0,0)) 
font = pg.font.Font(None, 36)
field_size = 48
zoom = field_size/32
rotation = 0
scroll_displacement = 0





library_folder = Path("assets/map_builder_sprites/")

layers = 3
visual_grid = [[[0]*int(state.WIDTH//field_size) for _ in range(int(state.HEIGHT//field_size))] for __ in range(layers)]


in_menu = False
draw_grid = False
place_delete = True
preview = True
ignore_next_click = False
do_transition = False
transition_backwards = False
save_rewuest =False



crosshair = pg.image.load(f"assets/goofy_crosshair.png")
crosshair = pg.transform.scale_by(crosshair, zoom)
place_crosshair = pg.image.load(f"assets/placing_crosshair.png")
place_crosshair = pg.transform.scale_by(place_crosshair, 0.5)

current_sprite_name = "la_toilette"
current_sprite = pg.image.load(f"assets/map_builder_sprites/{current_sprite_name}.png")
current_sprite = pg.transform.scale_by(current_sprite, zoom)
old_current_sprite = pg.image.load(f"assets/map_builder_sprites/{current_sprite_name}.png")
current_sprite_preview = pg.image.load(f"assets/map_builder_sprites/{current_sprite_name}.png")


clock = pg.time.Clock()   
counter = 0



save_grid = []

sprite_dict = {}



#LAYER
build_layer = 0
layer_mode = False
red_layer = pg.image.load("assets/map_signals/red.png")
red_layer = pg.transform.scale_by(red_layer, zoom)

#BUILD
rmb_held = False
lmb_held = False


update_color_shifted()
update_map_builder_sprites()


while game_loop:   

    clock.tick()    
    mouse_pos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()  
    events = pg.event.get()

    if current_sprite != old_current_sprite:
        current_sprite_preview = pg.image.load(f"assets/color_shifted/{rotation%360}_{current_sprite_name}_image.png")


    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE] or keys[pg.K_q]:

            game_loop = False    

    if in_menu:
        screen.fill((100, 100, 100))
        in_menu_func(events)
    
    else:
        screen.fill((100, 100, 100)) # change for fututer maps
        pg.mouse.set_visible(False)


    for event in events: 

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_m or event.key == pg.K_TAB:
                in_menu = not in_menu
                
            
            if in_menu == False:

                if event.key == pg.K_r:

                    rotation += 90

                if event.key == pg.K_g:
                    draw_grid = not draw_grid
                    print(draw_grid)
                
                if event.key == pg.K_p:
                    preview = not preview

                if event.key == pg.K_s:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
                        save_rewuest = True

                if event.key == pg.K_o:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
                        visual_grid = load_save_grid(input("enter filename: "))                  
                      
                if event.key == pg.K_t:
                    do_transition = True
                    mouse_transition_start = mouse_pos

                if event.key == pg.K_h:
                    current_sprite = pg.image.load(f"assets/map_builder_sprites/hitbox_full.png")
                    current_sprite = pg.transform.scale_by(current_sprite, zoom)

                if event.key == pg.K_0:
                    visual_grid = [[[0]*int(state.WIDTH//field_size) for _ in range(int(state.HEIGHT//field_size))] for __ in range(layers)]



                #LAYER CONTROL

                if event.key == pg.K_l:
                    layer_mode = not layer_mode
                    print("HHH")

                if event.key == pg.K_1 or event.key == pg.K_KP_PLUS:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT] or event.key == pg.K_KP_PLUS:
                        print("plus")
                        build_layer += 1
                        if build_layer > 2:
                            build_layer = 2

                if event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                    print("minus")
                    build_layer -= 1
                    if build_layer < 0:
                        build_layer = 0

        #BUILD HOLD
        rmb_held = pg.mouse.get_pressed()[2]
        lmb_held = pg.mouse.get_pressed()[0]
        


        if round(mouse_pos[1] // field_size) < int(state.HEIGHT//field_size) and round(mouse_pos[0] // field_size) < int(state.WIDTH//field_size):
            if (lmb_held or rmb_held or event.type == pg.MOUSEBUTTONDOWN) and in_menu == False:
                if lmb_held or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1): 
                    if ignore_next_click:

                        ignore_next_click = False
                        continue

                    x = mouse_pos[0] // field_size
                    y = mouse_pos[1] // field_size

                    print(x,y)
                    
                    if visual_grid[build_layer][y][x] == 0:
                        visual_grid[build_layer][y][x] = (sprite_dict[f"assets/map_builder_sprites_rotated/{rotation%360}_{current_sprite_name}_image.png"],  rotation%360, current_sprite_name)
                        print(f"changed field:{y},{x}")


                if rmb_held or (event.type == pg.MOUSEBUTTONDOWN and event.button == 3): 

                    x = mouse_pos[0] // field_size
                    y = mouse_pos[1] // field_size
                    
                    if visual_grid[build_layer][y][x] != 0:
                        visual_grid[build_layer][y][x] = 0
                        print(f"changed field:{y},{x}")

                if (event.type == pg.MOUSEBUTTONDOWN and event.button == 2):
                    print( [round(mouse_pos[1] // field_size)])
                    print([round(mouse_pos[0] // field_size)])
                    if visual_grid[build_layer][round(mouse_pos[1] // field_size)][round(mouse_pos[0] // field_size)] != 0:
                        current_sprite, rotation, current_sprite_name = visual_grid[build_layer][round(mouse_pos[1] // field_size)][round(mouse_pos[0] // field_size)]
                        print("H",rotation)
                    

                
        save_save_grid(visual_grid)








    if counter == 0:
        visual_grid = load_save_grid("temp_save")


    if in_menu == False:
        if layer_mode:
            show_layers = range(build_layer+1)
        else:
            show_layers = range(0,3)
        
        for local_layer in show_layers:
            for row in range(len(visual_grid[local_layer])):
                for col in range(len(visual_grid[local_layer][row])):
                    coords = (col * field_size, row * field_size)
                    
                    x = coords[0]
                    y = coords[1]

                    if isinstance(visual_grid[local_layer][row][col], tuple):
                        iteration_image = visual_grid[local_layer][row][col][0]
                        screen.blit(iteration_image, (x, y))

                    if not save_rewuest:
                        if local_layer == build_layer:

                            if draw_grid:
                                pg.draw.rect(screen, (255, 255, 255), (x, y, field_size, field_size), 1)
                                            
                            if preview and place_delete:
                                screen.blit(current_sprite_preview, (round(mouse_pos[0] // field_size) * field_size + field_size/8, round(mouse_pos[1] // field_size) * field_size + field_size/8))


                        #LAYER
                        if layer_mode and visual_grid[local_layer][row][col]==0:
                            screen.blit(red_layer, (x,y))



            if not save_rewuest:
                screen.blit(place_crosshair, (mouse_pos[0]-8, mouse_pos[1]-8))
    if not save_rewuest:
        if True or layer_mode:
            font = pg.font.Font(None, 30)
            text = font.render(f"layer: {build_layer}", True, (0,0,0))
            screen.blit(text, (5, 5))


    counter += 1

    pg.display.update()

    if save_rewuest:
        save_save_grid(visual_grid, input("enter filename: "), True)
        save_rewuest = False

pg.quit()