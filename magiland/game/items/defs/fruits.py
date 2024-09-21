from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 10

class Fruit(Item):
    #Note to self, add healing effect thru init
    # Fruits give a special status effect TBD
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, False, size)
    
##    def initData(self):
##        data = super().initData()
##        return data

    def tick(self, data, player, world):
        data["animations"].tick()

FRUITS = []
Fruit("debug_sword", "sword", 1).addToGroup(FRUITS)
Fruit("orange", "orange", 1).addToGroup(FRUITS)
Fruit("banana", "banana", 1).addToGroup(FRUITS)
Fruit("watermelon", "watermelon", 1).addToGroup(FRUITS)
Fruit("apple", "apple", 1).addToGroup(FRUITS)
Fruit("lemon", "lemon", 1).addToGroup(FRUITS)
