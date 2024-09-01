from .basic import BasicTile
from .grass import GrassTile
from .barrier import BarrierTile
from .darksand import DarkSandTile


OVERWORLD_TILES = []
GrassTile().addTileToList(OVERWORLD_TILES)
BarrierTile().addTileToList(OVERWORLD_TILES)
DarkSandTile().addTileToList(OVERWORLD_TILES)
BasicTile("bloodstone", "bloodstone").addTileToList(OVERWORLD_TILES)
BasicTile("sand", "sand").addTileToList(OVERWORLD_TILES)
BasicTile("kr1stal", "kr1stal").addTileToList(OVERWORLD_TILES)
BasicTile("snow", "snow").addTileToList(OVERWORLD_TILES)
BasicTile("snow2", "snow2", False).addTileToList(OVERWORLD_TILES)
BasicTile("swamp", "swamp").addTileToList(OVERWORLD_TILES)
BasicTile("deepdark", "deepdark", False).addTileToList(OVERWORLD_TILES)
BasicTile("void",
          "barrier").addTileToList(OVERWORLD_TILES)


ALL_TILES = []
ALL_TILES += OVERWORLD_TILES
