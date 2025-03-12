import picture
import stddraw

from utils import GameObject


class ClassicEnemy(GameObject):

    def __init__(self, name, x, y, width, height, p):
        super().__init__(name, x, y, width, height, None)
        self.allow_draw = True
        self.p = p

    def _draw(self):

        stddraw.picture(self.p, self.x, self.y, self.width, self.height)

class EnemyController:

    RIGHT = 0
    LEFT = 1

    def __init__(self, w, h, enemy_count=64):
        self.w = w
        self.h = h

        self.max_per_row = 16

        self.enemy_height = 50

        self.direction = self.RIGHT

        p = picture.Picture("resources/pngegg.png")

        a_ratio = p.width() / p.height()
        self.enemy_width = self.enemy_height * a_ratio

        start_x = self.enemy_width + 10
        start_y = self.h - self.enemy_height

        self.enemy_list = []

        for i in range(0, enemy_count):

            self.enemy_list.append(ClassicEnemy(
                "enemy",
                start_x + (i % self.max_per_row)*(10 + self.enemy_width) + (50 if (i % self.max_per_row) > 7 else 0),
                start_y - (i // self.max_per_row)*(10 + self.enemy_height),
                self.enemy_width,
                self.enemy_height,
                p)
            )

    def step(self):

        move_down = False

        for enemy in self.enemy_list:
            if self.direction == self.RIGHT:
                enemy.x += 50
            else:
                enemy.x -= 50

        for enemy in self.enemy_list:

            if enemy.x >= self.w - self.enemy_width:
                self.direction = self.LEFT
                move_down = True
                break

            if enemy.x <= self.enemy_width:
                self.direction = self.RIGHT
                move_down = True
                break

        if move_down:
            for enemy in self.enemy_list:
                enemy.y -= 10

    def render(self):
        for enemy in self.enemy_list:
            enemy.draw()