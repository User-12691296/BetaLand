from ..classes import Item
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Gun(Item):
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, False, size)
    
    def initData(self):
        data = super().initData()
        return data

    def tick(self, data, player, world):
        data["animations"].tick()

    def damageTick(self, data, player, world):
        # Handle Swing
        data["rot"] = -(player.getFacing()+90)
        data["rot"] = data["rot"] % 360

    def fireInTheHole(self, data, player, world, tile_pos, tile):
        pizza = PROJECTILE_CLASSES.Pizza(player.pos, -data["rot"]-45)
        pizza.giveImmunity(player)
        world.addProjectile(pizza)

    def onLeft(self, data, player, world, tile_pos, tile):
        self.fireInTheHole(data, player, world, tile_pos, tile)
        return True


GUNS = []
Gun("debug_sword", "sword", 1).addToGroup(GUNS)
Gun("pizza_gun", "pizza_gun", 1).addToGroup(GUNS)

