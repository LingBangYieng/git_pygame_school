import pygame as pg
import numpy as np
from class_vectorz import *

class Buttonz:

    def __init__(self, width:int, height:int, position:Vectorz, screen:pg.surface):
        
        self.w = width
        self.h = height
        self.position = position

        self.draw_button(screen)

    def draw_button(self, screen:pg.surface):
        pg.draw.rect(screen, "red", self.position.tuple,(self.w, self.h))