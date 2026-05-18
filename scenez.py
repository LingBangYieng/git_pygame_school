import pygame as pg
import numpy as np
from class_vectorz import *
from class_collide_rect import *
from globals import *

pg.font.init()


class Buttonz:

    def __init__(self, position: tuple, size: tuple, screen:pg.surface, shadow: bool, text: str = "", text_color: tuple = (0, 0, 0), text_size: int = 20, round_corner_value : int = 10, button_color: tuple = (120, 120, 120), command=None):


        font = pg.font.Font("assets/born2bsporty-fs.regular.otf", text_size)
        self.screen = screen

        self.x = position[0]
        self.y = position[1]
        self.w, self.h = size
        

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
        
        self.hitbox = HitBox(((self.x, self.y), (self.w, self.h)))

    def draw_button(self):
        if self.shadow:
            pg.draw.rect(self.screen, self.button_color, (self.x_s, self.y_s, self.w_s, self.h_s), border_radius=self.corner_int)

        
        loc_color = self.button_color
        if self.hitbox.check_collision(HitBox(MHB_rect[0])): 
            loc_color =  tuple(min(e+50, 255) for e in loc_color)
        pg.draw.rect(self.screen, tuple(min(e+60, 255) for e in loc_color), (self.x, self.y, self.w, self.h), border_radius=self.corner_int)
        pg.draw.rect(self.screen, tuple(min(e+30, 255) for e in self.button_color), (self.x, self.y, self.w, self.h), 3, self.corner_int)
        self.screen.blit(self.text_object, (self.x + self.w//2 - self.text_w//2 , self.y + self.h//2 - self.text_h//2 ))

        # (self.x + self.w//2 - self.text_w, self.y + self.h//2 - self.text_h)


class Scenez:

    button_list = []
    text_list = []

    def __init__(self, screen: pg.surface):
        self.screen = screen


    def draw_scene(self):

        for button in Scenez.button_list:
            button.draw_button()
        
        for text, x, y in Scenez.text_list:
            self.screen.blit(text, (x, y))

    def add_button(self, button: Buttonz):
        Scenez.button_list.append(button)
    
    def add_text(self, text: str, text_color: tuple, text_x: int, text_y: int, text_size: int, three_d: bool = False):
        font = pg.font.Font("assets/born2bsporty-fs.regular.otf", text_size)
        if three_d:
            text0: pg.font.Font = font.render(text, True, text_color)
            text1: pg.font.Font = font.render(text, True, tuple(min(e+30, 255) for e in text_color))
            text2: pg.font.Font = font.render(text, True, tuple(min(e+60, 255) for e in text_color))
            if text_size > 50:
                Scenez.text_list.append((text0, text_x - text0.get_width()//2, text_y - text0.get_height()//2))
                Scenez.text_list.append((text1, text_x - text1.get_width()//2 + 2.5, text_y - text1.get_height()//2 - 2.5))
                Scenez.text_list.append((text2, text_x - text2.get_width()//2 + 5, text_y - text2.get_height()//2 - 5))
            else:
                Scenez.text_list.append((text0, text_x - text0.get_width()//2, text_y - text0.get_height()//2))
                Scenez.text_list.append((text1, text_x - text1.get_width()//2 + 1.25, text_y - text1.get_height()//2 - 1.25))
                Scenez.text_list.append((text2, text_x - text2.get_width()//2 + 2.5, text_y - text2.get_height()//2 - 2.5))
        else:
            text: pg.font.Font = font.render(text, True, text_color)
            Scenez.text_list.append((text, text_x - text.get_width()//2, text_y - text.get_height()//2))



