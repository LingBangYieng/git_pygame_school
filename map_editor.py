import pygame as pg
from pathlib import Path
from helper_pygame import image_color_shifter


pg.font.init()
pg.display.init()      





def in_menu_func(events):

    global current_sprite, in_menu, current_sprite_string, ignore_next_click, old_current_sprite, scroll_displacement

    sprite_text_positions = {}


    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 4:
                scroll_displacement += 35
            if event.button == 5:
                scroll_displacement -= 35



    for i, file in enumerate(library_folder.iterdir()):

        text = font.render(f"{file.stem}", True, (255, 255, 255))

        x = (width*size - text.get_width()) // 2
        y = height // 10 + 60 * (i) + scroll_displacement
        w = text.get_width()
        h = text.get_height() + scroll_displacement

        

        screen.blit(text, (x, y))
        current_sprite_library = pg.image.load(f"assets/map_builder_sprites/{file.stem}.png")
        screen.blit(current_sprite_library, (x + 10 + w, y))
        w_curr, h_curr = current_sprite_library.get_size()

        x_hit_rect = x - 10 
        y_hit_rect = y - 10 
        w_hit_rect = w + 30 + w_curr
        h_hit_rect = h_curr + 20

        

        pg.draw.rect(screen, (0, 0, 0 ), (x_hit_rect , y_hit_rect, w_hit_rect, h_hit_rect), 2)

        # screen.blit(current_sprite_library, (x + 10 + w, y))
        # w_curr, h_curr = current_sprite_library.get_size()
        # pg.draw.rect(screen, (0, 0, 0 ), (x -10 , y - 10, w + 30 + w_curr, h_curr + 20), 2)

        screen.blit(crosshair, (mouse_pos[0] - 8, mouse_pos[1] - 8))

        sprite_text_positions[file.stem] = (x_hit_rect, y_hit_rect, w_hit_rect, h_hit_rect)

        m_x, m_y = mouse_pos

        for name, (x, y, w, h) in sprite_text_positions.items():

            if x <= m_x <= x + w and y <= m_y <= y + h:
                
                for event in events:

                    if event.type == pg.MOUSEBUTTONDOWN:

                        if event.button == 1:

                            current_sprite_string = f"assets/map_builder_sprites/{name}.png"
                            current_sprite = pg.image.load(current_sprite_string)
                            current_sprite = pg.transform.scale_by(current_sprite, 2)
                            in_menu = False
                            ignore_next_click = True

                            print(f"clicked on: {name}")


        

        print(scroll_displacement)
                        







game_loop = True
size = 2.25
width, height = 400, 200  
screen = pg.display.set_mode((width*size, height*size))   
font = pg.font.Font(None, 36)
field_size = 64
rotation = 0
scroll_displacement = 0



current_sprite_string = "assets/map_builder_sprites/la_toilette.png"
library_folder = Path("assets/map_builder_sprites/")

visual_grid = [[0]*int(size*width//field_size) for _ in range(int(size*height//field_size))]
image_grid = [[0]*int(size*width//field_size) for _ in range(int(size*height//field_size))]



in_menu = False
draw_grid = True
place_delete = True
preview = False
ignore_next_click = False


crosshair = pg.image.load(f"assets/goofy_crosshair.png")
crosshair = pg.transform.scale_by(crosshair, 2)
del_crosshair = pg.image.load(f"assets/deletion_crosshair.png")
place_crosshair = pg.image.load(f"assets/placing_crosshair.png")
place_crosshair = pg.transform.scale_by(place_crosshair, 0.5)

current_sprite = pg.image.load(f"assets/map_builder_sprites/la_toilette.png")
current_sprite = pg.transform.scale_by(current_sprite, 2)
old_current_sprite = pg.image.load(f"assets/map_builder_sprites/la_toilette.png")
current_sprite_preview = pg.image.load(f"assets/map_builder_sprites/la_toilette.png")


clock = pg.time.Clock()   
counter = 0





while game_loop:   



    clock.tick()    
    mouse_pos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()  
    events = pg.event.get()

    if current_sprite != old_current_sprite:

        current_sprite_string = image_color_shifter(current_sprite_string, "blue")
        current_sprite_preview = pg.image.load(current_sprite_string)
        current_sprite_preview = pg.transform.scale_by(current_sprite_preview, 1.5)
        current_sprite_preview = pg.transform.rotate(current_sprite_preview, rotation)
        


    for event in events:
        if event.type == pg.QUIT or keys[pg.K_ESCAPE] or keys[pg.K_q]:

            game_loop = False    

    if in_menu:
        screen.fill((100, 100, 100))
        in_menu_func(events)
    
    else:
        screen.fill((150, 150, 150))
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
                


        if event.type == pg.MOUSEBUTTONDOWN and in_menu == False:

            if event.button == 2:

                place_delete = not place_delete
                print("mode should've switched")

            if event.button == 1 and place_delete:
                if ignore_next_click:

                    ignore_next_click = False
                    continue

                x = mouse_pos[0] // field_size
                y = mouse_pos[1] // field_size
                
                if visual_grid[y][x] == 0:
                    visual_grid[y][x] = (current_sprite, rotation)
                    print(f"changed field:{y},{x}")

            if event.button == 1 and place_delete == False:

                x = mouse_pos[0] // field_size
                y = mouse_pos[1] // field_size
                
                if visual_grid[y][x] != 0:
                    visual_grid[y][x] = 0
                    print(f"changed field:{y},{x}")



    if in_menu == False:
        for row in range(len(visual_grid)):
            for col in range(len(visual_grid[row])):
                coords = (col * field_size, row * field_size)
                
                x = coords[0]
                y = coords[1]

                if draw_grid:
                    pg.draw.rect(screen, (255, 255, 255), (x, y, field_size, field_size), 1)
                
                if isinstance(visual_grid[row][col], tuple):
                    iteration_image = pg.transform.rotate(visual_grid[row][col][0], visual_grid[row][col][1])
                    screen.blit(iteration_image, (x, y))

                if preview and place_delete:
                    screen.blit(current_sprite_preview, (round(mouse_pos[0] // field_size) * field_size + 8, round(mouse_pos[1] // field_size) * field_size + 8))



        if place_delete:
            screen.blit(place_crosshair, (mouse_pos[0]-8, mouse_pos[1]-8))

        if place_delete == False:
            screen.blit(del_crosshair, (mouse_pos[0]-8, mouse_pos[1]-8))


    # pg.draw.circle(screen, (255, 255, 255), mouse_pos, 1)

    pg.display.update()

pg.quit()