################################################
# Student Name: Meezaan Ryklief
# Student Number: 26031825
################################################

import numpy as np
import stddraw
import time

import GameSettings
from GameController import Game

w = GameSettings.WIDTH
h = GameSettings.HEIGHT

b = 0

game = Game(w, h)

fps = GameSettings.FPS

frame_time = 1 / fps

def main():

    # Set scale one-to-one with canvas
    stddraw.setCanvasSize(w, h)
    stddraw.setXscale(0, w)
    stddraw.setYscale(0, h)

    # The following is for the FPS counter
    # it tries to keep the fps as consistent as possible
    # by sleeping for a certain amount of time

    fps_lst = []

    prev_time = time.perf_counter()  # More precise than time.time()
    avg_fps_diff = 0

    i = 0
    while True:
        start_time = time.perf_counter()

        if game.render(i):
            i = -1

        # Ensure the loop runs at the correct FPS
        elapsed_time = time.perf_counter() - start_time
        sleep_time = frame_time - elapsed_time
        sleep_time = 1/(1 / sleep_time + avg_fps_diff)

        avg_fps = np.average(fps_lst[-21:-2])

        # Render FPS
        # stddraw.setFontSize(24)
        # stddraw.setPenColor(stddraw.RED)
        # stddraw.text(100, 100, "FPS: %.2f" % (
        #     avg_fps
        # ))

        stddraw.show(max(sleep_time * 1000, 0))

        # Compute FPS based on full frame duration
        total_frame_time = time.perf_counter() - start_time
        fps_lst.append(1 / total_frame_time)

        avg_fps = np.average(fps_lst[-20:])

        avg_fps_diff = fps + 5 - avg_fps

        i += 1

if __name__ == '__main__':
    main()