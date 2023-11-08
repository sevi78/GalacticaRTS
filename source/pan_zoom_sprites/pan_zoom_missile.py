import math
import random

import pygame.math

from pygame import Vector2

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.utils import global_params
from source.utils.positioning import rot_center

MISSILE_SPEED = 1.0
MISSILE_POWER = 50
MISSILE_RANGE = 3000


class PanZoomMissile__(PanZoomGameObject):  # original
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = MISSILE_SPEED
        self.explode_if_target_reached = True

    def damage(self):
        if not self.target:
            return
        self.target.energy -= MISSILE_POWER
        if self.target.energy <= 0:
            self.explode()


class PanZoomMissile_try(PanZoomGameObject):
    """
    Summary
    The PanZoomMissile class is a subclass of PanZoomGameObject that represents a missile object in a game. It inherits the properties and methods of its parent class and adds additional functionality specific to missiles.
    Example Usage
    missile = PanZoomMissile(win, x, y, width, height, pan_zoom, image_name, target=target)
    missile.update()
    Code Analysis
    Main functionalities
    Inherits properties and methods from the PanZoomGameObject class.
    Sets the speed and explosion behavior of the missile.
    Calculates the target position and sets it as the missile's target.
    Calculates the steering angle based on the target position and current position of the missile.
    Damages the target if it exists and explodes if the target's energy is depleted.

    Methods
    __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs): Initializes the PanZoomMissile object with the given parameters. Sets the speed, explosion behavior, target position, steering angle, and other attributes.
    calculate_perpendicular(self, direction): Calculates the perpendicular vector to the given direction vector.
    calculate_error(self): Calculates the error vector between the target position and the current position of the missile.
    calculate_cross_track_error(self): Calculates the cross-track error, which is the dot product of the error vector and the perpendicular vector to the steering direction.
    calculate_steering_angle(self): Calculates the steering angle based on the cross-track error and the speed of the missile.
    damage(self): Damages the target by reducing its energy. If the target's energy is depleted, the missile explodes.

    Fields
    speed: The speed of the missile.
    explode_if_target_reached: A boolean indicating whether the missile should explode when it reaches its target.
    target: The target object that the missile is aiming at.
    target_position: The position of the target object.
    steering_angle: The angle at which the missile should steer towards the target.
    rotation_smoothing: The smoothing factor for the rotation of the missile.
    prev_angle: The previous angle of rotation for the missile.
    world_x: The x-coordinate of the missile in the game world.
    world_y: The y-coordinate of the missile in the game world.
    target_reached: A boolean indicating whether the missile has reached its target.
    """
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = random.uniform(MISSILE_SPEED / 2, MISSILE_SPEED)
        self.explode_if_target_reached = True
        self.target = kwargs.get("target")
        self.target_position = None
        self.set_target_position()
        self.speed = MISSILE_SPEED
        self.steering_angle = 0
        self.rotation_smoothing = 15
        self.prev_angle = None
        self.world_x = x
        self.world_y = y
        self.target_reached = False

    # def calculate_perpendicular(self, direction):
    #     # Define the original vector
    #     v = direction
    #
    #     # Calculate the perpendicular vector
    #     p = pygame.math.Vector2(-v.y, v.x)
    #
    #     # Normalize the perpendicular vector
    #     p.normalize_ip()
    #
    #     return p
    #
    # def calculate_error(self):
    #     error = self.target_position - Vector2(self.world_x, self.world_y)
    #     return error
    #
    # def calculate_cross_track_error(self):
    #     error = self.calculate_error()
    #     direction = Vector2(math.cos(math.radians(self.steering_angle)), math.sin(math.radians(self.steering_angle)))
    #     cross_track_error = error.dot(self.calculate_perpendicular(direction))
    #     return cross_track_error
    #
    # def calculate_steering_angle(self):
    #     cross_track_error = self.calculate_cross_track_error()
    #     steering_angle = math.degrees(math.atan2(2.5 * cross_track_error, self.speed))
    #     return steering_angle

    def damage(self):
        if not self.target:
            return
        self.target.energy -= MISSILE_POWER
        if self.target.energy <= 0:
            self.explode()


class PanZoomMissile(PanZoomGameObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.explode_if_target_reached = True
        self.target = kwargs.get("target")
        self.speed = MISSILE_SPEED

    def damage(self):
        if not self.target:
            return
        self.target.energy -= MISSILE_POWER
        if self.target.energy <= 0:
            self.explode()