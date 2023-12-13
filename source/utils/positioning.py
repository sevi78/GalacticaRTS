import math

import pygame
from pygame_widgets.util import drawText

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils import global_params


def smooth_position(prev_x, prev_y, x, y, smooth):
    new_x, new_y = None, None

    if abs(prev_x - x) > smooth:
        new_x = prev_x + smooth if x > prev_x else prev_x - smooth
    else:
        new_x = x

    if abs(prev_y - y) > smooth:
        new_y = prev_y + smooth if y > prev_y else prev_y - smooth
    else:
        new_y = y

    return new_x, new_y


def rot_center(image, angle, x, y):
    """
    rotates the image around its center
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def get_distance(pos_a, pos_b):
    if not pos_a:
        return 0

    x = pos_a[0]
    y = pos_a[1]
    x1 = pos_b[0]
    y1 = pos_b[1]
    distance = math.dist((x, y), (x1, y1))

    return distance


def limit_positions(obj, screen_size):
    """
    this hides the obj if it is outside the screen
    """

    border = 0
    x, y = obj.get_position()

    def hide_obj_outside_view():
        if x <= border or x >= screen_size[0] - border or y <= border or y >= screen_size[1] - border:
            obj.hide()
        else:
            obj.show()

    if hasattr(obj, "property"):
        if not obj.property == "ship" or obj.property == "planet":
            hide_obj_outside_view()
    else:
        hide_obj_outside_view()


def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def prevent_object_overlap(objects, min_dist):
    smoothing = 100
    for obj1 in objects:
        for obj2 in objects:
            if obj1 != obj2:
                distance = distance_between_points(obj1.world_x, obj1.world_y, obj2.world_x, obj2.world_y)
                if distance < min_dist:

                    # Calculate the direction vector
                    dx = obj1.world_x - obj2.world_x
                    dy = obj1.world_y - obj2.world_y

                    # Normalize the direction vector
                    try:
                        length = math.sqrt(dx * dx + dy * dy)
                    except ZeroDivisionError:
                        length = 1

                    try:
                        dx /= length
                        dy /= length
                    except ZeroDivisionError:
                        dx = 1
                        dy = 1

                    # Move the ships apart
                    adjustment = (min_dist - distance) / 2 / smoothing
                    obj1.world_x += dx * adjustment
                    obj1.world_y += dy * adjustment
                    obj2.world_x -= dx * adjustment
                    obj2.world_y -= dy * adjustment





