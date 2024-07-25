import pygame
import numpy as np
import os

import events
from textures import TextureAtlas

ASSETS = os.path.join("assets", "game")

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
        
    def onMouseDown(self, pos, button):
        adj_pos = [p+d for p, d in zip(pos, self.player_pos)]
        self.world.onMouseDown(adj_pos, button)

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


class BasicTile:
    def __init__(self, tileid, tex_name, tile_list):
        self.tileid = tileid
        self.tex_name = tex_name

        tile_list.append(self)

        self._atlas_given = False

    def setAtlas(self, atlas):
        self.atlas = atlas

        self.tex_loc = self.atlas.getTextureLoc(self.tex_name)

        self._atlas_given = True

    def getTileID(self):
        return self.tileid

    def onLeft(self, world, tile_pos): pass
    def onRight(self, world, tile_pos): pass
    def onWalk(self, world, tile_pos): pass

    def draw(self, surface, pos):
        if self._atlas_given:
            self.atlas.drawTextureAtLoc(surface, pos, self.tex_loc)

class GrassTile(BasicTile):
    def __init__(self, tile_list):
        super().__init__("grass", "grass", tile_list)

    def onLeft(self, world, tile_pos):
        world.setTileID(tile_pos, "barrier")

class BarrierTile(BasicTile):
    def __init__(self, tile_list):
        super().__init__("barrier", "barrier", tile_list)

    def onRight(self, world, tile_pos):
        world.setTileID(tile_pos, "grass")

OVERWORLD_TILES = []
GrassTile(OVERWORLD_TILES)
BarrierTile(OVERWORLD_TILES)
BasicTile("gremlin",
          "barrier",
          OVERWORLD_TILES)
    
        
class World(events.EventAcceptor):
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS, "tiles")
        SIZE    = 32
        EXT     = ".png"

    ALL_TILES = OVERWORLD_TILES

    
    def __init__(self):
        self.loadWorld()

        self.buffer = pygame.Surface((3200, 3200))

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)

        self.tiles = {}
        for tileClass in self.ALL_TILES:
            tileClass.setAtlas(self.tileAtlas)
            self.tiles[tileClass.getTileID()] = tileClass

        self.updateMapToBuffer()

    def loadWorld(self):
        self.world_data = np.array(["grass", "grass"]*5000, dtype='<U16').reshape((100, 100))

    def getTileID(self, tile_pos):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        try:
            return self.world_data[tile_pos[1]][tile_pos[0]]
        except IndexError:
            return None

    def getTile(self, tile_pos):
        return self.tiles[self.getTileID(tile_pos)]

    def setTileID(self, tile_pos, tile_id):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        if not tile_id in self.tiles.keys():
            return None

        try:
            self.world_data[tile_pos[1]][tile_pos[0]] = tile_id
            self.updateTileToBuffer(tile_pos)
        except IndexError:
            return None
        
    def onMouseDown(self, pos, button):
        tile_size = self.tileAtlas.getTextureSize()
        tile_pos = (*(p//t for p, t in zip(pos, tile_size)),)

        if button == pygame.BUTTON_LEFT:
            self.getTile(tile_pos).onLeft(self, tile_pos)

        elif button == pygame.BUTTON_RIGHT:
            self.getTile(tile_pos).onRight(self, tile_pos)

    def updateTileToBuffer(self, tile_pos):
        tileid = self.world_data[tile_pos[1]][tile_pos[0]]
        self.tiles[tileid].draw(self.buffer, (tile_pos[0]*self.tileAtlas.getTextureWidth(), tile_pos[1]*self.tileAtlas.getTextureHeight()))
        
    def updateMapToBuffer(self):
        for i in range(self.world_data.shape[0]): #y
            for j in range(self.world_data.shape[1]): #x
                self.updateTileToBuffer((j, i))

    def draw(self, surface, delta):
        surface.blit(self.buffer, delta)
