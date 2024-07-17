import pygame

RETURN_TO_MAIN_MENU = pygame.USEREVENT + 0
GAME_START = pygame.USEREVENT + 1
OPEN_SETTINGS = pygame.USEREVENT + 2

class EventAcceptor:
    def onMouseMotion(self, pos): pass
    def onMouseDown(self, pos, buttons): pass
    def onMouseUp(self, pos, button): pass
