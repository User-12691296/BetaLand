import pygame
import numpy as np
import math
import os

from misc import events
from misc.textures import TextureAtlas, getAllXFilesInFolder
from ..items import PlayerInventory, Inventory, ItemStack

#ASSETS = os.path.join("assets", "game")


class Entity(events.EventAcceptor):
    def __init__(self):
        self.pos = [0, 0]

        self.cooldowns = {}

        self.movable = True

    def setWorld(self, world):
        self.world = world

    def onSpawn(self):
        pass

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def move(self, delta):
        if self.movable:
            self.pos[0] += delta[0]
            self.pos[1] += delta[1]

    def setMovable(self, val):
        self.movable = val

    @staticmethod
    def getNeededAssets():
        return tuple()

    # All entities of the same class share the same textures, but are loaded in different places
    @classmethod
    def setAtlas(cls, atlas):
        cls.atlas = atlas

    def kill(self):
        self.world.removeEntity(self)

    def getBufferPos(self):
        return self.world.tilePosToBufferPos(self.pos)

    def registerCooldown(self, cooldown, frames):
        self.cooldowns[cooldown] = frames

    def isCooldownActive(self, cooldown):
        return self.cooldowns.get(cooldown, False)

    def tick(self):
        for cooldown in self.cooldowns.keys():
            self.cooldowns[cooldown] -= 1
        
    def draw(self, surface): pass

class Creature(Entity):
    def __init__(self, health, size=(1, 1)):
        super().__init__()
        
        self.max_health = health
        self.health = health

        self.size = size

        self.hitbox = pygame.Rect((0, 0), size)

    def onSpawn(self):
        super().onSpawn()

    def changeHealth(self, delta):
        self.health += delta

    def updateHitbox(self):
        self.hitbox.center = self.getPos()

    def collidesWith(self, point):
        return self.hitbox.collidepoint(point)

    def tick(self):
        super().tick()

        self.updateHitbox()

    def damage(self, damage):
        self.true_damage = self.calcDamageModifiers(damage)

        self.changeHealth(-self.true_damage)

        if self.health <= 0:
            self.kill()

    def kill(self):
        self.world.killEntity(self)

    def calcDamageModifiers(self, damage):
        return damage # No changes to damage, can be overridden for entities with armor



INITIAL_PLAYER_HEALTH = 10

class Player(Creature):    
    def __init__(self):
        super().__init__(INITIAL_PLAYER_HEALTH)

        self.loadHUD()
        self.loadInventory()

        self.disp = False

    def loadHUD(self):
        self.hud = PlayerHUD(self)

    def loadInventory(self):
        self.inventory = PlayerInventory()
        self.inventory.setPlayer(self)
        self.inventory.setItemStack(ItemStack("lil_sword", 45), 10)
        self.inventory.setItemStack(ItemStack("epic_sword", 35), 11)
        self.inventory.setItemStack(ItemStack("cool_sword", 12), 12)

    @staticmethod
    def getNeededAssets():
        return ["player1"]

    def setManager(self, manager):
        self.manager = manager

    def tick(self):
        super().tick()
        
        self.handleMotion()

        self.facing = self.getFacing()

        self.inventory.tick(self, self.world)

    def handleMotion(self):
        if self.isCooldownActive("movement_input"):
            return

        self.prev_pos = [self.pos[0], self.pos[1]]
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.move(( 0, -1))
        if pressed[pygame.K_a]:
            self.move((-1,  0))
        if pressed[pygame.K_s]:
            self.move(( 0,  1))
        if pressed[pygame.K_d]:
            self.move(( 1,  0))

        self.disp = pressed[pygame.K_ESCAPE]

        if not self.world.isTileValidForWalking(self.pos):
            self.pos = self.prev_pos

        self.registerCooldown("movement_input", 1)

    def getFacing(self):
        mouse_loc = self.world.bufferPosToTilePos(self.manager.screenPosToBufferPos(pygame.mouse.get_pos()))
        angle = math.atan2(mouse_loc[1]-self.pos[1], mouse_loc[0]-self.pos[0])-45

        return (math.degrees(angle))

    def onKeyDown(self, key, unicode, mod):
        if key == pygame.K_e:
            self.inventory.changeSelectedStack(1)
        if key == pygame.K_q:
            self.inventory.changeSelectedStack(-1)

    def onMouseDown(self, pos, button):
        # If anything uses the button, player will hog mouse input
        used = 0
        
        used += int(self.hud.onMouseDown(pos, button))
        
        return bool(used)

    def worldClosed(self):
        self.inventory.close()
        
    def kill(self):
        pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))
            
    def getMapDelta(self):
        bpos = self.getBufferPos()
        return (-bpos[0], -bpos[1])

    def getHealth(self):
        return self.health

    def getHealthPercentage(self):
        return self.health/self.max_health

    def draw(self, surface):
        # Draw player sprite
        pos = self.manager.bufferPosToScreenPos(self.getBufferPos())
        self.atlas.drawTexture(surface, pos, "player1")

        # Draw GUI
        self.hud.draw(surface)

class PlayerHUD(events.EventAcceptor):
    HEALTH_BAR_BOUNDS = pygame.Rect((10, 10), (500, 20))
    INVENTORY_POS = (1600, 100)
    
    def __init__(self, player):
        self.player = player

        self.item_rot = 0

    def onMouseDown(self, pos, button):
        used = 0
        
        # Inventory
        used += int(self.player.inventory.onMouseDown(pos, button, self.INVENTORY_POS))

        return bool(used)

    def drawHealthBar(self, surface):
        bar = self.HEALTH_BAR_BOUNDS

        # Background
        pygame.draw.rect(surface, (128, 128, 128), bar)

        # Health stats
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(bar.topleft, (bar.width*self.player.getHealthPercentage(), bar.height)))

    def drawInventory(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        self.player.inventory.draw(surface, self.INVENTORY_POS)
        self.player.inventory.drawActiveStack(surface, mouse_pos)

        self.drawHandHeld(surface)

    def drawHandHeld(self, surface):
        stack = self.player.inventory.getSelectedStack()

        if stack:
            pos = self.player.manager.bufferPosToScreenPos(self.player.getBufferPos())
            stack.drawInWorld(surface,
                                   (pos[0]+self.player.world.TILE_SIZE[0]//2,
                                    pos[1]+self.player.world.TILE_SIZE[1]//2))
        
    def draw(self, surface):
        self.drawHealthBar(surface)
        self.drawInventory(surface)


class TestCreature(Creature):
    def __init__(self):
        super().__init__(10)

    @staticmethod
    def getNeededAssets():
        return ["enemy1"]

    def draw(self, surface):
        self.atlas.drawTexture(surface, self.world.tilePosToBufferPos(self.pos), "enemy1")
        

class Enemy(Creature):
    def __init__(self, health):
        super().__init__(health)

    def onSpawn(self):
        super().onSpawn()
        pass
        
class Slime(Enemy):
    def __init__(self):
        super().__init__(5)

    @staticmethod
    def getNeededAssets():
        return ["slime"]

    def draw(self, surface):
        self.atlas.drawTexture(surface, self.world.tilePosToBufferPos(self.pos), "slime")
