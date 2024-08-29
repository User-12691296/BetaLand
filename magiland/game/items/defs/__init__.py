from ..classes import Item
from .swords import Sword

ALL_ITEM_CLASSES = []


SWORDS = []
Sword("debug_sword", "sword", 2).addToGroup(SWORDS)
Sword("epic_sword", "emerald_studded_sword", 2, 300, 5).addToGroup(SWORDS)
Sword("cool_sword", "ruby_studded_sword", 0, 90, 3).addToGroup(SWORDS)
Sword("lil_sword", "sapphire_studded_sword", 0, 360, 60).addToGroup(SWORDS)


ALL_ITEM_CLASSES += SWORDS
