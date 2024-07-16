import pygame
import events
import menus

class MainWindowManager(events.EventAcceptor):
    def __init__(self, screen):
        self.screen = screen
        self.main_menu = menus.MainMenu(self.screen.get_size())
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.main_menu.onMouseMotion(self.screen.translatePointFromScreen(event.pos))

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.main_menu.onMouseDown(self.screen.translatePointFromScreen(event.pos), event.button)

        if event.type == pygame.MOUSEBUTTONUP:
            self.main_menu.onMouseUp(self.screen.translatePointFromScreen(event.pos), event.button)

    def draw(self, surface):
        self.main_menu.draw(self.screen.get())
