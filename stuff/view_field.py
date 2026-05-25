import pygame as pg
import numpy as np
import random as r


"""
(255, 255, 255)    white
(255, 0, 0)        red
(255, 255, 0)      yellow
(0, 255, 0)        green
(0, 255, 255)      cyan 
(0, 0, 255)        blue
(255, 0, 255)      purple
(0, 0, 0)          black
(46, 150, 172)     best
"""










pg.font.init()
pg.display.init()           #needed pygame inits

game_loop = True
size = 6   #3 or above is highly recommended, allows easy screen resizing for debugging
width, height = 400, 200            #width and height of screen which will be multiplied by size 
screen = pg.display.set_mode((width*size, height*size))         #create screen object on which everything will happen
background = pg.image.load(f"assets/big_background.jpg")        #load optional image for better visuality
font = pg.font.SysFont("arial", 20)             #create font object --> enables writing on screen       
font = pg.font.Font("assets/born2bsporty-fs.regular.otf", 20)  
speed = 1 * size                   #speed * size to scale with screen to not slow down / speed up
position_circle = pg.Vector2((width*size)/2, (height*size)/2)        #create vector object --> important for player movement, can be accessed as tuple --> first value of tuble is tuple[0] second is tuple [1]
radius = int(2.5 * size / 1.5)              #           #radius used for radius in circle and in width of lines and rectangle --> screen dependant, has to be int for pygame to get, increase if lines are too small
view_field_xy_position = pg.Rect(0, 0, width*size//3, height*size//3)       #create Rect object --> thing its all about, (// int division) by 3 to be able to see screen, in actual use it'd be the exact size of screen 
random_xy_width_height = r.randint(0, width*size//3), r.randint(0, height*size//3)  #create random point on screen to explain relation between screen and world coords will later be blue


def move(position_circle,speed):        #function init


    keys = pg.key.get_pressed()         #get the list .get_pressed() from pygame and name keys

    if keys[pg.K_LSHIFT]:       
        speed *= 1.5        #if shift is pressed speed = speed * 1.5 --> makes rectangle move faster than usual
    if keys[pg.K_w]:
        position_circle[1] = position_circle[1] - speed #if w pressed --> add a vector in direction of key press in w case --> North  (since pygame screen are topleft to right x increase and topleft to bottom y increase has to be negativ y to go north)
    if keys[pg.K_a]:
        position_circle[0] = position_circle[0] - speed #if a pressed --> goal is go left and achieved by adding vector facing opposite x --> calculate -x which is position_circle[0] <-- (is a tuple)
    if keys[pg.K_s]:
        position_circle[1] = position_circle[1] + speed #if s pressed --> opposite goal of w (south), add vector in direction of y --> positive
    if keys[pg.K_d]:    
        position_circle[0] = position_circle[0] + speed #if d pressed --> opposite goal of a (west), add vector facing in direction of x --> positive

    view_field_xy_position.topleft = (position_circle[0] - width*size//2//3, position_circle[1] - height*size//2//3)    #.topleft of rect object returns coords of topleft corner of rect, those coords are replaced with the newly calculated numbers     
                                                                                                                        #of position_cicle which are now the coordinates of the topleft of the rectangle 
    
    return position_circle, view_field_xy_position  #returns the values for later use

clock = pg.time.Clock()     #pygam clock init for fps cap


while game_loop:        #game_loop is always true while game should run
    clock.tick(60)      #set fps cap
    # pygame.QUIT event means the user clicked X to close your window
    keys = pg.key.get_pressed()  #get the list .get_pressed() from pygame and name keys

    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:      #press escape or x to exit programm
            game_loop = False                   #gameloop now false which means that after this final loop the programm will stop
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:                                                                     #press r to generate new circle (if pre-generated was unfortunate)
                random_xy_width_height = r.randint(0, width*size//3), r.randint(0, height*size//3)      #create random point on screen to explain relation between screen and world coords will later be blue


 

    screen.fill((0, 0, 0))              #if not here screen would bloat, because everything that moves leaves a trail


    screen.blit(background, view_field_xy_position.topleft, view_field_xy_position)        #enable if better visuality is needed

    move(position_circle, speed)            #allows player ionput for movement

    mouse_pos = pg.mouse.get_pos()          #get mouse_position

    position_random_circle = random_xy_width_height[0] + view_field_xy_position.topleft[0], random_xy_width_height[1] + view_field_xy_position.topleft[1]   #vector addition to calculate screen coords of blue circle , (red + pink) red(view_field) pink(random_xy)

    pg.draw.rect(screen, (255, 0, 0), view_field_xy_position, radius//2)                #draws rect on screen with color (255, 0, 0) at coords view_field_xy_position with width of  radius//2
    pg.draw.circle(screen, (255, 0, 0), view_field_xy_position.topleft, radius//1.5)        
    pg.draw.line(screen, (255, 0, 0), (0, 0), view_field_xy_position.topleft, radius//2)        

    pg.draw.circle(screen, (0, 255, 0), position_circle, radius//1.5)       #draws circle on screen with color (0, 255, 0) at coords position_circle with radius of  radius//2
    pg.draw.line(screen, (0, 255, 0), (0, 0), position_circle, radius//2)

    #green circle and line are drawn to show middle of screen and vector to middle of screen
    
    pg.draw.circle(screen, (0, 0, 255), mouse_pos, radius//1.5)
    pg.draw.line(screen, (0, 0, 255), (0, 0), mouse_pos, radius//2)    #draws line on screen with color (0, 0, 255) at starting coords 0,0 (origin) to ending coords of mouse_pos with width radius//2

    pg.draw.line(screen, (255, 0, 255), mouse_pos, view_field_xy_position.topleft, radius//2)

    #all pg.draw basically just draw what was calculated earlier

    view_field_xy_coords_of_circle = mouse_pos[0] - view_field_xy_position.topleft[0], mouse_pos[1] - view_field_xy_position.topleft[1]  #calculate vector pink = blue - red

    screen.blit(font.render(f"{view_field_xy_position.topleft}world coord", True, (255, 255, 255)), (view_field_xy_position.topleft))   #prints on screen red coords
    screen.blit(font.render(f"{tuple(round(position_circle))}world coord", True, (255, 255, 255)), (position_circle))  #prints on screen green coords
    screen.blit(font.render(f"{mouse_pos}world coord / {view_field_xy_coords_of_circle}screen coord", True, (255, 255, 255)), (mouse_pos)) #prints on screen blue, purple coords     


    pg.display.update()     #needed for pygame to update the screen correctly

pg.quit()