import pygame
import math

from misc import events
from ..classes import Entity, Creature, Enemy
from ...items import PlayerInventory, ItemStack
from ...world import GROUP_MANAGER

from constants import GAME


INITIAL_PLAYER_HEALTH = 10

class Player(Creature):    
    def __init__(self):
        super().__init__(INITIAL_PLAYER_HEALTH)

        self.loadHUD()
        self.loadInventory()
        self.initAttributes()

        self.disp = False

    def loadHUD(self):
        self.hud = PlayerHUD(self)

    def loadInventory(self):
        self.inventory = PlayerInventory()
        self.inventory.setPlayer(self)
        self.inventory.setItemStack(ItemStack("lil_sword", 45), 10)
        self.inventory.setItemStack(ItemStack("epic_sword", 35), 11)
        self.inventory.setItemStack(ItemStack("cool_sword", 12), 12)
        self.inventory.setItemStack(ItemStack("golf_club",1),1)
        self.inventory.setItemStack(ItemStack("knightmare_scythe",1),2)
        self.inventory.setItemStack(ItemStack("ice_blade",1),3)
        self.inventory.setItemStack(ItemStack("golf_club", 1), 1)
        self.inventory.setItemStack(ItemStack("soul_cannon",1),4)
        self.inventory.setItemStack(ItemStack("sanguine_slasher",1),5)
        self.inventory.setItemStack(ItemStack("lemon",1),18)
        self.inventory.setItemStack(ItemStack("apple",1),19)
        self.inventory.setItemStack(ItemStack("cosmic_mace",1),20)
        self.inventory.setItemStack(ItemStack("celestial_mace",1),21)
        self.inventory.setItemStack(ItemStack("lava_mace",1),22)
        self.inventory.setItemStack(ItemStack("kr1stal_mace",1),23)
        self.inventory.setItemStack(ItemStack("pizza_gun",1),16)
        self.inventory.setItemStack(ItemStack("crystal_raygun",1),6)
        self.inventory.setItemStack(ItemStack("bomb", 121), 7)
        self.inventory.setItemStack(ItemStack("basic_crossbow",1),17)

    def initAttributes(self):
        # Frames per movement
        self.defineAttribute("movement_speed", GAME.PLAYER_WALKING_SPEED)
        self.setAttribute("movement_speed", GAME.PLAYER_WALKING_SPEED)

        # Decimal number, outside -1 to +1 range causes problems, -5 to +5 is fatal
        self.defineAttribute("temperature", 0)
        self.setAttribute("temperature", 0)

        # Integer part represents its place in the bar chart
        # Rational part represents fullness
        self.defineAttribute("vibes", 2.0)
        self.setAttribute("vibes", 2.0)

        # 0 to 1
        # < 0.2 halves movement speed
        # < 0.1 causes screen shaking
        self.defineAttribute("hunger", 0)
        self.setAttribute("hunger", 1)

        # 0 to 1
        # < 0.8 fatal
        self.defineAttribute("oxygen", 1)
        self.setAttribute("oxygen", 1)

        # Integer from 0 to 5
        # 1 - Half movement speed
        # 2 - Half damage
        # 3 - No movement
        # 4 - No damage
        # 5 - Fatal
        self.defineAttribute("fatigue", 0)
        self.setAttribute("fatigue", 0)

        # 0 to 1
        # > 0.4 plays funny sound
        # > 1.0 teleports you to the final boss, half movement, controls flipped
        self.defineAttribute("insanity", 0)
        self.setAttribute("insanity", 0)

        # 0 to 1
        # 0 fatal
        self.defineAttribute("thirst", 1)
        self.setAttribute("thirst", 1)

    @staticmethod
    def getNeededAssets():
        return ["player1"]

    def setManager(self, manager):
        self.manager = manager

    def isPlayer(self):
        return True

    def getTemperaturePercentage(self):
        temp = self.getAttribute("temperature")
        return (temp+5)/10

    def temperatureTick(self):
        tileid = self.world.getTileID(self.pos)

        for group_name in GROUP_MANAGER.getGroupsWithTile(tileid):
            biome_temp = GROUP_MANAGER.getGroup(group_name).getExtras().get("temperature", 0)

            # Player temperature becomes 10% closer to biome temperature every tick
            self.setAttribute("temperature", (9*self.getAttribute("temperature")+temp)/10)

    def tick(self):
        super().tick()

        self.inventory.tick(self, self.world)

    def movementTick(self):
        super().movementTick()
        
        self.handleMotion()
        self.updateFacing()
        
    def damageTick(self):
        super().damageTick()

        for entity in self.world.getEntitiesInRangeOfTile(self.pos, 2):
            if entity.isItemEntity():
                self.inventory.addItemStack(entity.stack)
                entity.kill()
            
        self.inventory.damageTick(self, self.world)
        
    def finalTick(self):
        super().finalTick()

        self.inventory.damageTick(self, self.world)

    def move(self, delta):
        super().move(delta)
        
        self.world.registerChange()

    def getMovementSpeed(self):
        return self.getAttribute("movement_speed")

    def setMovementSpeed(self, speed):
        self.setAttribute("movement_speed", speed)

    def handleMotion(self):
        if self.isCooldownActive("movement_input"):
            return

        self.prev_pos = [self.pos[0], self.pos[1]]

        moved = False

        pressed = pygame.key.get_pressed()
        if pressed[GAME.CONTROLS_KEYS["up"]]:
            self.move(( 0, -1))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["left"]]:
            self.move((-1,  0))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["down"]]:
            self.move(( 0,  1))
            moved = True
        if pressed[GAME.CONTROLS_KEYS["right"]]:
            self.move(( 1,  0))
            moved = True


        ##DEBUG
        if pressed[pygame.K_i]:
            self.move(( 0, -10))
            moved = True
        if pressed[pygame.K_j]:
            self.move((-10,  0))
            moved = True
        if pressed[pygame.K_k]:
            self.move(( 0,  10))
            moved = True
        if pressed[pygame.K_l]:
            self.move(( 10,  0))
            moved = True
        ##

        if not self.world.isTileValidForWalking(self.pos):
            self.pos = self.prev_pos
            return

        if moved:
            self.registerCooldown("movement_input", self.getMovementSpeed())
            self.world.setMovingAnimation(self.movement_this_tick, lambda:self.getCooldownFrame("movement_input"))

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
        if key == pygame.K_t:
            self.inventory.throwSelectedStack(self.world, self.pos)

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

    def draw(self, display):
        pos = self.manager.bufferPosToScreenPos(self.getBufferPos())
        player_texture = self.atlas.getTexture("player1")

        rotated_texture = pygame.transform.rotate(player_texture, -self.facing_angle+90)

        rotated_rect = rotated_texture.get_rect(center=pos)
        display.blit(rotated_texture, rotated_rect.center)

        self.hud.draw(display)
        

class PlayerHUD(events.EventAcceptor):
    TOPLEFT_BAR_BOUNDS = pygame.Rect((10, 10), (500, 20))
    INVENTORY_POS = (1600, 100)
    
    def __init__(self, player):
        self.player = player

        self.item_rot = 0

    def onMouseDown(self, pos, button):
        used = 0
        
        # Inventory
        used += int(self.player.inventory.onMouseDown(pos, button, self.INVENTORY_POS))

        return bool(used)

    def drawBars(self, surface):
        current = self.TOPLEFT_BAR_BOUNDS

        

    def drawHealthBar(self, surface, pos):
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
