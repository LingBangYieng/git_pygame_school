from class_collide_rect import HitBox
import pygame as pg
import numpy as np
from helper_pygame import *
#from globals import *
from pathfind_non_visual import a_star

pg.font.init()

def get_topleft(image: pg.Surface, position: tuple):
    return image.get_rect(center=position).topleft



class Entityz:

    def __init__(self, position:tuple = (0, 0), hitbox: HitBox = None, path_to_image: str = "assets/middled_player", image_scale: float = 1, image_rotation: float = 0, isAnimated = False, path_to_animation = ""):
        '''position should be center position of the object'''
        #genral
        self.alive = True

        #geometry
        self.position = position
        self.velo = (0, 0)

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
                 path_to_animation = "assets/rockety_anim.png",
                 damage = 20):
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
            self.deathEvent = lambda: state.entityScene.castRectExplosion(self.position, self.explosionRadius)


        self.damage = damage
        

    def calc_alpha(self):
        if self.alive:
            middle_screen_x, middle_screen_y = wtsc(self.position, vwp)

            dx = pg.mouse.get_pos()[0] - middle_screen_x
            dy = pg.mouse.get_pos()[1] - middle_screen_y

            self.alpha_radians = np.arctan2(-dy, dx)
            self.alpha = np.degrees(self.alpha_radians)


    def remote_calc_alpha(self):
        if not self.alive:
            return

        middle_screen_x, middle_screen_y = wtsc(self.position, vwp)

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
                screen.blit(self.image, wtsc(self.top_left_position, vwp))

                # self.hitbox.show_HB()
                rect = self.image.get_rect(topleft = self.top_left_position)
                rect.topleft = wtsc(rect.topleft, vwp)
                # pg.draw.rect(screen, "white", rect , 3)
        else:
            if self.isAnimated:
                self.animation.alive = False




class Itemz(Entityz):

    def __init__(self, position = (0, 0), hitbox = None, path_to_image_non_highlighted = "assets/goofy_revolver.png", image_scale = 1, image_rotation = 0, instruction = None, instructionArgs:list = []):
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image_non_highlighted, image_scale=image_scale, image_rotation=image_rotation)

        path_to_image_non_highlighted = path_to_image_non_highlighted.replace(".png", "", 1)
        self.image_highlighted = pg.image.load(path_to_image_non_highlighted + "_highlighted.png")
        self.image_highlighted = super().adjustImage(self.image_highlighted, image_scale, image_rotation)
        self.instrArgs = instructionArgs
        self.instr = instruction

        self.hostageSaved = False


    def draw(self):
        super().update_HB()
        mouse_HB = HitBox((screen_to_world_coords_rare_use(pg.mouse.get_pos(), vwp), (1, 1)))

        if mouse_HB.check_collision(self.hitbox):
            screen.blit(self.image_highlighted, wtsc(self.top_left_position, vwp))
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                self.do_instr()
                updateScreens()
                self.hostageSaved = True
                self.die()

        else:
            screen.blit(self.image, wtsc(self.top_left_position, vwp))
        # self.hitbox.show_HB()


    def do_instr(self):
        if self.instrArgs:
            self.instr(self.instrArgs)
        else:
            self.instr() 


class Hostage(Itemz):
    hfont = pg.font.Font("assets/born2bsporty-fs.regular.otf", int(7.5*s.GameScale))

    def __init__(self, position=(0, 0), hitbox=None, path_to_image_non_highlighted="assets/goofy_revolver.png", image_scale=1, image_rotation=0, instruction = None, instructionArgs:list = []):
        super().__init__(position=position, hitbox=hitbox, path_to_image_non_highlighted=path_to_image_non_highlighted, image_scale=image_scale, image_rotation=image_rotation)

        self.text_object = Hostage.hfont.render("SAVE HOSTAGE", True, "white")
        self.text_w_d2 = self.text_object.get_width() / 2
        self.text_h_d2 = self.text_object.get_height() / 2
        self.image_scale = image_scale
        self.instrArgs = instructionArgs
        self.instr = instruction

    def draw(self):
        super().draw()
        if state.MHB_rect.check_collision(self.hitbox):
            screen.blit(self.text_object, wtsc((self.position[0] - self.text_w_d2, self.position[1] - 16*self.image_scale - self.text_h_d2), vwp))

            



