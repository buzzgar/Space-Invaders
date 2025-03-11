class GameObject:
    def __init__(self, name, x, y, width, height, color):
        self.x = x
        self.y = y
        self.name = name

        self.width = width
        self.height = height

        self.color = color

        self.is_alive = False
        self.is_destroyed = False

        self.allow_draw = False

    def draw(self):
        if self.allow_draw:
            self._draw()

    def _draw(self):
        pass