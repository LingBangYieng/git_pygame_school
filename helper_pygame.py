import pygame as pg
import numpy as np
from PIL import Image
from class_vectorz import Vectorz
from globals import *


# def random_pos_gen(old_random):

#     while True:
#         random_start = r.choice(r.choice(sqaure_matrix))
#         random_end = r.choice(r.choice(sqaure_matrix))

#         if (random_start != random_end and (random_start, random_end) != old_random and random_start not in obstacle_set and random_end not in obstacle_set):
#             print(random_start, random_end)
#             return random_start, random_end


def world_to_screen_coords(world_coords_object, view_field_xy_position):
    
    screen_coords = (world_coords_object[0] - view_field_xy_position.topleft[0], world_coords_object[1] - view_field_xy_position.topleft[1])
    return screen_coords



def spritesheet_cutter_2d(frame_width: int, frame_height: int, num_frames: int, sprite_sheet: pg.Surface) -> list:
    """
    Cuts a 2D spritesheet into individual frames.

    Args:
        frame_width (int): Width of each frame.
        frame_height (int): Height of each frame.
        sprite_sheet (pg.Surface): The full spritesheet image.

    Returns:
        list: List of pg.Surface objects, each representing a frame.
    """
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    cols = sheet_width // frame_width
    rows = sheet_height // frame_height

    counter = 0
    for row in range(rows):
        for col in range(cols):
            counter+=1
            if counter > num_frames:
                break
            frame = pg.Surface((frame_width, frame_height), pg.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), 
                       (col * frame_width, row * frame_height, frame_width, frame_height))
            frames.append(frame)
    return frames


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



def image_color_shifter(path_to_image: str, color_shift: str, name: str, strength: int = 0.25) -> str:       # adds a color shift (white'll look greenish or other color'ish) to an image

    possible_color_shifts = {               # dict that stores color tuples (rgb) keys are strings that are given in arguments
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



"""
implement usage iof Vectorz!!!!!
"""

class Bullet:

    def __init__(self, bullet_speed: float, static_bullet_sprite: pg.surface, bullet_position: tuple, alpha: float = 0, lifetime: float = 200):
        
        self.speed = bullet_speed
        self.sprite = static_bullet_sprite
        self.position = bullet_position
        self.alpha = alpha
        self.alpha_radians = alpha * np.pi / 180
        self.lifetime = lifetime


        self.pierce = None
        # [self.move() for _ in range(5)]


    def move(self):
        
        velocity_vector = np.cos(self.alpha_radians) * self.speed, -np.sin(self.alpha_radians) * self.speed
        self.position = (self.position[0] + velocity_vector[0], self.position[1] + velocity_vector[1])
        self.lifetime -= 1

    def draw(self, screen: pg.display, view_field_xy_position):

        bullet_image_rotated = pg.transform.rotate(self.sprite, self.alpha - 90)
        # bullet_rect = bullet_image_rotated.get_rect(center = (self.position[0] + 16, self.position[1] + 16))  # 16 --> bullet sprite size # 
        self.move()
        screen.blit(bullet_image_rotated, world_to_screen_coords(self.position, view_field_xy_position))
     



def check_boundaries(row: int, col: int, array: list[list]):
    if row < len(array) and col < len(array[0]) and row >= 0 and col >= 0:
        return True
    return False



def cast_ray(start_position:tuple, end_position:tuple, length:int, exactness: int, field_size: int, array: list[list]):


    start = start_position
    x0 = start[0]
    y0 = start[1]

    end = end_position
    x1 = end[0]
    y1 = end[1]

    vertical_points = []
    horizontal_points = []

    exactness = exactness
    length = length
    length2= length * length

    m = 1000
    if abs(x0 - x1) > 0.001:
        m = (y0 - y1) / (x0 - x1)

    #direction_check
    if x1 > x0: plus_x = 1
    else: plus_x = -1
    if y1 > y0: plus_y = 1
    else: plus_y = -1

    #get first chunk edge
    c_x = (x0//field_size) + (x1 > x0)
    c_y = (y0//field_size) + (y1 > y0)

    for i in range(length//field_size+1):  

        #get second chunk edge, direction applied
        edge_x = (c_x + plus_x * i) * field_size
        edge_y = (c_y + plus_y * i) * field_size

        #get distance from start to direfctional chunk line
        dx = edge_x - x0 
        dy = edge_y - y0

        #get missing side vertical
        c_distance_y = y0 + m * dx
        #get missing side horizontal
        if abs(m) > 1e-6: c_distance_x = x0 + dy / m
        else: c_distance_x = x0 + dy * 1000

        # pg.draw.circle(screen, "yellow", (edge_x, c_distance_y), 5)
        vertical_points.append((edge_x, c_distance_y,"v"))

        # pg.draw.circle(screen, "yellow", (c_distance_x, edge_y), 5)
        horizontal_points.append((c_distance_x, edge_y,"h"))

        points = vertical_points + horizontal_points

    
    
    res = []
    for x,y,type in points:
        #get checkpoint
        if type == "h":
            y_p = y + field_size/exactness
            y_n = y - field_size/exactness
            res.append((x,y_p))
            res.append((x,y_n))
        else:
            x_p = x + field_size/exactness
            x_n = x - field_size/exactness
            res.append((x_p, y))
            res.append((x_n, y))
    points = res

    res = []
    for x,y in points:
        dist = (x-x0)**2+(y-y0)**2
        if dist <= length2:
            res.append((x,y,dist))
    points = res

    points = sorted(points, key=lambda p: p[2])
    
    for x, y, distance in points:
        row, col = int(y/field_size), int(x/field_size)
        if check_boundaries(row, col, array):
            if array[row][col] != 0:
                return ((row, col), (x, y), distance)
    return None



class Animationz:

    def __init__(self, pathToSpriteSheet:str = "assets/walk_anim.png", frameSizeSpriteOnSpriteSheet:tuple = (32, 32), numFrames: int = 12, imageScale: float = 1, animationSpeed: float = 0.2):

        self.scale = imageScale
        self.animationSpeed = animationSpeed
        self.frameIndex = 0.0
        self.alive = True

        self.imageRaw = pg.image.load(pathToSpriteSheet)
        self.imageList = spritesheet_cutter_2d(frameSizeSpriteOnSpriteSheet[0], frameSizeSpriteOnSpriteSheet[1], numFrames, self.imageRaw)

        for i, image in enumerate(self.imageList):
            if self.scale != 1:
                image = pg.transform.scale_by(image, self.scale)
            self.imageList[i] = image


    def play_looped(self, position:tuple = (0, 0), rotation: float = 0):

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(self.imageList):
            self.frameIndex = 0

        frame = self.imageList[int(self.frameIndex)]

        frame = pg.transform.rotate(frame, rotation - 90)
        frame_rect = frame.get_rect(center = position) 
        frame_rect.center = world_to_screen_coords(position, vwp)
        # print(self.frameIndex)
        screen.blit(frame, frame_rect.topleft)
    
    def play(self, position:tuple = (0, 0), rotation: float = 0):
        if self.alive:
            self.frameIndex += self.animationSpeed

            if self.frameIndex >= len(self.imageList):
                self.alive = False
                return

            frame = self.imageList[int(self.frameIndex)]

            frame = pg.transform.rotate(frame, rotation - 90)
            frame_rect = frame.get_rect(center = position) 
            frame_rect.center = world_to_screen_coords(position, vwp)
            # print(self.frameIndex)
            screen.blit(frame, frame_rect.topleft)