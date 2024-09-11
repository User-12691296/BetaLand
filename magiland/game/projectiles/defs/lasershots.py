from ..classes import Projectile

class CrystalLaserShot(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.2

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["lasershotcrystal"]

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity):
                entity.damage(0.4)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "lasershotcrystal", display_topleft)

LASERSHOTS = []
CrystalLaserShot.addToGroup(LASERSHOTS)
