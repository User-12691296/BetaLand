import pygame
import os

class TextureAtlas:
    def __init__(self, path, ext, texture_size, asset_list, rescale=False):
        self.path = path
        self.ext = ext
        self.size = texture_size
        self.asset_list = asset_list
        self.rescale = False

        self.default = pygame.Surface(texture_size)

        self.createAtlas()

    def createAtlas(self):
        self.atlas = pygame.Surface((self.size[0]*len(self.asset_list), self.size[1]))

        for i, asset_name in enumerate(self.asset_list):
            path = os.path.join(self.path, asset_name+self.ext)
            self.loadTexture(i, path)
        
    def loadTexture(self, loc, filepath):
        texture = pygame.image.load(filepath).convert()

        if self.rescale:
            texture = pygame.transform.scale(texture, self.size)

        self.atlas.blit(texture, (loc*self.size[0], 0))

    def getAtlas(self):
        return self.atlas

    def getTextureAtLoc(self, loc):
        return self.atlas.subsurface(pygame.Rect((self.size[0]*loc, 0), self.size))

    def getTexture(self, asset_name):
        try:
            loc = self.asset_list.index(asset_name)
            return getTextureAtLoc(loc)
        except ValueError:
            return self.default

    def drawTextureAtLoc(self, surface, pos, loc):
        surface.blit(self.getTextureAtLoc(loc), pos)

    def drawTexture(self, surface, pos, asset_name):
        surface.blit(self.getTexture(asset_name), pos)
