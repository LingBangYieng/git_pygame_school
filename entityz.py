from class_collide_rect import HitBox
import pygame as pg
import numpy as np
from helper_pygame import world_to_screen_coords

class Entityz:

    def __init__(self, screen:pg.surface, view_field_xy_position:tuple, position:tuple = (0, 0), hitbox: HitBox = None, path_to_image: str = "assets/middled_player", image_scale: float = 1, image_rotation: float = 0):
        self.image = pg.image.load(path_to_image)

        
        self.alive = True
        self.screen = screen

    
        if image_scale != 1:
            self.image = pg.transform.scale_by(self.image, image_scale)
        if image_rotation != 0:
            self.image = pg.transform.rotate(self.image, image_rotation)

        pg.draw.circle(screen, "blue", world_to_screen_coords(position, view_field_xy_position), 5)
        self.position = self.image.get_rect(center=position).topleft
        pg.draw.circle(screen, "red", world_to_screen_coords(self.position, view_field_xy_position), 5)
        self.view = view_field_xy_position
        

        if hitbox:
            self.hitbox = HitBox((self.position, hitbox.get_size()))
        else:
            self.hitbox = HitBox((world_to_screen_coords(self.position, view_field_xy_position), self.image.get_size()))

        
    
    def die(self):
        self.alive = False

    def update_HB(self, view_field_xy_position):
        rect = self.image.get_rect(topleft=self.position)
        x, y = rect.center
        x -= self.hitbox.get_size()[0]/2
        y -= self.hitbox.get_size()[1]/2
        self.hitbox = HitBox((world_to_screen_coords((x,y), view_field_xy_position), self.hitbox.get_size()))



    

class Bulletz(Entityz):


    def __init__(self, screen:pg.surface, view_field_xy_position:tuple, position = (0, 0), hitbox: HitBox=None, path_to_image = "assets/middled_player", image_scale: float = 1, bullet_speed: float = 25, lifetime: float = 200, remote_control: bool = False):
        super().__init__(screen=screen, view_field_xy_position=view_field_xy_position, position=position, hitbox=hitbox, path_to_image=path_to_image, image_scale=image_scale)

        self.speed = bullet_speed
        self.remote_control = remote_control
        self.lifetime = lifetime

        


        self.calc_alpha()

    def calc_alpha(self):
        if self.alive:
            middle_screen_x, middle_screen_y = self.position

            mouse_pos = (pg.mouse.get_pos()[0] - middle_screen_x, pg.mouse.get_pos()[1] - middle_screen_y)
            self.alpha = 0
            if mouse_pos[1] < 0:
                self.alpha = (np.acos(mouse_pos[0]/ np.linalg.norm(np.array(mouse_pos)))) * 180 / np.pi
            else:
                self.alpha = -(np.acos(mouse_pos[0]/ np.linalg.norm(np.array(mouse_pos)))) * 180 / np.pi

            self.alpha_radians = self.alpha * np.pi / 180

        


    def move(self, view_field_xy_position):
        if self.remote_control:
            self.calc_alpha()
        velocity_vector = np.cos(self.alpha_radians) * self.speed, -np.sin(self.alpha_radians) * self.speed
        self.position = (self.position[0] + velocity_vector[0], self.position[1] + velocity_vector[1])
        self.update_HB(view_field_xy_position)
        self.lifetime -= 1

        if self.lifetime < 0:
            self.die()


    def draw(self, view_field_xy_position):
        if self.alive:
            self.move(view_field_xy_position)
            bullet_image_rotated = pg.transform.rotate(self.image, self.alpha - 90)
            self.screen.blit(bullet_image_rotated, world_to_screen_coords(self.position, view_field_xy_position))
