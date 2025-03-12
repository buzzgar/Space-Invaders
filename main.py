import threading

import numpy as np
import picture
import stdaudio
import stddraw
import time
from entities.Enemy import EnemyController
from entities.GroundEntity import Ground
from utils.utils import collides

def play_audio_background(filename):
    thread = threading.Thread(target=stdaudio.playFile, args=(filename,))
    thread.daemon = True  # Ensures the thread stops when the main program exits
    thread.start()


w = 1024
h = 720

GAME_FPS = 60
frame_time = 1 / GAME_FPS

last_shot_fired = time.time()

is_in_menu = False

enemy_controller = EnemyController(w, h)
ground_level = Ground(0, 0, w, 40)

star_01 = picture.Picture("assets/spr_stars01.png")
star_02 = picture.Picture("assets/spr_stars02.png")

b = 0

def main_menu():
    pass

def game_loop():
    global b, last_shot_fired

    pressed_key = stddraw.getKeysPressed()

    if pressed_key[stddraw.K_q]:
        exit(1)

    if pressed_key[stddraw.K_s]:
        if time.time() - last_shot_fired > 1:
            play_audio_background("assets/sounds/blast-101soundboard")

            last_shot_fired = time.time()

    ground_level.draw()

    enemy_controller.step()
    enemy_controller.render()

    for enemy in enemy_controller.enemy_list:
        if not enemy.allow_draw:
            continue

        if collides(ground_level, enemy):
            enemy.allow_draw = False
            b += 1

def render():
    global is_in_menu
    stddraw.clear(stddraw.BLACK)

    #stddraw.picture(star_01, w//2, h//2, w, h)
    #stddraw.picture(star_02, w//2, h//2, w, h)

    game_loop()

    if is_in_menu:
        main_menu()

if __name__ == '__main__':

    stddraw.setCanvasSize(w, h)
    stddraw.setXscale(0, w)
    stddraw.setYscale(0, h)

    stddraw._show()

    fps_lst = []

    prev_time = time.perf_counter()  # More precise than time.time()
    avg_fps_diff = 0

    while True:
        start_time = time.perf_counter()

        render()

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
        stddraw.text(100, 100, "%.2f: %.2f" % (
            avg_fps, (1/(total_frame_time))
        ))

        avg_fps_diff = GAME_FPS + 5 - avg_fps

        stddraw._show()