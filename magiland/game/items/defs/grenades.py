from ..classes import Item
from misc import animations
import math
import pygame

class Bomb(Item):
    def __init__(self):
        super().__init__("bomb", "crystal_geode", True, 0)

        self.damage = 5
        self.range = 10
    
    def tick(self, data, player, world):
        data["animations"].tick()

    def ignite(self, data, player, world, tile_pos, tile):
        data["animations"].create("explosion_progress", 18, lambda: self.detonate(data, player, world, tile_pos, tile))

    def detonate(self, data, player, world, tile_pos, tile):
        for entity in world.getEntitiesInRangeOfTile(tile_pos, self.range):
            entity.damage(self.damage)

        data["stack"].consume()
    
    def onLeft(self, data, player, world, tile_pos, tile):
        self.ignite(data, player, world, tile_pos, tile)
        return True

    def drawInWorld(self, data, surface, center):
        super().drawInWorld(data, surface, center)

        if data["animations"].exists("explosion_progress"):
            pygame.draw.circle(surface, (255, 255, 255), (surface.get_width()//2, surface.get_height()//2), data["animations"].getFrame("explosion_progress")**2*2)

        
GRENADES = []
Bomb().addToGroup(GRENADES)
