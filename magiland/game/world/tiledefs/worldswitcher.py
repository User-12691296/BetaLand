from .basic import BasicTile

class WorldSwitcher(BasicTile):
    def init(self, tileid, tex_name, world_to_change, rscat=True):
        super().init(tileid, tex_name, rscat)
        self.world_to_change = world_to_change

    def onLeft(self, world, tile_pos):
        world.player.manager.changeWorld(self.world_to_change)
