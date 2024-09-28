from .player import Player
from .crystalbarrel import *
from .slimes import *
from .blob import *
from .crystalenemies import *
from .swampenemies import *
from .dessertenemies import *
from .frozenenemies import *
from .mountainenemies import *
from .darknessenemies import *
from .item import ItemEntity

ALL_ENTITY_CLASSES = []


ALL_ENTITY_CLASSES.append(Player)
ALL_ENTITY_CLASSES.append(ItemEntity)

ALL_ENTITY_CLASSES += CRYSTALBRONZE
ALL_ENTITY_CLASSES += CRYSTALSILVER
ALL_ENTITY_CLASSES += CRYSTALGOLD
ALL_ENTITY_CLASSES += CRYSTALPLAT

ALL_ENTITY_CLASSES += SLIMES
ALL_ENTITY_CLASSES += BLOBS

# Add crystal enemies to a group of enemies
ALL_ENTITY_CLASSES += CRYSTALGOLEMS
ALL_ENTITY_CLASSES += CRYSTALKNIGHTS
ALL_ENTITY_CLASSES += CRYSTALSCORPIONS
ALL_ENTITY_CLASSES += CRYSTALSIMES
ALL_ENTITY_CLASSES += CRYSTALBATS

# Add swamp enemies to a group of enemies
ALL_ENTITY_CLASSES += SWAMPANACONDAS
ALL_ENTITY_CLASSES += SWAMPOTTERS
ALL_ENTITY_CLASSES += SWAMPTANGLERS
ALL_ENTITY_CLASSES += SWAMPSLIMES

# Add dessert enemies to a group of enemies
ALL_ENTITY_CLASSES += DESSERTKNIGHTS
ALL_ENTITY_CLASSES += DESSERTSLIMES
ALL_ENTITY_CLASSES += DESSERTSANDWURMS
ALL_ENTITY_CLASSES += DESSERTRAIDERS

# Add frozen enemies to a group of enemies
ALL_ENTITY_CLASSES += FROZENKNIGHTS
ALL_ENTITY_CLASSES += FROZENSLIMES
ALL_ENTITY_CLASSES += FROZENTROLLS
ALL_ENTITY_CLASSES += FROZENPUFFERS
ALL_ENTITY_CLASSES += FROZENWOLVES

# Add mountain enemies to a group of enemies
ALL_ENTITY_CLASSES += MOUNTAINGOLEMS
ALL_ENTITY_CLASSES += MOUNTAINSLIMES
ALL_ENTITY_CLASSES += MOUNTAINEAGLES
ALL_ENTITY_CLASSES += MOUNTAINGOATS
ALL_ENTITY_CLASSES += MOUNTAINTROLLS
ALL_ENTITY_CLASSES += MOUNTAINBATS


# Add darkness enemies to a group of enemies
ALL_ENTITY_CLASSES += DARKNESSGHOSTS
ALL_ENTITY_CLASSES += DARKNESSGRAVETRAPPERS
ALL_ENTITY_CLASSES += DARKNESSJUMPSCARES
ALL_ENTITY_CLASSES += DARKNESSKNIGHTMARE1
ALL_ENTITY_CLASSES += DARKNESSKNIGHTMARE2
ALL_ENTITY_CLASSES += DARKNESSSPREADERS
ALL_ENTITY_CLASSES += DARKNESSBATS
