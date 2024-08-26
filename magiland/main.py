import pygame
pygame.init()

from screen import Screen
# Create the screen
ASPECT_RATIO = 8/5
RESOLUTION = 1600
SCREEN = Screen(ASPECT_RATIO, RESOLUTION)


from managers import MainWindowManager
from misc import events

# Reroutes events and drawing commands through a manager to clean the main code
main_manager = MainWindowManager(SCREEN)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        else:
            main_manager.handleEvent(event)

    # Tick the loop
    main_manager.tick()

    # Draw to screen
    SCREEN.get().fill((0, 0, 0))

    main_manager.draw(SCREEN.get())
    
    SCREEN.update()

    # FPS control
    clock.tick(60)

pygame.quit()
