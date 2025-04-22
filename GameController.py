import math
import time
from typing import List

import picture
import stddraw

import GameSettings
from entities.Enemy import EnemyController
from entities.GroundEntity import Ground
from entities.ModifierPowerUps import ModifierController, Modifier, FireRateModifier
from entities.Shooter import Shooter
from entities.missile_class import MissileController, ShieldController
from menu import Gif, TitleScreen
from utils.SoundManager import SoundPlayer
from utils.utils import collides

star_01 = picture.Picture("assets/game_backgrounds/back.png")
star_02 = picture.Picture("assets/game_backgrounds/back.png")

class PlayerProperties:

    fire_rate = GameSettings.fire_rate
    player_lives = 5
enemies_destroyed = 0  # tally enemy deaths

    def __init__(self, sound_player: SoundPlayer):
        self.sound_player = sound_player

    def default_fire_rate(self):
        self.fire_rate = GameSettings.fire_rate

    def player_lost_health(self):
        self.player_lives -= 1

    def apply_modifiers(self, i, modifiers: List[Modifier]):
        for modifier in modifiers:
            if not modifier.is_picked_up:
                continue

            if modifier.is_active(i):
                if modifier.modifier_type == modifier.FIRE_RATE_MODIFIER:
                    modifier: FireRateModifier
                    self.fire_rate = modifier.fire_rate
                elif modifier.modifier_type == modifier.HEALTH_MODIFIER:
                    self.player_lives += 1
                    self.sound_player.play_audio_background(GameSettings.health_up_sound)

