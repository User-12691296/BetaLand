from .basic import BasicTile
from ...entities import ENTITY_CLASSES

class DarkSandTile(BasicTile):
    def __init__(self):
        super().__init__("sand2", "darksand", False)

    def onRight(self, world, tile_pos):
        blob = ENTITY_CLASSES.Blob()
        blob.setPos(tile_pos)
        world.addEntity(blob)
