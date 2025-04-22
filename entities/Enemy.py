import math
import random

import picture
import stddraw

import GameSettings
from utils.utils import GameObject


class ClassicEnemy(GameObject):

    CLASSIC_ENEMY = 0
    FREEZE_ENEMY = 1
    BOMB_ENEMY = 2

    def __init__(self, name, x, y, width, height, p):
        super().__init__(name, x, y, width, height, None)
        self.allow_draw = True
        self.is_alive = True
        self.p = p

        self.death_preview_frame = 12

        self.enemy_type = self.CLASSIC_ENEMY

    def _draw(self):
        if self.death_preview_frame > 1 and not self.is_alive:
            self.death_preview_frame -= 1
        elif not self.is_alive:
            self.allow_draw = False

        if not self.is_alive:
            self.p = picture.Picture("assets/enemy/explosion/frame_{frame}.png".format(frame=12 - self.death_preview_frame))

        stddraw.picture(self.p, self.x, self.y, self.width, self.height)

    def kill_enemy(self):
        self.is_alive = False
        self.is_destroyed = True

class FreezeEnemy(ClassicEnemy):

    def __init__(self, name, x, y, width, height, p):
        super().__init__(name, x, y, width, height, p)
        self.enemy_type = self.FREEZE_ENEMY

class BombEnemy(ClassicEnemy):

    def __init__(self, name, x, y, width, height, p):
        p = picture.Picture("assets/enemy/pngegg-bomb-dropper.png")

        super().__init__(name, x, y, width, height, p)
        self.enemy_type = self.BOMB_ENEMY

    def draw(self):
        super().draw()

        if random.randint(0, 200) == 0 and self.is_alive:
            return True

class EnemyDrops(GameObject):

    def __init__(self, name, x, y):

        self.p = picture.Picture("assets/enemy/bomb.png")

        width = self.p.width()
        height = self.p.height()

        super().__init__(name, x, y, width, height, None)

        self.allow_draw = True
        self.is_alive = True

        self.bomb_preview_frame = 12

    def _draw(self):

        if self.bomb_preview_frame > 1 and not self.is_alive:
            self.bomb_preview_frame -= 1
        elif not self.is_alive:
            self.allow_draw = False

        if not self.is_alive:
            self.p = picture.Picture("assets/enemy/explosion/frame_{frame}.png".format(frame=12 - self.bomb_preview_frame))

        stddraw.picture(self.p, self.x, self.y, self.width, self.height)

    def kill_enemy(self):
        self.is_alive = False
        self.is_destroyed = True

class EnemyController:

    RIGHT = 0
    LEFT = 1

    def __init__(self, w, h, enemy_count=36, wave=1):
        self.w = w
        self.h = h

        enemy_count = enemy_count * wave
        self.enemy_count = enemy_count

        self.wave = wave

        self.max_per_row = 8

        self.enemy_height = 50

        self.direction = self.RIGHT

        p = picture.Picture(GameSettings.enemy_sprite_path)

        a_ratio = p.width() / p.height()
        self.enemy_width = self.enemy_height * a_ratio

        start_x = self.enemy_width + 10
        start_y = self.h - self.enemy_height

        self.enemy_list = []

        for i in range(0, enemy_count):
            x, y = self.enemy_position_striped(i, start_x, start_y)

            if i % 36 > 0:
                self.enemy_list.append(ClassicEnemy(
                    "enemy",
                    x,
                    y,
                    self.enemy_width,
                    self.enemy_height,
                    p)
                )
            else:
                self.enemy_list.append(BombEnemy(
                    "enemy",
                    x,
                    y,
                    self.enemy_width,
                    self.enemy_height,
                    p)
                )

        self.break_list = []
        self.drop_list = []

    def get_alive_enemies(self, include_breaks=True):

        if not include_breaks:
            return [enemy for enemy in self.enemy_list if enemy.is_alive]

        return [enemy for enemy in self.enemy_list + self.break_list if enemy.is_alive]

    def get_active_drops(self):
        return [drop for drop in self.drop_list if drop.is_alive]

    def enemy_position_default(self, i, start_x, start_y):

        return (start_x + (i % self.max_per_row) * (10 + self.enemy_width) + (50 if (i % self.max_per_row) > 7 else 0),
                start_y - (i // self.max_per_row) * (10 + self.enemy_height))

    def enemy_position_striped(self, i, start_x, start_y):
        repeat = 36

        x = self.w - start_x * 2

        max_per_stripe = x // 2 // self.enemy_width

        y = start_y + self.enemy_height * (i//max_per_stripe) + i // max_per_stripe * 100

        i = i % max_per_stripe

        if i > 0:
            x -= self.enemy_width * ((i + 1)//2) * (1 if i % 2 == 0 else -1)
            y -= self.enemy_height * (i//2) + self.enemy_height * (0 if i % 2 == 0 else 1)

        return x, y

    def step(self):

        move_down = False

        for enemy in self.get_alive_enemies(False):
            if self.direction == self.RIGHT:
                enemy.x += GameSettings.alien_speed_x
            else:
                enemy.x -= GameSettings.alien_speed_x

        for enemy in self.get_alive_enemies(False):

            if enemy.x >= self.w - self.enemy_width:
                self.direction = self.LEFT
                move_down = True
                break

            if enemy.x <= self.enemy_width:
                self.direction = self.RIGHT
                move_down = True
                break

        for drop in self.drop_list:
            if drop.is_alive:
                drop.y -= 10

        if random.randint(0, 300) == 0:
            if len(self.get_alive_enemies()) > 0:
                self.break_list.append(self.enemy_list.pop(random.randint(0, len(self.enemy_list) - 1)))

        if move_down:
            for enemy in self.enemy_list:
                enemy.y -= GameSettings.alien_speed_y

    def render_breaks(self, shooter_x, shooter_y):
        for enemy in self.break_list:
            angle = math.atan2(shooter_y - enemy.y, shooter_x - enemy.x)
            enemy.x += GameSettings.alien_speed_x * math.cos(angle) * 0.8
            enemy.y += GameSettings.alien_speed_y * math.sin(angle) * 0.8

    def render(self):
        for enemy in self.enemy_list:
            drop = enemy.draw()

            if drop:
                self.drop_list.append(EnemyDrops("drop", enemy.x, enemy.y))

        for drop in self.drop_list:
            drop.draw()

        for enemy in self.break_list:
            enemy.draw()
            
