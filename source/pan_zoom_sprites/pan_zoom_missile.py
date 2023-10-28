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


class PanZoomMissile__(PanZoomGameObject):#original
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


class PanZoomMissile(PanZoomGameObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = random.uniform(MISSILE_SPEED/2, MISSILE_SPEED)
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

    def set_target_position__(self):
        if hasattr(self.target, "property"):
            if self.target.property == "planet":
                self.target_position = self.pan_zoom.screen_2_world(self.target.screen_x, self.target.screen_y)
                return

            if self.target.property == "ship":
                self.target_position = self.target.rect.center

            if self.target.property == "ufo":
                x,y = Vector2((self.target.world_x, self.target.world_y))
                x_offset, y_offset = int(self.target.rect.width/3), int(self.target.rect.height/3)
                x -= random.randint(- x_offset, x_offset)
                y -= random.randint(- y_offset, y_offset)
                self.target_position = (x, y)
    def calculate_perpendicular(self, direction):
        # Define the original vector
        v = direction

        # Calculate the perpendicular vector
        p = pygame.math.Vector2(-v.y, v.x)

        # Normalize the perpendicular vector
        p.normalize_ip()

        return p

    def calculate_error(self):
        error = self.target_position - Vector2(self.world_x, self.world_y)
        return error

    def calculate_cross_track_error(self):
        error = self.calculate_error()
        direction = Vector2(math.cos(math.radians(self.steering_angle)), math.sin(math.radians(self.steering_angle)))
        cross_track_error = error.dot(self.calculate_perpendicular(direction))
        return cross_track_error

    def calculate_steering_angle(self):
        cross_track_error = self.calculate_cross_track_error()
        steering_angle = math.degrees(math.atan2(2.5 * cross_track_error, self.speed))
        return steering_angle

    def rotate_image_to_target__(self):
        target = self.target_position
        rel_x, rel_y = target.x - self.world_x, target.y - self.world_y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # Smoothing algorithm
        if self.prev_angle:
            diff = angle - self.prev_angle
            if abs(diff) > self.rotation_smoothing:
                angle = self.prev_angle + 5 * (diff / abs(diff))

        self.prev_angle = angle
        new_image, new_rect = rot_center(self.image, angle, self.rect.x, self.rect.y)
        self.image = new_image
        self.rect = new_rect

    def move_towards_target__(self):
        self.steering_angle = self.calculate_steering_angle()
        self.rotate_image_to_target()

        # Calculate the displacement vector for each time step
        displacement = Vector2(self.speed * math.cos(math.radians(self.steering_angle)), self.speed * math.sin(math.radians(self.steering_angle)))

        # Move the missile towards the target position with a constant speed
        self.world_x += displacement.x
        self.world_y += displacement.y
        print ("missile.move_towards_target", self.world_x, self.world_y)
        # Check if the missile has reached the target position
        if self.calculate_error().length() < self.speed:
            self.target_reached = True

    def damage(self):
        if not self.target:
            return
        self.target.energy -= MISSILE_POWER
        if self.target.energy <= 0:
            self.explode()


