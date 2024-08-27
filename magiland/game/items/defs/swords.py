from ..classes import Item

class Sword(Item):
    def __init__(self, itemid, tex_name):
        super().__init__(itemid, tex_name, False)

    def onLeft(self, player, world, tile_pos, tile):
        player.damage(5)
