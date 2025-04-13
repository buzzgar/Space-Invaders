import stddraw 
import stdio 
import stdarray
from picture import Picture
import math
import numpy as np

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
    def __init__(self, file):
        # self.x0 = x0
        # self.y0 = y0

        self.file = file
        
        self.missile = stdarray.create1D(500) #2D array with 500 rows (for num of missiles) and 3 column (for y and x coordinates AND ANGLE)
        self.num_missiles = 0
    
    def generate(self,x,y,angle):
        if self.num_missiles < 500:
            self.missile[self.num_missiles] = Missile(self.file, x, y, angle)
            self.missile[self.num_missiles].allow_draw = True
            self.num_missiles += 1

    def sequence(self):
        for i in range(self.num_missiles):
            self.y = self.missile[i].x #stores starting position of missile
            self.x = self.missile[i].y
            self.angle = self.missile[i].angle

            self.missile[i].draw()

            #moves missile at an angle 
            self.missile[i].x += 10 * np.sin(self.angle) #update y pos
            self.missile[i].y += 10 * np.cos(self.angle) #update x pos

    def end(self): #destory missile once in contact with enemy 
        stddraw.clear()


def main():
    
    #setup 
    canvas = Canvas(10.0,10.0)
    canvas.setup() 

    #initialise dimensions of missile 
    missile = Missile("../assets/laser.gif")
    
    while True: #inifinte loop constantly checking if key is pressed 
        stddraw.clear()  #every time it loops this statement clears pervious position of missile
        x = 5
        y = 1
        
        if stddraw.hasNextKeyTyped(): 
            key = stddraw.nextKeyTyped()
            if key == ' ': #check if new missile is being called, then creates it 
                missile.generate(x,y, 90)
            if key == 'a': #moves left
                missile.generate(x,y, 135)
            if key == 'b': #moves right 
                missile.generate(x,y,45) 
        #angled trajectory 
        missile.sequence()

        stddraw.show(50) #show final frame (blank screen) ALWAYS LAST THING IN WHILE LOOP  

if __name__ == '__main__':
    main()

