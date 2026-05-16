import pygame as pg
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
    
    def show_HB(self, screen: pg.surface, color: tuple = (0, 0, 255)):
        if self.exists:
            pg.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 3)

    def get_size(self):
        return (self.w, self.h)
    