import pygame
import numpy as np
import os

from misc import events
from misc.textures import TextureAtlas, getAllXFilesInFolder
from ..items import PlayerInventory, Inventory, ItemStack

ASSETS = os.path.join("assets", "game")


class Entity(events.EventAcceptor):
    def __init__(self):
        self.pos = [0, 0]

        self.cooldowns = {}

    def setWorld(self, world):
        self.world = world

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

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
    def __init__(self, health):
        super().__init__()
        
        self.max_health = health
        self.health = health

    def changeHealth(self, delta):
        self.health += delta

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

    def handleMotion(self):
        if self.isCooldownActive("movement_input"):
            return

        self.prev_pos = [self.pos[0], self.pos[1]]
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.pos[1] -= 1
        if pressed[pygame.K_a]:
            self.pos[0] -= 1
        if pressed[pygame.K_s]:
            self.pos[1] += 1
        if pressed[pygame.K_d]:
            self.pos[0] += 1

        self.disp = pressed[pygame.K_ESCAPE]

        if not self.world.isTileValidForWalking(self.pos):
            self.pos = self.prev_pos

        self.registerCooldown("movement_input", 1)

    def onKeyDown(self, key, unicode, mod):
        if key == pygame.K_e:
            self.inventory.changeSelectedStack(1)
        if key == pygame.K_q:
            self.inventory.changeSelectedStack(-1)

        if key == pygame.K_z:
            self.hud.rot += 10
        if key == pygame.K_c:
            self.hud.rot -= 10

    def onMouseDown(self, pos, button):
        # If anything uses the button, player will hog mouse input
        used = 0
        
        used += int(self.HUD.onMouseDown(pos, button))
        
        return bool(used)

    def worldClosed(self):
        self.inventory.close()
        
    def kill(self):
        pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))
            
    def getMapDelta(self):
        bpos = self.getBufferPos()
        return (-bpos[0], -bpos[1])

    def damage(self, damage):
        self.true_damage = self.calcDamageModifiers(damage)

        self.changeHealth(-self.true_damage)

        if self.health <= 0:
            self.kill()

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

        self.rot = 0

    def onMouseDown(self, pos, button):
        used = 0

        if pos[0] == 0 and pos[1] == 0:
            self.rot += 10
        
        # Inventory
        ipos = [pos[0], pos[1]]
        ipos[0] -= self.INVENTORY_POS[0]
        ipos[1] -= self.INVENTORY_POS[1]

        used += int(self.player.inventory.onMouseDown(ipos, button))

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
            stack.item.drawInWorld(surface,
                                   (pos[0]+self.player.world.TILE_SIZE[0]//2,
                                    pos[1]+self.player.world.TILE_SIZE[1]//2),
                                   self.rot,
                                   (64, -64))
        
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
        
