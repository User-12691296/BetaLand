from .basic import BasicTile
from ...entities import ENTITY_CLASSES

class DarkSandTile(BasicTile):
    def __init__(self):
        super().__init__("sand2", "darksand", False)

    def onRight(self, world, tile_pos):
        slime = ENTITY_CLASSES.Slime()
        slime.setPos(tile_pos)
        world.addEntity(slime)
