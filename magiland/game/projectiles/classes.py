import pygame
import numpy as np
import math

from misc import events

from constants import GAME


class Projectile(events.EventAcceptor):
    def __init__(self, start, angle, speed):
        self.start = start
        self.angle = angle
        self.speed = speed

        self.pos = start

    @classmethod
    def fromStartEnd(self, start, end, speed):
        tx = end[0] - start[0]
        ty = end[1] - start[1]
        angle = math.atan2(ty, tx)

        return cls(start, angle, speed)

    def setWorld(self, world):
        self.world = world

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def getMovementDelta(self):
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)

        return (dx, dy)

    def tick(self): pass

    def movementTick(self):
        delta = self.getMovementDelta()
        self.move(delta)

    def damageTick(self): pass
    def finalTick(self): pass

    def draw(self, surface): pass
