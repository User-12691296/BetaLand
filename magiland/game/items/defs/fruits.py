from ..classes import Item
from misc import animations
import math
import time
from constants import GAME

SWING_FRAMES = 10

"""
This class only affects players because fruits can only affect players but if you want to create an effect in general:
it will work the exact same, just give the creature an action function and a reverse action function and then set the ticker to 1
"""

class Fruit(Item):
    #Note to self, add healing effect thru init
    # Fruits give a special status effect TBD
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration = 60):
        super().__init__(itemid, tex_name, True, size)
        self.heal_amount = heal_amount
        
        self.ticker = 0

        self.effect_time = 0
        self.effect_duration = effect_duration

    def effect(self, player, world, tile, tile_pos):
        pass

    def reverse_effect(self, player, world, tile, tile_pos):
        pass

    def onLeft(self, data, player, world, tile, tile_pos):
        player.changeHealth(self.heal_amount)
        self.effect(player, world, tile, tile_pos)
        player.inventory.setItemStack(None,0)


    def tick(self, data, player, world):
        data["animations"].tick()

# def placeholderFunction():
#     return lambda x,y,z: None

class Lemon (Fruit):
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration):
        super().__init__(itemid, tex_name, size, heal_amount, effect_duration)

    def effect(self, player, world, tile, tile_pos):
        player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED*0.5)
        player.giveEffect("speed", self.effect_duration, lambda x, y, z:None, self.reverse_effect)
        # player.giveEffect("testing", self.effect_duration+40, lambda x,y,z: print("hi"), lambda x,y,z:print("done"))

    def reverse_effect(self, player, world, player_tile_pos):
        player.setMovementSpeed(GAME.PLAYER_WALKING_SPEED)


FRUITS = []
Fruit("debug_sword", "sword", 1, 100).addToGroup(FRUITS)
Fruit("orange", "orange", 1, 30).addToGroup(FRUITS)
Fruit("banana", "banana", 1, 30).addToGroup(FRUITS)
Fruit("watermelon", "watermelon", 1, 30).addToGroup(FRUITS)
Fruit("apple", "apple", 1, 100).addToGroup(FRUITS)
Lemon("lemon", "lemon", 1, 30, 100).addToGroup(FRUITS)
