import json
import os
from ...entities import ENTITY_CLASSES as EC


SPAWNING_IDS = {"lava_knight":      EC.DessertKnight,
                "desert_raiders":   EC.DessertRaider,
                "darknessbronze_barrel": EC.DarknessBronze,
                "darknesssilver_barrel": EC.DarknessSilver,
                "darknessgold_barrel": EC.DarknessGold,
                "darknessplatinum_barrel": EC.DarknessPlat,
                "frozenbronze_barrel": EC.FrozenBronze,
                "frozensilver_barrel": EC.FrozenSilver,
                "frozengold_barrel": EC.FrozenGold,
                "frozenplatinum_barrel": EC.FrozenPlat,
                "crystalbronze_barrel": EC.CrystalBronze,
                "crystalsilver_barrel": EC.CrystalSilver,
                "crystalgold_barrel": EC.CrystalGold,
                "crystalplatinum_barrel": EC.CrystalPlat,
                "dessertbronze_barrel": EC.DessertBronze,
                "dessertsilver_barrel": EC.DessertSilver,
                "dessertgold_barrel": EC.DessertGold,
                "dessertplatinum_barrel": EC.DessertPlat,
                "mountainbronze_barrel": EC.MountainBronze,
                "mountainsilver_barrel": EC.MountainSilver,
                "mountaingold_barrel": EC.MountainGold,
                "mountainplatinum_barrel": EC.MountainPlat,
                "swampbronze_barrel": EC.SwampBronze,
                "swampsilver_barrel": EC.SwampSilver,
                "swampgold_barrel": EC.SwampGold,
                "swampplatinum_barrel": EC.SwampPlat,
                
                "crab_boss": EC.WormBoss,
                "hunger_crystal": EC.HungerCrystal
}

SPAWNING_TABLES_FILE = os.path.join("game", "world", "tilegroups", "spawning.json")

def initialiseSpawning():
    with open(SPAWNING_TABLES_FILE) as file:
        SPAWNING_REGISTRY.setSpawningTables(json.load(file))

class SpawningRegistry:
    def __init__(self):
        self.tables = {}

    def setSpawningTables(self, tables):
        self.tables = tables

    def getEntityClass(self, spawning_id):
        return SPAWNING_IDS[spawning_id]

    def createSpawningInstructions(self, spawning_id, loc):
        inst = {}
        inst["loc"] = loc
        inst["class"] = self.getEntityClass(spawning_id)
        return inst

    def getWorldTable(self, world_name):
        return self.tables.get(world_name, {})

    def getFixedSpawningInstructions(self, world_name, general=True):
        instructions = []

        world = self.getWorldTable(world_name).get("fixed", {})

        for spawning_id in world.keys():
            for loc in world[spawning_id]:
                instructions.append(self.createSpawningInstructions(spawning_id, loc))
        
        if general:
            all_ = self.getWorldTable("all").get("fixed", {})

            for spawning_id in all_.keys():
                for loc in all_[spawning_id]:
                    instructions.append(self.createSpawningInstructions(spawning_id, loc))

        return instructions

SPAWNING_REGISTRY = SpawningRegistry()
