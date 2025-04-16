import stddraw 
import stdio 
import stdarray
from picture import Picture
import math
import numpy as np
from scipy.ndimage import rotate
from utils.utils import GameObject


#from Gif import setup, draw_frames
class Canvas: 
    def __init__(self, width, height):
        self.w = width 
        self.h = height

    def setup(self): 
        stddraw.setCanvasSize(700,700)
        stddraw.clear(stddraw.GRAY)
        stddraw.setXscale(0.0,self.w)
        stddraw.setYscale(0.0,self.w)

class Missile(GameObject):
    def __init__(self, file, x, y, angle):
        self.pic = Picture(file)
        super().__init__(None, x, y, self.pic.width(), self.pic.height(), None)

        self.angle = np.radians(angle)


    def _draw(self):
        stddraw.picture(self.pic, self.x, self.y)

class MissileController:
    def __init__(self, file, player_height):
        # self.x0 = x0
        # self.y0 = y0

        self.file = file
        self.h = player_height
        self.missile = stdarray.create1D(500) #2D array with 500 rows (for num of missiles) and 3 column (for y and x coordinates AND ANGLE)
        self.num_missiles = 0
    
    def generate(self,x,y,angle):

        self.file = ("assets/missile/rotated_" + str(angle) + ".png")

        #
        x -= math.sin(np.radians(angle)) * self.h/2
        y -= self.h/2 - (math.cos(np.radians(angle)) * self.h/2)
        if self.num_missiles < 500:
            self.missile[self.num_missiles] = Missile(self.file, x, y, angle)
            self.missile[self.num_missiles].allow_draw = True
            self.num_missiles += 1

    def sequence(self):
        for i in range(self.num_missiles):
            self.y = self.missile[i].y #stores starting position of missile
            self.x = self.missile[i].x
            self.angle = self.missile[i].angle

            self.missile[i].draw()

            #moves missile at an angle 
            self.missile[i].x += 10 * np.sin(-self.angle) #update y pos
            self.missile[i].y += 10 * np.cos(self.angle) #update x pos


