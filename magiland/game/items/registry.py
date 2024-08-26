import pygame
import os

from misc.textures import TextureAtlas

ASSETS = "assets/game"


def initialiseItems():
    REGISTRY.loadAtlas()
    registerAllItems()
    
def registerAllItems():
    REGISTRY.addItem(Item("debug_sword", "sword"))
    REGISTRY.addItem(Item("epic_sword", "emerald_studded_sword"))
    REGISTRY.addItem(Item("cool_sword", "ruby_studded_sword"))
    REGISTRY.addItem(Item("lil_sword", "sapphire_studded_sword"))

class ITEM_TEXTURE_PRESETS:
    FOLDER       = os.path.join(ASSETS, "items")
    SIZE         = 64
    EXT          = ".png"
    RESCALE      = True
    TRANSPARENCY = True

class Item:
    def __init__(self, itemid, tex_name, stackable=True):
        self.itemid = itemid
        self.tex_name = tex_name
        self.stackable = stackable

        self._atlas_given = False

    def setAtlas(self, atlas):
        self.atlas = atlas

        self.tex_loc = self.atlas.getTextureLoc(self.tex_name)

        self._atlas_given = True

    def isStackable(self):
        return self.stackable

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
