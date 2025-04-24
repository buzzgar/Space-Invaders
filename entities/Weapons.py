################################################
# Student Name: Ayesha Hofmeyer
# Student Number: 26990571
################################################

import math

import numpy as np
import stdarray
import stddraw
from picture import Picture

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
        self.file = file # stores image path
        
        #stores the image in self.pic which will  be used to initialise the heigth and width of the image 
        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=self.frame)) #replace {frame:03d} with self.frame as a 3 digit number 
        super().__init__(None, x, y, self.pic.width(), self.pic.height(), None) # retrieve width and height 

        self.angle = np.radians(angle)

    def _draw(self):
        # stores the specific frame for specific angle the missile is fired at. this will be used to generte the missile animation 
        # cycles through 5 frames at a speed of 1 frame every 10 sec 
        self.pic = Picture(self.file + "/frame_{frame:03d}.png".format(frame=(self.frame % 50) // 10)) 
        stddraw.picture(self.pic, self.x, self.y) #displays the frame 

        self.frame += 1 # increments self.frame so that animation changes to next frame next time _draw function is called
class MissileController:
    def __init__(self, file, player_height, screen_width, screen_height):
        self.file = file # stores image path
        self.h = player_height 
        
        self.missile = stdarray.create1D(1000) # array to trajactory od each new missilie fired 
        self.num_missiles = 0 # incerments when new missile fired

        self.screen_width = screen_width
        self.screen_height = screen_height

    def generate(self, x, y, angle):        
        self.angle = angle

        # centres the starting x and y positions of the missile to the centre of shooter 
        self.x -= math.sin(np.radians(self.angle)) * self.h / 2
        self.y -= self.h / 2 - (math.cos(np.radians(self.angle)) * self.h / 2)

        self.file = ("assets/missile/angle_" + str(angle)) # assigns self.file the directory path for the specific angle missile is to be fired at 

        # missile is added to array
        # once 1000 missile positions are stored in the array, self.num_missiles increments from zero again and overwrites old missile x,y with new missile positions
        self.missile[self.num_missiles % 1000] = Missile(self.file, self.x, self.y, self.angle) 
        self.missile[self.num_missiles % 1000].allow_draw = True # flags that missile can be drawn/visible 
        self.num_missiles += 1 # increments self.num_missiles each time new missile fired 

    def sequence(self):
        for i in range(self.num_missiles):
            # stores starting positions of new missile
            self.y = self.missile[i].y  
            self.x = self.missile[i].x
            self.angle = self.missile[i].angle

            # draws missile from curent stored position  
            self.missile[i].draw()

            # moves missile at the stipulated angle
            self.missile[i].x += 10 * np.sin(-self.angle) # update y pos trajcectory based on the given angle 
            self.missile[i].y += 10 * np.cos(self.angle)  # update x pos trajectroy based on the angle 

            # flags that missile cannot be drawn/visible 
            if self.missile[i].x < 0 or self.missile[i].x > self.screen_width or self.missile[i].y < 0 or self.missile[i].y > self.screen_height:
                self.missile[i].allow_draw = False


class Shield(GameObject):
    def __init__(self, file, x, y):
        self.file = file
        self.pic = Picture(self.file)
        super().__init__(None, x, y, self.pic.width(), self.pic.height(), None)

    def _draw(self):
        stddraw.picture(self.pic, self.x, self.y)


class ShieldController:

    def __init__(self):
        self.file = "assets/shield_resized.png"

        self.shield_active = False
        self.shield = None

    def visibility(self):  # ensures next time press key, opposite happens
        if self.shield_active:
            self.shield_active = False
        else:
            self.shield_active = True
        return self.shield_active

    def generate(self, x, y):

        if not self.shield_active:
            return False

        self.shield = Shield(self.file, x, y)

    def draw(self):
        if not self.shield_active:
            return False
        else:
            self.shield._draw()

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
