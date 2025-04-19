import color
import stddraw
import stdio
import stdarray
from picture import Picture
import math
import numpy as np

import utils.utils
from utils.utils import GameObject

class Missile(GameObject):
    def __init__(self, file, x, y, angle):

        self.frame = 0
        self.file = file

        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=self.frame))
        super().__init__(None, x, y, self.pic.width(), self.pic.height(), None)

        self.angle = np.radians(angle)
    def _draw(self):
        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=(self.frame % 50) // 10))
        stddraw.picture(self.pic, self.x, self.y)

        self.frame += 1


class MissileController:
    def __init__(self, file, player_height, screen_width, screen_height):
        # self.x0 = x0
        # self.y0 = y0

        self.file = file
        self.h = player_height
        self.missile = stdarray.create1D(
            500)  #2D array with 500 rows (for num of missiles) and 3 column (for y and x coordinates AND ANGLE)
        self.num_missiles = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def generate(self, x, y, angle):

        self.file = ("assets/missile/angle_" + str(angle))

        x -= math.sin(np.radians(angle)) * self.h / 2
        y -= self.h / 2 - (math.cos(np.radians(angle)) * self.h / 2)
        if self.num_missiles < 500:
            self.missile[self.num_missiles] = Missile(self.file, x, y, angle)
            self.missile[self.num_missiles].allow_draw = True
            self.num_missiles += 1

    def sequence(self):
        for i in range(self.num_missiles):
            self.y = self.missile[i].y  #stores starting position of missile
            self.x = self.missile[i].x
            self.angle = self.missile[i].angle

            self.missile[i].draw()

            #moves missile at an angle
            self.missile[i].x += 10 * np.sin(-self.angle)  #update y pos
            self.missile[i].y += 10 * np.cos(self.angle)  #update x pos

            if self.missile[i].x < 0 or self.missile[i].x > self.screen_width or self.missile[i].y < 0 or self.missile[i].y > self.screen_height:
                self.missile[i].allow_draw = False
