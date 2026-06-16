import pygame as pg
from class_collide_rect import HitBox
from scenez import *
from helper_pygame import *
import time
from entityz import *

#from globals import *



# state.WIDTH, state.HEIGHT = 1280, 720

pg.display.init()
pg.mixer.init()

pg.display.set_caption("Redundant")
icon = pg.image.load("assets/goofy_revolver.png")
icon = pg.transform.rotate(icon, 45)
pg.display.set_icon(icon)
screen = pg.display.set_mode((state.WIDTH, state.HEIGHT))

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

def change_resolution(args):
    # global screen, current_scene
    state.FULLSCREEN = False
    state.WIDTH, state.HEIGHT = args[0], args[1]
    
    bs()

def fullscreen():
    # global screen, current_scene
    state.FULLSCREEN = True
    state.WIDTH,state.HEIGHT = pg.display.get_desktop_sizes()[0]
    bs()

def startPgSchoolShii():
    # from pygame_school_shiit import RUN
    # RUN()
    global overlay
    overlay = pg.Surface((state.WIDTH, state.HEIGHT), pg.SRCALPHA)
    with open("pygame_school_shiit.py") as f:
        exec(f.read())




import json
def updateSettings():
    global screen, current_scene

    rebuildSettings()
    saveSettings = {}
    for settingKey in state.SETTINGS.keys():
        saveSettings[settingKey] = state.SETTINGS[settingKey]
    
    with open("settings.json", "w") as f:
        json.dump(saveSettings, f, indent=4)
    
    if state.FULLSCREEN: screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    else: screen = pg.display.set_mode((state.WIDTH, state.HEIGHT))
    createLobby()
    current_scene = settings
    # switch_scene(lobby) #maybe cricticla

    
def readSettings():
    with open("settings.json", "r") as f:
        sett = json.load(f)
    state.SETTINGS = sett

def rebuildSettings():
    state.SETTINGS["RESOLUTION"] = f"{state.WIDTH}x{state.HEIGHT}"
    state.SETTINGS["FULLSCREEN"] = state.FULLSCREEN



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
    buttonBacktbt = Buttonz((state.WIDTH * 0.02, state.HEIGHT - state.HEIGHT * 0.02 - state.HEIGHT * 0.025), (state.WIDTH * 0.05, state.HEIGHT * 0.025), screen, True, "Back", (0, 0, 0), int(state.HEIGHT * 0.0125), 5, tbtBlue, switch_scene, [lobby])
    contents.add_image(tbt)
    contents.add_button(buttonBacktbt)

    color_theme = TannedBrown
    color_theme = NightlyFuchsia
    buttonBack = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.525), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Back", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, switch_scene, [lobby])
    buttonResolution0 = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.62), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "1920 x 1080", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, change_resolution, [1920, 1080])
    buttonResolution1 = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.715), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "1280 x 720", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, change_resolution, [1280, 720])
    buttonFullscreen = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.81), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Fullscreen", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, fullscreen)
    buttonSave = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.905), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Apply", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, updateSettings)
    


    settings.add_button(buttonBack)
    settings.add_button(buttonResolution0)
    settings.add_button(buttonResolution1)
    settings.add_button(buttonFullscreen)
    settings.add_button(buttonSave)

    background = Imagez(position=(0, 0), pathToImage="assets/may_background.png", isBackground=True)
    content = Buttonz((state.WIDTH * 0.15 - state.WIDTH * 0.08, state.HEIGHT * 0.57), (5, 5), screen, False, "", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, switch_scene, [contents], False)
    buttonStart = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.43), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Start Game", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, startPgSchoolShii)
    buttonSettings = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.525), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Settings", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, switch_scene, [settings])
    buttonQuit = Buttonz((state.WIDTH * 0.5 - state.WIDTH * 0.08, state.HEIGHT * 0.62), (state.WIDTH * 0.16, state.HEIGHT * 0.07), screen, True, "Quit", (0, 0, 0), int(state.HEIGHT * 0.04), 5, color_theme, quit_game)
    title = "Redundant"
    version = "alpha v0.1"
    featured = "Abdul, Agmar, Kreatin"

    lobby.add_image(background)
    lobby.add_button(buttonStart)
    lobby.add_button(buttonSettings)
    lobby.add_button(buttonQuit)
    lobby.add_button(content)
    lobby.add_text(title, color_theme, state.WIDTH * 0.5, state.HEIGHT * 0.14, int(state.HEIGHT * 0.15), True)
    lobby.add_text(version, color_theme, state.WIDTH * 0.96, state.HEIGHT * 0.97, int(state.HEIGHT * 0.025), True)
    lobby.add_text(featured, color_theme, state.WIDTH * 0.07, state.HEIGHT * 0.97, int(state.HEIGHT * 0.025), True)

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
        #     state.WIDTH, state.HEIGHT = 1920, 1080
        #     screen = pg.display.set_mode((state.WIDTH, state.HEIGHT))
        #     lobby = createLobby(state.WIDTH=state.WIDTH, state.HEIGHT=state.HEIGHT)
        #     current_scene = lobby
        # if keys[pg.K_o]:
        #     state.WIDTH, state.HEIGHT = 1280, 720
        #     screen = pg.display.set_mode((state.WIDTH, state.HEIGHT))
        #     lobby = createLobby(state.WIDTH=state.WIDTH, state.HEIGHT=state.HEIGHT)
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