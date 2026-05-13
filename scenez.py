from Buttons import Buttonz
from class_collide_rect import HitBox
import pygame as pg

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
            text1: pg.font.Font = font.render(text, True, (text_color[0]+30, text_color[1]+30, text_color[2]+30))
            text2: pg.font.Font = font.render(text, True, (text_color[0]+60, text_color[1]+60, text_color[2]+60))
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



