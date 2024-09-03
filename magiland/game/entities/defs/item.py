import random

from ..classes import Entity


class ItemEntity(Entity):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

    @staticmethod
    def getNeededAssets():
        return []

    def placeInWorld(self, world, pos, scat=0):
        real_pos = pos
        real_pos[0] += random.choice([1, 0, -1])*scat
        real_pos[1] += random.choice([1, -1] if real_pos[0]==pos[0] else [1, 0, -1])*scat
        self.setPos(real_pos)

        world.addEntity(self)

    def draw(self, surface):
        super().draw(surface)

        stack.drawAsStack(surface, self.world.player.manager.bufferPosToScreenPos(self.world.tilePosToBufferPos(self.pos)))
