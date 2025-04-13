import stddraw
import stdio 
import stdarray
import stdaudio
from picture import Picture #picture class so can get widths and heights of picture for background


class Music: 
    def __init__(self,file):
        self.filename = file
    
    def play_audio(self):
        stdaudio.playFile(self.filename)

class Gif:
    def __init__(self,num_frames):
        self.frames = stdarray.create1D(num_frames, "") #create array to store each frame 

        for i in range(0, num_frames): #populate array
            self.frames[i] = Picture(str(i+1) + ".jpg")

        self.dimensions = self.frames[0] #set up standard dimensions for all frames 

        self.w = self.dimensions.width()
        self.h = self.dimensions.height()
    
        self.x_centre = self.w / 2
        self.y_centre = self.h / 2

           
    def setup(self): 
        stddraw.setCanvasSize(self.w,self.h) #use dimensions of image as canvas size 

        stddraw.setXscale(0.0, self.w) #sets canvas to image dimensions 
        stddraw.setYscale(0.0,self.h)

    def draw_frame(self, i): 
        stddraw.clear()
        stddraw.picture(self.frames[i], self.x_centre, self.y_centre)

class TitleScreen: 
    def __init__(self, width, height):
        self.w = width  #defines width and height throughout class 
        self.h = height 
    
        self.x_centre = self.w / 2
        self.y_centre = self.h / 2
    
    def instructions(self):
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(50)
        stddraw.text(self.x_centre, self.h - 100, "COSMIC CONQUISTADORS")
        stddraw.setFontSize(28)
        stddraw.text(self.x_centre, self.h - 200, "Instructions:")
        stddraw.setFontSize(24)
        stddraw.text(self.x_centre, self.h - 300, "[A] move left, [S] stop move, [D] move right")
        stddraw.text(self.x_centre, self.h - 350 , "[Q] rotate left, [W] stop rotate, [E] rotate right")
        stddraw.text(self.x_centre, self.y_centre, "[Space] to shoot")
        stddraw.text(self.x_centre, self.y_centre - 100, "[H] for help")
        stddraw.text(self.x_centre, self.y_centre - 200, "[X] to quit")
        stddraw.setFontSize(35)
        stddraw.text(self.x_centre, self.y_centre - 300, "Press any key to start")




def main():

    #play music 
#    stdaudio.playFile("intromusic")
   
    #setup gif 
    gif = Gif(num_frames = 5) 
    gif.setup() 

    #setup title screen
    menu = TitleScreen(gif.w,gif.h)

    i = 1 
    while True:
        for i in range(0,5):
            gif.draw_frame(i)
            menu.instructions()
            stddraw.show(100)
if __name__ == '__main__':
    main() 
