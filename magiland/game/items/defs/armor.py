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
Armor("iron_helmet", "iron_helmet", 0, 3.8, 10).addToGroup(ARMORS)
Armor("croc", "croc", 0, 1, 10).addToGroup(ARMORS)
Armor("swamp_armor", "swamp_armor", 0, 1.5, 10).addToGroup(ARMORS)
Armor("crystal_armor", "crystal_armor", 0, 2, 10).addToGroup(ARMORS)
Armor("arctic_armor", "arctic_armor", 0, 2.4, 10).addToGroup(ARMORS)
Armor("deepdark_armor", "deepdark_armor", 0, 2.6, 10).addToGroup(ARMORS)
Armor("dragon_hide", "dragon_hide", 0, 3, 10).addToGroup(ARMORS)