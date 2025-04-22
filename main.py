import math

import numpy as np
import picture
import stddraw
import time

from GameController import Game

w = 1024
h = 720
star_01 = picture.Picture("assets/spr_stars01.png")
star_02 = picture.Picture("assets/spr_stars02.png")

b = 0

game = Game(w, h)

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

        if game.render(i):
            i = -1

        # Ensure the loop runs at the correct FPS
        elapsed_time = time.perf_counter() - start_time
        sleep_time = game.frame_time - elapsed_time
        sleep_time = 1/(1 / sleep_time + avg_fps_diff)

        if sleep_time > 0:
            time.sleep(sleep_time)

        # Compute FPS based on full frame duration
        total_frame_time = time.perf_counter() - start_time
        fps_lst.append(1 / total_frame_time)

        avg_fps = np.average(fps_lst[-20:])

        # Render FPS
        stddraw.setPenColor(stddraw.RED)
        # stddraw.text(100, 100, "FPS: %.2f" % (
        #     avg_fps
        # ))

        avg_fps_diff = game.fps + 5 - avg_fps

        stddraw._show()

        i += 1