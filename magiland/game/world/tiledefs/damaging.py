from .basic import BasicTile

class DamageTile(BasicTile):
    def __init__(self, tileid, tex_name, damage_value, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        
        self.damage_value = damage_value
        
    def onWalk(self, world, tile_pos):
        player = world.getPlayer()
        player.damage(self.damage_value)