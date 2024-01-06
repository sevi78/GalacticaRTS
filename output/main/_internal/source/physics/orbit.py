import math

import pygame

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.positioning import get_distance


def get_orbit_pos(self):
    if self.orbit_object.property == "ufo":
        pos = self.orbit_object.rect.center
    else:
        pos = self.orbit_object.rect.center
    return pos


def get_orbit_angle(x, y, x1, y1):
    """ sets the orbit angle, needed for correct positioning
    """
    # Calculate the difference in x and y coordinates
    delta_x = x1 - x
    delta_y = y - y1  # Invert the y-coordinate

    # Calculate the angle using atan2 function
    angle_rad = math.atan2(delta_y, delta_x)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Adjust the angle to be between 0 and 360 degrees
    orbit_angle = (angle_deg + 360) % 360

    return orbit_angle


def set_orbit_angle(self, value):
    self.orbit_angle = value


def set_orbit_object_id(self, orbit_object_id):
    """ sets the orbit id needed to find the orbit object
    """
    self.orbit_object_id = orbit_object_id
    set_orbit_object(self)


def set_orbit_object(self):
    """ sets the orbit object based on the orbit id
    """
    ignore = ["Sun", "Sun1"]
    if self.name not in ignore:
        orbit_object = [i for i in sprite_groups.planets if i.id == self.orbit_object_id]
        if len(orbit_object) > 0:
            self.orbit_object = orbit_object[0]
    else:
        self.orbit_object_id = self.id
        self.orbit_object = self


def set_orbit_distance(self, obj):
    """ sets orbit distance, used for displaying the orbit
    """
    if obj:
        self.orbit_distance = get_distance(self.center, obj.center)
    else:
        print("set_orbit_distance: no obj:", self.name, obj.name)


def orbit_around(orbit_object, orbit_center, **kwargs):
    panzoom = pan_zoom_handler
    zoom = panzoom.zoom

    orbit_radius = kwargs.get("orbit_radius", 150) * zoom
    orbit_angle = math.atan2(orbit_object.get_screen_y() - orbit_center.get_screen_y(), orbit_object.get_screen_x() - orbit_center.get_screen_x())

    if hasattr(orbit_object, "speed"):
        orbit_speed = orbit_object.speed / int(global_params.fps)
    else:
        orbit_speed = orbit_object.orbit_speed / int(global_params.fps)
    orbit_angle += orbit_speed * global_params.time_factor * (1 + zoom)

    new_x = orbit_center.get_screen_x() + orbit_radius * math.cos(orbit_angle) + orbit_center.orbit_speed * global_params.time_factor
    new_y = orbit_center.get_screen_y() + orbit_radius * math.sin(orbit_angle) + orbit_center.orbit_speed * global_params.time_factor

    return new_x, new_y


def orbit(obj, orbit_obj, orbit_speed, direction):
    if not orbit_obj:
        return

    if hasattr(obj, "enemy"):
        orbit_speed = orbit_speed/5

    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)
    obj.orbit_radius = pos_diff.length()
    if not obj.orbit_angle:
        obj.orbit_angle = pos_diff.angle_to(pygame.math.Vector2(0, 1))

    obj.orbit_angle += orbit_speed * global_params.time_factor
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(obj.orbit_angle * direction)  # Rotate by the negative angle
    obj.world_x, obj.world_y = (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)
