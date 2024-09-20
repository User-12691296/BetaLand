import os
import pygame
import numpy
import json

IMAGE_PATH = "level3whysitcalledthis.png"
WORLD_NAME = "level_3"
LEVELS_PATH = "levels.json"

TILE_SEP = ";"
TILE_DATA_SEP = ","
SIZE_STORAGE = "size"
ROWS_STORAGE = "tiles"

IGNORE_TILE_VAL = "error"
RG_DEFS = {(0, 0): IGNORE_TILE_VAL,
           (0, 255):"grass",
           (255, 0):"barrier",
           (15,15):"darkwall",
           (5, 5): "deepdark",
           (255, 245): "sand",
           (245, 255): "sandlight",
           (255, 200): "sanddark",
           (200, 255): "sandoasis",
           (100, 100): "kr1stalfloor",
           (100, 0): "kr1stalrunes",
           (0, 100): "kr1stal",
           (160, 250): "snow",
           (160, 200): "snow2",
           (150, 150): "swamp",
           (150, 0): "swampaccent",
           (0, 150): "swampwater",
           (50, 50): "mountain",
           (50, 0): "mountainsnow",
           (0, 50): "mountainsnowier",
           (200, 200): "volcano",
           (200, 0): "volcanolava",
           (0, 200): "volcanorock",
           (1,1):"black"}
            


with open(LEVELS_PATH, "r") as levels_file:
    levels = json.load(levels_file)


image = pygame.image.load(IMAGE_PATH)
size = image.get_rect().size

def createTile(tileid, elevation):
    """Return the string that represents the tile in the levels file"""
    data = TILE_DATA_SEP.join((tileid, str(elevation)))

    return data + TILE_SEP

def getElevationFromB(B):
    """If even, take at face value, if odd then square it"""
    if B%2 == 0:
        return B

    else:
        return B**2


rows = {}
for tile_y in range(size[1]):
    row = ""
    for tile_x in range(size[0]):
        tile_raw = image.get_at((tile_x, tile_y))

        RG = tile_raw[0:2]
        B = tile_raw[2]

        tileid = RG_DEFS.get(RG, IGNORE_TILE_VAL)

        if tileid != IGNORE_TILE_VAL:
            elevation = getElevationFromB(B)

            tile_data = createTile(tileid, elevation)

            row += tile_data

        else:
            row += createTile(IGNORE_TILE_VAL, 0)

    rows[tile_y] = row

level = {SIZE_STORAGE:size, ROWS_STORAGE:rows}

levels[WORLD_NAME] = level

with open(LEVELS_PATH, "w") as levels_file:
    json.dump(levels, levels_file)

