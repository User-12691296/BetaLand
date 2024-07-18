import pygame
import events

class GameWindow(events.Alpha):
    def __init__(self, screen_size):
        self.load_bgs()

        self.red = True

    def load_bgs(self):
        pass
    
    ## EVENTS
    def start(self):
        print("Game starting!")
        
    def onKeyDown(self, key, mod, unicode):
        if key == pygame.K_a:
            self.red = not self.red

        if key == pygame.K_l:
            pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))

    def close(self):
        print("Game closing!")
    
    ## DRAW
    def draw(self, surface):
        self.draw_bg(surface)

    def draw_bg(self, surface):
        surface.fill((192, 0, 0) if self.red else (0, 0, 0))
        
