from ..classes import Enemy


class Blob(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["blob"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, surface):
        super().draw(surface)
        
        self.atlas.drawTexture(surface, self.world.tilePosToBufferPos(self.pos), "blob")

BLOBS=[]
Blob.addToGroup(BLOBS)