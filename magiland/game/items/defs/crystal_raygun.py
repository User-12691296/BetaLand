from .guns import Gun
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class CrystalRaygun(Gun):
##    def __init__(self, itemid, tex_name, size):
##        super().__init__(itemid, tex_name, False, size)
##    
##    def initData(self):
##        data = super().initData()
##        return data
##
##    def tick(self, data, player, world):
##        data["animations"].tick()
##
##    def damageTick(self, data, player, world):
##        # Handle Swing
##        data["rot"] = -(player.getFacing()+90)
##        data["rot"] = data["rot"] % 360
    def fire(self, data, player, world, tile_pos, tile):
        super().fireInTheHole(data,player,world,tile_pos,tile)
        laser = PROJECTILE_CLASSES.CrystalLaserShot(player.pos, -data["rot"]-45)
        laser.giveImmunity(player)
        world.addProjectile(laser)
        
    def onLeft(self, data, player, world, tile_pos, tile):
        super().onLeft(data,player,world,tile_pos,tile)
        self.fire(data, player, world, tile_pos, tile)
        return True


CRYSTALRAYGUN = []
CrystalRaygun("debug_sword", "sword", 1).addToGroup(CRYSTALRAYGUN)
CrystalRaygun("crystal_raygun", "crystal_raygun", 2).addToGroup(CRYSTALRAYGUN)

