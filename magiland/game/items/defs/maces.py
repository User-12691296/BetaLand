from .swords import Sword
from ...projectiles import PROJECTILE_CLASSES
from misc import animations
import math

SWING_FRAMES = 10

class Mace(Sword):

    def __init__(self, itemid, tex_name, damage, size, swing_angle=60, swing_range=None, player_damage_on_hit=0, amount_of_projectiles=8, laser = PROJECTILE_CLASSES.CrystalLaserShot):
        super().__init__(itemid, tex_name, damage, size, swing_angle, swing_range, player_damage_on_hit)

        self.angles = []
        self.amount_of_projectiles = amount_of_projectiles

        for i in range (self.amount_of_projectiles):
            self.angles.append((360/self.amount_of_projectiles)*i)

        self.laser = laser

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
    
        for angle in self.angles:
            laser = self.laser(player.pos, -data["rot"] + angle)
            laser.giveImmunity(player)
            world.addProjectile(laser)
                                    
MACES = []
Mace("debug_sword", "sword", 1000, 2).addToGroup(MACES)
Mace("wood_mace", "wood_mace", 20, 0, 300, 5).addToGroup(MACES)
Mace("stone_mace", "stone_mace", 20, 0, 300, 5).addToGroup(MACES)
Mace("kr1stal_mace", "kr1stal_mace", 20, 1, 300, 5, amount_of_projectiles=20).addToGroup(MACES)
Mace("lava_mace", "lava_mace", 20, 1, 300, 5, amount_of_projectiles=20).addToGroup(MACES)
Mace("celestial_mace", "celestial_mace", 20, 2, 300, 5, amount_of_projectiles=16, laser=PROJECTILE_CLASSES.PoisonDart).addToGroup(MACES)
Mace("cosmic_mace", "cosmic_mace", 20, 2, 300, 5, amount_of_projectiles=16).addToGroup(MACES)


