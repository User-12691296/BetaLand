from ..classes import Enemy
from constants.game import TILE_SIZE
from constants.assets import BOSS_PATH
import pygame
import random
import math
import os
from ...projectiles import PROJECTILE_CLASSES
from .darknessenemies import DarknessKnightmare1

class CrabBoss (Enemy):
    def __init__(self):
        super().__init__(100, 2, 8)
        self.size = (5,5)
        self.radius = 5
        self.hitbox = pygame.Rect((0, 0), self.size)
        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "DIAMONDKINGCRAB.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

    @staticmethod
    def getNeededAssets():
        return ["DIAMONDKINGCRAB"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.1)

    def movementTick(self):
        if self.attack_pattern == 0 or self.attack_pattern == 2:
            super().movementTick()
        else:
            pass

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().pos
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern)

    def updatePositionForPattern1(self):
        self.x = self.initial_player_pos[0] + round(5*math.cos(math.radians(self.attack_progress*20)))
        self.y = self.initial_player_pos[1] + round(5*math.sin(math.radians(self.attack_progress*20)))
        self.setPos([self.x, self.y])
        if self.attack_progress > 360/5:
           self.attack_progress = 0
           self.attack_pattern = 0
           self.registerCooldown("attack_pattern_cooldown", 120)

    def handleAttacksForPattern1(self):
        pass

    def updatePositionForPattern2(self):
        self.setAttribute("movement_speed", self.normal_movement_speed/2)
        if self.attack_progress > 100:
            self.setAttribute("movement_speed", self.normal_movement_speed)
            self.attack_progress = 0
            self.attack_pattern = 0
            self.registerCooldown("attack_pattern_cooldown", 120)        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        # HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))

# FINAL BOSSES
class CraneBoss (Enemy):
    def __init__(self):
        super().__init__(200, 2, 8)
        self.size = (5,5)
        self.radius = 2
        self.hitbox = pygame.Rect((0, 0), self.size)
        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "KungFuKrane.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()


    @staticmethod
    def getNeededAssets():
        return ["KungFuKrane"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.size[0]-1):
            if not entity.isEnemy():
                entity.damage(0.2)

    def movementTick(self):
        if self.attack_pattern == 0:
            super().movementTick()
        else:
            pass

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 2)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().pos
            
        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        if self.attack_pattern == 2:
            self.updatePositionForPattern2()
            self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

        # print(self.attack_progress, self.attack_pattern, self.getCooldownFrame("attack_pattern_cooldown"))

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        


    def updatePositionForPattern1(self):
        self.x = self.initial_player_pos[0] + round(5*math.cos(math.radians(self.attack_progress*20)))
        self.y = self.initial_player_pos[1] + round(5*math.sin(math.radians(self.attack_progress*20)))
        self.setPos([self.x, self.y])
        if self.attack_progress > 360/5:
           self.attack_progress = 0
           self.attack_pattern = 0
           self.registerCooldown("attack_pattern_cooldown", 120)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 4
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.Arrow(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)

        self.registerCooldown("bullets", 10)

    def updatePositionForPattern2(self):
        speed = 1
        self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
        self.y = self.initial_player_pos[1]
        self.setPos((self.x, self.y))
        if self.attack_progress > 40*speed:
            self.clearAttributes(100)

    def handleAttacksForPattern2(self):
        self.handleAttacksForPattern1()
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))

        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))

