import pygame as pg
import numpy as np
from PIL import Image
import random
from settingsClass import Settings
#from globals import *

pg.display.init()


def get_hitbox_size(pathToImage:str):
        originalImage = Image.open(pathToImage)
        imgArray = np.array(originalImage)
        alphaArray = imgArray[:, :, 3]

        RMax, RMin = 0, 100000

        for row in range(len(alphaArray)):
            rowValueList = []
            for col in range(len(alphaArray[row])):
                if alphaArray[row,col] > 0:
                    rowValueList.append(col)
            if rowValueList:
                RMax = max(RMax, max(rowValueList))
                RMin  = min(RMin , min(rowValueList))
        


        CMax, CMin = 0, 100000

        for col in range(len(alphaArray[0])):
            colValueList = []
            for row in range(len(alphaArray)):
                if alphaArray[row,col] > 0:
                    colValueList.append(row)
            if colValueList: 
                CMax = max(CMax, max(colValueList))
                CMin  = min(CMin , min(colValueList))

        w = max(RMax - RMin, CMax - CMin)
        return (w,w)
                    





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

# class Bullet:

#     def __init__(self, bullet_speed: float, static_bullet_sprite: pg.surface, bullet_position: tuple, alpha: float = 0, lifetime: float = 200):
        
#         self.speed = bullet_speed
#         self.sprite = static_bullet_sprite
#         self.position = bullet_position
#         self.alpha = alpha
#         self.alpha_radians = alpha * np.pi / 180
#         self.lifetime = lifetime


#         self.pierce = None
#         # [self.move() for _ in range(5)]


#     def move(self):
        
#         velocity_vector = np.cos(self.alpha_radians) * self.speed, -np.sin(self.alpha_radians) * self.speed
#         self.position = (self.position[0] + velocity_vector[0], self.position[1] + velocity_vector[1])
#         self.lifetime -= 1

#     def draw(self, screen: pg.display, view_field_xy_position):

#         bullet_image_rotated = pg.transform.rotate(self.sprite, self.alpha - 90)
#         # bullet_rect = bullet_image_rotated.get_rect(center = (self.position[0] + 16, self.position[1] + 16))  # 16 --> bullet sprite size # 
#         self.move()
#         screen.blit(bullet_image_rotated, wtsc(self.position, view_field_xy_position))
     



def check_boundaries(row: int, col: int, array: list[list]):
    if row < len(array) and col < len(array[0]) and row >= 0 and col >= 0:
        return True
    return False



def ocast_ray(start_position:tuple, end_position:tuple, length:int, exactness: int, field_size: int, array: list[list]):


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

        # pg.draw.circle(screen, "yellow", wtsc((edge_x, c_distance_y), vwp), 5)
        vertical_points.append((edge_x, c_distance_y,"v"))

        # pg.draw.circle(screen, "yellow", wtsc((c_distance_x, edge_y),vwp), 5)
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
    return (None,None,None)




