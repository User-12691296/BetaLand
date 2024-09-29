import pygame
pygame.init()

from screen import Screen
# Create the screen
ASPECT_RATIO = 8/5
RESOLUTION = 1600
SCREEN = Screen(ASPECT_RATIO, RESOLUTION)

from managers import MainWindowManager
from misc import events

clean_close = False

# Reroutes events and drawing commands through a manager to clean the main code
main_manager = MainWindowManager(SCREEN)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    # Tick before input
    main_manager.first_tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        #     clean_close = True

        # else:
        #     main_manager.handleEvent(event)

        main_manager.handleEvent(event)

    # Tick after input
    main_manager.main_tick()

    # Draw to screen
    SCREEN.get().fill((0, 0, 0))

    main_manager.draw(SCREEN.get())
    
    SCREEN.update()

    # FPS control
    clock.tick(60)

pygame.quit()


if False:#clean_close == False:
    from misc import closer
