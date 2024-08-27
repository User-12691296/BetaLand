from .basic import BasicTile

class BarrierTile(BasicTile):
    def __init__(self):
        super().__init__("barrier", "barrier", False)

    def onLeft(self, world, tile_pos):
        player = world.getPlayer()

        player.damage(0.5)

    def onRight(self, world, tile_pos):
        world.setTileElevation(tile_pos, 0)
        world.setTileID(tile_pos, "grass")
