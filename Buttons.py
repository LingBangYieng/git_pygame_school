import pygame as pg
import numpy as np
from class_vectorz import *
from class_collide_rect import *

class Buttonz:

    def __init__(self, position: tuple, size_x: int, size_y: int, screen:pg.surface, shadow: bool):

        self.screen = screen

        self.x = position[0]
        self.y = position[1]
        self.w = size_x
        self.h = size_y
        self.shadow = shadow

        if shadow:
            self.x_s = self.x - 5
            self.y_s = self.y + 5
            self.w_s = self.w 
            self.h_s = self.h 
        
        self.hitbox = HitBox(self.x, self.y, self.w, self.h)

    def draw_button(self):
        if self.shadow:
            pg.draw.rect(self.screen, (120, 120, 120), (self.x_s, self.y_s, self.w_s, self.h_s))

        
        pg.draw.rect(self.screen, (180, 180, 180), (self.x, self.y, self.w, self.h))
        pg.draw.rect(self.screen, (230, 230, 230), (self.x, self.y, self.w, self.h), 3)

        