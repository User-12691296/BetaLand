from .basic import BasicTile
from .grass import GrassTile
from .barrier import BarrierTile
from .sanddark import SandDarkTile
from .damaging import DamageTile
from .slowing import SlowTile
from .cactus import Cactus


OVERWORLD_TILES = []
GrassTile().addTileToList(OVERWORLD_TILES)
BarrierTile().addTileToList(OVERWORLD_TILES)
SandDarkTile().addTileToList(OVERWORLD_TILES)
BasicTile("bloodstone", "bloodstone").addTileToList(OVERWORLD_TILES)
BasicTile("sand", "sand").addTileToList(OVERWORLD_TILES)
BasicTile("sandlight", "sandlight").addTileToList(OVERWORLD_TILES)
BasicTile("sandoasis", "sandoasis", False).addTileToList(OVERWORLD_TILES)
Cactus("sandcactus", "sandcactus", 0.1, 2).addTileToList(OVERWORLD_TILES)


BasicTile("kr1stal", "kr1stal").addTileToList(OVERWORLD_TILES)
BasicTile("kr1stalfloor", "kr1stalfloor").addTileToList(OVERWORLD_TILES)
BasicTile("kr1stalrunes", "kr1stalrunes").addTileToList(OVERWORLD_TILES)

BasicTile("snow", "snow").addTileToList(OVERWORLD_TILES)
BasicTile("snow2", "snow2", False).addTileToList(OVERWORLD_TILES)

BasicTile("swamp", "swamp").addTileToList(OVERWORLD_TILES)
BasicTile("swampaccent", "swampaccent").addTileToList(OVERWORLD_TILES)
BasicTile("swampwater", "swampwater").addTileToList(OVERWORLD_TILES)

BasicTile("deepdark", "deepdark", False).addTileToList(OVERWORLD_TILES)
BasicTile("darkwall", "darkwall", False).addTileToList(OVERWORLD_TILES)

BasicTile("mountain", "mountain").addTileToList(OVERWORLD_TILES)
BasicTile("mountainsnow", "mountainsnow").addTileToList(OVERWORLD_TILES)
BasicTile("mountainsnowier", "mountainsnowier").addTileToList(OVERWORLD_TILES)

BasicTile("volcano", "volcano").addTileToList(OVERWORLD_TILES)
DamageTile("volcanolava", "volcanolava", 0.2, False).addTileToList(OVERWORLD_TILES)
DamageTile("volcanomolten", "volcanomolten", 0.1).addTileToList(OVERWORLD_TILES)

BasicTile("void", "barrier").addTileToList(OVERWORLD_TILES)
BasicTile("black", "black").addTileToList(OVERWORLD_TILES)


ALL_TILES = []
ALL_TILES += OVERWORLD_TILES
