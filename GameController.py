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
from utils.SoundManager import play_audio_background
from utils.background import Background
from utils.utils import collides

star_01 = picture.Picture("assets/spr_stars01.png")
star_02 = picture.Picture("assets/spr_stars02.png")

class Game:

    MENU_SCREEN_FLAG = 100
    GAME_SCREEN_FLAG = 200
    GAME_OVER_SCREEN_FLAG = 300

    ROTATION_ANTICLOCKWISE = -1
    ROTATION_CLOCKWISE = 1

    MOVING_LEFT = -1
    MOVING_RIGHT = 1

    def __init__(self, w, h):
        self.rotating_direction = None
        self.moving_direction = None

        self.game_over_class = None
        self.missile_controller = None
        self.shooter = None
        self.ground_level = None
        self.enemy_controller = None
        self.running = True

        #counts when missile hits the enemy
        self.targert_hit_count = 0
        
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

        self.gif = Gif(num_frames=5)

        self.menu = TitleScreen(w, h)

    def main_menu(self, i):

        if stddraw.hasNextKeyTyped():
            self.is_in_menu = False

            return True

        self.gif.draw_frame((i % 50) // 10)
        self.menu.instructions()
        play_audio_background(GameSettings.intro_sound)
        return False

    def game_over(self):

        self.game_over_class.game_over()

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def reset(self):
        self.is_in_menu = True
        self.is_player_dead = False

        self.enemy_controller = EnemyController(self.w, self.h)
        self.ground_level = Ground(0, 0, self.w, 40)
        self.shooter = Shooter("", 0, 0, self.w, 40, None, playerFile=GameSettings.player_sprite_path, scaleFactor=40)
        self.missile_controller = MissileController(None, self.shooter.get_height())
        self.game_over_class = GameOverScreen(self.w, self.h)

        self.moving_direction = 0
        self.rotating_direction = 0

    def game_loop(self, i):

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
                    
                    if time.time() - self.last_shot_fired > 0.2:
                        self.last_shot_fired = time.time()
                        angle = int(round(self.shooter.get_angle() * 180 / math.pi, 5))

                        self.missile_controller.generate(x, y, angle)

                    if time.time() - self.last_shot_fired_sound > 1:
                        self.last_shot_fired_sound = time.time()
                        play_audio_background(GameSettings.gun_fire_sound)

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
        self.enemy_controller.render()

        self.shooter.drawShooter()

        # display counter
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(100, self.ground_level.height//2, "Hits: + " + str(self.targert_hit_count))

        for enemy in self.enemy_controller.enemy_list:
            if not enemy.allow_draw:
                continue

            if collides(self.ground_level, enemy):
                enemy.allow_draw = False

            if collides(self.shooter, enemy):
                enemy.allow_draw = False
                self.is_player_dead = True
                play_audio_background(GameSettings.game_over_sound)

            for missile in self.missile_controller.missile:
                if not missile:
                    continue

                if not missile.allow_draw:
                    continue

                if collides(missile, enemy):
                    missile.allow_draw = False
                    enemy.allow_draw = False
                    self.targert_hit_count += 1

    def render(self, i):
        global star_01, star_02

        stddraw.clear(stddraw.BLACK)

        w = self.w
        h = self.h

        #stddraw.picture(star_02, w//2, h//2, w, h)
        
        if self.is_in_menu:
            return self.main_menu(i)
        elif self.is_player_dead:
            self.game_over()
        else:
            self.game_loop(i)

