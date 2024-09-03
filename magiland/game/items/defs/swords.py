from ..classes import Item
from misc import animations
import math

SWING_FRAMES = 10

class Sword(Item):
    def __init__(self, itemid, tex_name, damage, size, swing_angle=60, swing_range=None, player_damage_on_hit=0):
        #player_damage_on_hit can be postive/negative for healing effect
        super().__init__(itemid, tex_name, False, size)

        self.damage = damage
        self.swing_angle = swing_angle
        # player_damage_on_hit stuff
        self.player_damage_on_hit = player_damage_on_hit
        self.player_damage_on_hit_once = False
        
        if not swing_range:
            self.swing_range = self.size + 2

        else:
            self.swing_range = swing_range

    def initData(self):
        data = super().initData()

        data["dps"] = 3
        
        return data

    def tick(self, data, player, world):
        data["animations"].tick()

    def damageTick(self, data, player, world):
        # Handle Swing
        angle = data["animations"].getPercentage("sword_swing")*self.swing_angle
        delta = data["animations"].getDelta("sword_swing")*self.swing_angle
        
        data["rot"] = -round(angle) + (self.swing_angle//2) - (player.getFacing()+90) - 12
        data["rot"] = data["rot"] % 360


        if data["animations"].exists("sword_swing"):
            for entity in world.getEntitiesInRangeOfTile(player.pos, self.swing_range):
                if entity == player:
                    continue
                
                if entity in data["entities_hit"]:
                    continue
                    
                angle_to = (180-round(math.degrees(math.atan2(player.pos[1]-entity.pos[1], player.pos[0]-entity.pos[0]))))%360

                if (angle_to >= data["rot"] - delta + 45) and (angle_to < data["rot"] + 45):
                    entity.damage(self.damage)
                    data["entities_hit"].append(entity)
                    # this sets do to false so it only hits once and then do to true so never again (till startSwing)
                    if self.player_damage_on_hit_once==False:
                        player.damage(self.player_damage_on_hit)                        
                        self.player_damage_on_hit_once=True

    def startSwing(self, data, player, world, tile_pos, tile):
        player.setMovable(False)    
        data["animations"].create("sword_swing", SWING_FRAMES, lambda: self.endSwing(data, player, world, tile_pos, tile))
        data["entities_hit"] = []

         # this resets it every time type shi  
        self.player_damage_on_hit_once=False

    def endSwing(self, data, player, world, tile_pos, tile):
        player.setMovable(True)

    def onLeft(self, data, player, world, tile_pos, tile):
        self.startSwing(data, player, world, tile_pos, tile)
        return True


SWORDS = []
Sword("debug_sword", "sword", 1000, 2).addToGroup(SWORDS)
Sword("epic_sword", "emerald_studded_sword", 20, 2, 300, 5).addToGroup(SWORDS)
Sword("cool_sword", "ruby_studded_sword", 3, 0, 90, 3).addToGroup(SWORDS)
Sword("lil_sword", "sapphire_studded_sword", 2, 0, 20, 2).addToGroup(SWORDS)
Sword("golf_club", "golf_club", 20, 0, 300, 5, 1).addToGroup(SWORDS)
Sword ("knightmare_scythe", "knightmare_scythe", 15,2,360,6,0.2).addToGroup(SWORDS)
Sword ("ice_blade", "ice_blade", 5,2,75,4).addToGroup(SWORDS)
