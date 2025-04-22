import math

import color
import stdaudio


class GameObject:

    def __init__(self, name, x, y, width, height, color):
        self.x = x
        self.y = y
        self.name = name

        self.width = width
        self.height = height

        self.color = color

        self.is_alive = False
        self.is_destroyed = False

        self.allow_draw = False

    def draw(self):
        if self.allow_draw:
            self._draw()

    def _draw(self):
        pass

class Music:
    def __init__(self, file):
        self.filename = file

    def play_audio(self):
        stdaudio.playFile(self.filename)

def collides(entity1: GameObject, entity2: GameObject) -> bool:

    e1_x = entity1.x - entity1.width//2
    e1_y = entity1.y - entity1.height//2

    e2_x = entity2.x - entity2.width//2
    e2_y = entity2.y - entity2.height//2

    return (
            e1_x + entity1.width > e2_x and
            e1_x < e2_x + entity2.width and
            e1_y + entity1.height > e2_y and
            e1_y < e2_y + entity2.height
    )

def rotate_2d_array(array, angle_degrees):
    height = len(array)
    width = len(array[0])
    angle_radians = math.radians(angle_degrees)

    # Calculate center of the original array
    cx, cy = width / 2.0, height / 2.0

    # Compute sine and cosine of the angle
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)

    # Estimate size of the new rotated image (bounding box)
    new_width = int(abs(width * cos_theta) + abs(height * sin_theta)) + 1
    new_height = int(abs(height * cos_theta) + abs(width * sin_theta)) + 1

    # Center of the new image
    new_cx, new_cy = new_width / 2.0, new_height / 2.0

    # Create new rotated array filled with 0
    rotated = [[0 for _ in range(new_width)] for _ in range(new_height)]

    for y_new in range(new_height):
        for x_new in range(new_width):
            # Coordinates in the new image, relative to its center
            x_shifted = x_new - new_cx
            y_shifted = y_new - new_cy

            # Inverse rotate to find the corresponding source coordinate
            x_orig = cos_theta * x_shifted + sin_theta * y_shifted + cx
            y_orig = -sin_theta * x_shifted + cos_theta * y_shifted + cy

            # Nearest neighbor interpolation
            x_nearest = int(round(x_orig))
            y_nearest = int(round(y_orig))

            if 0 <= x_nearest < width and 0 <= y_nearest < height:
                rotated[y_new][x_new] = array[y_nearest][x_nearest]

    return rotated

def rgb_to_int(rgb):
    r, g, b = rgb
    return (r << 16) + (g << 8) + b

def int_to_rgb(value):
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = value & 0xFF
    return (r, g, b)
