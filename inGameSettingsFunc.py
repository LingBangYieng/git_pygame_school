from scenez import *
from helper_pygame import *

def bs():
    # buttonclick.play()
    pass

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

def BackToGame():
    global ESCRunning
    ESCRunning = False
    print("hhhhh", ESCRunning)
    bs()

def updateSettings():
    s.applySettings()
    global screen, current_scene

    if state.FULLSCREEN: screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    # else: screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
    updateScreens()

    current_scene = createSettingsScene()

def quitGame():
    state.game_loop = False
    BackToGame()

current_scene = None
def createSettingsScene():
    settings = Scenez(screen)
    NightlyFuchsia = (72, 28, 43)
    color_theme = NightlyFuchsia

    buttonCount = 6
    buttonHeight = s.HEIGHT * 0.07
    topRowHeight = s.HEIGHT - buttonHeight * buttonCount/2
    # print(topRowHeight, s.HEIGHT)

    buttonBack = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.525), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Back", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, BackToGame)
    buttonResolution0 = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.62), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "1920 x 1080", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, change_resolution, "1920x1080")
    buttonResolution1 = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.715), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "1280 x 720", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, change_resolution, "1280x720")
    buttonFullscreen = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.81), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Fullscreen", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, fullscreen)
    buttonSave = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.905), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Apply", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, updateSettings)
    
    buttonQuit = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 1), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Quit Game", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, quitGame)
    

    settings.add_button(buttonBack)
    settings.add_button(buttonResolution0)
    settings.add_button(buttonResolution1)
    settings.add_button(buttonFullscreen)
    settings.add_button(buttonSave)

    settings.add_button(buttonQuit)
    return settings

ESCRunning = True
def GoEscMenu():
    state.soundChannel.pause()
    global current_scene, ESCRunning
    ESCRunning = True
    settingsMenu = createSettingsScene()
    current_scene = settingsMenu
    while ESCRunning:
        state.MHB_rect.setPos(pg.mouse.get_pos())
        state.events = pg.event.get()
        for event in state.events:
            if event.type == pg.QUIT:
                pg.quit()
                return

        screen.fill((0, 0, 0))
        # print(ESCRunning)
        
        current_scene.draw_scene()

        pg.display.flip()
    
    
    state.soundChannel.unpause()
    return



    