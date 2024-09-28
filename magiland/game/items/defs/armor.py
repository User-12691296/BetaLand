from ..classes import Item
from misc import animations

SWING_FRAMES = 10

class Armor(Item):
    def __init__(self, itemid, tex_name, size, armor_points, dmg_threshold):
        super().__init__(itemid, tex_name, False, size)
        self.armor_points = armor_points
        self.dmg_threshold = dmg_threshold

    def equip(self, player):
        player.setArmorValues(self.armor_points, self.dmg_threshold)

    def unequip(self, player):
        player.setArmorValues(0, 0)

    def isArmor(self):
        return True

    def tick(self, data, player, world):
        data["animations"].tick()

ARMORS = []
Armor("iron_helmet", "iron_helmet", 0, 10000, 10).addToGroup(ARMORS)
