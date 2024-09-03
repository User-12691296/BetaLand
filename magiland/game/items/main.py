import pygame
import numpy as np
import os

from misc import events
from misc.textures import TextureAtlas

from . import registry
from .classes import *

        
def initialiseItems(item_entity_class):
    REGISTRY = registry.ItemRegistry()
    REGISTRY.loadAtlas()

    ItemStack.setRegistry(REGISTRY)
    Inventory.setItemEntityClass(item_entity_class)
    
    registry.registerAllItems(REGISTRY)
