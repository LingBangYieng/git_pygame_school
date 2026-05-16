import pygame as pg
from helper_pygame import *
from globals import *

class HitBox:

    def __init__(self, rect = None, ):
        if rect is None:
            self.exists = False
        elif isinstance(rect, pg.Rect):
            self.x, self.y, self.w, self.h = tuple(rect)
            self.exists = True
        else:
            pos, size = rect
            self.x, self.y = pos
            self.w, self.h = size
            self.exists = True

    def check_collision(self, other)->bool:
        if self.exists and other.exists:
            if ((self.x < other.x + other.w) and (other.x < self.x + self.w) and (self.y < other.y + other.h) and (other.y < self.y + self.h)):
                return True
        return False
    
    def show_HB(self, inMenu: bool =False, color: tuple = (0, 0, 255)):
        loc_vwp = vwp.copy()
        if inMenu:
            loc_vwp.topleft = (0,0)
        if self.exists:
            x,y = world_to_screen_coords((self.x, self.y), loc_vwp)
            pg.draw.rect(screen, color, (x,y, self.w, self.h), 3)

    def get_size(self):
        return (self.w, self.h)
    