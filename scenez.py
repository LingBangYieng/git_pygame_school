from class_collide_rect import HitBox
import pygame as pg


pg.font.init()

class Widgetz:

    def __init__(self, position = (0, 0), size = (100, 100), widget=None):

        self.x = position[0]
        self.y = position[1]
        self.w = size[0]
        self.h = size[1]
        self.padding: tuple
        self.parent = None
        self.widget = widget

        if widget is not None:
            widget.parent = self
            self.widget = widget

            if isinstance(widget, Widgetz):
                widget.x += self.x
                widget.y += self.y
                widget.update()

            if isinstance(widget, WidgetHandlerz):
                for wid in widget.widgets:
                    wid.x += self.x
                    wid.y += self.y
                    wid.update()

    def draw(self, screen):
        if self.widget is not None:
            self.widget.draw(screen)
        pass

class WidgetHandlerz:

    def __init__(self, widgets: list[Widgetz] = None, anchor="center"):

        self.padding: tuple
        self.parent = None
        self.widgets = widgets
        self.anchor = anchor

        for widget in self.widgets:
            widget.parent = self #ambigious


    def update(self):
        for widget in self.widgets:
            if self.anchor == "center" or "c":
                
                widget.x += self.parent.w/2 - widget.w/2
                widget.y += self.parent.h/2 - widget.h/2
                widget.update()


    def draw(self, screen):
        if self.widgets is not None:
            for widget in self.widgets:
                widget.draw(screen)
    

class Columnz(WidgetHandlerz):
    
    def __init__(self, widgets = None, anchor="center"):
        super().__init__(widgets, anchor)

class Textz(Widgetz):
    
    def __init__(self, position = (0, 0),        text: str = "", text_color: tuple = (0, 0, 0), text_size: int = 20, three_d: bool = False):
        

        self.font = pg.font.Font("assets/born2bsporty-fs.regular.otf", text_size)

        self.text_size = text_size
        self.text = text
        self.text_color = text_color
        self.text_object = self.font.render(self.text, True, self.text_color)

        super().__init__(position = position, size=self.text_object.get_size())

        self.three_d = three_d

    def update(self):
        adfgsroiuh sdfagoiuhsdfgoiuhjbdfgilojuh
        
    def draw(self, screen):

        if self.three_d:
            text0: pg.font.Font = self.font.render(self.text, True, self.text_color)
            text1: pg.font.Font = self.font.render(self.text, True, (self.text_color[0]+30, self.text_color[1]+30, self.text_color[2]+30))
            text2: pg.font.Font = self.font.render(self.text, True, (self.text_color[0]+60, self.text_color[1]+60, self.text_color[2]+60))
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

    def __init__(self, position=(0, 0),  pathToImage:str = "assets/goofy_katana.png", scale:float = None, rotation: float = None, has_hitbox: bool = False):

   
        self.pathToImage = pathToImage
        self.temp_img = pg.image.load(self.pathToImage)
        super().__init__(position=position, size=self.temp_img.get_size())
        self.scale = scale
        self.rotation = rotation
        if has_hitbox:
            self.update()

    def update(self):
        self.hitbox = HitBox(self.x, self.y, self.w, self.h)
    
    def draw(self, screen):
        
        if self.scale:
            self.temp_img = pg.transform.scale_by(self.temp_img, self.scale)
        if self.rotation:
            self.temp_img = pg.transform.scale_by(self.temp_img, self.scale)
        screen.blit(self.temp_img,(self.x, self.y))


class Containerz(Widgetz):

    def __init__(self, position: tuple, size: tuple,      shadow: bool=True, round_corner_value : int = 10, button_color: tuple = (120, 120, 120), handler = None):

        super().__init__(position=position, size=size , widget=handler)

        self.handler = handler
        self.shadow = shadow

        self.corner_int = round_corner_value
        self.button_color = button_color

        
        if handler is not None:
            handler.update()
        self.update()

    def update(self):
        if self.shadow:
            self.x_s = self.x - 5
            self.y_s = self.y + 5
            self.w_s = self.w
            self.h_s = self.h
        
    

    def draw(self, screen):
        if self.shadow:
            pg.draw.rect(screen, self.button_color, (self.x_s, self.y_s, self.w_s, self.h_s), border_radius=self.corner_int)

        pg.draw.rect(screen, (self.button_color[0] + 60, self.button_color[1] + 60, self.button_color[2] + 60), (self.x, self.y, self.w, self.h), border_radius=self.corner_int)
        pg.draw.rect(screen, (self.button_color[0] + 30, self.button_color[1] + 30, self.button_color[2] + 30), (self.x, self.y, self.w, self.h), 3, self.corner_int)
        if self.handler is not None:
            # for wid in self.widget:
            self.handler.draw(screen)


class Buttonz(Containerz):
    def __init__(self, position, size, shadow, round_corner_value = 10, button_color = (120, 120, 120), widget=None):
        super().__init__(position, size, shadow, round_corner_value, button_color, widget)
        super().update()
        
        
    def update(self):
        super().update()
        self.hitbox = HitBox(self.x, self.y, self.w, self.h) #need to update all things that aree parent dependants also with superupdate




class Scenez:

    # button_list = []
    # text_list = []

    def __init__(self, screen: pg.surface, widgets = list[Widgetz]):
        self.screen = screen
        self.widgets = widgets

    def draw(self):
        for wid in self.widgets:
            wid.draw(self.screen)












    # def draw_scene(self):

    #     for button in Scenez.button_list:
    #         button.draw()
        
    #     for text, x, y in Scenez.text_list:
    #         self.screen.blit(text, (x, y))


    # def add_button(self, button: Buttonz):
    #     Scenez.button_list.append(button)
    
    # def add_text(self, text: str, text_color: tuple, text_x: int, text_y: int, text_size: int, three_d: bool = False):
    #     font = pg.font.Font("assets/born2bsporty-fs.regular.otf", text_size)
    #     if three_d:
    #         text0: pg.font.Font = font.render(text, True, text_color)
    #         text1: pg.font.Font = font.render(text, True, (text_color[0]+30, text_color[1]+30, text_color[2]+30))
    #         text2: pg.font.Font = font.render(text, True, (text_color[0]+60, text_color[1]+60, text_color[2]+60))
    #         if text_size > 50:
    #             Scenez.text_list.append((text0, text_x - text0.get_width()//2, text_y - text0.get_height()//2))
    #             Scenez.text_list.append((text1, text_x - text1.get_width()//2 + 2.5, text_y - text1.get_height()//2 - 2.5))
    #             Scenez.text_list.append((text2, text_x - text2.get_width()//2 + 5, text_y - text2.get_height()//2 - 5))
    #         else:
    #             Scenez.text_list.append((text0, text_x - text0.get_width()//2, text_y - text0.get_height()//2))
    #             Scenez.text_list.append((text1, text_x - text1.get_width()//2 + 1.25, text_y - text1.get_height()//2 - 1.25))
    #             Scenez.text_list.append((text2, text_x - text2.get_width()//2 + 2.5, text_y - text2.get_height()//2 - 2.5))
    #     else:
    #         text: pg.font.Font = font.render(text, True, text_color)
    #         Scenez.text_list.append((text, text_x - text.get_width()//2, text_y - text.get_height()//2))



