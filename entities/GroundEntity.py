################################################
# Student Name: Meezaan Ryklief
# Student Number: 26031825
################################################

import stddraw

from utils.utils import GameObject


class Ground(GameObject):
    def __init__(self, x, y, width, height, color=stddraw.WHITE):
        super().__init__("Ground Level", x, y, width, height, color)

        self.x = x + self.width//2
        self.y = y + self.height//2

        self.allow_draw = True

    def _draw(self):
        stddraw.setPenColor(self.color)
        stddraw.setFontSize(24)
        stddraw.filledRectangle(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.text(self.x, self.y, self.name)