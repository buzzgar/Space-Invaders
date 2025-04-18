import math
import time

import picture
import stddraw

import GameSettings
from GameOver import GameOverScreen
from entities.Enemy import EnemyController
from entities.GroundEntity import Ground
from entities.Shooter import Shooter
from entities.missile_class import MissileController
from menu import Gif, TitleScreen
from utils.SoundManager import SoundPlayer
from utils.utils import collides

star_01 = picture.Picture("assets/spr_stars01.png")
star_02 = picture.Picture("assets/spr_stars02.png")

enemies_destroyed = 0  # tally enemy deaths


class Game:
    MENU_SCREEN_FLAG = 100
    GAME_SCREEN_FLAG = 200
    GAME_OVER_SCREEN_FLAG = 300

    ROTATION_ANTICLOCKWISE = -1
    ROTATION_CLOCKWISE = 1

    MOVING_LEFT = -1
    MOVING_RIGHT = 1

    def __init__(self, w, h):
        self.success = None
        self.hit_points = {}
        self.rotating_direction = None
        self.moving_direction = None

        self.game_over_class = None
        self.missile_controller = None
        self.shooter = None
        self.ground_level = None
        self.enemy_controller = None
        self.running = True

        # counts when missile hits the enemy
        self.targert_hit_count = 0
        self.player_lives = 5

        self.w = w
        self.h = h

        self.fps = GameSettings.FPS

        self.current_screen = self.MENU_SCREEN_FLAG

        self.frame_time = 1 / self.fps

        self.last_shot_fired_sound = time.time()
        self.last_shot_fired = time.time()

        self.is_in_menu = True
        self.is_player_dead = False

        self.reset()

        self.intro_gif = Gif("menu", num_frames=5)
        self.fail_gif = Gif("fail", num_frames=2)
        self.win_gif = Gif("win", num_frames=4)

        self.menu = TitleScreen(w, h)

        self.sound_player = SoundPlayer()

    def main_menu(self, i):

        if stddraw.hasNextKeyTyped():
            self.is_in_menu = False

            return True

        self.intro_gif.draw_frame((i // 5) % 5)
        self.menu.instructions()

        return False

    def game_over(self, i):

        self.fail_gif.draw_frame((i // 60) % 2)
        #self.game_over_class.game_over()

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def show_win_screen(self, i):

        self.win_gif.draw_frame((i // 10) % 4)
        #self.game_over_class.success()


        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def reset(self):
        self.is_in_menu = True
        self.is_player_dead = False
        self.success = False

        self.enemy_controller = EnemyController(self.w, self.h)
        self.ground_level = Ground(0, 0, self.w, 40)
        self.shooter = Shooter("", 0, 0, self.w, 40, None, playerFile=GameSettings.player_sprite_path, scaleFactor=40)
        self.missile_controller = MissileController(None, self.shooter.get_height(), self.w, self.h)
        self.game_over_class = GameOverScreen(self.w, self.h)

        self.moving_direction = 0
        self.rotating_direction = 0

        self.player_lives = 5
        self.hit_points = {}

        self.targert_hit_count = 0

    def game_loop(self, i):
        global enemies_destroyed
        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()

            if i > 0:
                match userInput:
                    case 'A' | 'a':
                        self.moving_direction = self.MOVING_LEFT
                    case 'D' | 'd':
                        self.moving_direction = self.MOVING_RIGHT
                    case 'q' | 'Q':
                        self.rotating_direction = self.ROTATION_ANTICLOCKWISE
                    case 'e' | 'E':
                        self.rotating_direction = self.ROTATION_CLOCKWISE
                    case 'w' | 'W':
                        self.rotating_direction = 0
                    case 's' | 'S':
                        self.moving_direction = 0
                    case 'x' | 'X':
                        quit()

                x, y = self.shooter.get_x() + self.shooter.get_width() / 2, self.shooter.get_y() + self.shooter.get_height()

                key = userInput
                if key == ' ':  # check if new missile is being called, then creates it

                    if time.time() - self.last_shot_fired > GameSettings.fire_rate:
                        self.last_shot_fired = time.time()
                        angle = int(round(self.shooter.get_angle() * 180 / math.pi, 5))

                        self.missile_controller.generate(x, y, angle)

                    if time.time() - self.last_shot_fired_sound > GameSettings.fire_rate:
                        self.last_shot_fired_sound = time.time()
                        self.sound_player.play_audio_background(GameSettings.gun_fire_sound)

        if self.moving_direction == self.MOVING_LEFT:
            self.shooter.moveLeft()
        elif self.moving_direction == self.MOVING_RIGHT:
            self.shooter.moveRight()

        if self.rotating_direction == self.ROTATION_ANTICLOCKWISE:
            self.shooter.anticlockwise()
        elif self.rotating_direction == self.ROTATION_CLOCKWISE:
            self.shooter.clockwise()

        self.missile_controller.sequence()

        self.shooter.drawShooter()

        self.ground_level.draw()

        self.enemy_controller.step()
        self.enemy_controller.render_breaks(self.shooter.get_x(), self.shooter.get_y())
        self.enemy_controller.render()

        self.shooter.drawShooter()

        # display counter
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(50, self.h - 20, "Hits: + " + str(self.targert_hit_count))

        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(self.w - 50, self.h - 20, f"♥ {self.player_lives}")

        enemies_flag = False
        for enemy in self.enemy_controller.enemy_list + self.enemy_controller.break_list:
            if enemy.allow_draw:
                enemies_flag = True
                break

        if not enemies_flag:
            self.success = True

        for hit in self.hit_points:
            stddraw.setFontSize(12)
            if i - hit > GameSettings.hit_point_frame_time:
                continue

            stddraw.setPenColor(stddraw.RED)
            stddraw.text(self.hit_points[hit][0], self.hit_points[hit][1], "+1")

        for enemy in self.enemy_controller.enemy_list + self.enemy_controller.break_list:
            if not enemy.allow_draw:
                continue

            if collides(self.ground_level, enemy):
                enemy.allow_draw = False

            if collides(self.shooter, enemy):
                enemy.allow_draw = False

                self.player_lives -= 1

                if self.player_lives == 0:
                    self.is_player_dead = True
                    self.sound_player.play_audio_background(GameSettings.game_over_sound)

            for missile in self.missile_controller.missile:
                if not missile:
                    continue

                if not missile.allow_draw:
                    continue

                if collides(missile, enemy):
                    missile.allow_draw = False
                    enemy.allow_draw = False
                    enemies_destroyed += 1
                    self.targert_hit_count += 1

                    self.hit_points[i] = (enemy.x, enemy.y)

                    self.sound_player.play_audio_background("assets/sounds/explosion-2")

    def render(self, i):
        global star_01, star_02, enemies_destroyed

        stddraw.clear(stddraw.BLACK)

        w = self.w
        h = self.h

        # stddraw.picture(star_02, w//2, h//2, w, h)

        if self.is_in_menu:
            #self.sound_player.play_audio_background(GameSettings.intro_sound)
            return self.main_menu(i)
        elif self.is_player_dead:
            self.game_over(i)
        #elif self.success:
            #self.success_screen()
        elif enemies_destroyed == len(self.enemy_controller.enemy_list):
            self.sound_player.play_audio_background(GameSettings.victory_sound)
            self.show_win_screen(i)
        else:
            self.game_loop(i)

    def success_screen(self):
        self.game_over_class.success()

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()
