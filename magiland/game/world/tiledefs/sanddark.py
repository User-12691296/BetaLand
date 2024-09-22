from .basic import BasicTile
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class SandDarkTile(BasicTile):
    def __init__(self):
        super().__init__("sanddark", "sanddark", False)

    def onRight(self, world, tile_pos):
        blob = ENTITY_CLASSES.CrystalGolem()
        blob.setPos(tile_pos)
        world.addEntity(blob)

    def onLeft(self, world, tile_pos):
        MountainEagle = ENTITY_CLASSES.MountainEagle()
        MountainEagle.setPos(tile_pos)
        world.addEntity(MountainEagle)
