################################################
# Student Name: Meezaan Ryklief
# Student Number: 26031825
################################################

from random import randint

import stddraw
from utils.PictureLoader import Picture

import GameSettings
from utils.utils import GameObject


class Modifier(GameObject):
    # FLAGS that indicate the type of modifier
    HEALTH_MODIFIER = 0
    FIRE_RATE_MODIFIER = 1
    FROZEN_MODIFIER = 2

    DISABLE_TIME = -1

    def __init__(self, x, y, filename):

        self.pic = Picture(filename)
        width = self.pic.width()
        height = self.pic.height()

        super().__init__("Modifier PowerUps", x, y, width, height)
        self.allow_draw = True

        self.is_picked_up = False
        self.frame_used = -1

        # Indicates how long the modifier is active in seconds
        self.allowed_time_use = self.DISABLE_TIME

        # Number of times the modifier can be used
        self.uses = 1

        self.modifier_type = None

    def _draw(self):
        stddraw.picture(self.pic, self.x, self.y, self.width, self.height)

    def pick_up(self, i):
        # Called when an player picks up/collides with the modifier

        self.is_picked_up = True
        self.allow_draw = False
        self.frame_used = i

    def is_active(self, i):
        # checks if the modifier is still active

        # If the allowed time is -1, determines if the modifier can be used based off the number of uses left
        if self.allowed_time_use == self.DISABLE_TIME:
            if self.uses > 0:
                self.uses -= 1
                return True
            return False

        # If the allowed time is not -1, determines if the modifier is still active
        if i - self.frame_used > self.allowed_time_use * GameSettings.FPS:
            return False
        return True


# Define modifier classes and set up there revalent attributes
class HealthUpModifier(Modifier):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)

        # Set amount of health received
        self.health_delta = 1
        # Disable time
        self.allowed_time_use = self.DISABLE_TIME

        # Set number of uses
        self.uses = 2

        self.modifier_type = Modifier.HEALTH_MODIFIER

# Change player fire rate
class FireRateModifier(Modifier):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)

        # Set fire rate
        self.fire_rate = 0.1
        # Set allowed time
        self.allowed_time_use = 3

        # Set modifier type
        self.modifier_type = Modifier.FIRE_RATE_MODIFIER

# Freeze enemies
class FreezeModifier(Modifier):
    def __init__(self, x, y, filename):
        super().__init__(x, y, filename)

        # Set freeze time
        self.allowed_time_use = 5

        # Set modifier type
        self.modifier_type = Modifier.FROZEN_MODIFIER


class ModifierController:
    def __init__(self, screen_width, screen_height):
        self.modifiers = []

        self.screen_width = screen_width
        self.screen_height = screen_height

    def frame_render(self, i):
        # Renders all modifiers/powerups on the screen
        # Also enables new modifiers to spawn randomly
        # Moves the modifiers down the screen

        if randint(0, GameSettings.CHANCE_OF_FIRE_RATE_MODIFIER) == 0:
            spawn_x, spawn_y = self.random_spawn_location()

            self.modifiers.append(FireRateModifier(
                spawn_x, spawn_y, "assets/modifiers/bullets-36.png"))

        if randint(0, GameSettings.CHANCE_OF_HEALTH) == 0:
            spawn_x, spawn_y = self.random_spawn_location()

            self.modifiers.append(HealthUpModifier(
                spawn_x, spawn_y, "assets/modifiers/heart-plus-36.png"))

        if randint(0, GameSettings.CHANCE_OF_FREEZE_BOMB) == 0:
            spawn_x, spawn_y = self.random_spawn_location()

            self.modifiers.append(FreezeModifier(spawn_x, spawn_y, "assets/modifiers/ice-bolt-48.png"))

        # Update positions of modifiers and draw
        for modifier in self.modifiers:
            modifier.y -= 5
            modifier.draw()

    def random_spawn_location(self):
        # Generates a random spawn location for a modifier

        return randint(int(self.screen_width * 0.2), int(self.screen_width * 0.8)), randint(
            int(self.screen_height * 0.8), self.screen_height)

    def get_modifiers(self) -> list:
        # Returns the list of modifiers
        return self.modifiers
