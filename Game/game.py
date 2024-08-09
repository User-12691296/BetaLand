import pygame
import numpy as np
import os

import events
from textures import TextureAtlas
from gameitems import initialiseItems, Item, ItemStack, Inventory
from gameentities import initialiseEntities, Entity, Creature, Player, TestCreature

ASSETS = os.path.join("assets", "game")

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        initialiseItems()
        initialiseEntities()
        
        self.loadBgs()
        self.loadWorld()
        self.loadPlayer()
        self.finaliseWorld()

    def loadWorld(self):
        self.world = World()

    def loadBgs(self):
        self.bg = pygame.Surface(self.screen_size)
        self.bg.fill((0, 0, 0))

    def loadPlayer(self):
        self.player = Player()
        self.player.setManager(self)
        self.player.setWorld(self.world)

    def finaliseWorld(self):
        self.world.setPlayer(self.player)

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
        self.world.tick()
        self.player.tick()
    
    ## EVENTS
    def start(self):
        self.player.health = self.player.max_health
        print("Game starting!")

    def onKeyDown(self, key, unicode, mod):
        self.player.onKeyDown(key, unicode, mod)
        self.world.onKeyDown(key, unicode, mod)

    def onKeyUp(self, key, unicode, mod):
        self.player.onKeyUp(key, unicode, mod)
        self.world.onKeyUp(key, unicode, mod)
        
    def onMouseDown(self, spos, button):        
        used = self.player.onMouseDown(spos, button)
        if not used:
            bpos = self.screenPosToBufferPos(spos)
            self.world.onMouseDown(bpos, button)

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
        self.world.draw(surface, viewing_rect)

    def drawPlayer(self, surface):
        self.player.draw(surface)


class BasicTile:
    def __init__(self, tileid, tex_name):
        self.tileid = tileid
        self.tex_name = tex_name

        self._atlas_given = False

    def addTileToList(self, tile_list):
        tile_list.append(self)

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

    def getDrawable(self):
        if self._atlas_given:
            return self.atlas.getTextureAtLoc(self.tex_loc)

        else:
            return pygame.Surface((1, 1))

class GrassTile(BasicTile):
    def __init__(self):
        super().__init__("grass", "grass")

    def onLeft(self, world, tile_pos):
        world.setTileID(tile_pos, "barrier")

class BarrierTile(BasicTile):
    def __init__(self):
        super().__init__("barrier", "barrier")

    def onLeft(self, world, tile_pos):
        player = world.getPlayer()

        player.damage(0.5)

    def onRight(self, world, tile_pos):
        world.setTileID(tile_pos, "grass")

OVERWORLD_TILES = []
GrassTile().addTileToList(OVERWORLD_TILES)
BarrierTile().addTileToList(OVERWORLD_TILES)
BasicTile("gremlin",
          "barrier").addTileToList(OVERWORLD_TILES)
    
TILE_SIZE = 128

