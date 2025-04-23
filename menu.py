################################################
# Student Name: Ayesha Hofmeyer
# Student Number: 26990571
################################################

import stddraw
import stdarray
from picture import Picture


class Gif:
    def __init__(self, directory, num_frames, x_centre, y_centre):
        self.frames = stdarray.create1D(num_frames, "")  # create array to store each frame

        for i in range(0, num_frames):  # populate array
            self.frames[i] = Picture(directory + "_" + str(i + 1) + ".png")

        self.x_centre = x_centre
        self.y_centre = y_centre

        self.i = 0

    def draw_frame(self, i):
        stddraw.picture(self.frames[i], self.x_centre, self.y_centre)


class TitleScreen:
    def __init__(self, width, height):
        self.w = width  # defines width and height throughout class
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
        stddraw.text(self.x_centre, self.h - 250, "[A] move left, [S] stop move, [D] move right")
        stddraw.text(self.x_centre, self.h - 300, "[Q] rotate left, [W] stop rotate, [E] rotate right")
        stddraw.text(self.x_centre, self.y_centre, "[Space] to shoot")
        stddraw.text(self.x_centre, self.y_centre - 50, "[H] for help")
        stddraw.text(self.x_centre, self.y_centre - 100, "[X] to quit")
        stddraw.setFontSize(35)
        stddraw.text(self.x_centre, self.y_centre - 300, "Press any key to start")

    def help(self):
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(20)
        self.x = self.w - 850
        self.y = self.h - 500
        stddraw.text(self.x - 120, self.y - 50, "Instructions:")
        stddraw.setFontSize(20)
        stddraw.text(self.x - 10, self.y - 75, "[A] move left, [S] stop move, [D] move right")
        stddraw.text(self.x - 5, self.y - 100, "[Q] rotate left, [W] stop rotate, [E] rotate right")
        stddraw.text(self.x - 47, self.y - 125, "[Space] to shoot, [J] for shield, [I] for target line")
        stddraw.text(self.x - 135, self.y - 150, "[X] to quit")

