import stdio
import stddraw
import time

fps = 60

is_in_menu = False

def main_menu():
    pass

def game_loop():
    pass

def render():
    global is_in_menu

    if is_in_menu:
        main_menu()

if __name__ == '__main__':

    stddraw.setCanvasSize(800, 600)
    stddraw.setXscale(0, 800)
    stddraw.setYscale(0, 600)

    stddraw._show()

    while True:

        stddraw.clear(stddraw.WHITE)

        render()

        time.sleep(1 / fps)
        stddraw._show()