class Map:
    MAX_BUFFER_SIZE = (2048, 2048)
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS, "tiles")
        SIZE    = TILE_SIZE
        EXT     = ".png"
        RESCALE = True
        
    def __init__(self, map_size):
        self.total_size = map_size
        self.createBlankBuffers()

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)

    def createBlankBuffers(self):
        self.buffers = []

        max_buffers_x_axis = self.total_size[0]//self.MAX_BUFFER_SIZE[0]
        max_buffers_y_axis = self.total_size[1]//self.MAX_BUFFER_SIZE[1]
        self.MAX_BUFFERS = [max_buffers_x_axis, max_buffers_y_axis]

        right_edge_buffer_width = self.total_size[0]%self.MAX_BUFFER_SIZE[0]
        bottom_edge_buffer_height = self.total_size[1]%self.MAX_BUFFER_SIZE[1]

        for y_buf_index in range(max_buffers_y_axis):
            # All buffers in current row
            row = []
            
            for x_buf_index in range(max_buffers_x_axis):
                buf = pygame.Surface(self.MAX_BUFFER_SIZE)
                row.append(buf)
                
            if right_edge_buffer_width > 0:
                buf = pygame.Surface((right_edge_buffer_width, self.MAX_BUFFER_SIZE[1]))
                row.append(buf)

            self.buffers.append(row)

        if bottom_edge_buffer_height > 0:
            row = []

            for x_buf_index in range(max_buffers_x_axis):
                buf = pygame.Surface((self.MAX_BUFFER_SIZE[0], bottom_edge_buffer_height))
                row.append(buf)

            if right_edge_buffer_width > 0:
                buf = pygame.Surface((right_edge_buffer_width, bottom_edge_buffer_height))
                row.append(buf)

            self.buffers.append(row)

    def getBufferAtLoc(self, buffer_loc):
        try:
            return self.buffers[buffer_loc[1]][buffer_loc[0]]
        except IndexError:
            print("Bad Buffer indexed:", buffer_loc)
            return None

    def bufferLocToVirtualPos(self, buffer_loc):
        return (self.MAX_BUFFER_SIZE[0]*buffer_loc[0],
                self.MAX_BUFFER_SIZE[1]*buffer_loc[1])

    def getRelevantBuffers(self, rect):
        # Keep errant inputs within bounds
        clamp = lambda x, mn, mx: mn if x < mn else mx if x > mx else x
        
        left_bound = clamp(rect.left//self.MAX_BUFFER_SIZE[0], 0, self.MAX_BUFFERS[0])
        right_bound = clamp(-(rect.right//-self.MAX_BUFFER_SIZE[0]), 0, self.MAX_BUFFERS[0]) # Ceil div
        top_bound = clamp(rect.top//self.MAX_BUFFER_SIZE[1], 0, self.MAX_BUFFERS[1])
        bottom_bound = clamp(-(rect.bottom//-self.MAX_BUFFER_SIZE[1]), 0, self.MAX_BUFFERS[1])

        relevant_buffers = [(x, y)
                            for x in range(left_bound, right_bound)
                            for y in range(top_bound, bottom_bound)]

        return relevant_buffers

    def blit(self, source, dest):
        rect = source.get_rect()
        rect.topleft = dest

        relevant_buffers = self.getRelevantBuffers(rect)

        for buffer_loc in relevant_buffers:
            delta = self.bufferLocToVirtualPos(buffer_loc)

            buffer = self.getBufferAtLoc(buffer_loc)

            buffer.blit(source, (dest[0]-delta[0], dest[1]-delta[1]))
        
    def setWorld(self, world):
        self.world = world

    def getMap(self):
        return self.buffer

    def bindTileAtlas(self, tile_class):
        tile_class.setAtlas(self.tileAtlas)

    def regenTile(self, tile_pos):
        tile = self.world.getTile(tile_pos)

        self.blit(tile.getDrawable(), self.world.tilePosToBufferPos(tile_pos))

    def regenMap(self):
        for i in range(self.world.getHeight()): #y
            for j in range(self.world.getWidth()): #x
                self.regenTile((j, i))

    def draw(self, surface, visible_rect):
        relevant_buffers = self.getRelevantBuffers(pygame.Rect((-visible_rect.left, -visible_rect.top),
                                                               visible_rect.size))
        
        for buffer_loc in relevant_buffers:
            v_pos = self.bufferLocToVirtualPos(buffer_loc)

            buffer = self.getBufferAtLoc(buffer_loc)

            if buffer != None:
                surface.blit(self.getBufferAtLoc(buffer_loc),
                                 (visible_rect.left+v_pos[0], visible_rect.top+v_pos[1]))
            

class World(events.EventAcceptor):
    ALL_TILES = OVERWORLD_TILES

    WORLD_SIZE = (100, 100)

    TILE_SIZE = (TILE_SIZE, TILE_SIZE)
    
    def __init__(self):
        self.loadWorld()

        self.map = Map((self.WORLD_SIZE[0]*self.TILE_SIZE[0], self.WORLD_SIZE[1]*self.TILE_SIZE[1]))
        self.map.setWorld(self)

        self.tiles = {}
        for tileClass in self.ALL_TILES:
            self.map.bindTileAtlas(tileClass)
            self.tiles[tileClass.getTileID()] = tileClass

        self.map.regenMap()

        self.entities = []

        self.addEntity(TestCreature())
        self.entities[0].setPos((2, 3))

    def loadWorld(self):
        self.world_data = np.array(["grass", "grass"]*5000, dtype='<U16').reshape((100, 100))

    def setPlayer(self, player):
        self.player = player

    def getPlayer(self):
        return self.player

    def getTileID(self, tile_pos):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        try:
            return self.world_data[tile_pos[1]][tile_pos[0]]
        except IndexError:
            return None

    def getTile(self, tile_pos):
        tileid = self.getTileID(tile_pos)
        if tileid != None:
            return self.tiles[tileid]

    def getTileRect(self, tile_pos):
        rect = pygame.Rect(self.tilePosToBufferPos(tile_pos),
                           self.TILE_SIZE)

        return rect

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

    def addEntity(self, entity):
        self.entities.append(entity)
        entity.setWorld(self)

    def removeEntity(self, entity):
        self.entities.remove(entity)

    def tick(self):
        for entity in self.entities:
            entity.tick()
        
    def onMouseDown(self, mouse_pos, button):
        world_pos = self.bufferPosToWorldPos(mouse_pos)

        clicked_tile = self.getTile(world_pos)

        if clicked_tile != None:
            if button == pygame.BUTTON_LEFT:
                clicked_tile.onLeft(self, world_pos)

            elif button == pygame.BUTTON_RIGHT:
                clicked_tile.onRight(self, world_pos)

    def bufferPosToWorldPos(self, bpos):
        return (int(bpos[0]//self.TILE_SIZE[0]), int(bpos[1]//self.TILE_SIZE[1]))
    
    def tilePosToBufferPos(self, wpos):
        return (wpos[0]*self.TILE_SIZE[0], wpos[1]*self.TILE_SIZE[1])

    def draw(self, surface, visible_rect):
        visible_world = pygame.Surface(visible_rect.size, pygame.SRCALPHA)

        for entity in self.entities:
            entity.draw(visible_world)

        surface.blit(visible_world, visible_rect.topleft)

        self.map.draw(surface, visible_rect)
