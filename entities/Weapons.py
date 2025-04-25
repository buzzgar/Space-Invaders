################################################
# Student Name: Ayesha Hofmeyer
# Student Number: 26990571
################################################

import math

import numpy as np
import stdarray
import stddraw
from utils.PictureLoader import Picture

from utils.utils import GameObject


#from Gif import setup, draw_frames
class Canvas:
    def __init__(self, width, height):
        self.w = width
        self.h = height

    def setup(self):
        stddraw.setCanvasSize(700, 700)
        stddraw.clear(stddraw.GRAY)
        stddraw.setXscale(0.0, self.w)
        stddraw.setYscale(0.0, self.w)

class Missile(GameObject):
    def __init__(self, file, x, y, angle):

        self.frame = 0
        self.file = file

        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=self.frame))
        super().__init__(None, x, y, self.pic.width(), self.pic.height())

        self.angle = np.radians(angle)

    def _draw(self):
        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=(self.frame % 50) // 10))
        stddraw.picture(self.pic, self.x, self.y)

        self.frame += 1

class MissileController:
    def __init__(self, file, player_height, screen_width, screen_height):
        self.file = file
        self.h = player_height

        self.missile_count = 100

        # array to store missiles
        self.missile = stdarray.create1D(self.missile_count)
        self.num_missiles = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def generate(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.file = ("assets/missile/angle_" + str(angle))

        self.x -= math.sin(np.radians(angle)) * self.h / 2
        self.y -= self.h / 2 - (math.cos(np.radians(self.angle)) * self.h / 2)

        #missile is added to array
        self.missile[self.num_missiles % self.missile_count] = Missile(self.file, self.x, self.y, self.angle) #replaces old moissiles with new missile positions
        self.missile[self.num_missiles % self.missile_count].allow_draw = True
        self.num_missiles += 1

    def sequence(self):
        for i in range(min(self.num_missiles, self.missile_count)):
            # Checks if missile is out of bounds, no point in drawing or updating values
            if self.missile[i].x < 0 or self.missile[i].x > self.screen_width or self.missile[i].y < 0 or self.missile[i].y > self.screen_height:
                self.missile[i].allow_draw = False
                continue

            self.y = self.missile[i].y  #stores starting position of missile
            self.x = self.missile[i].x
            self.angle = self.missile[i].angle

            self.missile[i].draw()

            #moves missile at an angle
            self.missile[i].x += 10 * np.sin(-self.angle)  #update y pos
            self.missile[i].y += 10 * np.cos(self.angle)  #update x pos

class Shield(GameObject):
    def __init__(self):
        self.file = "assets/shield_resized.png"
        self.pic = Picture(self.file)
        super().__init__(None, 0, 0, self.pic.width(), self.pic.height())

    def visibility(self):  # ensures next time press key, opposite happens
        if self.allow_draw:
            self.allow_draw = False
        else:
            self.allow_draw = True

        return self.allow_draw
    def update_pos(self, x, y):
        self.x = x
        self.y = y
    def _draw(self):
        stddraw.picture(self.pic, self.x, self.y)

class AimController:
    def __init__(self):
        self.aim_active = False

        self.length = 500

    def visibility(self): #ensures next time press key, opposite happens
        if self.aim_active:
            self.aim_active = False
        else :
            self.aim_active = True
        return self.aim_active

    def generate(self, x, y, angle):
        self.x_start = x
        self.y_start = y
        self.angle = angle

        # calcuates x and y positiob given angle of player
        self.x_end = x + self.length * math.cos(self.angle)
        self.y_end = y + self.length * math.sin(self.angle)

    def draw(self):
        if not self.aim_active:
            return False
        else:
            stddraw.setPenColor(stddraw.RED)
            stddraw.line(self.x_start, self.y_start, self.x_end, self.y_end)