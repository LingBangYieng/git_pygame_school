import pygame as pg
import numpy as np
from class_vectorz import *
from class_collide_rect import *

pg.font.init()


class Buttonz:

    

    def __init__(self, position: tuple, size_x: int, size_y: int, screen:pg.surface, shadow: bool, text: str = "", text_color: tuple = (0, 0, 0), text_size: int = 20, round_corner_value : int = 10, button_color: tuple = (120, 120, 120)):


        font = pg.font.Font(None, text_size)
        self.screen = screen

        self.x = position[0]
        self.y = position[1]
        self.w = size_x
        self.h = size_y

        self.text = text
        self.text_color = text_color
        self.text_object = font.render(self.text, True, self.text_color)
        self.text_w = self.text_object.get_width()
        self.text_h = self.text_object.get_height()


        self.shadow = shadow

        self.corner_int = round_corner_value
        self.button_color = button_color

        if shadow:
            self.x_s = self.x - 5
            self.y_s = self.y + 5
            self.w_s = self.w 
            self.h_s = self.h 
        
        self.hitbox = HitBox(self.x, self.y, self.w, self.h)

    def draw_button(self):
        if self.shadow:
            pg.draw.rect(self.screen, self.button_color, (self.x_s, self.y_s, self.w_s, self.h_s), border_radius=self.corner_int)

        
        
        pg.draw.rect(self.screen, (self.button_color[0] + 60, self.button_color[1] + 60, self.button_color[2] + 60), (self.x, self.y, self.w, self.h), border_radius=self.corner_int)
        pg.draw.rect(self.screen, (self.button_color[0] + 30, self.button_color[1] + 30, self.button_color[2] + 30), (self.x, self.y, self.w, self.h), 3, self.corner_int)
        self.screen.blit(self.text_object, (self.x + self.w//2 - self.text_w//2 , self.y + self.h//2 - self.text_h//2 ))

        # (self.x + self.w//2 - self.text_w, self.y + self.h//2 - self.text_h)