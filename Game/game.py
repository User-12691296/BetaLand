import pygame
import numpy as np
import os

import events
from textures import TextureAtlas
from gameitems import initialiseItems, Item, ItemStack, Inventory

ASSETS = os.path.join("assets", "game")

class GameManager(events.Alpha):
    def __init__(self, screen_size):
        self.screen_size = screen_size

        initialiseItems()
        
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
        self.world.draw(surface, self.getScreenBufferDelta())

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
    
TILE_SIZE = 32

class Map:
    class MAP_TILES_TEXTURE_PRESETS:
        FOLDER  = os.path.join(ASSETS, "tiles")
        SIZE    = TILE_SIZE
        EXT     = ".png"
        
    def __init__(self):        
        self.buffer = pygame.Surface((3200, 3200))

        self.tileAtlas = TextureAtlas.fromPreset(self.MAP_TILES_TEXTURE_PRESETS)

    def setWorld(self, world):
        self.world = world

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

        self.map = Map()
        self.map.setWorld(self)

        self.tiles = {}
        for tileClass in self.ALL_TILES:
            self.map.bindTileAtlas(tileClass)
            self.tiles[tileClass.getTileID()] = tileClass

        self.map.regenMap()

        self.entities = []

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
    
    def worldPosToBufferPos(self, wpos):
        return (wpos[0]*self.TILE_SIZE[0], wpos[1]*self.TILE_SIZE[1])

    def draw(self, surface, delta):
        map_ = self.map.getMap()
        surface.blit(map_, delta)


class Entity(events.EventAcceptor):
    def __init__(self):
        self.pos = [0, 0]

    def setWorld(self, world):
        self.world = world

    def setPos(self, pos):
        self.pos = pos

    def kill(self):
        self.world.removeEntity(self)

    def getBufferPos(self):
        return self.world.worldPosToBufferPos(self.pos)

    def tick(self): pass
    def draw(self, surface): pass

class Creature(Entity):
    def __init__(self, health):
        super().__init__()
        
        self.max_health = health
        self.health = health

    def changeHealth(self, delta):
        self.health += delta

    def calcDamageModifiers(self, damage):
        return damage # No changes to damage, can be overridden for entities with armor

    def damage(self, damage):
        self.true_damage = self.calcDamageModifiers(damage)

        self.changeHealth(-self.true_damage)

        if self.health <= 0:
            self.kill()

    def getHealth(self):
        return self.health

    def getHealthPercentage(self):
        return self.health/self.max_health
    
    
class PlayerHUD(events.EventAcceptor):
    HEALTH_BAR_BOUNDS = pygame.Rect((10, 10), (500, 20))
    INVENTORY_POS = (1600, 100)
    
    def __init__(self, player):
        self.player = player

    def onMouseDown(self, pos, button):
        used = 0
        
        # Inventory
        ipos = [pos[0], pos[1]]
        ipos[0] -= self.INVENTORY_POS[0]
        ipos[1] -= self.INVENTORY_POS[1]

        used += int(self.player.inventory.onMouseDown(ipos, button))

        return bool(used)

    def drawHealthBar(self, surface):
        bar = self.HEALTH_BAR_BOUNDS

        # Background
        pygame.draw.rect(surface, (128, 128, 128), bar)

        # Health stats
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(bar.topleft, (bar.width*self.player.getHealthPercentage(), bar.height)))

    def drawInventory(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        self.player.inventory.draw(surface, self.INVENTORY_POS)
        self.player.inventory.drawActiveStack(surface, mouse_pos)        
        
    def draw(self, surface):
        self.drawHealthBar(surface)
        self.drawInventory(surface)

INITIAL_PLAYER_HEALTH = 10

class Player(Creature):
    def __init__(self):
        super().__init__(INITIAL_PLAYER_HEALTH)

        self.loadHUD()
        self.loadInventory()

    def loadHUD(self):
        self.HUD = PlayerHUD(self)

    def loadInventory(self):
        self.inventory = Inventory(27, 8, (100, 100))
        self.inventory.setItemStack(ItemStack("debug_sword", 45), 10)

    def setManager(self, manager):
        self.manager = manager

    def tick(self):
        self.handleMotion()

    def handleMotion(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.pos[1] -= .1
        if pressed[pygame.K_a]:
            self.pos[0] -= .1
        if pressed[pygame.K_s]:
            self.pos[1] += .1
        if pressed[pygame.K_d]:
            self.pos[0] += .1

    def onMouseDown(self, pos, button):
        # If anything uses the button, player will hog mouse input
        used = 0
        
        used += int(self.HUD.onMouseDown(pos, button))
        
        return bool(used)

    def worldClosed(self):
        self.inventory.close()
        
    def kill(self):
        pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))
            
    def getMapDelta(self):
        bpos = self.getBufferPos()
        return (-bpos[0], -bpos[1])

    def draw(self, surface):
        # Draw player sprite
        pos = self.manager.bufferPosToScreenPos(self.getBufferPos())
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(pos, (80, 120)))

        # Draw GUI
        self.HUD.draw(surface)
