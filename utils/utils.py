################################################
# Student Name: Meezaan Ryklief
# Student Number: 26031825
################################################

import math

import stdaudio

import GameSettings


class GameObject:

    def __init__(self, name, x, y, width, height):
        # All game objects have a name, x and y position, width and height

        self.x = x
        self.y = y
        self.name = name

        self.width = width
        self.height = height

        self.is_alive = False
        self.is_destroyed = False

        # A flag to determine if the game object is allowed to be drawn, off by default
        self.allow_draw = False

    def draw(self):
        # Method to draw the game object if on the screen

        screen_width = GameSettings.WIDTH
        screen_height = GameSettings.HEIGHT

        if self.allow_draw and screen_width > self.x > 0 and screen_height > self.y > 0:
            self._draw()

    def _draw(self):
        pass

def collides(entity1: GameObject, entity2: GameObject, off_screen_collision=False) -> bool:
    # Class to check if any GameObjects/Entities are colliding

    # If any game object is off the screen, we exclude it from the collision or if the game object is not allowed to be drawn
    if not off_screen_collision:
        if entity1.x + entity1.width < 0 or entity1.x > GameSettings.WIDTH or entity1.y + entity1.height < 0 or entity1.y > GameSettings.HEIGHT:
            return False

    if not entity1.allow_draw or not entity2.allow_draw:
        return False

    # All GameObjects have an xy coordinate system from the center
    # To check for collision, we need to change the coordinates to the top left corner

    e1_x = entity1.x - entity1.width//2
    e1_y = entity1.y - entity1.height//2

    e2_x = entity2.x - entity2.width//2
    e2_y = entity2.y - entity2.height//2

    # Return true if the two GameObjects are colliding
    return (
            e1_x + entity1.width > e2_x and
            e1_x < e2_x + entity2.width and
            e1_y + entity1.height > e2_y and
            e1_y < e2_y + entity2.height
    )