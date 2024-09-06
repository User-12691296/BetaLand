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

""" class CrystalLevel(World):
    world_name = "crystal_level"
    
    def __init__(self):
        self.world_name = "crystal_level"
        
        super().__init__(ALL_TILES) 
        
class DeepDarkLevel(World):
    world_name = "deep_dark_level"
    
    def __init__(self):
        self.world_name = "deep_dark_level"
        
        super().__init__(ALL_TILES) """

LOADABLE_WORLDS = (Overworld, Level1, DeepDarkLevel)
