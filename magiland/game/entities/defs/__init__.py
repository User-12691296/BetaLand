from .player import Player
from .slimes import SLIMES, Slime
from .blob import BLOBS, Blob
from .crystalenemies import CRYSTALGOLEMS, CrystalGolem, CRYSTALKNIGHTS, CrystalKnight, CRYSTALSCORPIONS, CrystalScorpion, CRYSTALSIMES, CrystalSlime
from .item import ItemEntity

ALL_ENTITY_CLASSES = []


ALL_ENTITY_CLASSES.append(Player)
ALL_ENTITY_CLASSES.append(ItemEntity)

ALL_ENTITY_CLASSES += SLIMES
ALL_ENTITY_CLASSES += BLOBS

# Add crystal enemies to a group of enemies
ALL_ENTITY_CLASSES += CRYSTALGOLEMS
ALL_ENTITY_CLASSES += CRYSTALKNIGHTS
ALL_ENTITY_CLASSES += CRYSTALSCORPIONS
ALL_ENTITY_CLASSES += CRYSTALSIMES
