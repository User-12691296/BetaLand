import pygame

from misc import events
import game
import menus

class MainWindowManager(events.EventAcceptor):
    def __init__(self, screen):
        self.screen = screen

        self.active_alpha = "main-menu"

        screen_size = self.screen.get_size()
        self.alphas = {"main-menu": menus.MainMenu(screen_size),
                       "settings-menu": menus.SettingsMenu(screen_size),
                       "game": game.GameManager(screen_size)}
    

    def callOnAllAlphas(self, action):
        for alpha in self.alphas.values():
            action(alpha)

    def callOnActiveAlpha(self, action):
        action(self.alphas[self.active_alpha])
    
    def handleEvent(self, event):
        if event.type == events.GAME_START:
            self.alphas[self.active_alpha].close()
            self.active_alpha = "game"
            self.alphas[self.active_alpha].start()
        
        if event.type == events.RETURN_TO_MAIN_MENU:
            self.alphas[self.active_alpha].close()
            self.active_alpha = "main-menu"
            self.alphas[self.active_alpha].start()
            
        if event.type == events.OPEN_SETTINGS:
            self.alphas[self.active_alpha].close()
            self.active_alpha = "settings-menu"
            self.alphas[self.active_alpha].start()
            
        if event.type == pygame.MOUSEMOTION:
            self.callOnActiveAlpha(lambda alpha: alpha.onMouseMotion(self.screen.translatePointFromScreen(event.pos)))

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.callOnActiveAlpha(lambda alpha: alpha.onMouseDown(self.screen.translatePointFromScreen(event.pos), event.button))

        if event.type == pygame.MOUSEBUTTONUP:
            self.callOnActiveAlpha(lambda alpha: alpha.onMouseUp(self.screen.translatePointFromScreen(event.pos), event.button))

        if event.type == pygame.KEYDOWN:
            self.callOnActiveAlpha(lambda alpha: alpha.onKeyDown(event.key, event.mod, event.unicode))

        if event.type == pygame.KEYUP:
            self.callOnActiveAlpha(lambda alpha: alpha.onKeyUp(event.key, event.mod, event.unicode))
            
    def draw(self, surface):
        self.alphas[self.active_alpha].draw(self.screen.get())

    def tick(self):
        self.alphas[self.active_alpha].tick()
