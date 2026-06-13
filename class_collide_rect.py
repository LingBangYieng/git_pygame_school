import pygame as pg
from helper_pygame import *
#from globals import screen, vwp

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

    def get_push_vector(self, other):
        if not self.check_collision(other):
            return (0, 0)

        dx1 = other.x + other.w - self.x
        dx2 = self.x + self.w - other.x

        dy1 = other.y + other.h - self.y
        dy2 = self.y + self.h - other.y

        overlap_x = dx1 if dx1 < dx2 else -dx2
        overlap_y = dy1 if dy1 < dy2 else -dy2

        if abs(overlap_x) < abs(overlap_y):
            return (overlap_x, 0)
        else:
            return (0, overlap_y)
        
    def show_HB(self, inMenu: bool =False, color: tuple = (0, 0, 255)):
        loc_vwp = vwp.copy()
        if inMenu:
            loc_vwp.topleft = (0,0)
        if self.exists:
            x,y = wtsc((self.x, self.y), loc_vwp)
            pg.draw.rect(screen, color, (x,y, self.w, self.h), 3)

    def get_size(self):
        return (self.w, self.h)