class Game:
    MENU_SCREEN_FLAG = 100
    GAME_SCREEN_FLAG = 200
    GAME_OVER_SCREEN_FLAG = 300

    ROTATION_ANTICLOCKWISE = -1
    ROTATION_CLOCKWISE = 1

    MOVING_LEFT = -1
    MOVING_RIGHT = 1

    def __init__(self, w, h):
        self.player_properties: PlayerProperties = None
        self.modifier_controller: ModifierController = None
        self.enemies_destroyed = None
        self.success = None
        self.hit_points = {}
        self.rotating_direction = None
        self.moving_direction = None

        self.game_over_class = None
        self.shield_controller = None
        self.missile_controller = None
        self.shooter = None
        self.ground_level = None
        self.enemy_controller: EnemyController = None
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

        self.shield_start_time = 0
        shield_active = False

        self.is_in_menu = True
        self.is_player_dead = False

        self.intro_gif = Gif("assets/main_menu_background/menu", 5, self.w//2, self.h//2)
        self.fail_gif = Gif("assets/end_game_screens/fail", 2, self.w//2, self.h//2)
        self.win_gif = Gif("assets/end_game_screens/win", 4, self.w//2, self.h//2)

        self.menu = TitleScreen(w, h)

        self.sound_player = SoundPlayer()

        self.reset()

        self.WIN_EVENT = False

    def main_menu(self, i):

        if stddraw.hasNextKeyTyped():
            self.is_in_menu = False

            return True

        self.intro_gif.draw_frame((i // 8) % 5)
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

        self.enemy_controller = EnemyController(self.w, self.h, wave=4)
        self.ground_level = Ground(0, 0, self.w, 40)
        self.shooter = Shooter("", 0, 0, self.w, 40, None, playerFile=GameSettings.player_sprite_path, scaleFactor=40)
        self.missile_controller = MissileController(None, self.shooter.get_height(), self.w, self.h)
        self.modifier_controller = ModifierController(self.w, self.h)
        self.player_properties = PlayerProperties(self.sound_player)
        self.shield_controller = ShieldController("assets/shield.jpg", self.shooter.get_height(), self.w, self.h)
        self.game_over_class = GameOverScreen(self.w, self.h)

        self.moving_direction = 0
        self.rotating_direction = 0

        self.player_lives = 5
        self.hit_points = {}

        self.target_hit_count = 0
        self.enemies_destroyed = 0

        self.WIN_EVENT = False
        self.sound_player.clear_buffer()

    def game_loop(self, i):
        global enemies_destroyed
        self.player_properties.default_fire_rate()
        self.player_properties.apply_modifiers(i, self.modifier_controller.get_modifiers())

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

                if key == 'u' or key == 'U':
                    x = self.shooter.get_x() + self.shooter.get_width() / 2  # centres x and y
                    y = self.shooter.get_y() + self.shooter.get_height() / 2
                    angle = int(round(self.shooter.get_angle() * 180 / math.pi, 5))

                    shield._draw()
                    shield_active = True
                    self.shield_start_time = time.time()
                    if time.time() - self.shield_start_time >= 10:
                        shield = self.shield_controller.generate(x, y, angle)
                        shield_active = False  # Hide shield # Calls stddraw.picture() internally


        if self.moving_direction == self.MOVING_LEFT:
            self.shooter.moveLeft()

        elif self.moving_direction == self.MOVING_RIGHT:
            self.shooter.moveRight()

        if self.rotating_direction == self.ROTATION_ANTICLOCKWISE:
            self.shooter.anticlockwise()

        elif self.rotating_direction == self.ROTATION_CLOCKWISE:
            self.shooter.clockwise()

        x = self.shooter.get_x() + self.shooter.get_width() / 2  # centres x and y
        y = self.shooter.get_y() + self.shooter.get_height() / 2
        angle = self.shooter.get_angle() + (math.pi / 2)  # ensures no rotation sets angle to 90 degrees

        self.missile_controller.aimline(x, y, angle)

        if stddraw.getKeysPressed()[stddraw.K_SPACE]:

            x, y = self.shooter.get_x() + self.shooter.get_width() / 2, self.shooter.get_y() + self.shooter.get_height()

            if i > 0:  # check if new missile is being called, then creates it

                if time.time() - self.last_shot_fired > self.player_properties.fire_rate:
                    self.last_shot_fired = time.time()
                    angle = int(round(self.shooter.get_angle() * 180 / math.pi, 5))

                    self.missile_controller.generate(x, y, angle)

                if time.time() - self.last_shot_fired_sound > GameSettings.fire_rate:
                    self.last_shot_fired_sound = time.time()
                    self.sound_player.play_audio_background(GameSettings.gun_fire_sound)

        self.missile_controller.sequence()

        self.shooter.drawShooter()

        self.ground_level.draw()

        self.enemy_controller.step()
        self.enemy_controller.render_breaks(self.shooter.get_x(), self.shooter.get_y())
        self.enemy_controller.render()

        self.shooter.drawShooter()

        self.modifier_controller.frame_render(i)

        # display counter
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(50, self.h - 20, "Hits: + " + str(self.target_hit_count))

        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(self.w - 50, self.h - 20, f"♥ {self.player_properties.player_lives}")

        for hit in self.hit_points:
            stddraw.setFontSize(12)
            if i - hit > GameSettings.hit_point_frame_time:
                continue

            stddraw.setPenColor(stddraw.RED)
            stddraw.text(self.hit_points[hit][0], self.hit_points[hit][1], "+1")

        for modifier in self.modifier_controller.get_modifiers():

            if collides(modifier, self.shooter):
                modifier.pick_up(i)

        for drop in self.enemy_controller.get_active_drops():

            for missile in self.missile_controller.missile:

                if not missile:
                    continue

                if not missile.allow_draw:
                    continue

                if collides(missile, drop):
                    drop.kill_enemy()

            if collides(drop, self.ground_level):
                drop.kill_enemy()

            if collides(drop, self.shooter):
                drop.kill_enemy()

                self.player_properties.player_lost_health()

                if self.player_properties.player_lives == 0:
                    self.is_player_dead = True
                    self.sound_player.play_audio_background(GameSettings.game_over_sound)
                else:
                    self.sound_player.play_audio_background(GameSettings.player_lost_health)

        for enemy in self.enemy_controller.get_alive_enemies():
            if not enemy.allow_draw:
                continue

            if collides(self.ground_level, enemy):
                enemy.kill_enemy()
                self.enemies_destroyed += 1

            if collides(self.shooter, enemy):
                enemy.kill_enemy()
                self.enemies_destroyed += 1

                self.player_properties.player_lost_health()

                if self.player_properties.player_lives == 0:
                    self.is_player_dead = True
                    self.sound_player.play_audio_background(GameSettings.game_over_sound)
                else:
                    self.sound_player.play_audio_background(GameSettings.player_lost_health)

            for missile in self.missile_controller.missile:
                if not missile:
                    continue

                if not missile.allow_draw:
                    continue

                if collides(missile, enemy):
                    missile.allow_draw = False
                    enemy.kill_enemy()
                    self.enemies_destroyed += 1
                    self.target_hit_count += 1

                    self.hit_points[i] = (enemy.x, enemy.y)

                    self.sound_player.play_audio_background("assets/sounds/explosion-2")

    def render(self, i):
        global star_01, star_02, enemies_destroyed

        w = self.w
        h = self.h

        if self.is_in_menu:
            #self.sound_player.play_audio_background(GameSettings.intro_sound)
            return self.main_menu(i)
        elif self.is_player_dead:
            self.game_over(i)
        #elif self.success:
            #self.success_screen()
        elif len(self.enemy_controller.get_alive_enemies()) == 0:
            if not self.WIN_EVENT:
                self.WIN_EVENT = True
                self.sound_player.clear_buffer()

            if self.sound_player.is_empty():
                self.sound_player.clear_buffer()
                self.sound_player.play_audio_background(GameSettings.victory_sound)

            self.show_win_screen(i)
        else:
            stddraw.clear(stddraw.BLACK)

            stddraw.picture(star_02, w//2, h//2, w, h)
            self.game_loop(i)

    def success_screen(self):
        self.game_over_class.success()

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def render_help(self):
        pass