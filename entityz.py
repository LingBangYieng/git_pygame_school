from class_collide_rect import HitBox
import pygame as pg
import numpy as np
from helper_pygame import world_to_screen_coords

from globals import *

def get_topleft(image: pg.Surface, position: tuple):
    return image.get_rect(center=position).topleft


class Entityz:

    def __init__(self, position:tuple = (0, 0), hitbox: HitBox = None, path_to_image: str = "assets/middled_player", image_scale: float = 1, image_rotation: float = 0):
        '''position should be center position of the object'''
        #genral
        self.alive = True

        #geometry
        self.position = position

        #draw
        self.original_image = self.adjustImage(pg.image.load(path_to_image), image_scale, image_rotation)
        self.image = self.original_image
        

        #physics
        if hitbox:
            self.hitbox = HitBox((self.top_left_position, hitbox.get_size()))
        else:
            #do this when hitbox is none, so its genertated
            self.hitbox = HitBox((self.top_left_position, self.image.get_size()))

    @property
    def top_left_position(self):
        return get_topleft(self.image, self.position)

    def adjustImage(self, image, scale, rotation):
        if scale != 1:
            image = pg.transform.scale_by(image, scale)
        if rotation != 0:
            image = pg.transform.rotate(image, rotation)
        return image
    
    def die(self):
        self.alive = False

    def update_HB(self):
        x, y = self.position
        x -= self.hitbox.get_size()[0]/2
        y -= self.hitbox.get_size()[1]/2
        pos = (x,y)
        self.hitbox = HitBox((pos, self.hitbox.get_size()))



class Bulletz(Entityz):

    def __init__(self, 
                 position = (0, 0), 
                 hitbox: HitBox=None, 
                 path_to_image = "assets/middled_player", 
                 image_scale: float = 1, 
                 bullet_speed: float = 25, 
                 lifetime: float = 200, 
                 remote_control: bool = False,
                 isDiag = False,
                 turnability:float = 3):
        '''lifetime is in frames'''
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image, image_scale=image_scale)

        self.speed = bullet_speed
        self.remote_control = remote_control
        self.lifetime = lifetime

        self.diag = 45 if isDiag else 0

        self.velo = (0.01,0.01)

        self.calc_alpha()
        self.turnability = turnability

        if remote_control:
            self.remote_calc_alpha()
        else:
            self.calc_alpha()

    def calc_alpha(self):
        if self.alive:
            middle_screen_x, middle_screen_y = world_to_screen_coords(self.position, vwp)

            dx = pg.mouse.get_pos()[0] - middle_screen_x
            dy = pg.mouse.get_pos()[1] - middle_screen_y

            self.alpha_radians = np.arctan2(-dy, dx)

            self.alpha = np.degrees(self.alpha_radians)


    def remote_calc_alpha(self):
        if not self.alive:
            return

        middle_screen_x, middle_screen_y = world_to_screen_coords(self.position, vwp)

        dx = pg.mouse.get_pos()[0] - middle_screen_x
        dy = pg.mouse.get_pos()[1] - middle_screen_y
        target_alpha = np.degrees(np.arctan2(-dy, dx))

        diff = (target_alpha - self.alpha + 180) % 360 - 180

        if abs(diff) > self.turnability:

            self.alpha += self.turnability * np.sign(diff)
        else:
            self.alpha = target_alpha

        self.alpha %= 360

        self.alpha_radians = np.radians(self.alpha)


    def move(self):
        if self.remote_control:
            self.remote_calc_alpha()
        velocity_vector = np.cos(self.alpha_radians) * self.speed, -np.sin(self.alpha_radians) * self.speed
        self.position = (self.position[0] + velocity_vector[0], self.position[1] + velocity_vector[1])
        self.update_HB()
        self.lifetime -= 1

        if self.lifetime < 0:
            self.die()


    def nmove(self):
        if self.remote_control:
            self.calc_alpha()

        mx, my = pg.mouse.get_pos()
        px, py = world_to_screen_coords(self.position, vwp)
        fac = 1/((mx-px)**2+(my-py)**2)
        force = (mx-px)*fac, (my-py)*fac

        self.velo = (
            self.velo[0] + force[0] * self.lightweight,
            self.velo[1] + force[1] * self.lightweight
        )

        # Cap speed
        speed = np.linalg.norm(self.velo)

        if speed > self.speed:
            self.velo = (
                self.velo[0] / speed * self.speed,
                self.velo[1] / speed * self.speed
            )

        self.position = (
            self.position[0] + self.velo[0],
            self.position[1] + self.velo[1]
        )

        self.update_HB()
        self.lifetime -= 1

        if self.lifetime < 0:
            self.die()



    def draw(self):
        if self.alive:
            self.move()
            self.image = pg.transform.rotate(self.original_image, self.alpha - 90 + self.diag) #why here
            screen.blit(self.image, world_to_screen_coords(self.top_left_position, vwp))

            # rect = self.image.get_rect(topleft = self.top_left_position)
            # rect.topleft = world_to_screen_coords(rect.topleft, vwp)
            # pg.draw.rect(screen, "white", rect , 3)


class Itemz(Entityz):

    def __init__(self, position = (0, 0), hitbox = None, path_to_image = "assets/middled_player", image_scale = 1, image_rotation = 0):
        super().__init__(position, hitbox, path_to_image, image_scale, image_rotation)