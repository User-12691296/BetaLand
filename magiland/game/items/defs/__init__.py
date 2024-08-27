from ..classes import Item

ALL_ITEM_CLASSES = []


SWORDS = []
Item("debug_sword", "sword").addToGroup(SWORDS)
Item("epic_sword", "emerald_studded_sword").addToGroup(SWORDS)
Item("cool_sword", "ruby_studded_sword").addToGroup(SWORDS)
Item("lil_sword", "sapphire_studded_sword").addToGroup(SWORDS)


ALL_ITEM_CLASSES += SWORDS
