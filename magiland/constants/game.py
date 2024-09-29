import os
import pygame

#MAP
TILE_SIZE = 64
TILE_RESOLUTION = 16

MAX_BUFFER_SIZE = (1024, 1024)

CORNER_ROUNDING_ELEV_DELTA = 5
OPAQUE_TILE_ELEV_DELTA = 3
WALKING_TILE_ELEV_DELTA = 2

PLAYER_WALKING_SPEED = 5
SMOOTH_PLAYER_MOTION = True
PLAYER_INVENTORY_SIZE = 25
PLAYER_INVENTORY_WIDTH = 8

ORIGINAL_CONTROLS_KEYS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "left": pygame.K_a,
    "throw": pygame.K_t,
    "inventory right": pygame.K_e,
    "inventory left": pygame.K_q,
    "pause": pygame.K_RETURN
}

SOUND_VOLUMES = {
    "Music": 50,
    "Sound Effects": 50
}

CONTROLS_KEYS = ORIGINAL_CONTROLS_KEYS.copy()

ITEM_LOCATION_AROUND_PLAYER = (48, -48)
