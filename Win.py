import stddraw


class WinScreen:
    def __init__(self, width, height):
        self.w = width  # defines width and height throughout class
        self.h = height

        self.x_centre = self.w // 2
        self.y_centre = self.h // 2

    def win(self):

        stddraw.clear(stddraw.GREEN)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(50)
        stddraw.text(self.x_centre, self.y_centre, "You Won!")
        stddraw.text(self.x_centre, self.y_centre - 100, "[R] to restart")