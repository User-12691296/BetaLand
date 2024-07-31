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
        self.loadPlayer()

    def loadWorld(self):
        self.world = World()

    def loadBgs(self):
        self.bg = pygame.Surface(self.screen_size)
        self.bg.fill((0, 0, 0))

    def loadPlayer(self):
        self.player = Player(self, self.world)

    ## HELPER
    def getScreenBufferDelta(self):
        player_delta = self.player.getScreenDelta()
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
        self.world.tick()
        self.player.tick()
    
    ## EVENTS
    def start(self):
        print("Game starting!")

    def onKeyDown(self, key, unicode, mod):
        self.world.onKeyDown(key, unicode, mod)
        self.player.onKeyDown(key, unicode, mod)

    def onKeyUp(self, key, unicode, mod):
        self.world.onKeyUp(key, unicode, mod)
        self.player.onKeyUp(key, unicode, mod)
        
    def onMouseDown(self, spos, button):
        bpos = self.screenPosToBufferPos(spos)
        self.world.onMouseDown(bpos, button)
        self.player.onMouseDown(bpos, button)

    def close(self):
        print("Game closing!")
    
    ## DRAW
    def draw(self, surface):
        self.drawBg(surface)
        self.drawWorld(surface)
        self.drawPlayer(surface)

    def drawBg(self, surface):
        surface.blit(self.bg, (0, 0))

    def drawWorld(self, surface):
        self.world.draw(surface, self.getScreenBufferDelta())

    def drawPlayer(self, surface):
        self.player.draw(surface)


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
    
TILE_SIZE = 32

class Map:
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS, "tiles")
        SIZE    = TILE_SIZE
        EXT     = ".png"
        
    def __init__(self, world):
        self.world = world
        
        self.buffer = pygame.Surface((3200, 3200))

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)

    def getMap(self):
        return self.buffer

    def bindTileAtlas(self, tile_class):
        tile_class.setAtlas(self.tileAtlas)

    def regenTile(self, tile_pos):
        tile = self.world.getTile(tile_pos)
        tile.draw(self.buffer, self.world.worldPosToBufferPos(tile_pos))

    def regenMap(self):
        for i in range(self.world.getHeight()): #y
            for j in range(self.world.getWidth()): #x
                self.regenTile((j, i))


class World(events.EventAcceptor):
    ALL_TILES = OVERWORLD_TILES

    WORLD_SIZE = (100, 100)

    TILE_SIZE = (TILE_SIZE, TILE_SIZE)
    
    def __init__(self):
        self.loadWorld()

        self.map = Map(self)

        self.tiles = {}
        for tileClass in self.ALL_TILES:
            self.map.bindTileAtlas(tileClass)
            self.tiles[tileClass.getTileID()] = tileClass

        self.map.regenMap()

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

    def getWidth(self):
        return self.WORLD_SIZE[0]

    def getHeight(self):
        return self.WORLD_SIZE[1]

    def setTileID(self, tile_pos, tile_id):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        if not tile_id in self.tiles.keys():
            return None

        try:
            self.world_data[tile_pos[1]][tile_pos[0]] = tile_id
            self.map.regenTile(tile_pos)
        except IndexError:
            return None

    def tick(self):
        pass
        
    def onMouseDown(self, mouse_pos, button):
        world_pos = self.bufferPosToWorldPos(mouse_pos)

        if button == pygame.BUTTON_LEFT:
            self.getTile(world_pos).onLeft(self, world_pos)

        elif button == pygame.BUTTON_RIGHT:
            self.getTile(world_pos).onRight(self, world_pos)

    def bufferPosToWorldPos(self, bpos):
        return (bpos[0]//self.TILE_SIZE[0], bpos[1]//self.TILE_SIZE[1])
    
    def worldPosToBufferPos(self, wpos):
        return (wpos[0]*self.TILE_SIZE[0], wpos[1]*self.TILE_SIZE[1])

    def draw(self, surface, delta):
        map_ = self.map.getMap()
        surface.blit(map_, delta)


class Player(events.EventAcceptor):
    def __init__(self, manager, world):
        self.manager = manager
        
        self.world = world
        
        self.pos = [100, 0]

    def tick(self):
        self.handleMotion()

    def handleMotion(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.pos[1] -= 1
        if pressed[pygame.K_a]:
            self.pos[0] -= 1
        if pressed[pygame.K_s]:
            self.pos[1] += 1
        if pressed[pygame.K_d]:
            self.pos[0] += 1
            
    def getScreenDelta(self):
        return (-self.pos[0], -self.pos[1])

    def draw(self, surface):
        pos = self.manager.bufferPosToScreenPos(self.pos)
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(pos, (80, 120)))
