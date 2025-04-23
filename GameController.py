################################################
# Student Name: Meezaan Ryklief, Ayesha Hofmeyer, Samkelo Nkabinde
# Student Number: 26031825, 26990571, 28118944
################################################

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
from entities.Weapons import MissileController, AimController, ShieldController
from menu import Gif, TitleScreen
from utils.SoundManager import SoundPlayer
from utils.utils import collides
from GameOver import GameOverScreen

star_02 = picture.Picture("assets/game_backgrounds/back.png")


class GameProperties:
    fire_rate = GameSettings.fire_rate
    player_lives = 5
    enemies_destroyed = 0  # tally enemy death

    def __init__(self, sound_player: SoundPlayer, enemy_controller: EnemyController):
        self.sound_player = sound_player
        self.enemy_controller = enemy_controller

    def default_fire_rate(self):
        self.fire_rate = GameSettings.fire_rate

    def player_lost_health(self):
        self.player_lives -= 1

    def apply_modifiers(self, i, modifiers: List[Modifier]):

        self.enemy_controller.frozen = False

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
                elif modifier.modifier_type == modifier.FROZEN_MODIFIER:
                    self.enemy_controller.frozen = True


class Game:
    MENU_SCREEN_FLAG = 100
    GAME_SCREEN_FLAG = 200
    GAME_OVER_SCREEN_FLAG = 300

    ROTATION_ANTICLOCKWISE = -1
    ROTATION_CLOCKWISE = 1

    MOVING_LEFT = -1
    MOVING_RIGHT = 1

    def __init__(self, w, h):
        # initialise variables
        self.game_properties: GameProperties = None
        self.modifier_controller: ModifierController = None
        self.enemies_destroyed = None
        self.hit_points = {}
        self.rotating_direction = None
        self.moving_direction = None

        self.game_over_class = None
        self.shield_controller: ShieldController = None
        self.missile_controller: MissileController = None
        self.aim_controller = AimController()
        self.shooter = None
        self.ground_level = None
        self.enemy_controller: EnemyController = None

        # counts when missile hits the enemy
        self.targert_hit_count = 0

        self.w = w
        self.h = h

        self.current_screen = self.MENU_SCREEN_FLAG

        self.last_shot_fired = time.time()

        self.is_in_menu = True
        self.is_player_dead = False

        self.help = False

        # Loads pictures and generates animation
        self.intro_gif = Gif("assets/main_menu_background/menu", self.w // 2, self.h // 2)
        self.fail_gif = Gif("assets/end_game_screens/fail", self.w // 2, self.h // 2)
        self.win_gif = Gif("assets/end_game_screens/win", self.w // 2, self.h // 2)

        self.menu = TitleScreen(w, h)

        self.sound_player = SoundPlayer()

        self.reset()

        self.WIN_EVENT = False

    def main_menu(self, i):
        # Enables controls for the main menu and renders it

        if stddraw.hasNextKeyTyped():
            self.is_in_menu = False

            return True

        self.intro_gif.draw_frame((i // 8) % 5)
        self.menu.instructions()

        return False

    def game_over(self, i):
        # Enables controls for game over and renders the game over animation

        self.fail_gif.draw_frame((i // 30) % 3)
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(50)
        stddraw.text(self.w / 2 + 400, self.h - 650, "Score: +" + str(self.target_hit_count))

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def show_win_screen(self, i):
        # Enables controls for win and renders the win animation

        self.win_gif.draw_frame((i // 30) % 2)  #drawn by group member Ayesha Hofmeyer (26990571)

        if stddraw.hasNextKeyTyped():
            userInput = stddraw.nextKeyTyped()
            match userInput:
                case 'R' | 'r':
                    self.reset()

    def reset(self):
        # initialise variables to an initial state so that we can reset game

        self.is_in_menu = True  # Setting flag to true forces rendering of main menu
        self.is_player_dead = False
        self.help = False

        self.enemy_controller = EnemyController(self.w, self.h, wave=4)
        self.ground_level = Ground(0, 0, self.w, 40)
        self.shooter = Shooter("", 0, 0, self.w, 40, None, playerFile=GameSettings.player_sprite_path, scaleFactor=40)
        self.missile_controller = MissileController(None, self.shooter.get_height(), self.w, self.h)
        self.modifier_controller = ModifierController(self.w, self.h)
        self.shield_controller = ShieldController(self.shooter.get_height(), self.w, self.h)
        self.aim_controller = AimController()
        self.game_over_class = GameOverScreen(self.w, self.h)
        self.game_properties = GameProperties(self.sound_player, self.enemy_controller)

        self.moving_direction = 0
        self.rotating_direction = 0

        self.hit_points = {}

        self.target_hit_count = 0
        self.enemies_destroyed = 0

        self.WIN_EVENT = False  # A flag that is set when the player wins the game
        self.sound_player.clear_buffer()  # Clears any sound being played from previous game

    def game_loop(self, i):

        self.game_properties.default_fire_rate()
        self.game_properties.apply_modifiers(i, self.modifier_controller.get_modifiers())

        # Checks for key inputs and applies them
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
                    case 'i' | 'I':  #adds aim line
                        self.aim_controller.visibility()  #turns aim line ON/OFF
                    case 'j' | 'J':
                        self.shield_controller.visibility()  #turns shield ON/OFF
                        if self.shield_controller.shield_active:
                            self.sound_player.play_audio_background(
                                "assets/sounds/shield_activate_sound")  #from pixabay.com
                    case 'h' | 'H':  #H acts as ON/OFF switch
                        self.render_help()
                    case 'x' | 'X':
                        quit()

        centered_x, centered_y, angle = self.shooter.get_x() + self.shooter.get_width() / 2, self.shooter.get_y() + self.shooter.get_height() / 2, self.shooter.get_angle() + math.pi / 2

        self.aim_controller.generate(centered_x, centered_y, angle)
        self.shield_controller.generate(centered_x, centered_y)

        if self.moving_direction == self.MOVING_LEFT:
            self.shooter.moveLeft()

        elif self.moving_direction == self.MOVING_RIGHT:
            self.shooter.moveRight()

        if self.rotating_direction == self.ROTATION_ANTICLOCKWISE:
            self.shooter.anticlockwise()

        elif self.rotating_direction == self.ROTATION_CLOCKWISE:
            self.shooter.clockwise()

        # Checking if space is pressed/key down so that there is continuous fire
        if stddraw.getKeysPressed()[stddraw.K_SPACE]:

            centered_x, centered_y = self.shooter.get_x() + self.shooter.get_width() / 2, self.shooter.get_y() + self.shooter.get_height()

            if i > 0:  # check if new missile is being called, then creates it

                # Check if enough time has passed since last shot, so that we can achieve a desired fire rate
                if time.time() - self.last_shot_fired > self.game_properties.fire_rate:
                    self.last_shot_fired = time.time()
                    angle = int(round(self.shooter.get_angle() * 180 / math.pi, 5))

                    self.missile_controller.generate(centered_x, centered_y, angle)
                    self.sound_player.play_audio_background(GameSettings.gun_fire_sound)

        self.enemy_controller.step()
        self.enemy_controller.render_breaks(self.shooter.get_x(), self.shooter.get_y())

        # Render all entities

        # Update the missile position
        self.missile_controller.sequence()

        self.shooter.drawShooter()

        self.ground_level.draw()

        self.enemy_controller.render()

        self.shield_controller.draw()

        self.aim_controller.draw()

        if self.help: #flags true when h is pressed, then renders help display
            self.menu.help()

        self.modifier_controller.frame_render(i)

        # display counter
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(50, self.h - 20, "Hits: + " + str(self.target_hit_count))

        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(24)
        stddraw.text(self.w - 50, self.h - 20, f"♥ {self.game_properties.player_lives}")

        for hit in self.hit_points:
            stddraw.setFontSize(12)

            # Ignore hitpoints that have already been displayed for than enough time
            if i - hit > GameSettings.hit_point_frame_time:
                continue

            stddraw.setPenColor(stddraw.RED)
            stddraw.text(self.hit_points[hit][0], self.hit_points[hit][1], "+1")

        # Check for collisions
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
                    missile.allow_draw = False

            if collides(drop, self.ground_level):
                drop.kill_enemy()

            if collides(drop, self.shooter):
                drop.kill_enemy()

                self.game_properties.player_lost_health()

                if self.game_properties.player_lives == 0:
                    self.is_player_dead = True
                    self.sound_player.play_audio_background(GameSettings.game_over_sound)
                else:
                    self.sound_player.play_audio_background(GameSettings.player_lost_health)

            if self.shield_controller.shield_active:  #if shield is currently visible / called

                if collides(self.shield_controller.shield,
                            drop):  #if shield collides with dropped objects, both destroyed
                    self.shield_controller.shield_active = False
                    drop.kill_enemy()
                    self.enemies_destroyed += 1
                    self.target_hit_count += 1

                    self.hit_points[i] = (drop.x, drop.y)

                    self.sound_player.play_audio_background("assets/sounds/shield_guard_sound")  #from pixabay.com

        for enemy in self.enemy_controller.get_alive_enemies():
            if not enemy.allow_draw:
                continue

            if collides(self.ground_level, enemy):
                enemy.kill_enemy()
                self.enemies_destroyed += 1

            if collides(self.shooter, enemy):
                enemy.kill_enemy()
                self.enemies_destroyed += 1

                self.game_properties.player_lost_health()

                if self.game_properties.player_lives == 0:
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

            if self.shield_controller.shield_active:  #if shield is currently visible / called

                if collides(self.shield_controller.shield, enemy):  #if shield collides with enemy, both destroyed
                    self.shield_controller.shield_active = False
                    enemy.kill_enemy()
                    self.enemies_destroyed += 1
                    self.target_hit_count += 1

                    self.hit_points[i] = (enemy.x, enemy.y)

                    self.sound_player.play_audio_background("assets/sounds/shield_guard_sound")  #from pixabay.com

    def render(self, i):
        # Redirects game to desired screen based of flags

        global star_02

        w = self.w
        h = self.h

        if self.is_in_menu:
            return self.main_menu(i)
        elif self.is_player_dead:
            self.game_over(i)
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

            stddraw.picture(star_02, w // 2, h // 2, w, h)
            self.game_loop(i)

    def render_help(self):
        if self.help:
            self.help = False
        else:
            self.help = True
