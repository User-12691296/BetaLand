from .basic import BasicTile
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class SandDarkTile(BasicTile):
    def __init__(self):
        super().__init__("sanddark", "sanddark", False)

    def onRight(self, world, tile_pos):
        knight = ENTITY_CLASSES.FrozenKnight()
        knight.setPos(tile_pos)
        world.addEntity(knight)

    def onLeft(self, world, tile_pos):
        slime = ENTITY_CLASSES.Slime()
        slime.setPos(tile_pos)
        world.addEntity(slime)
