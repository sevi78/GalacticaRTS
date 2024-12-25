import pygame


def limit_number(n: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(n, max_value))


def get_sum_up_to_n(dict_, n):
    sum_ = 0
    for key, value in dict_.items():
        if key < n:
            sum_ += value

    return sum_

import math
import pygame
def degrees_to_vector2(rotation_angle: float, movement_speed: float) -> pygame.math.Vector2:
    angle_radians = math.radians(rotation_angle)
    x_component = -math.sin(angle_radians) * movement_speed
    y_component = math.cos(angle_radians) * movement_speed
    return pygame.math.Vector2(x_component, y_component)


def get_rotate_correction_angle(image_points_to:str)-> int:
    """
    Returns the angle correction for rotation based on the 'image_points_to':

    0 - image is looking to the right
    90 - image is looking up
    180 - image is looking to the left
    270 - image is looking down

    """
    rotation_correction_angles = {"right": 0, "up": -90, "left": -180, "down": -270}
    return rotation_correction_angles[image_points_to]