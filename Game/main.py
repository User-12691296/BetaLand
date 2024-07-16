import pygame
pygame.init()

from screen import Screen
from menus import MainMenu

# Create the screen
ASPECT_RATIO = 8/5
RESOLUTION = 1600
screen = Screen(ASPECT_RATIO, RESOLUTION)

main_menu = MainMenu(screen.get_size())


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            main_menu.onMouseMotion(screen.translatePointFromScreen(event.pos))

        if event.type == pygame.MOUSEBUTTONDOWN:
            main_menu.onMouseDown(screen.translatePointFromScreen(event.pos), event.button)

        if event.type == pygame.MOUSEBUTTONUP:
            main_menu.onMouseUp(screen.translatePointFromScreen(event.pos), event.button)
            
    screen.get().fill((0, 0, 0))

    main_menu.draw(screen.get())

    screen.update()

    clock.tick(60)

pygame.quit()
