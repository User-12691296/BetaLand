from .slowing import SlowTile

class Cactus(SlowTile):
    def __init__(self, tileid, tex_name, damage_value, slow_value, rscat=True):
        super().__init__(tileid, tex_name, rscat)
        
        self.damage_value = damage_value
        self.slow_value = slow_value
        
    def onWalk(self, world, tile_pos):

        # A BIT BUGGY, WORTH FIXING LATER, BUT JUMPY WHENEVER YOU CHANGE SPEED

        super().onWalk(world, tile_pos)
        player = world.getPlayer()
        player.damage(self.damage_value)