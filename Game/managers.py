import pygame
import events
import menus

class MainWindowManager(events.EventAcceptor):
    def __init__(self, screen):
        self.screen = screen

        self.active_menu = "main"
        
        self.menus = {"main": menus.MainMenu(self.screen.get_size()),
                      "settings": menus.SettingsMenu(self.screen.get_size())}
    

    def callOnAllMenus(self, action):
        for menu in self.menus.values():
            action(menu)

    def callOnActiveMenu(self, action):
        action(self.menus[self.active_menu])
    
    def handleEvent(self, event):
        if event.type == events.RETURN_TO_MAIN_MENU:
            self.active_menu = "main"
            
        if event.type == events.OPEN_SETTINGS:
            self.active_menu = "settings"
            
        if event.type == pygame.MOUSEMOTION:
            self.callOnActiveMenu(lambda menu: menu.onMouseMotion(self.screen.translatePointFromScreen(event.pos)))
            #self.main_menu.onMouseMotion(self.screen.translatePointFromScreen(event.pos))

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.callOnActiveMenu(lambda menu: menu.onMouseDown(self.screen.translatePointFromScreen(event.pos), event.button))
            #self.main_menu.onMouseDown(self.screen.translatePointFromScreen(event.pos), event.button)

        if event.type == pygame.MOUSEBUTTONUP:
            self.callOnActiveMenu(lambda menu: menu.onMouseUp(self.screen.translatePointFromScreen(event.pos), event.button))
            #self.main_menu.onMouseUp(self.screen.translatePointFromScreen(event.pos), event.button)

    def draw(self, surface):
        self.menus[self.active_menu].draw(self.screen.get())

    def tick(self):
        pass
