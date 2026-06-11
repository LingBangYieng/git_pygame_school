import pygame as pg
from class_collide_rect import HitBox
from scenez import *
from helper_pygame import *
#from globals import *



WIDTH, HEIGHT = 1280, 720

pg.display.init()
pg.mixer.init()

pg.display.set_caption("Redundant")
icon = pg.image.load("assets/goofy_revolver.png")
icon = pg.transform.rotate(icon, 45)
pg.display.set_icon(icon)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

buttonclick = pg.mixer.Sound("assets/buttonclick.mp3")
buttonclick.set_volume(0.5)

lobby_song = pg.mixer.music.load("assets/stragi_existent.mp3")
pg.mixer.music.set_volume(0.125)
pg.mixer.music.play(-1)

def bs():
    buttonclick.play()

def quit_game():
    global running
    running = False
    bs()

def switch_scene(scene:Scenez):
    global current_scene
    current_scene = scene[0]
    bs()

def change_resolution(args):
    global screen, current_scene
    width, height = args[0], args[1]
    screen = pg.display.set_mode((width, height))
    lobby = createLobby(width, height)
    current_scene = lobby
    bs()

def fullscreen():
    global screen, current_scene
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    w, h = screen.get_size()
    lobby = createLobby(w, h)
    current_scene = lobby
    bs()



def createLobby(WIDTH, HEIGHT):
    lobby = Scenez(screen)
    settings = Scenez(screen)
    contents = Scenez(screen)

    NightlyFuchsia = (72, 28, 43)
    DebugGreen = (0, 100, 0)
    TannedBrown = (211, 188, 156)
    tbtBlue = (46, 150, 172)

    tbt = Imagez(pathToImage="assets/bluetiger_black_C.png", isBackground=True)
    buttonBacktbt = Buttonz((WIDTH * 0.02, HEIGHT - HEIGHT * 0.02 - HEIGHT * 0.025), (WIDTH * 0.05, HEIGHT * 0.025), screen, True, "Back", (0, 0, 0), int(HEIGHT * 0.0125), 5, tbtBlue, switch_scene, [lobby])
    contents.add_image(tbt)
    contents.add_button(buttonBacktbt)

    color_theme = TannedBrown
    color_theme = NightlyFuchsia
    buttonBack = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.525), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "Back", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, switch_scene, [lobby])
    buttonResolution0 = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.62), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "1920 x 1080", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, change_resolution, [1920, 1080])
    buttonResolution1 = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.715), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "1280 x 720", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, change_resolution, [1280, 720])
    buttonFullscreen = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.81), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "Fullscreen", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, fullscreen)

    settings.add_button(buttonBack)
    settings.add_button(buttonResolution0)
    settings.add_button(buttonResolution1)
    settings.add_button(buttonFullscreen)

    background = Imagez(position=(0, 0), pathToImage="assets/may_background.png", isBackground=True)
    content = Buttonz((WIDTH * 0.15 - WIDTH * 0.08, HEIGHT * 0.57), (5, 5), screen, False, "", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, switch_scene, [contents], False)
    buttonStart = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.43), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "Start Game", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme)
    buttonSettings = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.525), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "Settings", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, switch_scene, [settings])
    buttonQuit = Buttonz((WIDTH * 0.5 - WIDTH * 0.08, HEIGHT * 0.62), (WIDTH * 0.16, HEIGHT * 0.07), screen, True, "Quit", (0, 0, 0), int(HEIGHT * 0.04), 5, color_theme, quit_game)
    title = "Redundant"
    version = "alpha v0.1"
    featured = "Abdul, Agmar, Kreatin"

    lobby.add_image(background)
    lobby.add_button(buttonStart)
    lobby.add_button(buttonSettings)
    lobby.add_button(buttonQuit)
    lobby.add_button(content)
    lobby.add_text(title, color_theme, WIDTH * 0.5, HEIGHT * 0.14, int(HEIGHT * 0.15), True)
    lobby.add_text(version, color_theme, WIDTH * 0.96, HEIGHT * 0.97, int(HEIGHT * 0.025), True)
    lobby.add_text(featured, color_theme, WIDTH * 0.07, HEIGHT * 0.97, int(HEIGHT * 0.025), True)

    return lobby


lobby = createLobby(WIDTH=WIDTH, HEIGHT=HEIGHT)




mouse_HB = HitBox(((0, 0), (1, 1)))
MHB = mouse_HB



current_scene = lobby

while running:

    events[0] = pg.event.get()
    keys = pg.key.get_pressed()
    for event in events[0]:
        if event.type == pg.QUIT:
            running = False
        # if keys[pg.K_p]:
        #     WIDTH, HEIGHT = 1920, 1080
        #     screen = pg.display.set_mode((WIDTH, HEIGHT))
        #     lobby = createLobby(WIDTH=WIDTH, HEIGHT=HEIGHT)
        #     current_scene = lobby
        # if keys[pg.K_o]:
        #     WIDTH, HEIGHT = 1280, 720
        #     screen = pg.display.set_mode((WIDTH, HEIGHT))
        #     lobby = createLobby(WIDTH=WIDTH, HEIGHT=HEIGHT)
        #     current_scene = lobby

    screen.fill("black")

    mx, my = (pg.mouse.get_pos())
    mouse_HB.x = mx
    mouse_HB.y = my
    MHB_rect[0] = HitBox(((mx,my),(1, 1)))

    current_scene.draw_scene()


    pg.display.update()

    clock.tick(69)

pg.quit()