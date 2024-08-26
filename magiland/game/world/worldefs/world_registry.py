from .world import World
from ..tiledefs import ALL_TILES

class Overworld(World):
    world_name = "overworld"
    
    def __init__(self):
        self.world_name = "overworld"

        super().__init__(ALL_TILES)

class Level1(World):
    world_name = "level_1"
    
    def __init__(self):
        self.world_name = "level_1"
        
        super().__init__(ALL_TILES)

LOADABLE_WORLDS = (Overworld, Level1)
