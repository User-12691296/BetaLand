import pygame
from misc import events
from constants import ASSETS
import os

class SettingsMenu(events.Alpha):
    def __init__(self, screen_size):
        bg = pygame.image.load(os.path.join(ASSETS.MENU_PATH, ASSETS.SETTINGS_MENU_BG)).convert()
        self.bg = pygame.transform.scale(bg, screen_size)

    def onMouseDown(self, pos, button):
        if button == pygame.BUTTON_LEFT:
            pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))

    def draw(self, surface):
        surface.blit(self.bg, (surface.get_rect().centerx-self.bg.get_rect().centerx, 0))
