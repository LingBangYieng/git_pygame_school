# import pygame as pg
# from scenez import Buttonz
# from class_collide_rect import HitBox
# from scenez import Scenez


# pg.display.init()
# screen = pg.display.set_mode((1280, 720))
# clock = pg.time.Clock()
# running = True


# button1 = Buttonz((1280//2 - 100, 720//2 - 50), 200, 50, screen, True, "Start Game", (0, 0, 0), 30, 5, (100, 50, 30))
# button2 = Buttonz((1280//2 - 100, 720//2 + 17.5), 200, 50, screen, True, "Settings", (0, 0, 0), 30, 5, (100, 50, 30))
# button3 = Buttonz((1280//2 - 100, 720//2 + 85), 200, 50, screen, True, "Quit", (0, 0, 0), 30, 5, (100, 50, 30))
                  
# inventory = Buttonz((900, 100), 300, 400, screen, True, "", (0, 0, 0), 30, 5, (100, 50, 30))
# slot0 = Buttonz((910, 440), 50, 50, screen, True, "O", (0, 0, 0), 30, 5, (130, 80, 60))

# title = "Redundant"
# version = "alpha v0.1"
# featured = "Abdul, Agmar, Kreatin"

# lobby = Scenez(screen)


# lobby.add_button(button1)
# lobby.add_button(button2)
# lobby.add_button(button3)

# lobby.add_button(inventory)
# lobby.add_button(slot0)

# lobby.add_text(title, (100, 50, 30), 1280//2 , 100, 80, True)
# lobby.add_text(version, (100, 50, 30),  1230, 700, 20, True)
# lobby.add_text(featured, (100, 50, 30),  90, 700, 20, True)



# mouse_HB = HitBox(0, 0, 1, 1)


# while running:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False

#     screen.fill("black")



#     mx, my = pg.mouse.get_pos()
#     mouse_HB.x = mx
#     mouse_HB.y = my

#     if slot0.hitbox.check_collision(mouse_HB):
#         print(f"\rTrue ", end="", flush=True)
#     else:
#         print(f"\rFalse", end="", flush=True)

#     lobby.draw_scene()


#     pg.display.flip()

#     clock.tick(60)

# pg.quit()


import pygame as pg
from scenez import *
from class_collide_rect import HitBox



pg.display.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True


# button1 = Buttonz((1280//2 - 100, 720//2 - 50), 200, 50, screen, True, "Start Game", (0, 0, 0), 30, 5, (100, 50, 30))
# button2 = Buttonz((1280//2 - 100, 720//2 + 17.5), 200, 50, screen, True, "Settings", (0, 0, 0), 30, 5, (100, 50, 30))
# button3 = Buttonz((1280//2 - 100, 720//2 + 85), 200, 50, screen, True, "Quit", (0, 0, 0), 30, 5, (100, 50, 30))
title = Textz(position=(0,0), text="jfyfdgxfdgxxd", text_color=(255, 255, 255), text_size=20, three_d=False)
slot0 = Buttonz((0, 0), (50, 50), True, 0, (100, 50, 30), widget=Columnz(widgets=[title]))      
image_in_inv = Imagez(position=(0, 0))      
inventory = Containerz(position=(900, 100), 
                       size=(300, 800), 
                       shadow=True, 
                       round_corner_value=0, 
                       button_color=(100, 50, 30), 
                       handler=Columnz(widgets=[
                           slot0, 
                        #    Buttonz((0, 200), (50, 50), True, 0, (0, 50, 30)),
                        #    Buttonz(position=(0,0), size=(30,30), round_corner_value=5, button_color=(195, 195,195), shadow=True), image_in_inv, title
                           ]))


# slot1 = Buttonz((0, 0), (50, 50), True, 5, (100, 50, 30))            
# inventory1 = Containerz((100, 100), (100, 400), True, 5, (100, 50, 30), widget=slot1)



# title = "Redundant"
# version = "alpha v0.1"
# featured = "Abdul, Agmar, Kreatin"

lobby = Scenez(screen, widgets=[inventory])


# # lobby.add_button(button1)
# # lobby.add_button(button2)
# # lobby.add_button(button3)

# lobby.add_button(inventory)
# lobby.add_button(slot0)

# lobby.add_text(title, (100, 50, 30), 1280//2 , 100, 80, True)
# lobby.add_text(version, (100, 50, 30),  1230, 700, 20, True)
# lobby.add_text(featured, (100, 50, 30),  90, 700, 20, True)



mouse_HB = HitBox(0, 0, 1, 1)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")



    mx, my = pg.mouse.get_pos()
    mouse_HB.x = mx
    mouse_HB.y = my

    if slot0.hitbox.check_collision(mouse_HB):
        print(f"\rTrue ", end="", flush=True)
    else:
        print(f"\rFalse", end="", flush=True)

    lobby.draw()


    pg.display.flip()

    clock.tick(60)

pg.quit()