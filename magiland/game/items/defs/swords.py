from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 14

class Sword(Item):
    def __init__(self, itemid, tex_name, size, swing_angle=60, swing_range=None):
        super().__init__(itemid, tex_name, False, size)

        self.swing_angle = swing_angle
        
        if not swing_range:
            self.swing_range = self.size + 2

        else:
            self.swing_range = swing_range

    def initData(self):
        data = super().initData()

        data["dps"] = 3
        
        return data

    def tick(self, data, player, world):
        data["animations"].tick()

        # Handle Swing
        angle = data["animations"].getPercentage("sword_swing")*self.swing_angle+15
        delta = data["animations"].getDelta("sword_swing")*self.swing_angle
        
        data["rot"] = -round(angle) + (self.swing_angle//2) - (player.getFacing()+90)


        for shift in range(0, round(delta), 5):
            if data["animations"].get("sword_swing"):
                real_angle = math.radians(-(45 + data["rot"] - shift))
                
                for i in range(1, self.swing_range):
                    pos = [*player.pos]
                    pos[0] += round(i*math.cos(real_angle))
                    pos[1] += round(i*math.sin(real_angle))

                    world.setTileID(pos, "grass")

                    for entity in world.getEntitiesOnTile(pos):
                        entity.damage(1)

    def onLeft(self, data, player, world, tile_pos, tile):
        player.setMovable(False)
        data["animations"].create("sword_swing", SWING_FRAMES, lambda: player.setMovable(True))

        return True