def cast_ray(start, end, unused, unused2, field_size, array, draw=False):
    x0, y0 = start
    x1, y1 = end

    dx = x1 - x0
    dy = y1 - y0

    x = int(x0 // field_size)
    y = int(y0 // field_size)

    end_x = int(x1 // field_size)
    end_y = int(y1 // field_size)

    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1

    t_delta_x = abs(field_size / dx) if dx != 0 else float('inf')
    t_delta_y = abs(field_size / dy) if dy != 0 else float('inf')

    next_x_boundary = (x + (step_x > 0)) * field_size
    next_y_boundary = (y + (step_y > 0)) * field_size

    t_max_x = abs((next_x_boundary - x0) / dx) if dx != 0 else float('inf')
    t_max_y = abs((next_y_boundary - y0) / dy) if dy != 0 else float('inf')

    step_axis = None  # 0 = x-step, 1 = y-step

    while True:

        if draw:
            pg.draw.rect(
                screen,
                (40, 40, 40),
                (x * field_size, y * field_size, field_size, field_size),
                1
            )

        if 0 <= y < len(array) and 0 <= x < len(array[0]):
            if array[y][x] != 0:

                # ✔ FRONT-FACE HIT FIX
                if step_axis == 0:
                    t_hit = t_max_x - t_delta_x
                else:
                    t_hit = t_max_y - t_delta_y

                hit_x = x0 + dx * t_hit
                hit_y = y0 + dy * t_hit

                if draw:
                    pg.draw.circle(screen, (255, 0, 0), (int(hit_x), int(hit_y)), 6)

                return True, (hit_x, hit_y), None

        if x == end_x and y == end_y:
            break

        # step DDA
        if t_max_x < t_max_y:
            t_max_x += t_delta_x
            x += step_x
            step_axis = 0
        else:
            t_max_y += t_delta_y
            y += step_y
            step_axis = 1

    return False, None, None


class Animationz:

    def __init__(self, pathToSpriteSheet:str = "assets/walk_anim.png", frameSizeSpriteOnSpriteSheet:tuple = (32, 32), numFrames: int = 12, imageScale: float = 1, animationSpeed: float = 0.2, stain=False, randomRot = False):

        self.scale = imageScale
        self.animationSpeed = animationSpeed
        self.frameIndex = 0.0
        self.alive = True
        self.loop = False


        self.isActive = True

        self.pos = (0, 0)
        self.rot = 0


        self.imageRaw = pg.image.load(pathToSpriteSheet)
        self.imageList = spritesheet_cutter_2d(frameSizeSpriteOnSpriteSheet[0], frameSizeSpriteOnSpriteSheet[1], numFrames, self.imageRaw)

        for i, image in enumerate(self.imageList):
            if self.scale != 1:
                image = pg.transform.scale_by(image, self.scale)
            self.imageList[i] = image


        #randoms
        if randomRot:
            self.randomRotation = random.random()*360
        else:
            self.randomRotation = 0


        #Stain
        self.stain = stain
        self.lastIndex = random.randint(0, len(self.imageList) - 2)



        self.stringPath = pathToSpriteSheet

    def update(self):
        if self.alive:
            if self.isActive:
                self.frameIndex += self.animationSpeed



                if not self.stain:
                    self.lastIndex = len(self.imageList)


                if self.frameIndex >= self.lastIndex:
                    if self.loop:
                        self.frameIndex = 0
                    else:
                        self.alive = False
                    
                    if self.stain:
                        self.alive = True
                        self.frameIndex = self.lastIndex
                    

                self.draw()

    


    def addToQueue(self):
        # print(len(allAnimsList), allAnimsList)
        if self.alive and self not in state.allAnimsList:
            state.allAnimsList.append(self)
        # if self.alive:
        #     print("alive", end="")
        # if self not in allAnimsList:
        #     print("      in List",  end="")
        # print()


    def draw(self):
        if self.alive:
            if self.isActive:
                frame = self.imageList[int(self.frameIndex)]

                frame = pg.transform.rotate(frame, self.rot - 90)
                frame_rect = frame.get_rect(center = self.pos) 
                frame_rect.center = wtsc(self.pos, vwp)
                screen.blit(frame, frame_rect.topleft)


    def play_looped(self, position:tuple = (0, 0), rotation: float = 0):
        self.pos = position
        self.rot = rotation
        self.loop = True

        self.isActive = True
        self.addToQueue()
    

    def play(self, position:tuple = (0, 0), rotation: float = 0):
        self.pos = position
        self.rot = rotation + self.randomRotation
        self.addToQueue()

    def revive(self):
        self.alive = True
        self.frameIndex = 0


    # def __hash__(self):
    #     return  hash(f"{self.stringPath},{self.hashCounter}")
    # def __eq__(self, value):
    #     return hash(self) == hash(value)
    

    def __repr__(self):
        return self.stringPath
    
    


def blur_surface(surface, scale_factor=0.25):
    w, h = surface.get_size()
    
    # shrink
    small = pg.transform.smoothscale(
        surface,
        (int(w * scale_factor), int(h * scale_factor))
    )
    
    # scale back up
    blurred = pg.transform.smoothscale(small, (w, h))
    
    return blurred




def checkBases(LTheta, RTheta, sightDistance, grid=None, position=None, precision=512):
    if grid is None:
        grid = state.HB_layer
    if position is None:
        position = state.playerPos

    hits = []
    HB_layer = grid

    baseAngles = np.linspace(LTheta,RTheta,precision)

    _, LHit, _ = cast_ray(position, np.array([sightDistance*np.cos(LTheta), sightDistance*np.sin(LTheta)])+position, sightDistance, 100, field_size=32*3, array=HB_layer)
    if not LHit: LHit = (np.array([sightDistance*np.cos(LTheta), sightDistance*np.sin(LTheta)])+position)
    _, RHit, _ = cast_ray(position, np.array([sightDistance*np.cos(RTheta), sightDistance*np.sin(RTheta)])+position, sightDistance, 100, field_size=32*3, array=HB_layer)
    if not RHit: RHit = (np.array([sightDistance*np.cos(RTheta), sightDistance*np.sin(RTheta)])+position)


    # print(len(baseAngles))
    hits.append(position)
    hits.append(LHit)
    for phi in baseAngles:
        _,hit,_ = cast_ray(position, np.array([sightDistance*np.cos(phi), sightDistance*np.sin(phi)])+position, sightDistance, 100, field_size=32*3, array=HB_layer)
        if not hit: hit = (np.array([sightDistance*np.cos(phi), sightDistance*np.sin(phi)])+position)
        hits.append(hit)
        # if hit:
            
        #     pg.draw.circle(screen, "red", hit, 5)
    hits.append(RHit)

    return hits





    
#####Globals#####
pg.mixer.init()

s = Settings()

class state:



    MHB_rect = None
    events = pg.event.get()
    playerPos = None
    counter = 0

    HB_layer = None

    allAnimsList = []

    animDict = {"player_walk":Animationz(imageScale=2, numFrames=14, frameSizeSpriteOnSpriteSheet=(64, 64), pathToSpriteSheet="assets/player_walk_gun.png", animationSpeed=0.4),
                "rocket" : Animationz(pathToSpriteSheet="assets/rockety_anim.png", numFrames=4, imageScale=2, animationSpeed=0.3)}



    CorpseList = []
    entityScene = None

    mx,my = (0,0)

    game_loop = True

    soundChannel = pg.mixer.Channel(0)




print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

class vis:
    overlay = pg.Surface((s.WIDTH, s.HEIGHT), pg.SRCALPHA)






    
screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
vis.overlay = pg.Surface((s.WIDTH, s.HEIGHT), pg.SRCALPHA)
vwp = pg.Rect(0, 0, s.WIDTH, s.HEIGHT)

def updateScreens():
    global screen,vwp
    num = pg.FULLSCREEN if s.FULLSCREEN else 0
    screen = pg.display.set_mode((s.WIDTH, s.HEIGHT), num)
    vis.overlay = pg.Surface((s.WIDTH, s.HEIGHT), pg.SRCALPHA)
    print(vis.overlay.get_size())
    print(s.WIDTH, s.HEIGHT)
    vwp.size = (s.WIDTH, s.HEIGHT)

def wtsc(world_coords_object, view_field_xy_position=vwp):
    screen_coords = (world_coords_object[0] - view_field_xy_position.topleft[0], world_coords_object[1] - view_field_xy_position.topleft[1])
    return screen_coords

def screen_to_world_coords_rare_use(screen_coords_object, view_field_xy_position=vwp):
    return (screen_coords_object[0] + view_field_xy_position.topleft[0], screen_coords_object[1] + view_field_xy_position.topleft[1])
################









def LightCone(pos, alphaDegr, fovDegr, sightDist):
    alpha_rad, fov_rad_half = np.deg2rad(alphaDegr), np.deg2rad(fovDegr/2)
    hits = checkBases(alpha_rad+fov_rad_half, alpha_rad-fov_rad_half, sightDistance=sightDist, position=pos, precision=128)
    pg.draw.polygon(vis.overlay, (0, 0, 0, 50), [wtsc(e) for e in hits])
    pg.draw.circle(vis.overlay, (0, 0, 0, 150), wtsc(pos), 20)

























pg.font.init()
class DebugScreen:
    '''use by creating a DebugScreen Variable (D = DebugScreen()), 
        and at end of gameloop (before screen update) put D.draw()
        wherever u want to wish to meassure a value, use D.add() to do so'''
    textSize = 20
    max_width = 0
    debugFont = pg.font.Font(None, textSize)

    def __init__(self):
        self.mainDict = {}

    def draw(self, pos=(50,50)):
        # res = []

        
        line_height = self.textSize*1.1

        renders = []
        for DebugKey in self.mainDict:
            DebugItem = self.mainDict[DebugKey]
            DebugValue = DebugItem["value"]
            DebugUnit = DebugItem["unit"]
            DebugLine = f"{DebugKey} :   {DebugValue} {DebugUnit}"
        
  
            DebugLineRender = self.debugFont.render(DebugLine, True, (255, 255, 255))
            renders.append(DebugLineRender)
            w,h = DebugLineRender.get_size()
            self.max_width = max(self.max_width, w)

        DebugText = pg.Surface((self.max_width*1.1, line_height*1.25*len(renders)), pg.SRCALPHA)
        DebugText.fill((0,0,0,255))
        screen.blit(DebugText, (pos[0]-line_height*0.25, pos[1]-line_height*0.25))

        for i in range(len(renders)):
            render = renders[i]
            screen.blit(render, (pos[0], pos[1]+line_height*1.25*i))

    def add(self, key, value="unknown", unit="", dec=1, avg=1,   enable_adaptive_units=False):
        '''
        args:
        key [str]  :  name of the varible that shall be displayed, use only once per Obj (will overwrite)
        value [any]:  the value to be represented e.g. clock.get_fps()
        unit [str] :  possible place for unit support (m, cm, L, Newton, meter), will be printed after the value
        dec [uint] : decimal places
        avg [uint] : number of elements to calculate temporal average
        enable_adaptive_units [bool]  :  enables automatic unit conversion between m,km,nm,mm,ns etc

        '''
        if avg<1:
            avg=1
            print("Warning, set avg to one since less makes no sense")

        value = self.__adapt_value(value)

        if key not in self.mainDict:
            self.mainDict[key] = {}
            self.mainDict[key]["valueList"] = []
        
        self.mainDict[key]["valueList"].append(value)
        if len(self.mainDict[key]["valueList"]) > avg:
            self.mainDict[key]["valueList"].pop(0)
        
        adaptive_unit_string, adaptive_units_factor =  self.__genAdaptiveUnit(unit, value) if enable_adaptive_units else (unit, 1)
        
        if isinstance(value, str):
            self.mainDict[key]["value"] = value
        else:
            self.mainDict[key]["value"] = np.round(np.sum(np.array(self.mainDict[key]["valueList"]), axis=0)/len(self.mainDict[key]["valueList"])  /  adaptive_units_factor, dec)
        self.mainDict[key]["unit"] = adaptive_unit_string + unit


    def __genAdaptiveUnit(self, unit, value):
        if unit.strip() == "" or value=="unknown" or abs(value) < 1e-12 or not isinstance(value, (int, float)):
            return ("",1)
        
        powerList = ["p", "n", "u", "m", "", "k", "M", "G", "T", "P"]

        index = int(np.log10(abs(value))/3)+4
        self.add("ind", index)
        return (powerList[index], 10**((index-4)*3))


    def __adapt_value(self, value):
        if isinstance(value, (tuple, list)):
            return np.array(value)
        if isinstance(value, pg.Vector2):
            return np.array([value[0], value[1]])
        if isinstance(value, (int, float, str)):
            return value





D = DebugScreen()