class WhaleBoss (Enemy):
    def __init__(self):
        super().__init__(200, 2, 8)
        self.size = (9,9)
        self.radius = 2
        self.hitbox = pygame.Rect((0, 0), self.size)
        self.attack_pattern = 0
        self.attack_progress = 0

        self.x, self.y = 0,0
        self.normal_movement_speed = 8

        self.image = pygame.image.load(os.path.join(BOSS_PATH, "DarknessWhaleBoss.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image_rect = self.image.get_rect()

        self.active = True

    @staticmethod
    def getNeededAssets():
        return ["DarknessWhaleBoss"]

    def isEnemy(self):
        return True
    
    def isBoss(self):
        return True

    def damageTick(self):
        if self.active:
            for entity in self.world.getEntitiesInRangeOfTile(self.pos, self.radius+1):
                if not entity.isEnemy():
                    entity.damage(0.5)


    def movementTick(self):
        pass

    def tick(self):
        super().tick()
        if self.attack_pattern == 0 and not self.isCooldownActive("attack_pattern_cooldown"):
            self.attack_pattern = random.randint(1, 1)
            self.attack_progress = 1
            self.initial_player_pos = self.world.getPlayer().pos.copy()
            if self.attack_pattern == 1:
                self.active = False
                self.alpha = 1
                self.pos = self.initial_player_pos
                self.registerCooldown("bullets", 10)


        if self.attack_pattern == 1:
            self.updatePositionForPattern1()
            self.handleAttacksForPattern1()

        # if self.attack_pattern == 2:
        #     self.updatePositionForPattern2()
        #     self.handleAttacksForPattern2()

        if self.attack_progress > 0:
            self.attack_progress += 1

    def clearAttributes(self, cooldown):
        self.attack_progress = 0
        self.attack_pattern = 0
        self.registerCooldown("attack_pattern_cooldown", cooldown)        

    def updatePositionForPattern1(self):
        if not self.active:
            self.alpha = self.attack_progress*7

            if self.alpha > 255:
                self.alpha = 255
                self.active = True
                self.clearAttributes(40)

    def handleAttacksForPattern1(self):
        if self.isCooldownActive("bullets"): 
            return

        number_of_bullets = 8
        variance = random.randint(0,45)
        for i in range(number_of_bullets):
            angle = (360/number_of_bullets)*i+variance
            pos = self.pos
            self.projectile = PROJECTILE_CLASSES.Arrow(pos, angle)
            self.projectile.giveImmunity(self)
            self.world.addProjectile(self.projectile)
        
        eagle = DarknessKnightmare1()
        eagle.setPos((self.pos[0] + random.randint(5,10)*(random.randint(0,1)*2-1), self.pos[1]+random.randint(5,10)*(random.randint(0,1)*2-1)))
        counter = 0
        while len(self.world.getEntitiesOnTile(eagle.pos)) > 1 or counter < 5:
            eagle.setPos((self.pos[0] + random.randint(5,10)*(random.randint(0,1)*2-1), self.pos[1]+random.randint(5,10)*(random.randint(0,1)*2-1)))
            counter+=1
        if counter != 5:
            self.world.addEntity(eagle)


        self.registerCooldown("bullets", 25)

    # def updatePositionForPattern2(self):
    #     speed = 1
    #     self.x = self.initial_player_pos[0]-20 + self.attack_progress//speed
    #     self.y = self.initial_player_pos[1]
    #     self.setPos((self.x, self.y))
    #     if self.attack_progress > 40*speed:
    #         self.clearAttributes(100)

    # def handleAttacksForPattern2(self):
    #     self.handleAttacksForPattern1()
        

    def draw(self, display, display_topleft=(0, 0)):
        self.updateHitbox()
        self.radius = 5
        bpos = self.world.tilePosToBufferPos(self.pos)
        spos = self.bufferPosToDisplayPos(bpos, display_topleft)

        # entity_texture = self.atlas.getTexture("DIAMONDKINGCRAB")
        rotated_image = pygame.transform.rotate(self.image, -self.facing_angle+90)
        final_rect = rotated_image.get_rect(center=spos)
        # final_texture = pygame.transform.scale(rotated_texture, (self.size[0]*TILE_SIZE, self.size[1]*TILE_SIZE))
        rotated_image.set_alpha(self.alpha)
        # final_rect = final_texture.get_rect(center=spos)
        display.blit(rotated_image, final_rect)

        HELP = self.bufferPosToDisplayPos(self.world.tilePosToBufferPos(self.hitbox.topleft), display_topleft)
        # pygame.draw.rect(display, (255,0,0,0.2), pygame.rect.Rect(HELP[0], HELP[1], 5*TILE_SIZE, 5*TILE_SIZE))
    

"""
def tick(self):
  super().tick()

  if self.attack_pattern == 0:
    self.attack_pattern = random.randint(1, 5)
    self.attack_progress = 0
    self.initial_player_pos = player.pos
  
  if self.attack_pattern == 1:
    self.updatePositionForPattern1()
    self.handleAttacksForPattern1()

  if self.attack_pattern == 2:
    ...
  
  self.attack_progress += 1

def updatePositionForPattern1(self):
  # Circle around the player with a radius of 10 tiles
  # For smooth motion or entity rotation, you'd have to run this code twice to figure out how much it's moved, then call self.move instead of just hard-setting the position
  self.x = self.initial_player_pos[0] + round(10*math.cos(self.attack_progress/360))
  self.y = self.initial_player_pos[1] + round(10*math.sin(self.attack_progress/360))

def updatePositionForPattern2(self):
  # Fly across the screen over the player - if the screen is 40 tiles wide this would be 1.25 seconds
  self.x = self.attack_progress//2
  self.y = self.initial_player_pos.pos[1]

def handleAttacksForPattern1(self):
  # Run a fireball attack with a cooldown
  # You could also have an if statement here, and only run this attack when it's in the middle of the screen
  # This would have it constantly firing every time the cooldown refreshes
  self.fireballCircle()

def fireballCircle(self):
  if self.isCooldownActive("fireball_circle"): # Part of the entity class
    return

  for i in range(8):
    angle = 45*i
    pos = self.pos
    self.world.addProjectile(pos, angle, "fireball")

  self.addCooldown("fireball_circle", 120)
"""