import pygame
import numpy as np
import os

import events
from textures import TextureAtlas

TILE_SIZE = 32
ASSETS = os.path.join("assets", "game")

class TEXTURES:
    TILES = ["barrier",
             "grass"]

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size
        
        self.loadBgs()
        self.loadWorld()

        self.player_pos = [0, 0]

    def loadWorld(self):
        self.world = World()

    def loadBgs(self):
        self.bg = pygame.Surface(self.screen_size)
        self.bg.fill((0, 0, 0))

    ## TICK
    def tick(self):
        self.handlePlayerMotion()

    def handlePlayerMotion(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.player_pos[1] -= 1
        if pressed[pygame.K_a]:
            self.player_pos[0] -= 1
        if pressed[pygame.K_s]:
            self.player_pos[1] += 1
        if pressed[pygame.K_d]:
            self.player_pos[0] += 1
    
    ## EVENTS
    def start(self):
        print("Game starting!")
        
    def onKeyDown(self, key, mod, unicode):
        pass

    def close(self):
        print("Game closing!")
    
    ## DRAW
    def draw(self, surface):
        self.drawBg(surface)
        self.drawWorld(surface)

    def drawBg(self, surface):
        surface.blit(self.bg, (0, 0))

    def drawWorld(self, surface):
        delta = [-coord for coord in self.player_pos]
        self.world.draw(surface, delta)
        
class World:
    def __init__(self):
        self.loadWorld()

        self.buffer = pygame.Surface((self.world_data.shape[0]*TILE_SIZE,
                                      self.world_data.shape[1]*TILE_SIZE))

        self.tileAtlas = TextureAtlas(os.path.join(ASSETS, "tiles"), ".png", (32, 32), TEXTURES.TILES)

        self.drawMapToBuffer()

    def loadWorld(self):
        self.world_data = np.array(np.random.random_sample(10000).reshape((100, 100))*2, dtype=np.int16)

    def drawMapToBuffer(self):
        for i in range(self.world_data.shape[0]): #y
            for j in range(self.world_data.shape[1]): #x
                self.tileAtlas.drawTextureAtLoc(self.buffer, (j*TILE_SIZE, i*TILE_SIZE), self.world_data[i][j])

    def draw(self, surface, delta):
        surface.blit(self.buffer, delta)
