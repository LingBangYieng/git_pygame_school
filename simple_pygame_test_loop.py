# Example file showing a basic pygame "game loop"
import pygame
from Buttons import Buttonz
from class_collide_rect import HitBox

# pygame setup
pygame.display.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

button1 = Buttonz((1280//2, 720//2), 200, 50, screen, True)

mouse_HB = HitBox(0, 0, 1, 1)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")



    mx, my = pygame.mouse.get_pos()
    mouse_HB.x = mx
    mouse_HB.y = my


    button1.draw_button()
    print(button1.hitbox.check_collision(mouse_HB))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()