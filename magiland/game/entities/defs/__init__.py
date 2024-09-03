from .player import Player
from .slimes import SLIMES, Slime
from .item import ItemEntity

ALL_ENTITY_CLASSES = []


ALL_ENTITY_CLASSES.append(Player)
ALL_ENTITY_CLASSES.append(ItemEntity)

ALL_ENTITY_CLASSES += SLIMES
