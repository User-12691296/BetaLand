import pygame

from ..classes import Enemy

class CrystalGolem(Enemy):
    def __init__(self):
        super().__init__(3, 0, 40)
        """ CODE FOR MOB DROPS
        self.loadInventory() """

    @staticmethod
    def getNeededAssets():
        return ["crystalgolem"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.4)

    """ CODE FOR MOB DROPS
    def tick(self):
        super().tick()
        if self.getHealth() <= 0:
            self.dropItem """
    
    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("crystalgolem")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class CrystalKnight(Enemy):
    def __init__(self):
        super().__init__(5, 0, 20)

    @staticmethod
    def getNeededAssets():
        return ["crystalknight"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("crystalknight")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class CrystalScorpion(Enemy):
    def __init__(self):
        super().__init__(8, 0, 25)

    @staticmethod
    def getNeededAssets():
        return ["crystalscorpion"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("crystalscorpion")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class CrystalSlime(Enemy):
    def __init__(self):
        super().__init__(4, 0, 1)

    @staticmethod
    def getNeededAssets():
        return ["crystalslime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.5)
                self.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("crystalslime")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)

class CrystalBat(Enemy):
    def __init__(self):
        super().__init__(5, 0, 25)

    @staticmethod
    def getNeededAssets():
        return ["crystalbat"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, display, display_topleft=(0, 0)):
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        entity_texture = self.atlas.getTexture("crystalbat")

        rotated_texture = pygame.transform.rotate(entity_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=spos)
        display.blit(rotated_texture, rotated_rect.center)


# Add crystal enemies to a group of enemies
CRYSTALGOLEMS = []
CrystalGolem.addToGroup(CRYSTALGOLEMS)

CRYSTALKNIGHTS = []
CrystalKnight.addToGroup(CRYSTALKNIGHTS)

CRYSTALSCORPIONS = []
CrystalScorpion.addToGroup(CRYSTALSCORPIONS)

CRYSTALSIMES = []
CrystalSlime.addToGroup(CRYSTALSIMES)

CRYSTALBATS = []
CrystalBat.addToGroup(CRYSTALBATS)
