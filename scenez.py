from class_collide_rect import HitBox
import pygame as pg
from globals import *

pg.font.init()

class Widgetz:

    def __init__(self, position=(0, 0), size=(0, 0), widgets=None, anchor:str = "topleft"):

        self.anchor = anchor
        self.local_x = position[0]
        self.local_y = position[1]

        self.x = self.local_x
        self.y = self.local_y

        self.w = size[0]
        self.h = size[1]

        self.parent = None
        self.widgets = widgets or []

        for widget in self.widgets:
            widget.parent = self

        self.update()

    def draw(self):
        if self.widgets is not None:
            for widget in self.widgets:
                widget.draw()

    def update(self):

        if self.parent:
            match self.anchor:
                case "topleft":
                    pass

                case "center":
                    self.local_x = self.parent.w/2 - self.w/2
                    self.local_y = self.parent.h/2 - self.h/2

            self.x = self.parent.x + self.local_x
            self.y = self.parent.y + self.local_y                  
        else:
            self.x = self.local_x
            self.y = self.local_y

        for widget in self.widgets:
            widget.update()


class Textz(Widgetz):
    
    def __init__(self, position = (0, 0),        text: str = "", text_color: tuple = (0, 0, 0), text_size: int = 20, three_d: bool = False, anchor: str = "center"):
        

        self.font = pg.font.Font("assets/born2bsporty-fs.regular.otf", text_size)

        self.text_size = text_size
        self.text = text
        self.text_color = text_color
        self.text_object = self.font.render(self.text, True, self.text_color)

        super().__init__(position = position, size=self.text_object.get_size(), anchor=anchor)
        
        self.three_d = three_d

        
    def draw(self):

        if self.three_d:
            text0: pg.font.Font = self.font.render(self.text, True, self.text_color)
            text1: pg.font.Font = self.font.render(self.text, True, tuple(min(e+30, 255) for e in self.text_color))
            text2: pg.font.Font = self.font.render(self.text, True, tuple(min(e+60, 255) for e in self.text_color))
            if self.text_size > 50:
                screen.blit(text0, (self.x, self.y))
                screen.blit(text1, (self.x + 2.5, self.y - 2.5))
                screen.blit(text2, (self.x + 5, self.y - 5))
            else:
                screen.blit(text0, (self.x, self.y))
                screen.blit(text1, (self.x + 1.25, self.y - 1.25))
                screen.blit(text2, (self.x + 2.5, self.y - 2.5))
        else:
            screen.blit(self.text_object, (self.x , self.y))
        
class Imagez(Widgetz):

    def __init__(self, position=(0, 0),  pathToImage:str = "assets/goofy_katana.png", scale:float = None, rotation: float = None, anchor:str = "center"):

   
        self.pathToImage = pathToImage
        self.image = pg.image.load(self.pathToImage)

        self.scale = scale
        self.rotation = rotation

        if self.scale:
            self.image = pg.transform.scale_by(self.image, self.scale)
        if self.rotation:
            self.image = pg.transform.rotate(self.image, self.rotation)

        super().__init__(position=position, size=self.image.get_size(), anchor=anchor)

    def draw(self):
        screen.blit(self.image,(self.x, self.y))


class Containerz(Widgetz):

    def __init__(self, position: tuple, size: tuple,      shadow: bool=True, round_corner_value : int = 10, button_color: tuple = (100, 50, 30), widgets = None, visible: bool = True, anchor:str = "topleft"):

        super().__init__(position=position, size=size , widgets=widgets, anchor=anchor)
        
        self.shadow = shadow

        self.corner_int = round_corner_value
        self.button_color = button_color

        self.visible = visible



    def draw(self):
        if self.visible:
            if self.shadow:
                pg.draw.rect(screen, self.button_color, (self.x - 5, self.y + 5, self.w, self.h), border_radius=self.corner_int)

            pg.draw.rect(screen, tuple(min(e+60, 255) for e in self.button_color), (self.x, self.y, self.w, self.h), border_radius=self.corner_int)
            pg.draw.rect(screen, tuple(min(e+30, 255) for e in self.button_color), (self.x, self.y, self.w, self.h), 3, self.corner_int)

        super().draw()

        


class Buttonz(Containerz):

    def __init__(self, position: tuple = (0, 0), size: tuple = (50, 50), shadow = True, round_corner_value = 10, button_color = (100, 50, 30), widget=None, visible = True, anchor:str = "topleft"):
        super().__init__(position=position, size=size, shadow=shadow, round_corner_value=round_corner_value, button_color=button_color, widgets=[widget], visible=visible, anchor=anchor)
        
    @property
    def hitbox(self):
        return HitBox(self.x, self.y, self.w, self.h) #need to update all things that aree parent dependants also with superupdate




# class Listz(Widgetz):
#     def __init__(self, position=(0, 0), size=(0, 0), widgets=None, anchor = "center", direction: str = "vertical", orientation: str = "center", fill_type: str = "full"):
#         self.direction = direction
#         super().__init__(position=position, size=size, widgets=widgets, anchor=anchor)
        
    
#     def update(self):
#         if self.widgets is not None:
#             if self.direction == "vertical":
#                 self.widgets[0].local_x = self.w/2 
#                 self.widgets[0].local_y = self.widgets[0].h/2
#                 for i in range(1, len(self.widgets)):
#                     widget = self.widgets[i]
#                     widget.local_x = self.w/2 
#                     widget.local_y += self.widgets[i-1].h/2

#                     widget.update()






class Scenez:

    def __init__(self, widgets = list[Widgetz]):
        self.widgets = widgets

    def draw(self):
        for wid in self.widgets:
            wid.draw()