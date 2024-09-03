from .swords import Sword
from misc import animations
import math

SWING_FRAMES = 10

class Board(Sword):

        #the only problem here is if you spam then it kills you lol
    def startSwing(self, data, player, world, tile_pos, tile):
        super().startSwing(data, player, world, tile_pos, tile)
        #if data entity is hit (anything is hit), if statement runs
        player.damage(1)

##    #this is logic error, runs for the whole swing so it does 10x damage (every tick)
##    def damageTick(self, data, player, world):
##        super().damageTick(data, player, world)
##        if data["entities_hit"]:
##        #if data entity is hit (anything is hit), if statement runs
##            player.damage(1)

    #fixes because we only look at endSwing
    def endSwing(self, data, player, world, tile_pos, tile):
        super().endSwing(data, player, world, tile_pos, tile)
        if data["entities_hit"]:
            player.damage(0)
        else:
            player.damage(-1)

 


BOARDS = []
Board("debug_sword", "sword", 1000, 2).addToGroup(BOARDS)
Board("golf_club", "golf_club", 20, 0, 300, 5).addToGroup(BOARDS)
