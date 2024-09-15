from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES


class SwampAnaconda(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["swampanaconda"]

    def isEnemy(self):
        return True

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 8 and not self.isCooldownActive("poisondart"):
            poisondart = PROJECTILE_CLASSES.PoisonDart.fromStartEnd(self.pos, self.world.player.getPos())
            poisondart.giveImmunity(self)
            self.world.addProjectile(poisondart)
            self.registerCooldown("lasershot", 60)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if entity.isEnemyTarget():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "swampanaconda")

class SwampOtter(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["swampotter"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "swampotter")

class SwampTangler(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["swamptangler"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "swamptangler")

class SwampSlime(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["swampslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "swampslime")


# Add crystal enemies to a group of enemies
SWAMPANACONDAS = []
SwampAnaconda.addToGroup(SWAMPANACONDAS)

SWAMPOTTERS = []
SwampOtter.addToGroup(SWAMPOTTERS)

SWAMPTANGLERS = []
SwampTangler.addToGroup(SWAMPTANGLERS)

SWAMPSLIMES = []
SwampSlime.addToGroup(SWAMPSLIMES)
