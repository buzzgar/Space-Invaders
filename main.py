import picture
import stdio
import stddraw
import time
from Enemy import ClassicEnemy, EnemyController
from GroundEntity import Ground
from utils import collides

w = 1920
h = 1080

fps = 110

is_in_menu = False

enemy_controller = EnemyController(w, h)
ground_level = Ground(0, 0, w, 40)

star_01 = picture.Picture("resources/spr_stars01.png")
star_02 = picture.Picture("resources/spr_stars02.png")

b = 0

def main_menu():
    pass

def game_loop():
    global b

    pressed_key = stddraw.getKeysPressed()

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

    stddraw.picture(star_01, w//2, h//2, w, h)
    stddraw.picture(star_02, w//2, h//2, w, h)

    game_loop()

    if is_in_menu:
        main_menu()

if __name__ == '__main__':

    stddraw.setCanvasSize(w, h)
    stddraw.setXscale(0, w)
    stddraw.setYscale(0, h)

    stddraw._show()

    while True:

        render()

        time.sleep(1 / fps)
        stddraw._show()