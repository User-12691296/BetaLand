from ..classes import Item
from .swords import Sword

ALL_ITEM_CLASSES = []


SWORDS = []
Sword("debug_sword", "sword").addToGroup(SWORDS)
Sword("epic_sword", "emerald_studded_sword").addToGroup(SWORDS)
Sword("cool_sword", "ruby_studded_sword").addToGroup(SWORDS)
Sword("lil_sword", "sapphire_studded_sword").addToGroup(SWORDS)


ALL_ITEM_CLASSES += SWORDS
