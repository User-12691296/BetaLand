from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 10

class Sword(Item):
    def __init__(self, itemid, tex_name, damage, size, swing_angle=60, swing_range=None):
        super().__init__(itemid, tex_name, False, size)

        self.damage = damage
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

    def damageTick(self, data, player, world):
        # Handle Swing
        angle = data["animations"].getPercentage("sword_swing")*self.swing_angle+12
        delta = data["animations"].getDelta("sword_swing")*self.swing_angle
        
        data["rot"] = -round(angle) + (self.swing_angle//2) - (player.getFacing()+90)

        for shift in range(0, round(delta), 5):
            if data["animations"].get("sword_swing"):
                real_angle = math.radians(-(45 + data["rot"] - shift))
                
                for i in range(1, self.swing_range):
                    pos = [*player.pos]
                    pos[0] += round(i*math.cos(real_angle))
                    pos[1] += round(i*math.sin(real_angle))

                    for entity in world.getEntitiesOnTile(pos):
                        if not entity in data["entities_hit"]:
                            entity.damage(self.damage)
                            world.setTileID(entity.getPos(), "grass")
                            data["entities_hit"].append(entity)

    def startSwing(self, data, player, world, tile_pos, tile):
        player.setMovable(False)
        data["animations"].create("sword_swing", SWING_FRAMES, lambda: self.endSwing(data, player, world, tile_pos, tile))

        data["entities_hit"] = []

    def endSwing(self, data, player, world, tile_pos, tile):
        player.setMovable(True)
        data["entities_hit"] = []

    def onLeft(self, data, player, world, tile_pos, tile):
        self.startSwing(data, player, world, tile_pos, tile)

        return True


SWORDS = []
Sword("debug_sword", "sword", 1000, 2).addToGroup(SWORDS)
Sword("epic_sword", "emerald_studded_sword", 20, 2, 300, 5).addToGroup(SWORDS)
Sword("cool_sword", "ruby_studded_sword", 3, 0, 90, 3).addToGroup(SWORDS)
Sword("lil_sword", "sapphire_studded_sword", 2, 0, 20, 2).addToGroup(SWORDS)
