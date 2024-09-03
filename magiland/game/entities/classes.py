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
        self.movement_this_tick = [0, 0]
        
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

    def collidesWith(self, pos):
        return (self.pos[0] == pos[0] and self.pos[1] == pos[1])

    def distanceTo2(self, pos):
        return (self.pos[0]-pos[0])**2 + (self.pos[1]-pos[1])**2

    def diagonalTo(self, pos):
        return max(abs(self.pos[0]-pos[0]), abs(self.pos[1]-pos[1]))

    def move(self, delta):
        if self.movable:
            self.pos[0] += delta[0]
            self.pos[1] += delta[1]

            self.movement_this_tick[0] += delta[0]
            self.movement_this_tick[1] += delta[1]

    def setMovable(self, val):
        self.movable = val

    @staticmethod
    def getNeededAssets():
        return []

    # All entities of the same class share the same textures, but are loaded in different places
    @classmethod
    def setAtlas(cls, atlas):
        cls.atlas = atlas

    @classmethod
    def addToGroup(cls, group):
        group.append(cls)

    def isAlive(self):
        return self.alive

    def isItemEntity(self):
        return False

    def isCreature(self):
        return False

    def isPlayer(self):
        return False
    
    def isEnemy(self):
        return False

    def isEnemyTarget(self):
        return False
    
    def kill(self):
        self.alive = False

    def getBufferPos(self):
        return self.world.tilePosToBufferPos(self.pos)

    def registerCooldown(self, cooldown, frames):
        self.cooldowns[cooldown] = frames

    def getCooldownFrame(self, cooldown):
        return self.cooldowns.get(cooldown, 0)

    def isCooldownActive(self, cooldown):
        return self.cooldowns.get(cooldown, 0) > 0

    def tick(self):
        for cooldown in (*self.cooldowns.keys(),):
            self.cooldowns[cooldown] -= 1
            if self.cooldowns[cooldown] <= 0:
                del self.cooldowns[cooldown]

        self.movement_this_tick = [0, 0]

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

    def isCreature(self):
        return True

    def isEnemyTarget(self):
        return True

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

    def isEnemy(self):
        return True

    def isEnemyTarget(self):
        return False
    
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
        
        

