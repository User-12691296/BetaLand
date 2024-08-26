from .basic import BasicTile

class GrassTile(BasicTile):
    def __init__(self):
        super().__init__("grass", "grass")

    def onLeft(self, world, tile_pos):
        world.setTileElevation(tile_pos, 10)
        world.setTileID(tile_pos, "barrier")
