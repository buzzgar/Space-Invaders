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

class Missile(GameObject):
    def __init__(self, file, x, y, angle):

        self.frame = 0
        self.file = file # stores image path

        # stores the image in self.pic which will  be used to initialise the height and width of the image
        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=self.frame)) # replace {frame:03d} with self.frame as a 3 digit number
        super().__init__(None, x, y, self.pic.width(), self.pic.height()) # initialise width and height of image

        self.angle = np.radians(angle)

    def _draw(self):
        # stores the specific frame for specific angle the missile is fired at. this will be used to generate the
        # missile animation cycles through 5 frames at a speed of 1 frame every 10 sec

        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=(self.frame % 50) // 10))
        stddraw.picture(self.pic, self.x, self.y) # displays the frame

        self.frame += 1 # increments self.frame so that animation changes to next frame next time _draw function is called

class MissileController:
    def __init__(self, player_height, screen_width, screen_height):
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

        # centres the starting x and y positions of the missile to the centre of shooter
        self.x -= math.sin(np.radians(self.angle)) * self.h / 2
        self.y -= self.h / 2 - (math.cos(np.radians(self.angle)) * self.h / 2)

        self.file = ("assets/missile/angle_" + str(angle)) # assigns self.file the directory path for the specific
        # angle missile is to be fired at

        # missile is added to array once 1000 missile positions are stored in the array, self.num_missiles increments
        # from zero again and overwrites old missile x,y with new missile positions
        self.missile[self.num_missiles % self.missile_count] = Missile(self.file, self.x, self.y, self.angle) #replaces old moissiles with new missile positions
        self.missile[self.num_missiles % self.missile_count].allow_draw = True # flags that missile can be drawn/visible
        self.num_missiles += 1 # increments self.num_missiles each time new missile fired

    def sequence(self):

        for i in range(min(self.num_missiles, self.missile_count)):
            # Checks if missile is out of bounds, no point in drawing or updating values
            if self.missile[i].x < 0 or self.missile[i].x > self.screen_width or self.missile[i].y < 0 or self.missile[i].y > self.screen_height:
                self.missile[i].allow_draw = False
                continue

            self.y = self.missile[i].y  #stores starting position of missile
            self.x = self.missile[i].x
            self.angle = self.missile[i].angle

            # draws missile from curent stored position
            self.missile[i].draw()

            # moves missile at the stipulated angle
            self.missile[i].x += 10 * np.sin(-self.angle) # update y pos trajectory based on the given angle
            self.missile[i].y += 10 * np.cos(self.angle)  # update x pos trajectory based on the angle

class Shield(GameObject):
    def __init__(self):
        self.file = "assets/shield_resized.png"
        self.pic = Picture(self.file) # stores image path
        super().__init__(None, 0, 0, self.pic.width(), self.pic.height()) # stores the image in self.pic which will
        # be used to initialise the heigth and width of the image

    def visibility(self):  # ensures next time press key, self.sheild_active flag inverts. so if shield active,
        # pressing key again with set the flag to false
        if self.allow_draw:
            self.allow_draw = False
        else:
            self.allow_draw = True

        return self.allow_draw

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def _draw(self):
        stddraw.picture(self.pic, self.x, self.y) # dispalys sheild image

class AimController:
    def __init__(self):
        self.aim_active = False # flag that tracks when aim is visible/drawn

        self.length = 500 # length of line

    def visibility(self): # ensures next time press key, self.aim_active flag inverts. so if shield active, pressing
        # key again with set the flag to false

        if self.aim_active:
            self.aim_active = False
        else :
            self.aim_active = True
        return self.aim_active

    def generate(self, x, y, angle):
        self.x_start = x
        self.y_start = y
        self.angle = angle

        # calculates x and y position given angle of player
        self.x_end = x + self.length * math.cos(self.angle)
        self.y_end = y + self.length * math.sin(self.angle)

    def draw(self):
        if not self.aim_active: # if shield aim flag is false, line not drawn
            return False
        else:
            stddraw.setPenColor(stddraw.RED)
            stddraw.line(self.x_start, self.y_start, self.x_end, self.y_end) # draws angled line at shooter's current x and y posiiton
