import math
import random

import pygame

from source.handlers.pan_zoom_sprite_handler import sprite_groups


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


def rot_center(image, angle, x, y, **kwargs):
    """
    rotates the image around its center
    """
    align = kwargs.get("align", "center")
    rotated_image = pygame.transform.rotate(image, angle)
    if align == "center":
        new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    if align == "topleft":
        new_rect = rotated_image.get_rect(topleft=image.get_rect(topleft=(x, y)).center)

    if align == "bottomleft":
        new_rect = rotated_image.get_rect(bottomleft=image.get_rect(bottomleft=(x, y)).center)

    if align == "topright":
        new_rect = rotated_image.get_rect(topright=image.get_rect(topright=(x, y)).center)

    if align == "bottomright":
        new_rect = rotated_image.get_rect(bottomright=image.get_rect(bottomright=(x, y)).center)

    # special hacky align for ships
    if align == "shipalign":
        new_rect = rotated_image.get_rect(topleft=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def limit_positions(obj, screen_size):  # unused
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


def prevent_object_overlap(objects, min_dist):  # this should be replaced with math.dist
    smoothing = 100
    for obj1 in objects:
        for obj2 in objects:
            if obj1 != obj2:
                distance = math.dist((obj1.world_x, obj1.world_y), (obj2.world_x, obj2.world_y))
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


def get_random_pos(left_end, right_end, top_end, bottom_end, central_compression):  # circular, more dense in the center
    radius = (right_end - left_end) / 2
    center_x = (right_end + left_end) / 2
    center_y = (top_end + bottom_end) / 2

    theta = 2 * math.pi * random.random()  # Random angle
    r = radius * (random.random() ** central_compression)  # Random radius to the power of 'power'

    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)

    return x, y


def align_horizontal(rect, h_align):
    #
    if h_align == "right_outside":
        return rect.right

    return rect.x


def align_vertical(rect, v_align):
    # if v_align == "below_the_bottom":
    #     x, y = pan_zoom_handler.screen_2_world(rect.x, rect.bottom)
    #     return y
    #
    # elif v_align == "over_the_top":
    #     x, y = pan_zoom_handler.screen_2_world(rect.x, rect.top )
    #     return y
    if v_align == "below_the_bottom":
        return rect.y + rect.height * 1.3

    elif v_align == "over_the_top":
        return rect.y - rect.height * .3

    return rect.y


def smooth_planet_positions__(width, height):  # ki
    center_x = width / 2
    center_y = height / 2
    for planet in sprite_groups.planets.sprites():
        # check if it has an orbit object

        if planet.orbit_object:
            dist_x = planet.world_x - center_x
            dist_y = planet.world_y - center_y
            distance_from_center = math.hypot(dist_x, dist_y)

            if distance_from_center > min(width, height) / 2:
                # Calculate the angle from the center to the current position
                angle = math.atan2(dist_y, dist_x)
                # Set the position to the edge of the circular boundary
                planet.world_x = center_x + (min(width, height) / 2) * math.cos(angle)
                planet.world_y = center_y + (min(width, height) / 2) * math.sin(angle)


import math


def smooth_planet_positions(width, height):
    center_x = width / 2
    center_y = height / 2
    boundary_radius = min(width, height) / 2

    for planet in sprite_groups.planets.sprites():
        if planet.orbit_object:
            dist_x = planet.world_x - center_x
            dist_y = planet.world_y - center_y
            distance_from_center = math.hypot(dist_x, dist_y)

            # Include the planet's radius in the boundary check
            if distance_from_center + planet.orbit_radius > boundary_radius:
                # Calculate the angle from the center to the current position
                angle = math.atan2(dist_y, dist_x)
                # Set the position to the edge of the circular boundary minus the planet's radius
                new_distance = boundary_radius - planet.orbit_radius
                planet.world_x = center_x + new_distance * math.cos(angle)
                planet.world_y = center_y + new_distance * math.sin(angle)