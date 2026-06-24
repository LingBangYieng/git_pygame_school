from scenez import *
from helper_pygame import *
from pathlib import Path
from pygame_school_shiit import pss

buttonclick = pg.mixer.Sound("assets/buttonclick.mp3")
buttonclick.set_volume(0.1 * s.SFX_VOLUME)

lobby_song = pg.mixer.music.load("assets/stragi_existent.mp3")
pg.mixer.music.set_volume(0.125 * s.SFX_VOLUME)
pg.mixer.music.play(-1)

def bs():
    buttonclick.play()
    pass

def switch_scene(scene:Scenez):
    global current_scene
    current_scene = scene[0]
    bs()


def change_resolution(arg):
    # global screen, current_scene
    s.FULLSCREEN = False
    s.RESOLUTION = arg
    bs()

def fullscreen():
    # global screen, current_scene
    s.FULLSCREEN = True
    w,h = pg.display.get_desktop_sizes()[0]
    s.RESOLUTION = f"{w}x{h}"
    bs()

def BackToGame():
    global ESCRunning
    ESCRunning = False
    print("hhhhh", ESCRunning)
    s.discardSettings()
    bs()

def updateSettings():
    s.applySettings()
    global screen, current_scene

    if s.FULLSCREEN: screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    # else: screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
    updateScreens()

    current_scene = createLevelScene()

def quitGame():
    state.game_loop = False
    BackToGame()

def getMaps():
    maps = []
    for file in Path("saves/").iterdir():
        if file.suffix == ".map":
            if file.stem == "temp_save":
                continue
            maps.append(file.stem)
    return maps

def switchMap(direction):
    maps = getMaps()
    global currentMapIndex, current_scene
    if direction == "left":
        currentMapIndex -= 1
    if direction == "right":
        currentMapIndex += 1

    currentMapIndex = max(0, min(currentMapIndex, len(maps) - 1))
    current_scene = createLevelScene()



current_scene = None
currentMapIndex = None
currentMapIndex = 0
def createLevelScene():
    global currentMapIndex
    levelSelect = Scenez(screen)
    NightlyFuchsia = (72, 28, 43)
    color_theme = NightlyFuchsia

    maps = getMaps()


    buttonCount = 6
    buttonHeight = s.HEIGHT * 0.07
    topRowHeight = s.HEIGHT - buttonHeight * buttonCount/2
    # print(topRowHeight, s.HEIGHT)

    buttonBack = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 1.1), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Back", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, BackToGame)
    buttonLeft = Buttonz((s.WIDTH * 0.125 - s.WIDTH * 0.08, topRowHeight * 1), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "←", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, switchMap, "left")
    buttonRight = Buttonz((s.WIDTH * 0.875 - s.WIDTH * 0.08, topRowHeight * 1), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "→", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, switchMap, "right")

    currentMapImage = pg.transform.scale_by(pg.image.load(f"saves/{maps[currentMapIndex]}_as.png"), 0.25)
    curr_w, curr_h = currentMapImage.get_size()


    currentMap = Imagez(position=(s.WIDTH * 0.5 - curr_w * 0.5, s.HEIGHT * 0.375 - curr_h * 0.5), pathToImage=f"saves/{maps[currentMapIndex]}_as.png", imageScale=0.25)
    
    buttonPlay = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 1), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, f"Play {maps[currentMapIndex]}", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, pss, maps[currentMapIndex])


    levelSelect.add_button(buttonBack)
    levelSelect.add_button(buttonLeft)
    levelSelect.add_button(buttonRight)
    levelSelect.add_button(buttonPlay)
    levelSelect.add_image(currentMap)
    return levelSelect

ESCRunning = True
def GoLevelMenu():
    state.soundChannel.pause()
    global current_scene, ESCRunning
    ESCRunning = True
    settingsMenu = createLevelScene()
    current_scene = settingsMenu
    state.MHB_rect = HitBox((pg.mouse.get_pos(), (1, 1)))
    while ESCRunning:
        state.MHB_rect.setPos(pg.mouse.get_pos())
        state.events = pg.event.get()
        for event in state.events:
            if event.type == pg.QUIT:
                pg.quit()
                return

        screen.fill((0, 0, 0))
        # print(ESCRunning)

        state.MHB_rect = HitBox((pg.mouse.get_pos(), (1, 1)))

        
        current_scene.draw_scene()

        pg.display.flip()
    
    
    state.soundChannel.unpause()
    return



    


# GoLevelMenu()