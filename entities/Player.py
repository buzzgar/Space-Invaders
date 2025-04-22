import picture
import stddraw

import GameSettings
from utils.utils import GameObject


class Player(GameObject):

    def __init__(self, name, x, y, width, height, p):
        super().__init__(name, x, y, width, height, None)
        self.allow_draw = True
        self.p = p

        self.angle = 0

    def _draw(self):

        stddraw.picture(self.p, self.x, self.y, self.width, self.height)

    def kill_enemy(self):
        self.is_alive = False
        self.allow_draw = False
        self.is_destroyed = True


