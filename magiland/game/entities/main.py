import pygame
import numpy as np
import math
import os

from misc import events
from misc.textures import TextureAtlas, getAllXFilesInFolder
from ..items import PlayerInventory, Inventory, ItemStack
from .pathfinding import PathFinder

from constants import GAME


class Entity(events.EventAcceptor):
    def __init__(self):
        self.pos = [0, 0]

        self.cooldowns = {}

        self.movable = True
        self.alive = True

    def setWorld(self, world):
        self.world = world

    def setOpaques(self, opaques):
        pass

    def onSpawn(self):
        pass

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def distanceTo2(self, pos):
        return (self.pos[0]-pos[0])**2 + (self.pos[1]-pos[1])**2

    def diagonalTo(self, pos):
        return max(abs(self.pos[0]-pos[0]), abs(self.pos[1]-pos[1]))

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

    def isAlive(self):
        return self.alive

    def isEnemy(self):
        return False
    
    def kill(self):
        self.alive = False

    def getBufferPos(self):
        return self.world.tilePosToBufferPos(self.pos)

    def registerCooldown(self, cooldown, frames):
        self.cooldowns[cooldown] = frames

    def isCooldownActive(self, cooldown):
        return self.cooldowns.get(cooldown, 0) > 0

    def tick(self):
        for cooldown in (*self.cooldowns.keys(),):
            self.cooldowns[cooldown] -= 1
            if self.cooldowns[cooldown] <= 0:
                del self.cooldowns[cooldown]

    def movementTick(self): pass
    def damageTick(self): pass
    def finalTick(self): pass
    
    def draw(self, surface): pass

class Creature(Entity):
    def __init__(self, health, size=(1, 1)):
        super().__init__()
        
        self.max_health = health
        self.health = health

        self.size = size

        self.hitbox = pygame.Rect((0, 0), size)

        self.damages_this_tick = []

    def onSpawn(self):
        super().onSpawn()

    def getHealth(self):
        return self.health

    def getHealthPercentage(self):
        return self.health/self.max_health

    def changeHealth(self, delta):
        self.health += delta
        self.health = min(self.max_health, self.health)

        if self.health <= 0:
            self.kill()

    def updateHitbox(self):
        self.hitbox.center = self.getPos()
        self.radius = self.hitbox.width//2

    def collidesWith(self, point):
        return self.hitbox.collidepoint(point)

    def distanceTo2(self, pos):
        dx = abs(self.pos[0]-pos[0])
        dy = abs(self.pos[1]-pos[1])

        return dx**2 - (self.radius * 2*dx) + dy**2 - (self.radius * 2*dy)

    def tick(self):
        super().tick()

        self.damages_this_tick = []

    def movementTick(self):
        super().movementTick()
        
        self.updateHitbox()

    def damageTick(self):
        super().damageTick()

    def finalTick(self):
        super().finalTick()

        self.sumDamage()

    def damage(self, damage, source=None):
        self.damages_this_tick.append((damage, source))

    def sumDamage(self):
        total_damage = 0

        dtt = 0

        while self.damages_this_tick:
            damage = max(self.damages_this_tick, key=lambda d: d[0])
            self.damages_this_tick.remove(damage)

            damage, source = damage
            true_damage = self.calcDamageModifiers(damage, dtt)
            total_damage += true_damage

            dtt += 1
        
        self.changeHealth(-total_damage)

    def calcDamageModifiers(self, damage, dtt=0):
        return (damage/(2**dtt))

    def draw(self, surface):
        self.drawHealthBar(surface)

    def drawHealthBar(self, surface):
        width = GAME.TILE_SIZE
        health_bar = pygame.Rect((0, 0), (width, 10))

        bpos = self.world.tilePosToBufferPos(self.getPos())

        health_bar.left = bpos[0]
        health_bar.top = bpos[1] - 20

        # Background
        pygame.draw.rect(surface, (255, 0, 0), health_bar)

        # Foreground
        health_bar.width = round(width*self.getHealthPercentage())
        pygame.draw.rect(surface, (0, 255, 0), health_bar)


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

        self.inventory.tick(self, self.world)

    def movementTick(self):
        super().movementTick()
        
        self.handleMotion()
        self.updateFacing()
        
    def damageTick(self):
        super().damageTick()

        self.inventory.damageTick(self, self.world)
        
    def finalTick(self):
        super().finalTick()

        self.inventory.damageTick(self, self.world)

    def move(self, delta):
        super().move(delta)
        
        self.world.registerChange()

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

        if not self.world.isTileValidForWalking(self.pos):
            self.pos = self.prev_pos

        self.registerCooldown("movement_input", 1)

    def updateFacing(self):
        if self.movable:
            mouse_loc = self.world.bufferPosToTilePos(self.manager.screenPosToBufferPos(pygame.mouse.get_pos()))
            angle = math.atan2(mouse_loc[1]-self.pos[1], mouse_loc[0]-self.pos[0])-45

            self.facing = math.degrees(angle)

    def getFacing(self):
        return self.facing

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
        self.alive = False
        
        pygame.event.post(pygame.event.Event(events.RETURN_TO_MAIN_MENU))
            
    def getMapDelta(self):
        bpos = self.getBufferPos()
        return (-bpos[0], -bpos[1])

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
        super().draw(surface)
        
        self.atlas.drawTexture(surface, self.world.tilePosToBufferPos(self.pos), "enemy1")
        

class Enemy(Creature):
    def __init__(self, health, stop_range=1, movement_speed=10):
        super().__init__(health)

        self.stop_range = stop_range
        self.movement_speed = movement_speed

    def setWorld(self, world):
        super().setWorld(world)

        self.pathfinder = PathFinder(self.world.size, self.stop_range)

    def setOpaques(self, opaques):
        super().setOpaques(opaques)

        self.pathfinder.setOpaques(opaques)

    def onSpawn(self):
        super().onSpawn()

        self.calcPath()

    def calcPath(self):
        self.pathfinder.calcPath(self.getPos(), self.world.getPlayer().getPos())

    def movementTick(self):
        super().movementTick()

        if self.world.changes_this_tick:
            self.calcPath()

        if self.isCooldownActive("movement"):
            return
        
        node = self.pathfinder.getNode()    
        if node:
            self.setPos(node)

        self.registerCooldown("movement", self.movement_speed)
        
        
class Slime(Enemy):
    def __init__(self):
        super().__init__(5, 0, 30)

    @staticmethod
    def getNeededAssets():
        return ["slime"]

    def isEnemy(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 1.5):
            if not entity.isEnemy():
                entity.damage(0.1)

    def draw(self, surface):
        super().draw(surface)
        
        self.atlas.drawTexture(surface, self.world.tilePosToBufferPos(self.pos), "slime")
