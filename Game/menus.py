import pygame
import events

ASSETS = "assets\\menus\\"

class MainMenuOption:
    def __init__(self, name, center):
        self.name = name

        self.rect = pygame.Rect(0, 0, 300, 100)
        self.rect.center = center

        self.hovered = False
        self.pressed = False
        
        self.font = pygame.font.SysFont("Times New Roman", 80)
        self.hovered_font = pygame.font.SysFont("Times New Roman", 100)

    def action(self):
        print(self.name)

    def checkHover(self, point):
        if self.rect.collidepoint(point):
            self.hovered = True
        else:
            self.hovered = False
            self.pressed = False

    def pressEvent(self, point):
        if self.rect.collidepoint(point):
            self.pressed = True

    def releaseEvent(self, point):
        if self.rect.collidepoint(point) and self.pressed:
            self.pressed = False
            self.action()

    def draw(self, surface):
        if not self.hovered:
            option_text = self.font.render(self.name, True, (175, 105, 239))
        else:
            if not self.pressed:
                option_text = self.hovered_font.render(self.name, True, (155, 95, 209))
            else:
                option_text = self.hovered_font.render(self.name, True, (80, 50, 100))
        surface.blit(option_text, (self.rect.centerx-option_text.get_rect().centerx, self.rect.centery-option_text.get_rect().centery))

class MainMenu(events.EventAcceptor):
    def __init__(self, screen_size):
        bg = pygame.image.load(ASSETS+"main-menu-bg.png")
        self.bg = pygame.transform.scale(bg, screen_size)
        
        self.fonts = {}

        self.fonts["title"] = pygame.font.SysFont("Times New Roman", 300)


        self.options = {}
        option_names = ("Play", "Settings", "Exit")

        y = 400 + 200
        
        for option_name in option_names:
            self.options[option_name] = MainMenuOption(option_name, (550, y))
            y += 120

    def onMouseDown(self, pos, button):
        if button == pygame.BUTTON_LEFT:
            for option in self.options.values():
                option.pressEvent(pos)

    def onMouseUp(self, pos, button):
        if button == pygame.BUTTON_LEFT:
            for option in self.options.values():
                option.releaseEvent(pos)
    
    def onMouseMotion(self, pos):
        for option in self.options.values():
            option.checkHover(pos)

    def draw(self, surface):
        # Background
        surface.blit(self.bg, (surface.get_rect().centerx-self.bg.get_rect().centerx, 0))

        # Title
        title_text = self.fonts["title"].render("Magiland", True, (0, 0, 0))
        surface.blit(title_text, (1200, 750))

        # Options
        for option in self.options.values():
            option.draw(surface)
