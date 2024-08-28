from ..classes import Item
from misc import animations
import math

class Sword(Item):
    def __init__(self, itemid, tex_name):
        super().__init__(itemid, tex_name, False)

    def initData(self):
        data = super().initData()

        data["dps"] = 3
        data["range"] = 2
        
        return data

    def tick(self, data, player, world):
        data["animations"].tick()

        # Handle Swing
        data["rot"] = data["animations"].getFrame("sword_swing")*-3

        if data["animations"].get("sword_swing"):
            real_angle = math.radians(-(45 + data["rot"]))
            pos = [*player.pos]
            pos[0] += round(data["range"]*math.cos(real_angle))
            pos[1] += round(data["range"]*math.sin(real_angle))

            world.setTileID(pos, "grass")

    def onLeft(self, data, player, world, tile_pos, tile):
        player.setMovable(False)
        data["animations"].create("sword_swing", 120, lambda: player.setMovable(True))
