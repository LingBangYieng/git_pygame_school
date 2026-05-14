import pygame as pg
class HitBox:

    def __init__(self, rect = None):
        
        if isinstance(rect, pg.Rect):
            self.x, self.y, self.w, self.h = tuple(rect)
        else:
            self.x, self.y, self.w, self.h = rect

    def check_collision(self, other)->bool:

        if ((self.x < other.x + other.w) and (other.x < self.x + self.w) and (self.y < other.y + other.h) and (other.y < self.y + self.h)):
            return True
        else:
            return False
