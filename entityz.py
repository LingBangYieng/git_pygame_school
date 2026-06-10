from class_collide_rect import HitBox
import pygame as pg
import numpy as np
from helper_pygame import *
#from globals import *
from pathfind_non_visual import a_star

def get_topleft(image: pg.Surface, position: tuple):
    return image.get_rect(center=position).topleft



class Entityz:

    def __init__(self, position:tuple = (0, 0), hitbox: HitBox = None, path_to_image: str = "assets/middled_player", image_scale: float = 1, image_rotation: float = 0, isAnimated = False, path_to_animation = ""):
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
            HB_w,HB_h = tuple(e*image_scale for e in (get_hitbox_size(path_to_image)))
            image_w, image_h = self.image.get_size()
            self.hitbox = HitBox(((self.top_left_position[0] + (image_w - HB_w)/2, self.top_left_position[1] + (image_h - HB_h)/2), (HB_w, HB_h)))


        self.deathEvent = None

        #Animation
        self.isAnimated= isAnimated
        if isAnimated:
            self.animation = Animationz(pathToSpriteSheet=path_to_animation, numFrames=4, imageScale=2, animationSpeed=0.3)

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
        if self.isAnimated:
            self.animation.alive = False 
        if self.deathEvent is not None:
            self.deathEvent()

    def update_HB(self):
        x, y = self.position
        x -= self.hitbox.get_size()[0]/2
        y -= self.hitbox.get_size()[1]/2
        pos = (x,y)
        self.hitbox = HitBox((pos, self.hitbox.get_size()))
    
    def update_HB_non_center(self):
        self.hitbox = HitBox((self.position, self.hitbox.get_size()))
    
    def draw(self):
        screen.blit(self.image, self.position)




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
                 turnability:float = 3,
                 explosive = False,
                 explosionRadius = 0,
                 isAnimated = False,
                 path_to_animation = "assets/rockety_anim.png"):
        '''lifetime is in frames'''
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image, image_scale=image_scale, isAnimated=isAnimated, path_to_animation=path_to_animation)

        self.speed = bullet_speed
        self.remote_control = remote_control
        self.lifetime = lifetime

        # state["entitySceneMain"].add_bullet(self)


        self.diag = 45 if isDiag else 0


        self.velo = (0.01,0.01)

        self.calc_alpha()
        self.turnability = turnability

        if remote_control:
            self.remote_calc_alpha()
        else:
            self.calc_alpha()



        self.isExplosive = explosive
        self.explosionRadius = explosionRadius
        if self.isExplosive:
            self.deathEvent = lambda: entityScenes[0].castRectExplosion(self.position, self.explosionRadius)



        

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
    
    def draw(self):
        if self.alive:
            self.move()

            if self.isAnimated:
                self.animation.play_looped(self.position, rotation=self.alpha + self.diag)
            else:
                self.image = pg.transform.rotate(self.original_image, self.alpha - 90 + self.diag) #why here
                screen.blit(self.image, world_to_screen_coords(self.top_left_position, vwp))
                self.hitbox.show_HB()
                rect = self.image.get_rect(topleft = self.top_left_position)
                rect.topleft = world_to_screen_coords(rect.topleft, vwp)
                # pg.draw.rect(screen, "white", rect , 3)
        else:
            if self.isAnimated:
                self.animation.alive = False




class Itemz(Entityz):

    def __init__(self, position = (0, 0), hitbox = None, path_to_image_non_highlighted = "assets/goofy_revolver.png", image_scale = 1, image_rotation = 0):
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image_non_highlighted, image_scale=image_scale, image_rotation=image_rotation)

        path_to_image_non_highlighted = path_to_image_non_highlighted.replace(".png", "", 1)
        self.image_highlighted = pg.image.load(path_to_image_non_highlighted + "_highlighted.png")
        self.image_highlighted = super().adjustImage(self.image_highlighted, image_scale, image_rotation)


    def draw(self):

        super().update_HB()
        mouse_HB = HitBox((screen_to_world_coords_rare_use(pg.mouse.get_pos(), vwp), (1, 1)))

        if mouse_HB.check_collision(self.hitbox):
            screen.blit(self.image_highlighted, world_to_screen_coords(self.top_left_position, vwp))
        else:
            screen.blit(self.image, world_to_screen_coords(self.top_left_position, vwp))
        self.hitbox.show_HB()


def C(pos, col="red"):
    pg.draw.circle(screen, col, world_to_screen_coords(pos, vwp), 3)
def px(coord):
    return coord[0]*CellSize,coord[1]*CellSize


