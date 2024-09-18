from .swords import Sword
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Mace(Sword):

##        #the only problem here is if you spam then it kills you lol
##    def startSwing(self, data, player, world, tile_pos, tile):
##        super().startSwing(data, player, world, tile_pos, tile)
##        #if data entity is hit (anything is hit), if statement runs
##        player.damage(1)
##
####    this is logic error, runs for the whole swing so it does 10x damage (every tick)
####    def damageTick(self, data, player, world):
####        super().damageTick(data, player, world)
####        if data["entities_hit"]:
####        #if data entity is hit (anything is hit), if statement runs
####            player.damage(1)
##
##    #fixes because we only look at endSwing
##    def endSwing(self, data, player, world, tile_pos, tile):
##        super().endSwing(data, player, world, tile_pos, tile)
##        if data["entities_hit"]:
##            player.damage(0)
##        else:
##            player.damage(-1)
    def onLeft(self, data, player, world, tile_pos, tile):
        super().onLeft(data, player, world, tile_pos, tile)
    
        angles = [0,45,90,135,180,225,270,315,360]
        for angle in angles:
            laser = PROJECTILE_CLASSES.CrystalLaserShot(player.pos, -data["rot"] + angle)
            laser.giveImmunity(player)
            world.addProjectile(laser)
                                    
MACES = []
Mace("debug_sword", "sword", 1000, 2).addToGroup(MACES)
Mace("wood_mace", "wood_mace", 20, 0, 300, 5).addToGroup(MACES)
Mace("stone_mace", "stone_mace", 20, 0, 300, 5).addToGroup(MACES)
Mace("kr1stal_mace", "kr1stal_mace", 20, 1, 300, 5).addToGroup(MACES)
Mace("lava_mace", "lava_mace", 20, 1, 300, 5).addToGroup(MACES)
Mace("celestial_mace", "celestial_mace", 20, 2, 300, 5).addToGroup(MACES)
Mace("cosmic_mace", "cosmic_mace", 20, 2, 300, 5).addToGroup(MACES)


