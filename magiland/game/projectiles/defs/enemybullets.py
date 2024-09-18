from ..classes import Projectile
## INCLUDES POISON DART, FEATHER
class PoisonDart(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["poison_dart"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(1)
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "poison_dart", display_topleft)

class Feather(Projectile):
    def __init__(self, start, angle):
        super().__init__(start, angle)

        self.speed = 0.3

    @classmethod
    def fromStartEnd(cls, start, end):
        return super().fromStartEnd(start, end)

    @staticmethod
    def getNeededAssets():
        return ["feather_bullet"]

    def movementTick(self):
        super().movementTick()

        if self.world.isTileOpaque(self.getTilePos()):
            self.kill()

    def damageTick(self):
        tpos = self.getTilePos()

        for entity in self.world.getEntitiesOnTile(tpos):
            if self.isValidHit(entity) and not entity.isEnemy():
                entity.damage(1)
                ##player.setAttribute("movement_speed", 10)                
                self.kill()

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        self.stdDraw(display, "feather_bullet", display_topleft)

ENEMYBULLETS = []
PoisonDart.addToGroup(ENEMYBULLETS)
Feather.addToGroup(ENEMYBULLETS)
