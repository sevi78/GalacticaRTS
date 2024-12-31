import math

import pygame

from source.configuration.game_config import config
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import rotate_image_to

POINTING_WEAPONS = ["laser", "phaser"]

def get_orbit_pos(self):#????
    if self.orbit_object.property == "ufo":
        pos = self.orbit_object.rect.center
    else:
        pos = self.orbit_object.rect.center
    return pos

def get_orbit_pos_(self):
    return self.orbit_object.rect.center


def set_orbit_object_id(self, orbit_object_id):
    """ sets the orbit id needed to find the orbit object
    """
    if not self.id == orbit_object_id:
        self.orbit_object_id = orbit_object_id
        set_orbit_object(self)
    else:
        print("set_orbit_object_id error: self.id == orbit_object_id!")


def set_orbit_object(self):# original
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


def set_orbit_object_(self):
    """ sets the orbit object based on the orbit id
    """

    orbit_objects = [i for i in sprite_groups.planets if i.id == self.orbit_object_id]
    if len(orbit_objects) > 0:
        self.orbit_object = orbit_objects[0]
    # else:
    #     self.orbit_object_id = self.id
    #     self.orbit_object = self



def orbit_with_constant_distance(
        obj, orbit_obj, orbit_speed, direction
        ):  # used for planets, new with constant orbit distance
    if not orbit_obj:
        return

    if hasattr(obj, "enemy"):
        orbit_speed = orbit_speed / 5

    # Calculate the position difference between the orbiting object and the object
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)

    # Set the orbit radius based on the current distance to the orbiting object
    obj.orbit_radius = pos_diff.length()

    # If the orbit angle is not set, calculate it based on the current position
    if not obj.orbit_angle:
        # Calculate the angle from the orbit center to the object
        obj.orbit_angle = math.degrees(math.atan2(pos_diff.y, pos_diff.x))
        # Adjust the angle for the direction of orbit
        if direction < 0:
            obj.orbit_angle += 180
        obj.orbit_angle %= 360

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * time_handler.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Keep the distance constant by adjusting the position based on the orbit radius
    new_pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Update the object's world position while maintaining the constant distance
    if config.app.game_client.is_host:
        obj.world_x = orbit_obj.world_x + new_pos.x
        obj.world_y = orbit_obj.world_y + new_pos.y


def orbit_ship(obj, orbit_obj, orbit_speed, direction):
    if not orbit_obj:
        return

    if not obj.state_engine.state == "attacking":
        obj.state_engine.set_state("orbiting")

    obj.orbiting = True

    if hasattr(obj, "enemy"):
        orbit_speed = orbit_speed / 5

    # Calculate the position difference between the orbiting object and the object
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)

    # Set the desired orbit radius
    desired_orbit_radius = obj.desired_orbit_radius  # pos_diff.length()

    # If the orbit angle is not set, calculate it based on the current position
    if not obj.orbit_angle:
        # Calculate the angle from the orbit center to the object
        obj.orbit_angle = math.degrees(math.atan2(pos_diff.y, pos_diff.x))
        # Adjust the angle for the direction of orbit
        if direction < 0:
            obj.orbit_angle += 180
        obj.orbit_angle %= 360

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * time_handler.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the desired orbit radius and angle
    pos = pygame.math.Vector2(desired_orbit_radius, 0).rotate(-obj.orbit_angle)

    # Gradually move the object towards the desired initial orbit position
    if math.dist((obj.world_x, obj.world_y), (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)) > 10:
        gradually_move_towards(obj, (obj.world_x, obj.world_y), (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y))
    else:
        # Update the object's world position
        if config.app.game_client.is_host:
            obj.world_x = orbit_obj.world_x + pos.x
            obj.world_y = orbit_obj.world_y + pos.y

    # rotate the image
    if obj.weapon_handler.current_weapon["name"] in  POINTING_WEAPONS:
        rotation_correction_angle = 90
    else:
        rotation_correction_angle = 180

    if not obj.state_engine.state == "attacking":
        obj.angle = rotate_image_to(obj, orbit_obj.rect.center, rotation_correction_angle)


def gradually_move_towards(obj, current_pos, target_pos):  # unused
    # Calculate the direction from the current position to the target position
    direction = (target_pos[0] - current_pos[0], target_pos[1] - current_pos[1])

    # Calculate the distance between the current position and the target position
    distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

    # Normalize the direction vector
    if distance != 0:
        direction = (direction[0] / distance, direction[1] / distance)

    # Calculate the displacement vector for each time step
    displacement = (
        direction[0] * obj.speed * time_handler.game_speed, direction[1] * obj.speed * time_handler.game_speed)

    # Move the object towards the target position with a constant speed
    if config.app.game_client.is_host:
        obj.world_x += displacement[0]
        obj.world_y += displacement[1]

    # Check if the object has reached the target position
    if distance <= obj.speed * time_handler.game_speed:
        return True  # Object has reached the target position
    else:
        return False  # Object is still moving towards the target position


"""
if obj is left of orbit_obj and upon orbit_obj: direction must be counterclockwise
if obj is right of orbit_obj and upon orbit_obj: direction must be clockwise
if obj is left of orbit_obj and below orbit_obj: direction must be clockwise
if obj is right of orbit_obj and below orbit_obj: direction must be counterclockwise
"""
