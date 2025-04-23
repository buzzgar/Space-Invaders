import time

import color
import stddraw
import stdio
import stdarray
from picture import Picture
import math
import numpy as np

import utils.utils
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

class ShieldController:
    def __init__(self, file, player_height, screen_width, screen_height):
        self.file = file  # Store the image path ("assets/shield.webp")
        self.player_height = player_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_shield = None  # Track the active shield

    def generate(self, x, y, angle):
        # Calculate adjusted position (so shield orbits the player)
        adjusted_x = x - math.sin(np.radians(angle)) * self.player_height / 2
        adjusted_y = y - (self.player_height / 2 - math.cos(np.radians(angle)) * self.player_height / 2)

        # Create or update the shield
        if self.active_shield is None:
            self.active_shield = Shield(self.file, adjusted_x, adjusted_y, angle)
        else:
            # Update existing shield's position/angle
            self.active_shield.x = adjusted_x
            self.active_shield.y = adjusted_y
            self.active_shield.angle = np.radians(angle)

        return self.active_shield

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
        self.file = file
        self.h = player_height
        self.missile = stdarray.create1D(
            500)  #2D array with 500 rows (for num of missiles) and 3 column (for y and x coordinates AND ANGLE)
        self.num_missiles = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.aimline_draw = False #checks if must generate aimline

    def generate(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.file = ("assets/missile/angle_" + str(angle))

        self.x -= math.sin(np.radians(angle)) * self.h / 2
        self.y -= self.h / 2 - (math.cos(np.radians(self.angle)) * self.h / 2)
        if self.num_missiles < 500:
            self.missile[self.num_missiles] = Missile(self.file, self.x, self.y, self.angle)
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

        self.x_end = x + self.length * math.cos(self.angle)
        self.y_end = y + self.length * math.sin(self.angle)

    def draw(self):
        if not self.aim_active:
            return False
        else:
            stddraw.setPenColor(stddraw.RED)
            stddraw.line(self.x_start, self.y_start, self.x_end, self.y_end)