class Enemyz(Entityz):

    def __init__(self, position = (0, 0), hitbox = None, path_to_image = "assets/middled_player", image_scale = 1, image_rotation = 0, type = "bombi"):
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image, image_scale=image_scale, image_rotation=image_rotation)
        self.alpha = self.calc_alpha_to_player()
        self.type = type

    def draw(self):
        if self.alive:
            self.alpha = self.calc_alpha_to_player()
            self.image = pg.transform.rotate(self.original_image, self.alpha - 90)
            screen.blit(self.image, world_to_screen_coords(self.top_left_position, vwp))
            self.hitbox.show_HB()
            self.a_move()
            self.update_HB()

    def calc_alpha_to_player(self):
        middle_screen_x, middle_screen_y = world_to_screen_coords(self.position, vwp)
        if playerPos[0]:player_x, player_y = world_to_screen_coords(playerPos[0], vwp)
        else: player_x, player_y = (0, 0)
        dx = player_x - middle_screen_x
        dy = player_y - middle_screen_y

        self.alpha_radians = np.arctan2(-dy, dx)
        return np.degrees(self.alpha_radians)
    

    def a_move(self):
        c_ene_pos = int(self.position[0]/CellSize+0.5), int(self.position[1]/CellSize+0.5)
        c_player_pos = int(playerPos[0][0]/CellSize+0.5) , int(playerPos[0][1]/CellSize+0.5)



        path = a_star(c_ene_pos, c_player_pos, state["HB_layer"])

        # C(c_ene_pos)
        C(px(c_player_pos), "blue")


        if path is not None:
            
            if len(path) > 2:
                c_next_goal_pos = path[1]
                for i in range(len(path)-1):
                    pg.draw.line(screen, "green", world_to_screen_coords(px(path[i]), vwp), world_to_screen_coords(px(path[i+1]), vwp))
            else:
                c_next_goal_pos = c_player_pos

            next_goal_pos = c_next_goal_pos[0]*CellSize, c_next_goal_pos[1]*CellSize
            C(next_goal_pos)
            dx, dy = next_goal_pos[0] - self.position[0], next_goal_pos[1] - self.position[1]
            dist = max(np.sqrt(dx**2 + dy**2), 0.1)
            velo = (dx / dist, dy / dist)
            self.position = velo[0]*10 + self.position[0], velo[1]*10 + self.position[1]



class EntityScenez:

    def __init__(self):
        self.enemyBulletList = []
        self.friendlyBulletList = []

        self.enemyList = []

        self.itemList = []
    

    def update_EntityScene(self):
        self.kill_enemy()
        self.updateList(self.enemyBulletList)
        self.updateList(self.friendlyBulletList)
        self.updateList(self.enemyList)
        self.updateList(self.itemList)

    def draw_EntityScene(self):
        self.update_EntityScene()

        for bullet in self.enemyBulletList: bullet.draw()
        for fbullet in self.friendlyBulletList: fbullet.draw()
        for enemy in self.enemyList: enemy.draw()
        for item in self.itemList: item.draw()

    def kill_enemy(self):
        for enemy in self.enemyList:
            if enemy.alive:
                for bullet in self.friendlyBulletList:
                    

                    if bullet.alive and enemy.hitbox.check_collision(bullet.hitbox):
                        if bullet.isExplosive:
                            self.castRectExplosion(bullet.position, 75)
                        else:
                            Animationz("assets/goofy_blood.png", (32, 32), 9, 4*0.8, 1).play(enemy.position, 0)

                        enemyHit_sound = pg.mixer.Sound("assets/enemyHit_sound.mp3")
                        enemyHit_sound.set_volume(0.1)
                        enemyHit_sound.play()

                        enemy.die()
                        if enemy.type == "bombi":
                            corpse = pg.image.load(f"assets/bombiCorpse_{random.randint(1,2)}.png")
                            corpse = pg.transform.scale_by(corpse, scale_player/1.25)
                            corpse = pg.transform.rotate(corpse, random.randint(0, 360))
                            CorpseList.append((corpse, enemy.position))
                        bullet.die()

    def castRectExplosion(self, position, radius):
        explosionHitbox = HitBox((tuple(e-radius for e in position), (2*radius, 2*radius)))
        explosionHitbox.show_HB()
        Animationz("assets/may_explosion.png", (32, 32), 6, 4/32*radius*0.8, 0.2).play(position, 0)
        for enemy in self.enemyList:
            if enemy.alive:
                if enemy.hitbox.check_collision(explosionHitbox):
                    enemy.die()


    
    def add_enemy(self, enemy:Enemyz):
        self.enemyList.append(enemy)
    
    def add_enemyBullet(self, bullet:Bulletz):
        self.enemyBulletList.append(bullet)
    
    def add_friendlyBulletList(self, bullet: Bulletz):
        self.friendlyBulletList.append(bullet)
    
    def add_item(self, item:Itemz):
        self.itemList.append(item)


    def updateList(self, lst):
        lst[:] = [e for e in lst if e.alive]


        