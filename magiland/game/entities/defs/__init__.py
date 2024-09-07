from .player import Player
from .slimes import SLIMES, Slime
from .blob import BLOBS, Blob
from .item import ItemEntity

ALL_ENTITY_CLASSES = []


ALL_ENTITY_CLASSES.append(Player)
ALL_ENTITY_CLASSES.append(ItemEntity)

ALL_ENTITY_CLASSES += SLIMES
ALL_ENTITY_CLASSES += BLOBS