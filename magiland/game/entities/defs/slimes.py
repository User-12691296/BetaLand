from ..classes import Enemy
from ...projectiles import PROJECTILE_CLASSES


class Slime(Enemy):
    def __init__(self):
        super().__init__(5, 3, 30)

    @staticmethod
    def getNeededAssets():
        return ["slime"]

    def damageTick(self):
        if self.world.player.diagonalTo(self.pos) <= 6 and not self.isCooldownActive("lasershot"):
            lasershot = PROJECTILE_CLASSES.CrystalLaserShot.fromStartEnd(self.pos, self.world.player.getPos())
            lasershot.giveImmunity(self)
            self.world.addProjectile(lasershot)
            self.registerCooldown("lasershot", 60)
            
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if entity.isEnemyTarget():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        super().draw(display, display_topleft)

        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)
        
        self.atlas.drawTexture(display, spos, "slime")


SLIMES = []
Slime.addToGroup(SLIMES)
