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


def ndigits(v: float, digit=4) -> int:
    """return a number of digits for a float:

    set digit to lowest number of digits, for example 0.0001 would be 4
    """

    n = 0

    if v < 1.0:
        n = max(0, math.ceil(-math.log10(abs(v))))
        n -= digit
    if v >= 1.0:
        n = max(0, math.ceil(math.log10(abs(v))))
        n += digit - 1

    return abs(n)