import random

from ..classes import Entity

from constants import GAME

class ItemEntity(Entity):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

    @staticmethod
    def getNeededAssets():
        return []

    def isItemEntity(self):
        return True

    def placeInWorld(self, world, pos, scat=0):
        real_pos = [*pos]
        real_pos[0] += random.choice([1, 0, -1])*scat
        real_pos[1] += random.choice([1, -1] if real_pos[0]==pos[0] else [1, 0, -1])*scat
        self.setPos(real_pos)

        world.addEntity(self)

    def draw(self, surface):
        super().draw(surface)

        center = [*self.world.tilePosToBufferPos(self.pos)]

        topleft = [coord + GAME.TILE_SIZE//2 for coord in center]
        
        self.stack.drawAsStack(surface, topleft)
