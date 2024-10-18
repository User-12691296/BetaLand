from .damaging import DamageTile
from ...items.classes import ItemStack
from ...entities import ENTITY_CLASSES
from ...projectiles import PROJECTILE_CLASSES

class VolcanoLava(DamageTile):
    def __init__(self):
        super().__init__("volcanolava", "volcanolava", 0.2)
        self.items = {}

    def gatherAllIDS(self, world, tile_pos):
        self.items = {}
        
        for entity in world.getEntitiesInRange(5):
            if entity.isItem():
                ID = entity.stack.getItemID()
                self.items[ID] = self.items.get(ID, 0) + entity.stack.getCount()
                

    def onLeft(self,world,tile_pos):
        player = world.getPlayer()
        for item in self.items:
            entity = ItemStack(item, self.items[item])
        
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "red_gem" and entity.getRarity() == 0:
                entity.setRarity(1)
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "green_gem" and entity.getRarity() == 1:
                entity.setRarity(2)
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "blue_gem" and entity.getRarity() == 2:
                entity.setRarity(3)
            
class VolcanoMolten(DamageTile):
    def __init__(self):
        super().__init__("volcanomolten", "volcanomolten", 0.1)    

    def gatherAllIDS(self, world, tile_pos):
        self.items = {}
        for entity in world.getEntitiesInRange(5):
            if entity.isItem():
                ID = entity.stack.getItemID()
                self.items[ID] = self.items.get(ID, 0) + entity.stack.getCount()
                

    def onLeft(self,world,tile_pos):
        player = world.getPlayer()
        for item in self.items:
            entity = ItemStack(item, self.items[item])
        
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "red_gem" and entity.getRarity() == 0:
                entity.setRarity(1)
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "green_gem" and entity.getRarity() == 1:
                entity.setRarity(2)
            if entity.isUpgradeable() and player.inventory.getSelectedStack().getItemID() == "blue_gem" and entity.getRarity() == 2:
                entity.setRarity(3)

