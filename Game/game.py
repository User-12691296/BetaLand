import pygame
import numpy as np
import os
import json
from fractions import Fraction

import events
from textures import TextureAtlas
from gameitems import initialiseItems, Item, ItemStack, Inventory
from gameentities import initialiseEntities, Entity, Creature, Player, TestCreature

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
    
TILE_SIZE = 64

class Quadrant:
    north = 0
    east = 1
    south = 2
    west = 3
    def __init__(self, cardinal, origin):
        self.cardinal = cardinal
        self.ox, self.oy = origin

    def transform(self, tile):
        row, col = tile
        if self.cardinal == self.north:
            return (self.ox + col, self.oy - row)

        if self.cardinal == self.south:
            return (self.ox - col, self.oy + row)

        if self.cardinal == self.east:
            return (self.ox + row, self.oy + col)

        if self.cardinal == self.west:
            return (self.ox - row, self.oy - col)

    @staticmethod
    def slope(tile):
        row_depth, col = tile
        return Fraction(2 * col - 1, 2 * row_depth)

    @staticmethod
    def is_symmetric(row, tile):
        row_depth, col = tile
        return (col >= row.depth * row.start_slope
                and col <= row.depth * row.end_slope)

    @staticmethod
    def round_ties_up(n):
        return int(n+0.5)

    @staticmethod
    def round_ties_down(n):
        return int(-((n-0.5)//-1))

class Row:
    def __init__(self, depth, start_slope, end_slope):
        self.depth = depth
        self.start_slope = start_slope
        self.end_slope = end_slope

    def tiles(self):
        min_col = Quadrant.round_ties_up(self.depth * self.start_slope)
        max_col = Quadrant.round_ties_down(self.depth * self.end_slope)

        for col in range(min_col-1, max_col + 1):
            yield (self.depth, col)


    def next(self):
        return Row(
            self.depth + 1,
            self.start_slope,
            self.end_slope)

class Map:
    MAX_BUFFER_SIZE = (2048, 2048)
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS, "tiles")
        SIZE    = TILE_SIZE
        EXT     = ".png"
        RESCALE = True
        
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.total_size = (map_size[0]*tile_size[0], map_size[1]*tile_size[1])
        self.createBlankBuffers()
        self.initFOV()

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)
        self.default_tile = self.tileAtlas.default
        
    def initFOV(self):
        self.shown_tiles = np.empty((self.map_size[1], self.map_size[0]), dtype="bool")

    def getTileVisibility(self, tile):
        return self.shown_tiles[tile[1]][tile[0]]
    
    def hideTile(self, tile):
        self.shown_tiles[tile[1]][tile[0]] = False

    def hideAllTiles(self):
        self.shown_tiles.fill(False)

    def showTile(self, tile):
        self.shown_tiles[tile[1]][tile[0]] = True

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
                            for x in range(left_bound, right_bound+1)
                            for y in range(top_bound, bottom_bound+1)]

        
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
        if self.getTileVisibility(tile_pos):
            tile = self.world.getTile(tile_pos)

            self.blit(tile.getDrawable(), self.world.tilePosToBufferPos(tile_pos))

        else:
            self.blit(self.default_tile, self.world.tilePosToBufferPos(tile_pos))

    def regenMap(self):
        for i in range(self.world.getHeight()): #y
            for j in range(self.world.getWidth()): #x
                self.regenTile((j, i))

    def calcFOV(self, origin):
        self.hideAllTiles()

        for i in range(4):
            quadrant = Quadrant(i, origin)

            def isTileOutOfBounds(tile):
                x, y = quadrant.transform(tile)

                if (origin[0]-x)**2 + (origin[1]-y)**2 > 100:
                    return True
                
                if x < 0 or x >= self.map_size[0]:
                    return True
                if y < 0 or y >= self.map_size[1]:
                    return True
                
                return False
            def reveal(tile):
                x, y = quadrant.transform(tile)
                self.showTile((x, y))


            def is_wall(tile):
                if tile is None:
                    return False

                x, y = quadrant.transform(tile)
                return self.world.isTileOpaque((x, y))


            def is_floor(tile):
                if tile is None:
                    return False

                x, y = quadrant.transform(tile)
                return not self.world.isTileOpaque((x, y))

            def scan(row):
                prev_tile = None
                
                for tile in row.tiles():
                    if isTileOutOfBounds(tile):
                        continue
                    
                    if is_wall(tile) or Quadrant.is_symmetric(row, tile):
                        reveal(tile)

                    if is_wall(prev_tile) and is_floor(tile):
                        row.start_slope = Quadrant.slope(tile)

                    if is_floor(prev_tile) and is_wall(tile):
                        next_row = row.next()
                        next_row.end_slope = Quadrant.slope(tile)
                        scan(next_row)

                    prev_tile = tile

                if is_floor(prev_tile):
                    scan(row.next())

                return

            first_row = Row(1, Fraction(-1), Fraction(1))
            scan(first_row)

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

    TILE_SIZE = (TILE_SIZE, TILE_SIZE)
    
    def __init__(self):
        self.size = (0, 0)
        
        self.loadWorld()

        self.map = Map(self.size, self.TILE_SIZE)
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
        with open("levels.json") as levels_file:
            world = self.__dict__.get("world_name", DEFAULT_WORLD)
            self.loadWorldFromFile(levels_file, world)

    def loadWorldFromFile(self, file, world_name):
        all_worlds = json.load(file)
        world_info = all_worlds[world_name]
        
        self.size = world_info["size"]

        self.loadWorldDataFromDict(world_info['tiles'])

    @staticmethod
    def splitRowDataIntoTileData(row_data, row_length):
        return row_data.split(";")[:row_length]

    @staticmethod
    def splitTileDataIntoTileInfo(tile_data):
        return tile_data.split(",")

    def loadWorldDataFromDict(self, rows):
        self.world_tile_ids = np.empty((self.size[1], self.size[0]), dtype="<U16")
        self.world_tile_elevations = np.empty((self.size[1], self.size[0]), dtype=np.int16)
        default_row = "grass,0;"*self.size[0]
        
        for row_index in range(self.size[1]):
            row_name = str(row_index)

            row_data = rows.get(row_name, default_row)

            tile_data_in_row = self.splitRowDataIntoTileData(row_data, self.size[0])

            for tile_index, tile_data in enumerate(tile_data_in_row):
                tileid, elevation = self.splitTileDataIntoTileInfo(tile_data)
                
                self.world_tile_ids[row_index][tile_index] = tileid
                self.world_tile_elevations[row_index][tile_index] = int(elevation)
                
        
    def setPlayer(self, player):
        self.player = player

    def getPlayer(self):
        return self.player

    def getTileID(self, tile_pos):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        try:
            return self.world_tile_ids[tile_pos[1]][tile_pos[0]]
        except IndexError:
            return None

    def getTile(self, tile_pos):
        tileid = self.getTileID(tile_pos)
        if tileid != None:
            return self.tiles[tileid]

    def getTileElevation(self, tile_pos):
        return self.world_tile_elevations[tile_pos[1]][tile_pos[0]]

    def isTileOpaque(self, tile_pos):
        return self.getTileID(tile_pos)=="barrier"

    def isTileValidForWalking(self, tile_pos):
        return not self.isTileOpaque(tile_pos)

    def getTileRect(self, tile_pos):
        rect = pygame.Rect(self.tilePosToBufferPos(tile_pos),
                           self.TILE_SIZE)

        return rect

    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def setTileID(self, tile_pos, tile_id):
        if (tile_pos[0] < 0 or tile_pos[1] < 0):
            return None
        
        if not tile_id in self.tiles.keys():
            return None

        try:
            self.world_tile_ids[tile_pos[1]][tile_pos[0]] = tile_id
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

        self.map.calcFOV((int(self.getPlayer().pos[0]), int(self.getPlayer().pos[1])))
        
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
        self.map.regenMap()
        self.map.draw(surface, visible_rect)
        
        visible_world = pygame.Surface(visible_rect.size, pygame.SRCALPHA)

        for entity in self.entities:
            entity.draw(visible_world)

        surface.blit(visible_world, visible_rect.topleft)

class Overworld(World):
    world_name = "overworld"
    
    def __init__(self):
        self.world_name = "overworld"

        super().__init__()

class Level1(World):
    world_name = "level_1"
    
    def __init__(self):
        self.world_name = "level_1"
        
        super().__init__()

LOADABLE_WORLDS = (Overworld, Level1)
