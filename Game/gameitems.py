import pygame
import numpy as np
import os

import events
from textures import TextureAtlas

pygame.font.init()

ASSETS = os.path.join("assets", "game")

def initialiseItems():
    REGISTRY.loadAtlas()
    loadItems()

def loadItems():
    REGISTRY.addItem(Item("debug_sword", "sword"))

class ITEM_TEXTURE_PRESETS:
    FOLDER       = os.path.join(ASSETS, "items")
    SIZE         = 64
    EXT          = ".png"
    RESCALE      = True
    TRANSPARENCY = True

class ItemRegistry:
    def __init__(self):
        self.items = {}

        self._atlas_loaded = False

    def loadAtlas(self):
        self.atlas = TextureAtlas.fromPreset(ITEM_TEXTURE_PRESETS)

        self._atlas_loaded = True

    def addItem(self, item):
        if not self._atlas_loaded:
            raise RuntimeError("Item registry texture atlas not loaded yet")
        
        self.items[item.getItemID()] = item

        item.setAtlas(self.atlas)

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def getItem(self, itemid):
        return self.items.get(itemid)

REGISTRY = ItemRegistry()

class Item:
    def __init__(self, itemid, tex_name):
        self.itemid = itemid
        self.tex_name = tex_name

        self._atlas_given = False

    def setAtlas(self, atlas):
        self.atlas = atlas

        self.tex_loc = self.atlas.getTextureLoc(self.tex_name)

        self._atlas_given = True

    def getItemID(self):
        return self.itemid

    def onLeft(self, player, world, tile, tile_pos): pass
    def onRight(self, player, world, tile, tile_pos): pass
    def onMiddle(self, player, world, tile, tile_pos): pass

    def draw(self, surface, center):
        if self._atlas_given:
            item_drawing_bounds = pygame.Rect((0, 0), self.atlas.getTextureSize())
            item_drawing_bounds.center = center

            self.atlas.drawTextureAtLoc(surface, item_drawing_bounds.topleft, self.tex_loc)
        
class ItemStack:
    ITEM_COUNTER_FONT = pygame.font.SysFont("Courier New", 40)
    
    def __init__(self, itemid, count):
        self.item = REGISTRY.getItem(itemid)
        self.count = count

    def draw(self, surface, center):
        self.item.draw(surface, center)
        
        stack_amount = self.ITEM_COUNTER_FONT.render(str(self.count), True, (255, 255, 255))
        surface.blit(stack_amount, center)
        

class Inventory(events.EventAcceptor):
    def __init__(self, size, width, grid_size):
        self.size = size
        self.width = width
        self.height = round(self.size/self.width+0.4999999999)
        self.grid_size = grid_size

        self.active_stack = None

        self.item_stacks = [None] * self.size

    def setItemStack(self, stack, loc):
        self.item_stacks[loc] = stack

    def addItemStack(self, stack):
        added = False
        
        for stack_loc in range(self.size):
            if self.getItemStack(stack_loc) == None:
                self.setItemStack(stack, stack_loc)
                added = True
                break

        if not added:
            self.active_stack = stack

    def getItemStack(self, loc):
        return self.item_stacks[loc]

    def swapActiveWithStack(self, loc):
        temp = self.active_stack
        self.active_stack = self.getItemStack(loc)
        self.setItemStack(temp, loc)

    def getPosOfStack(self, loc, topleft):
        # Grid position of item stack
        grid = [0, 0]
        grid[0] = loc %  self.width
        grid[1] = loc // self.width

        # Position of item stack relative to square one
        rel_pos = [0, 0]
        rel_pos[0] = grid[0]*self.grid_size[0]
        rel_pos[1] = grid[1]*self.grid_size[1]

        # Position of item stack relative to top left of inventory
        rel_pos[0] += self.grid_size[0] // 2
        rel_pos[1] += self.grid_size[1] // 2

        # Absolute position of item stack
        pos = [0, 0]
        pos[0] = rel_pos[0] + topleft[0]
        pos[1] = rel_pos[1] + topleft[1]

        return pos

    def onMouseDown(self, ipos, button):
        # If mouse click outside of inventory bounds, quit
        if (ipos[0] < 0) or (ipos[1] < 0):
            return False
        if (ipos[0] >= self.width*self.grid_size[0]) or (ipos[1] >= self.height*self.grid_size[1]):
            return False

        # Get stack clicked on
        grid = [0, 0]
        grid[0] = ipos[0]//self.grid_size[0]
        grid[1] = ipos[1]//self.grid_size[1]

        stack_loc = grid[0] + self.width*grid[1]

        if stack_loc >= self.size:
            return False

        # Bring it to the active stack
        self.swapActiveWithStack(stack_loc)

        return True

    def close(self):
        self.addItemStack(self.active_stack)
        self.active_stack = None

    def draw(self, surface, topleft):
        for stack_loc in range(self.size):
            pos = self.getPosOfStack(stack_loc, topleft)
            
            pygame.draw.circle(surface, (100, 50, 50), pos, 40)

            stack = self.getItemStack(stack_loc)
            if stack:
                stack.draw(surface, pos)

    def drawActiveStack(self, surface, pos):
        if self.active_stack:
            self.active_stack.draw(surface, pos)
