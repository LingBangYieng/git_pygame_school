import pygame as pg
from class_collide_rect import HitBox
from scenez import *
from helper_pygame import *
import time
from entityz import *
from pygame_school_shiit import pss

#from globals import *



# s.WIDTH, s.HEIGHT = 1280, 720

pg.display.init()
pg.mixer.init()

pg.display.set_caption("Redundant")
icon = pg.image.load("assets/goofy_revolver.png")
icon = pg.transform.rotate(icon, 45)
pg.display.set_icon(icon)
screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))

clock = pg.time.Clock()
running = True

# buttonclick = pg.mixer.Sound("assets/buttonclick.mp3")
# buttonclick.set_volume(0.1)

# lobby_song = pg.mixer.music.load("assets/stragi_existent.mp3")
# pg.mixer.music.set_volume(0.125)
# pg.mixer.music.play(-1)



def bs():
    # buttonclick.play()
    pass

def quit_game():
    global running
    running = False
    bs()

def switch_scene(scene:Scenez):
    global current_scene
    current_scene = scene[0]
    bs()

def change_resolution(arg):
    # global screen, current_scene
    state.FULLSCREEN = False
    s.RESOLUTION = arg
    
    bs()

def fullscreen():
    # global screen, current_scene
    state.FULLSCREEN = True
    w,h = pg.display.get_desktop_sizes()[0]
    s.RESOLUTION = f"{w}x{h}"
    bs()

def startPgSchoolShii():
    # from pygame_school_shiit import RUN
    # RUN()
    global overlay
    overlay = pg.Surface((s.WIDTH, s.HEIGHT), pg.SRCALPHA)
    # with open("pygame_school_shiit.py") as f:
    #     exec(f.read())
    pss()



def updateSettings():
    s.applySettings()
    global screen, current_scene

    if state.FULLSCREEN: screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    else: screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))

    createLobby()
    current_scene = settings
    switch_scene([lobby]) #maybe cricticla

    
# def readSettings():
#     with open("settings.json", "r") as f:
#         sett = json.load(f)
#     state.SETTINGS = sett

# def rebuildSettings():
#     state.SETTINGS["RESOLUTION"] = f"{s.WIDTH}x{s.HEIGHT}"
#     state.SETTINGS["FULLSCREEN"] = state.FULLSCREEN



lobby = Scenez(screen)
settings = Scenez(screen)

def createLobby():
    global lobby, settings
    lobby = Scenez(screen)
    settings = Scenez(screen)
    contents = Scenez(screen)

    NightlyFuchsia = (72, 28, 43)
    DebugGreen = (0, 100, 0)
    TannedBrown = (211, 188, 156)
    tbtBlue = (46, 150, 172)

    tbt = Imagez(pathToImage="assets/bluetiger_black_C.png", isBackground=True)
    buttonBacktbt = Buttonz((s.WIDTH * 0.02, s.HEIGHT - s.HEIGHT * 0.02 - s.HEIGHT * 0.025), (s.WIDTH * 0.05, s.HEIGHT * 0.025), screen, True, "Back", (0, 0, 0), int(s.HEIGHT * 0.0125), 5, tbtBlue, switch_scene, [lobby])
    contents.add_image(tbt)
    contents.add_button(buttonBacktbt)

    color_theme = TannedBrown
    color_theme = NightlyFuchsia
    buttonBack = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.525), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Back", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, switch_scene, [lobby])
    buttonResolution0 = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.62), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "1920 x 1080", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, change_resolution, "1920x1080")
    buttonResolution1 = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.715), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "1280 x 720", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, change_resolution, "1280x720")
    buttonFullscreen = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.81), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Fullscreen", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, fullscreen)
    buttonSave = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.905), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Apply", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, updateSettings)
    


    settings.add_button(buttonBack)
    settings.add_button(buttonResolution0)
    settings.add_button(buttonResolution1)
    settings.add_button(buttonFullscreen)
    settings.add_button(buttonSave)

    background = Imagez(position=(0, 0), pathToImage="assets/may_background.png", isBackground=True)
    content = Buttonz((s.WIDTH * 0.15 - s.WIDTH * 0.08, s.HEIGHT * 0.57), (5, 5), screen, False, "", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, switch_scene, [contents], False)
    buttonStart = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.43), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Start Game", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, startPgSchoolShii)
    buttonSettings = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.525), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Settings", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, switch_scene, [settings])
    buttonQuit = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, s.HEIGHT * 0.62), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Quit", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, quit_game)
    title = "Redundant"
    version = "alpha v0.1"
    featured = "Abdul, Agmar, Kreatin"

    lobby.add_image(background)
    lobby.add_button(buttonStart)
    lobby.add_button(buttonSettings)
    lobby.add_button(buttonQuit)
    lobby.add_button(content)
    lobby.add_text(title, color_theme, s.WIDTH * 0.5, s.HEIGHT * 0.14, int(s.HEIGHT * 0.15), True)
    lobby.add_text(version, color_theme, s.WIDTH * 0.96, s.HEIGHT * 0.97, int(s.HEIGHT * 0.025), True)
    lobby.add_text(featured, color_theme, s.WIDTH * 0.07, s.HEIGHT * 0.97, int(s.HEIGHT * 0.025), True)

    return lobby


lobby = createLobby()




mouse_HB = HitBox(((0, 0), (1, 1)))
MHB = mouse_HB



current_scene = lobby

while running:

    state.events = pg.event.get()
    keys = pg.key.get_pressed()
    for event in state.events:
        if event.type == pg.QUIT:
            running = False
        # if keys[pg.K_p]:
        #     s.WIDTH, s.HEIGHT = 1920, 1080
        #     screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        #     lobby = createLobby(s.WIDTH=s.WIDTH, s.HEIGHT=s.HEIGHT)
        #     current_scene = lobby
        # if keys[pg.K_o]:
        #     s.WIDTH, s.HEIGHT = 1280, 720
        #     screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        #     lobby = createLobby(s.WIDTH=s.WIDTH, s.HEIGHT=s.HEIGHT)
        #     current_scene = lobby

    screen.fill("black")

    mx, my = (pg.mouse.get_pos())
    mouse_HB.x = mx
    mouse_HB.y = my
    state.MHB_rect = HitBox(((mx,my),(1, 1)))

    current_scene.draw_scene()


    pg.display.update()

    clock.tick(69)

pg.quit()