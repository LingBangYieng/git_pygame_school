from scenez import *
from helper_pygame import *

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

    current_scene = createGameOverScene()

def quitGame():
    state.game_loop = False
    BackToGame()

current_scene = None
def createGameOverScene():
    GameOver = Scenez(screen)
    NightlyFuchsia = (72, 28, 43)
    color_theme = NightlyFuchsia

    buttonCount = 2
    buttonHeight = s.HEIGHT * 0.07
    topRowHeight = s.HEIGHT - buttonHeight * buttonCount/2

    buttonBackToLobby = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.70), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Back to Lobby", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, BackToGame)
    buttonQuitGame = Buttonz((s.WIDTH * 0.5 - s.WIDTH * 0.08, topRowHeight * 0.80), (s.WIDTH * 0.16, s.HEIGHT * 0.07), screen, True, "Ok", (0, 0, 0), int(s.HEIGHT * 0.04), 5, color_theme, quitGame)

    # GameOver.add_button(buttonBackToLobby)
    GameOver.add_button(buttonQuitGame)

    GameOver.add_text("You Lost", color_theme, s.WIDTH * 0.5, s.HEIGHT * 0.25, int(s.HEIGHT * 0.15), True)

    return GameOver

ESCRunning = True
def GameOverSCreen():
    state.soundChannel.pause()
    global current_scene, ESCRunning
    ESCRunning = True
    settingsMenu = createGameOverScene()
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



    