# ADD A COOLDOWN FOR THIS IN PARTICULAR
from ..classes import Item
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Bow(Item):
    def __init__(self, itemid, tex_name, size):
        super().__init__(itemid, tex_name, False, size)
    
##    def initData(self):
##        data = super().initData()
##        return data

    def tick(self, data, player, world):
        data["animations"].tick()

    def damageTick(self, data, player, world):
        # Handle Swing
        data["rot"] = -(player.getFacing()+90)
        data["rot"] = data["rot"] % 360

    def fireInTheHole(self, data, player, world, tile_pos, tile):
        arrow = PROJECTILE_CLASSES.Arrow(player.pos, -data["rot"]-45)
##        if not pizza.isCooldownActive("pizza"):
        arrow.giveImmunity(player)
        world.addProjectile(arrow)
##            pizza.registerCooldown("lasershot", 60)

##        player.setAttribute("movement_speed", 10)
        
    def onLeft(self, data, player, world, tile_pos, tile):
        self.fireInTheHole(data, player, world, tile_pos, tile)
        return True

#class Crossbow(Item):pass
# Do we need separate for crossbow?

BOWS = []
Bow("debug_sword", "sword", 1).addToGroup(BOWS)
Bow("basic_crossbow", "basic_crossbow", 1).addToGroup(BOWS)

