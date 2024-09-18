import pygame
import os
import json

from .world import LOADABLE_WORLDS
from misc import events
from .items import initialiseItems
from .entities import initialiseEntities, ENTITY_CLASSES
from .projectiles import initialiseProjectiles, PROJECTILE_CLASSES

ASSETS = os.path.join("assets", "game")

DEFAULT_WORLD = "overworld"
# world_set = [["overworld", [1,1]], ["level_1", [1,1]], ["crystal_level", [10,50]], ["deep_dark_level", [125,15]], ["maze_level", [1,1]], ["level_3", [1,1]]]
world_set = [["overworld", [1,1]], ["level_1", [1,1]], ["crystal_level", [10,50]], ["deep_dark_level", [125,15]], ["level_3", [100,10]]]
world_counter = 0 # 0 is overworld, 1 is level_1, 2 is crystal_level, 3 is deep_dark_level, 4 is maze_level, 5 is level_3

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        initialiseItems(ENTITY_CLASSES.ItemEntity)
        initialiseEntities()
        initialiseProjectiles()
        
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
        self.player = ENTITY_CLASSES.Player()
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
    def first_tick(self):
        self.player.tick()
        self.getWorld().tick()
    
    def main_tick(self):
        self.player.movementTick()
        self.getWorld().movementTick()

        self.player.damageTick()
        self.getWorld().damageTick()

        self.player.finalTick()
        self.getWorld().finalTick()
    
    ## EVENTS
    def start(self):
        print("Game starting!")
        self.player.setAttribute("health", self.player.getAttribute("max_health"))
        self.player.alive = True
        self.first_tick()

    def onKeyDown(self, key, unicode, mod):
        global world_set, world_counter

        if key == pygame.K_SPACE:
            world_set[world_counter].pop(1)
            world_set[world_counter].append(self.player.getPos())

            world_counter += 1  
            self.changeWorld(world_set[world_counter][0])
            self.player.setPos(world_set[world_counter][1])
            
            if world_counter == len(world_set)-1:
                world_counter = -1 # Reset the counter

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

    def onMouseUp(self, spos, button):        
        used = self.player.onMouseUp(spos, button)
        if not used:
            bpos = self.screenPosToBufferPos(spos)
            self.getWorld().onMouseUp(bpos, button)

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
