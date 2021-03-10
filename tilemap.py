import pygame as pg
from settings import *

# By default, the collide method uses the default rect of the player.
# We create this custom method to compare the player's 'hit_rect' instead.
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())  # ignore \n chars to avoid extra tiles on map

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.centerx + int(WINDOW_WIDTH / 2)
        y = -target.rect.centery + int(WINDOW_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left hand side
        y = min(0, y)  # top
        x = max(-(self.width - WINDOW_WIDTH), x)  # right side
        y = max(-(self.height - WINDOW_HEIGHT), y)  # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)