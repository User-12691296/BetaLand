from ..classes import Projectile

class Pizza(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.4

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["pizza_bullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(2)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "pizza_bullet", display_topleft)

class SoulBlast(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["soul_blast"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(2)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)
        self.stdDraw(display, "soul_blast", display_topleft)

PLAYERBULLETS = []
Pizza.addToGroup(PLAYERBULLETS)
SoulBlast.addToGroup(PLAYERBULLETS)
