import pygame
import numpy as np
import os
import json

from .world import LOADABLE_WORLDS
from misc import events
from .items import initialiseItems
from .entities import initialiseEntities, Entity, Creature, Player, TestCreature

ASSETS = os.path.join("assets", "game")

DEFAULT_WORLD = "overworld"

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        initialiseItems()
        initialiseEntities()
        
        self.loadBgs()
        self.loadWorlds()
        self.loadPlayer()
        self.finaliseWorlds()

    def loadWorlds(self):
        self.worlds = {}
        for world in LOADABLE_WORLDS:
            self.worlds[world.world_name] = world()
        
        self.active_world = DEFAULT_WORLD

    def loadBgs(self):
        self.bg = pygame.Surface(self.screen_size)
        self.bg.fill((0, 0, 0))

    def loadPlayer(self):
        self.player = Player()
        self.player.setManager(self)
        self.player.setWorld(self.getWorld())

    def finaliseWorlds(self):
        for world in self.worlds.values():
            world.setPlayer(self.player)

    def getWorld(self):
        return self.worlds[self.active_world]

    def changeWorld(self, world_name):
        self.active_world = world_name
        self.player.setWorld(self.getWorld())

    ## HELPER
    def getScreenBufferDelta(self):
        player_delta = self.player.getMapDelta()
        center_delta = (self.screen_size[0]//2, self.screen_size[1]//2)
        return (player_delta[0]+center_delta[0], player_delta[1]+center_delta[1])
    
    def screenPosToBufferPos(self, spos):
        delta = self.getScreenBufferDelta()
        return (spos[0]-delta[0], spos[1]-delta[1])

    def bufferPosToScreenPos(self, bpos):
        delta = self.getScreenBufferDelta()
        return (bpos[0]+delta[0], bpos[1]+delta[1])

    ## TICK
    def tick(self):
        self.player.tick()
        self.getWorld().tick()
    
    ## EVENTS
    def start(self):
        self.player.health = self.player.max_health
        print("Game starting!")

    def onKeyDown(self, key, unicode, mod):
        if key == pygame.K_SPACE:
            self.changeWorld("level_1")
            return
        
        self.player.onKeyDown(key, unicode, mod)
        self.getWorld().onKeyDown(key, unicode, mod)

    def onKeyUp(self, key, unicode, mod):
        self.player.onKeyUp(key, unicode, mod)
        self.getWorld().onKeyUp(key, unicode, mod)
        
    def onMouseDown(self, spos, button):        
        used = self.player.onMouseDown(spos, button)
        if not used:
            bpos = self.screenPosToBufferPos(spos)
            self.getWorld().onMouseDown(bpos, button)

    def close(self):
        self.player.worldClosed()
    
    ## DRAW
    def draw(self, surface):
        self.drawBg(surface)
        self.drawWorld(surface)
        self.drawPlayer(surface)

    def drawBg(self, surface):
        surface.blit(self.bg, (0, 0))

    def drawWorld(self, surface):
        viewing_rect = pygame.Rect(self.getScreenBufferDelta(), self.screen_size)
        self.getWorld().draw(surface, viewing_rect)

    def drawPlayer(self, surface):
        self.player.draw(surface)
