import stddraw
from menu import Gif

class Gif:
    def __init__(self, name, num_frames):
        self.frames = stdarray.create1D(num_frames, "")  # create array to store each frame
        self.name = name
        for i in range(0, num_frames):  # populate array
            self.frames[i] = Picture("assets/" + self.name + "_" + str(i + 1) + ".png")

        self.dimensions = self.frames[0]  # set up standard dimensions for all frames

        self.w = self.dimensions.width()
        self.h = self.dimensions.height()

        self.x_centre = self.w / 2
        self.y_centre = self.h / 2

    def setup(self):
        stddraw.setCanvasSize(self.w, self.h)  # use dimensions of image as canvas size

        stddraw.setXscale(0.0, self.w)  # sets canvas to image dimensions
        stddraw.setYscale(0.0, self.h)

    def draw_frame(self, i):
        stddraw.clear()
        stddraw.picture(self.frames[i], self.x_centre, self.y_centre)

class GameOverScreen:
    def __init__(self, width, height):
        self.w = width  # defines width and height throughout class
        self.h = height

        self.x_centre = self.w // 2
        self.y_centre = self.h // 2

    def success(self):

        stddraw.clear(stddraw.GREEN)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(50)
        stddraw.text(self.x_centre, self.y_centre, "You Won!")
        stddraw.text(self.x_centre, self.y_centre - 100, "[R] to restart")