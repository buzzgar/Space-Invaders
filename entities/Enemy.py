################################################
# Student Name: Meezaan Ryklief
# Student Number: 26031825
################################################

import math
import random

from utils.PictureLoader import Picture
import stddraw

import GameSettings
from utils.utils import GameObject


class ClassicEnemy(GameObject):

    CLASSIC_ENEMY = 0
    FREEZE_ENEMY = 1
    BOMB_ENEMY = 2

    def __init__(self, name, x, y, width, height, p):
        super().__init__(name, x, y, width, height)
        self.allow_draw = True
        self.is_alive = True
        self.p = p

        self.death_preview_frame = GameSettings.DEATH_FRAME_TIME

        self.enemy_type = self.CLASSIC_ENEMY

        self.frozen = False
        self.frozen_pic = Picture("assets/enemy/frozen-enemy.png")

    def _draw(self):

        if self.death_preview_frame > 1 and not self.is_alive:
            self.death_preview_frame -= 1
        elif not self.is_alive:
            self.allow_draw = False

        p = self.p

        if not self.is_alive:
            p = Picture("assets/enemy/explosion/frame_{frame}.png".format(frame=12 - self.death_preview_frame))
        elif self.frozen:
            p = self.frozen_pic

        stddraw.picture(p, self.x, self.y, self.width, self.height)

    def kill_enemy(self):
        self.is_alive = False
        self.is_destroyed = True

    def draw(self, frozen=False):
        self.frozen = frozen
        super().draw()

class BombEnemy(ClassicEnemy):

    def __init__(self, name, x, y, width, height, p):
        p = Picture("assets/enemy/pngegg-bomb-dropper.png")

        super().__init__(name, x, y, width, height, p)
        self.enemy_type = self.BOMB_ENEMY

    def draw(self, frozen=False):
        super().draw(frozen)

        if random.randint(0, GameSettings.CHANCE_OF_ENEMY_DROPPING_BOMB) == 0 and self.is_alive:
            return True

class EnemyDrops(GameObject):

    def __init__(self, name, x, y):

        self.p = Picture("assets/enemy/bomb.png")

        width = self.p.width()
        height = self.p.height()

        super().__init__(name, x, y, width, height)

        self.allow_draw = True
        self.is_alive = True

        self.bomb_preview_frame = GameSettings.DEATH_FRAME_TIME

    def _draw(self):

        if self.bomb_preview_frame > 1 and not self.is_alive:
            self.bomb_preview_frame -= 1
        elif not self.is_alive:
            self.allow_draw = False

        if not self.is_alive:
            self.p = Picture("assets/enemy/explosion/frame_{frame}.png".format(frame=12 - self.bomb_preview_frame))

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

        self.frozen = False

        p = Picture(GameSettings.enemy_sprite_path)

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

        # Check how many enemies are on the screen

        enemies_on_screen = 0

        for enemy in self.get_alive_enemies(True):
            # is on screen
            if 0 < enemy.y < self.h and 0 < enemy.x < self.w:
                enemies_on_screen += 1

        # if less than 5, don't freeze
        if enemies_on_screen < 5:
            self.frozen = False

        # Update the positions of all the bombs if alive/active
        for drop in self.drop_list:
            if drop.is_alive:
                drop.y -= 10

        # If enemies are frozen don't update any positions and return
        if self.frozen:
            return

        move_down = False

        # Update enemy x positions that are alive and have not broken formation
        for enemy in self.get_alive_enemies(False):
            if self.direction == self.RIGHT:
                enemy.x += GameSettings.alien_speed_x
            else:
                enemy.x -= GameSettings.alien_speed_x

        # Checks if any enemy is at boundary, then change direction and move down
        for enemy in self.get_alive_enemies(False):

            if enemy.x >= self.w - self.enemy_width:
                self.direction = self.LEFT
                move_down = True
                break

            if enemy.x <= self.enemy_width:
                self.direction = self.RIGHT
                move_down = True
                break

        # Randomly allows a random enemy to break formation, with a chance of one in 300
        if random.randint(0, GameSettings.CHANCE_OF_BREAK_AWAY) == 0:
            if len(self.get_alive_enemies()) > 0:
                self.break_list.append(self.enemy_list.pop(random.randint(0, len(self.enemy_list) - 1)))

        if move_down:
            for enemy in self.enemy_list:
                enemy.y -= GameSettings.alien_speed_y

    def render_breaks(self, shooter_x, shooter_y):
        # Update the positions of all the breakaway enemies

        if self.frozen:
            return

        for enemy in self.break_list:
            angle = math.atan2(shooter_y - enemy.y, shooter_x - enemy.x)
            enemy.x += GameSettings.alien_speed_x * math.cos(angle) * 0.8
            enemy.y += GameSettings.alien_speed_y * math.sin(angle) * 0.8

    def render(self):
        for enemy in self.enemy_list:
            drop = enemy.draw(self.frozen)

            if drop:
                self.drop_list.append(EnemyDrops("drop", enemy.x, enemy.y))

        for drop in self.drop_list:
            drop.draw()

        for enemy in self.break_list:
            enemy.draw(self.frozen)
            