#######################
def C(pos, col="red"):
    pg.draw.circle(screen, col, wtsc(pos, vwp), 3)
def px(coord):
    return coord[0]*s.CellSize,coord[1]*s.CellSize
#######################

class Enemyz(Entityz):

    def __init__(self, position = (0, 0), hitbox = None, path_to_image = "assets/middled_player.png", image_scale = 1, image_rotation = 0, type = "bombi"):
        super().__init__(position=position, hitbox=hitbox, path_to_image=path_to_image, image_scale=image_scale, image_rotation=image_rotation)
        self.alpha_radians = 0
        self.alpha = self.calc_alphas()
        self.type = type
        self.extra = (0,0)

        self.genPathBool = True
        self.oldPath = None

        self.hasSeenAgo = 100
        self.setRandomGoalAgo = 100
        self.randomGaol = None

        self.velo = (0, 0) # needed?


        self.hp = 1
        self.timer = 30
        self.lit = False


        self.fovDegr = 60
        self.sightDist = 600

        self.static = False

        self.speed = 5

        self.isreali_ambient = pg.mixer.Sound("assets/israeli_ambient_quiet.mp3")



        self.prevAlpha = 0

        self.invokeTime = None

        

    def draw(self):
    
        if self.alive:
            self.checkHealth()
            self.checkDist()



            self.smooth_alpha(self.calc_alphas())




            self.image = pg.transform.rotate(self.original_image, self.alpha - 90)
            screen.blit(self.image, wtsc(self.top_left_position, vwp))
            # self.hitbox.show_HB()
            self.move()
            self.update_HB()

            LightCone(self.position, -self.alpha, self.fovDegr, self.sightDist)


    def smooth_alpha(self, target, factor=0.1):
        diff = (target - self.alpha + 180) % 360 - 180
        self.alpha += diff * factor
        self.alpha %= 360

    def calc_alphas(self):
        #saved IMPRTONAT
        self.alpha_to_player = np.rad2deg(self.alpha_radians) if state.playerPos is None else np.rad2deg(np.atan2(-(state.playerPos[1] - self.position[1]),(state.playerPos[0] - self.position[0])))
        self.distToPlayer_sqr = 10000000 if state.playerPos is None else (self.position[0] - state.playerPos[0])**2 + (self.position[1] - state.playerPos[1])**2
        
        if self.velo == (0,0):
            # print("using avoid", self.velo ,np.rad2deg(self.alpha_radians)) MMM
            return np.degrees(self.alpha_radians)

        #alpha override
        self.alpha_radians = np.arctan2(-self.velo[1], self.velo[0])
        # print("not using over", (-self.velo[1], self.velo[0]), np.degrees(self.alpha_radians))MMM
        return np.degrees(self.alpha_radians)
    

    def aStarPath(self, goal="player", visual=True):
        # D.add("E", "A")MMM
        
        c_ene_pos = int(self.position[0]/s.CellSize), int(self.position[1]/s.CellSize)

        if goal == "player":
            c_player_pos = int(state.playerPos[0]/s.CellSize+0.5) , int(state.playerPos[1]/s.CellSize+0.5)
        else:
            c_player_pos = int(goal[0]/s.CellSize+0.5) , int(goal[1]/s.CellSize+0.5)

        playerInHB = state.HB_layer[c_player_pos[1]][c_player_pos[0]]
        if playerInHB:
            # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            self.genPathBool = False
            if self.savedPath is not None: path = self.savedPath.copy()
            else: path = None
        else:
            if self.genPathBool:
                path = a_star(c_ene_pos, c_player_pos, state.HB_layer)
                if path: self.savedPath = path.copy()
                self.genPathBool = False
                if path is not None:
                    self.oldPath = path.copy()
            else:
                path = self.oldPath
                self.genPathBool = True

        # C(c_ene_pos)
        C(px(c_player_pos), "blue")


        if path is not None:
            
            # chosen = 1
            # for i in range(1,len(path)):
            #     if ((px(path[i])[0] - self.position[0])**2 + (px(path[i])[1] - self.position[1])**2) < s.CellSize/2:
            #         chosen = i


            if len(path) > 2:
                c_next_goal_pos = path[1]
                if visual:
                    for i in range(len(path)-1):
                        pg.draw.line(screen, "green", wtsc(px(path[i]), vwp), wtsc(px(path[i+1]), vwp))
            else:
                c_next_goal_pos = c_player_pos

            next_goal_pos = c_next_goal_pos[0]*s.CellSize + s.CellSize/2, c_next_goal_pos[1]*s.CellSize + s.CellSize/2
            C(next_goal_pos)
            dx, dy = next_goal_pos[0] - self.position[0], next_goal_pos[1] - self.position[1]
            
            dist = max(np.sqrt(dx**2 + dy**2), 0.1)
            if dist<s.CellSize/2 and self.savedPath: #dx<s.CellSize and dy<s.CellSize and self.savedPath:
                self.savedPath.pop(0)
            


            # print("me:", self.position )
            # print("goal:", next_goal_pos) MMM
            # print("path:", path[:3] if path else None)

            self.velo = (dx / dist, dy / dist)
            

    def move(self):
        # print(self.static)
        basespeed = 5

        if self.lit:
            return
        
        self.velo = (0, 0)

        self.hasSeenAgo += 1
        # print(self.hasSeenAgo)
        # print(f"{self.distToPlayer_sqr}")
        # D.add("ggg", f"{self.distToPlayer_sqr:.2f}, {self.sightDist**2:.2f}, {self.alpha-self.fovDegr/2:.2f},{ self.alpha_to_player:.2f} ,{self.alpha+self.fovDegr/2:.2f}")
        # if self.distToPlayer_sqr < self.sightDist**2 and self.alpha-self.fovDegr/2 <= self.alpha_to_player <= self.alpha+self.fovDegr/2:
        diff = (self.alpha_to_player - self.alpha + 180) % 360 - 180
        if abs(diff) <= self.fovDegr / 2 and self.distToPlayer_sqr < self.sightDist**2*1.1:
            # print("see u")#, self.distToPlayer_sqr , self.sightDist**2 , self.alpha-self.fovDegr/2 <= self.alpha_to_player <= self.alpha+self.fovDegr/2)
            # D.add("case", "cansee")MMM
            if self.seePath():
                # D.add("case", "cansee_full")MMM
                # print("found you")MMM
                self.speed = 7
                if self.hasSeenAgo != 1:
                    # self.isreali_ambient = pg.mixer.Sound("assets/israeli_ambient_quiet.mp3")
                    self.isreali_ambient.set_volume(0.4 * s.SFX_VOLUME)
                    state.soundChannel.play(self.isreali_ambient)

                self.hasSeenAgo = 0


        elif self.hasSeenAgo < 400:
            # D.add("case", "have seen u recnet")MMM
            # print("wherea u")MMM
            # if self.distToPlayer_sqr < 200**2 or self.static:
            #     print("inv")
            #     self.standStill(100)

            # print("where are u")
            self.aStarPath()

        else:
            # D.add("case", "guess hes gone")MMM
            self.randomPath()


        # print(self.extra)
        if self.speed > basespeed:
            self.speed *= 0.999
        else:
            self.speed = basespeed
        # print(self.speed)
        if not self.static:
            self.position = self.velo[0]*self.speed+self.extra[0] + self.position[0], self.velo[1]*self.speed+self.extra[1] + self.position[1]
            self.extra = (0,0)


    def seePath(self, sprint=2) -> bool:
        # D.add("E", "S")MMM
        _, coll, dist = cast_ray(self.position, state.playerPos, 5000, 100, 32*3, state.HB_layer)

        gx,gy = state.playerPos
        dx, dy =  gx - self.position[0], gy - self.position[1]
        raw_dist = max(np.sqrt(dx**2 + dy**2), 0.1)

        if coll:
            cx,cy = coll
            cdx, cdy =  cx - self.position[0], cy - self.position[1]
            dist = max(np.sqrt(cdx**2 + cdy**2), 0.1)


        doMove = False
        if coll:
            # print("c", end="")
            pg.draw.circle(screen, "red", wtsc(coll, vwp), 10)
            if dist > raw_dist:
                # print("a", end="")
                doMove = True
        else:
            doMove = True
        
            

        # print(doMove)
        if doMove:
            # try:
            #     print("coll", coll, "hit ignore", dist > raw_dist)
            #     print(dist, raw_dist)
            # except:
            #     pass
            self.velo = (dx / raw_dist * sprint, dy / raw_dist * sprint)
            pg.draw.circle(screen, "pink",  wtsc(self.position, vwp), 10)
            return True
        # else:
        #     if coll:
        #         pg.draw.circle(screen, "red", wtsc(coll, vwp), 10)

        
        return False
    

    def randomPath(self):
        self.setRandomGoalAgo += random.randint(1,2)
        if self.setRandomGoalAgo > 400 or self.randomGaol == None:
            crx, cry = random.randint(0, len(state.HB_layer[0])), random.randint(0, len(state.HB_layer))
            while not check_boundaries(cry,crx,state.HB_layer) or state.HB_layer[cry][crx]: 
                crx, cry = random.randint(2, len(state.HB_layer[0])-2), random.randint(2, len(state.HB_layer)-2)
            self.randomGaol = (crx*s.CellSize,cry*s.CellSize)
            self.setRandomGoalAgo = 0

        if self.setRandomGoalAgo > 170 and self.randomGaol:
            self.aStarPath(goal=self.randomGaol)

    def standStill(self, time):
        if self.invokeTime == None:
            self.invokeTime = state.counter
        # print(self.invokeTime)MMM
        if state.counter - self.invokeTime < time:
            #do in the time
            self.static = True
        else:
            self.static = False
            self.invokeTime = None

    # def turnAround(self):
    #     if self.invokeTime == None:
    #         self.invokeTime = state.counter
    #     if state.counter - self.invokeTime < 360:
    #         #do in the time
    #         self.static = True
    #     else:
    #         self.static = False
    #         self.invokeTime = None


    # def invokeCount(self):
    #     for invKey in self.invokeDict.keys:
    #         self.invokeDict[f]


    def die(self):
        super().die()
        if self.type == "bombi":
            corpse = pg.image.load(f"assets/bombiCorpse_{random.randint(1,2)}.png")
            corpse = pg.transform.scale_by(corpse, s.GameScale/1.5)
            corpse = pg.transform.rotate(corpse, random.randint(0, 360))
            state.CorpseList.append((corpse, self.position))
        try:
            self.isreali_ambient.stop()
        except:
            pass

    def takeDamage(self, damage=0):
        self.checkHealth()
        self.hp -= damage

    def checkHealth(self):
        if self.hp < 0:
            self.die()

    def checkDist(self):
        # print(self.position[0]-state.playerPos[0])
        if abs(self.position[0]-state.playerPos[0]) < s.CellSize/8:
            if abs(self.position[1]-state.playerPos[1]) < s.CellSize/8:
                self.explode()
        if self.lit:
            self.explode()


    def explode(self):
        self.timer -= 1
        self.lit = True
        if self.timer<0:
            state.entityScene.castRectExplosion(self.position, 100)

        

    # def saveToFile(self):
    #     return self.saveToString()
    #     return "&".join(
    #         f"{attr}={getattr(self, attr)!r}"
    #         for attr in dir(self)
    #         if not callable(getattr(self, attr)) 
    #         and not attr.startswith("__")
    #         and not callable(getattr(self, attr))
    #     )
    

    # def saveToString(self):
    #     return "&".join(
    #         f"{name}={repr(value)}"
    #         for name, value in self.__dict__.items()
    #     )
        
    # def loadFromString(self, s):
    #     for part in s.split("&"):
    #         name, value = part.split("=", 1)

    #         # Try to recover basic Python types
    #         try:
    #             value = eval(value)
    #         except:
    #             pass
    #         print(name, value, type(name), type(value))
    #         setattr(self, name, value)
    #     return self            


