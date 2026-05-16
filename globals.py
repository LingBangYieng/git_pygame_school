import pygame as pg
from settings import *

screen = pg.display.set_mode((width*size, height*size))
view_field_xy_position = vwp = pg.Rect(0, 0, width*size, height*size)
