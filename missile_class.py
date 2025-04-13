import stddraw 
import stdio 
import stdarray
from picture import Picture
import math
import numpy as np
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

class Missile: 
    def __init__(self, file):
        self.pic = Picture(file) #assign vars
    
       # self.x0 = x0  
       # self.y0 = y0 
        
        self.missile = stdarray.create2D(500,3) #2D array with 500 rows (for num of missiles) and 3 column (for y and x coordinates AND ANGLE) 
        self.num_missiles = 0
    
    def generate(self,x,y,angle):
        if self.num_missiles < 500:
            self.x0 = x
            self. y0 = y
            self.angle = np.radians(angle) 
            #set at starting x and y position  
            self.missile[self.num_missiles][0] = self.y0
            self.missile[self.num_missiles][1] = self.x0
            self.missile[self.num_missiles][2] = self.angle 
            self.num_missiles += 1

    def sequence(self):
        for i in range(self.num_missiles):
            self.y = self.missile[i][0] #stores starting position of missile
            self.x = self.missile[i][1]
            self.angle = self.missile[i][2]
            stddraw.picture(self.pic,self.x,self.y) #generates missile at new position 
            #moves missile at an angle 
            self.missile[i][0] += 0.1 * np.sin(self.angle) #update y pos
            self.missile[i][1] += 0.1 * np.cos(self.angle) #update x pos

    def end(self): #destory missile once in contact with enemy 
        stddraw.clear()


def main():
    
    #setup 
    canvas = Canvas(10.0,10.0)
    canvas.setup() 

    #initialise dimensions of missile 
    missile = Missile("laser.gif")
    
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

   #     stddraw.circle(5,9,0.5) #enemy
   #     y = 9 
   #     while y >= 1: 
   #         stddraw.clear()
   #         stddraw.circle(5,y,0.5)
   #         y -= 1
   #     stddraw.show(100)

        #check if any missiles have touched enemy 
    #    for i in range(missile.num_missiles):
    #        if missile.missile[i][0] >= 5: 
    #            missile.end() 

        stddraw.show(50) #show final frame (blank screen) ALWAYS LAST THING IN WHILE LOOP  

if __name__ == '__main__':
    main()

