import math
import threading

import numpy as np
import picture
import stdaudio
import stddraw
import stdarray
import time

import GameSettings
from entities.Enemy import EnemyController
from entities.GroundEntity import Ground
from entities.Shooter import Shooter
from entities.missile_class import Missile, MissileController
from menu import Gif, TitleScreen
from utils.SoundManager import play_audio_background
from utils.utils import collides


w = 1024
h = 720

GAME_FPS = GameSettings.FPS
frame_time = 1 / GAME_FPS

last_shot_fired = time.time()

is_in_menu = True

enemy_controller = EnemyController(w, h)
ground_level = Ground(0, 0, w, 40)
shooter = Shooter("", 0, 0, w, 40, None, playerFile='assets/player1.txt', scaleFactor=40)
missile_controller = MissileController("assets/laser.gif")

gif = Gif(num_frames=5)
#gif.setup()

# setup title screen
menu = TitleScreen(w, h)

angle = 5

star_01 = picture.Picture("assets/spr_stars01.png")
star_02 = picture.Picture("assets/spr_stars02.png")

b = 0

def main_menu(i):
    global is_in_menu
    if stddraw.hasNextKeyTyped():
        is_in_menu = False

    gif.draw_frame((i % 50) // 10)
    menu.instructions()

def game_loop():
    global b, last_shot_fired

    pressed_key = stddraw.getKeysPressed()

    if stddraw.hasNextKeyTyped():
        userInput = stddraw.nextKeyTyped()
        match userInput:
            case 'A' | 'a':
                shooter.move(userInput)
            case 'D' | 'd':
                shooter.move(userInput)
            case 'q' | 'Q':
                shooter.rotate(angle)
            case 'e' | 'E':
                shooter.rotate(-angle)
            case 'x' | 'X':
                quit()

        x, y = shooter.get_x() + shooter.get_width() / 2, shooter.get_y() + shooter.get_height()

        key = userInput
        if key == ' ':  # check if new missile is being called, then creates it
            missile_controller.generate(x, y, -shooter.get_angle() * 180 / math.pi)
            play_audio_background(GameSettings.gun_fire_sound)

    missile_controller.sequence()

    shooter.drawShooter()
    print(shooter.width, shooter.height, shooter.x, shooter.y)

    if pressed_key[stddraw.K_s]:
        if time.time() - last_shot_fired > 1:
            last_shot_fired = time.time()

    ground_level.draw()

    enemy_controller.step()
    enemy_controller.render()

    shooter.drawShooter()

    for enemy in enemy_controller.enemy_list:
        if not enemy.allow_draw:
            continue

        if collides(ground_level, enemy):
            enemy.allow_draw = False
            b += 1

        if collides(shooter, enemy):
            enemy.allow_draw = False
            b += 1

        for missile in missile_controller.missile:
            if not missile:
                continue

            if not missile.allow_draw:
                continue

            if collides(missile, enemy):
                missile.allow_draw = False
                enemy.allow_draw = False

def render(i):
    global is_in_menu
    stddraw.clear(stddraw.BLACK)

    #stddraw.picture(star_01, w//2, h//2, w, h)
    #stddraw.picture(star_02, w//2, h//2, w, h)

    if is_in_menu:
        main_menu(i)
    else:
        game_loop()

if __name__ == '__main__':

    stddraw.setCanvasSize(w, h)
    stddraw.setXscale(0, w)
    stddraw.setYscale(0, h)

    stddraw._show()

    fps_lst = []

    prev_time = time.perf_counter()  # More precise than time.time()
    avg_fps_diff = 0

    i = 0
    while True:
        start_time = time.perf_counter()

        render(i)

        # Ensure the loop runs at the correct FPS
        elapsed_time = time.perf_counter() - start_time
        sleep_time = frame_time - elapsed_time
        sleep_time = 1/(1 / sleep_time + avg_fps_diff)

        if sleep_time > 0:
            time.sleep(sleep_time)

        # Compute FPS based on full frame duration
        total_frame_time = time.perf_counter() - start_time
        fps_lst.append(1 / total_frame_time)

        avg_fps = np.average(fps_lst[-20:])

        # Render FPS
        stddraw.setPenColor(stddraw.RED)
        stddraw.text(100, 100, "FPS: %.2f" % (
            avg_fps
        ))

        avg_fps_diff = GAME_FPS + 5 - avg_fps

        stddraw._show()

        i += 1
