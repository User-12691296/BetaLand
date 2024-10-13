import json
import os
from ...entities import ENTITY_CLASSES as EC

SPAWNING_IDS = {"lava_knight":      EC.DessertKnight,
                "desert_raiders":   EC.DessertRaider}

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
