from ..classes import Item
from misc import animations
import math
import time
from constants import GAME

class PotionItem(Item):
    def __init__(self, itemid, tex_name, size, effect, effect_duration=60):
        super().__init__(itemid, tex_name, False, size)
        self.effect = effect
        self.effect_duration = effect_duration

    def apply_effect(self, player, world, player_tile_pos):
        pass

    def reverse_effect(self, player, world, player_tile_pos):
        pass

    def onUse(self, data, player, world, tile, tile_pos):
        self.apply_effect(player, world, tile, tile_pos)
        player.inventory.setItemStack(None, 0)

    def tick(self, data, player, world):
        data["animations"].tick()

class HealingPotionItem(PotionItem):
    def __init__(self, itemid, tex_name, size, heal_amount, effect_duration):
        super().__init__(itemid, tex_name, size, "Healing", effect_duration)
        self.heal_amount = heal_amount

    def apply_effect(self, player, world, tile, tile_pos):
        player.changeHealth(self.heal_amount)
        player.setAttribute("effect_time", 1)
        player.setAttribute("action", self.reverse_effect)
        player.setAttribute("effect_duration", self.effect_duration)

    def reverse_effect(self, player, world, player_tile_pos):
        # Healing effect might not need a reverse effect
        pass

class ManaPotionItem(PotionItem):
    def __init__(self, itemid, tex_name, size, mana_amount, effect_duration):
        super().__init__(itemid, tex_name, size, "Mana", effect_duration)
        self.mana_amount = mana_amount

    def apply_effect(self, player, world, tile, tile_pos):
        player.changeMana(self.mana_amount)
        player.setAttribute("effect_time", 1)
        player.setAttribute("action", self.reverse_effect)
        player.setAttribute("effect_duration", self.effect_duration)

    def reverse_effect(self, player, world, player_tile_pos):
        # Mana effect might not need a reverse effect
        pass

class StrengthPotionItem(PotionItem):
    def __init__(self, itemid, tex_name, size, strength_amount, effect_duration):
        super().__init__(itemid, tex_name, size, "Strength", effect_duration)
        self.strength_amount = strength_amount

    def apply_effect(self, player, world, tile, tile_pos):
        player.increaseStrength(self.strength_amount)
        player.setAttribute("effect_time", 1)
        player.setAttribute("action", self.reverse_effect)
        player.setAttribute("effect_duration", self.effect_duration)

    def reverse_effect(self, player, world, player_tile_pos):
        player.decreaseStrength(self.strength_amount)

class SpeedPotionItem(PotionItem):
            def __init__(self, itemid, tex_name, size, speed_increase, effect_duration):
                super().__init__(itemid, tex_name, size, "Speed", effect_duration)
                self.speed_increase = speed_increase

            def apply_effect(self, player, world, tile, tile_pos):
                player.changeSpeed(self.speed_increase)
                player.setAttribute("effect_time", 1)
                player.setAttribute("action", self.reverse_effect)
                player.setAttribute("effect_duration", self.effect_duration)

            def reverse_effect(self, player, world, player_tile_pos):
                player.changeSpeed(-self.speed_increase)