class EntityScenez:

    def __init__(self):
        self.enemyBulletList = []
        self.friendlyBulletList = []

        self.enemyList = []

        self.itemList = []
        self.hostageList = []

        self.updatedhostageList = []
    

    def update_EntityScene(self):
        self.kill_enemy()
        self.updateList(self.enemyBulletList)
        self.updateList(self.friendlyBulletList)
        self.updateList(self.enemyList)
        self.updateList(self.itemList)
        self.updateList(self.updatedhostageList)
        # self.updateList(self.hostageList)

    def draw_EntityScene(self):
        self.update_EntityScene()

        for bullet in self.enemyBulletList: bullet.draw()
        for fbullet in self.friendlyBulletList: fbullet.draw()
        for enemy in self.enemyList: enemy.draw()
        for item in self.itemList: item.draw()
        for hostage in self.updatedhostageList: hostage.draw()

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
                        enemyHit_sound.set_volume(0.1 * s.SFX_VOLUME)
                        enemyHit_sound.play()

                        enemy.takeDamage(bullet.damage)
                        state.bulletsInInv += 1

                        bullet.die()

    def castRectExplosion(self, position, radius):
        explosionHitbox = HitBox((tuple(e-radius for e in position), (2*radius, 2*radius)))
        # explosionHitbox.show_HB()
        Animationz("assets/may_explosion.png", (32, 32), 6, 4/32*radius*0.8, 0.2).play(position, 0)
        # pg.draw.polygon(vis.overlay, (0, 0, 0, 50), checkBases(0, 2*np.pi, 2000, state.HB_layer, pos=enemy.position))

        for enemy in self.enemyList:
            if enemy.alive:
                if enemy.hitbox.check_collision(explosionHitbox):
                    enemy.die()
        if state.playerHB.check_collision(explosionHitbox):
            state.gameOver = True


    
    def add_enemy(self, enemy:Enemyz):
        self.enemyList.append(enemy)

    def add_hostage(self, hostage:Hostage):
        self.hostageList.append(hostage)
        self.updatedhostageList.append(hostage)

    def add_enemyBullet(self, bullet:Bulletz):
        self.enemyBulletList.append(bullet)
    
    def add_friendlyBulletList(self, bullet: Bulletz):
        self.friendlyBulletList.append(bullet)
    
    def add_item(self, item:Itemz):
        self.itemList.append(item)


    def updateList(self, lst):
        lst[:] = [e for e in lst if e.alive]


    # def saveToFile(self):
    #     storeAllText = "\n".join([enemy.saveToFile() for enemy in self.enemyList])
    #     with open("saveTest.txt", "w") as f:
    #         f.write(storeAllText)

    # def loadFromFile(self):
    #     with open("saveTest.txt", "r") as f:
    #         storeAllText = f.read()
    #     self.enemyBulletList = [Enemyz().loadFromString(singleEnemyString) for singleEnemyString in storeAllText.split("\n")]


        