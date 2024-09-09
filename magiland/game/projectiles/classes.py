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

    @classmethod
    def fromStartEnd(self, start, end, speed):
        tx = end[0] - start[0]
        ty = end[1] - start[1]
        angle = math.atan2(ty, tx)

        return cls(start, angle, speed)

    def getMovement(self):
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)

        return (dx, dy)

    def draw(self):
        
