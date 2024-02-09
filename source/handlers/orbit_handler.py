import math

import pygame
from pygame import Vector2

from source.configuration import global_params
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import get_distance


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


def orbit__(obj, orbit_obj, orbit_speed, direction):
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
        obj.orbit_angle = pos_diff.angle_to(pygame.math.Vector2(1, 0)) if direction > 0 else pos_diff.angle_to(pygame.math.Vector2(-1, 0))

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Update the object's world position
    obj.world_x = orbit_obj.world_x + pos.x
    obj.world_y = orbit_obj.world_y + pos.y


import pygame


def orbit___(obj, orbit_obj, orbit_speed, direction):
    if not orbit_obj:
        return

    if hasattr(obj, "enemy"):
        orbit_speed = orbit_speed / 5

    # Calculate the position difference between the orbiting object and the object
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)

    # Set the orbit radius based on the current distance to the orbiting object
    obj.orbit_radius = pos_diff.length()

    # Dynamically calculate the initial orbit angle based on the current position
    if not obj.orbit_angle:
        # Calculate the angle from the orbit center to the object
        initial_angle = pos_diff.angle_to(pygame.math.Vector2(1, 0))
        # Adjust the angle based on the direction of orbit
        if direction < 0:
            initial_angle = -initial_angle
        obj.orbit_angle = initial_angle

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Update the object's world position
    obj.world_x = orbit_obj.world_x + pos.x
    obj.world_y = orbit_obj.world_y + pos.y


import pygame
import math


def orbit____(obj, orbit_obj, orbit_speed, direction):
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
        obj.orbit_angle = math.degrees(math.atan2(-pos_diff.y, pos_diff.x))
        # Adjust the angle for the direction of orbit
        if direction < 0:
            obj.orbit_angle += 180
        obj.orbit_angle %= 360

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Update the object's world position
    obj.world_x = orbit_obj.world_x + pos.x
    obj.world_y = orbit_obj.world_y + pos.y


import pygame
import math


def orbit(obj, orbit_obj, orbit_speed, direction):
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
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Update the object's world position
    obj.world_x = orbit_obj.world_x + pos.x
    obj.world_y = orbit_obj.world_y + pos.y



def orbit_ship_(obj, orbit_obj, orbit_speed, direction):
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
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)


    # get distance to orbit position
    if get_distance((obj.world_x,obj.world_y), pos) > 10:
        gradually_move_towards(obj,(obj.world_x,obj.world_y), pos)
    else:

        # Update the object's world position
        obj.world_x = orbit_obj.world_x + pos.x
        obj.world_y = orbit_obj.world_y + pos.y

def gradually_move_towards_(obj, current_pos, target_pos):
    # Calculate the direction from the current position to the target position
    direction = target_pos - current_pos

    # Calculate the distance between the current position and the target position
    distance = direction.length()

    # Normalize the direction vector
    if distance != 0:
        direction /= distance

    # Calculate the displacement vector for each time step
    displacement = direction * obj.speed * global_params.game_speed

    # Move the object towards the target position with a constant speed
    obj.world_x += displacement.x
    obj.world_y += displacement.y

    # Check if the object has reached the target position
    if distance <= obj.speed * global_params.game_speed:
        return True  # Object has reached the target position
    else:
        return False  # Object is still moving towards the target position


def orbit_ship__(obj, orbit_obj, orbit_speed, direction):
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
        obj.orbit_angle = pos_diff.angle_to(pygame.math.Vector2(1, 0)) if direction > 0 else pos_diff.angle_to(pygame.math.Vector2(-1, 0))

    # Update the orbit angle based on the orbit speed and game speed
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Gradually move the object towards the desired initial orbit position


    target_pos = pygame.math.Vector2(orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)
    if gradually_move_towards(obj,(obj.world_x, obj.world_y), target_pos ):
        # Update the object's world position
        obj.world_x = orbit_obj.world_x + pos.x
        obj.world_y = orbit_obj.world_y + pos.y


def gradually_move_towards__(obj, current_pos, target_pos):
    direction = target_pos + Vector2(current_pos[0], current_pos[1])

    # Calculate the distance between the current position and the target position
    distance = direction.length() * pan_zoom_handler.zoom

    # Normalize the direction vector
    try:
        direction.normalize()
    except Exception as e:
        print(f"move_towards_target error! (direction.normalize()):{e}")

    # Calculate the displacement vector for each time step
    displacement = direction * obj.speed * global_params.game_speed

    # Calculate the number of time steps needed to reach the target position
    time_steps = int(distance / obj.speed) / pan_zoom_handler.zoom

    # Move the obj towards the target position with a constant speed
    try:
        obj.world_x += displacement.x / time_steps
        obj.world_y += displacement.y / time_steps
    except ZeroDivisionError as e:
        print(f"move_towards_target error! (self.world_x += displacement.x / time_steps...):{e}")

    if (obj.world_x, obj.world_y) == (target_pos.x, target_pos.y):
        return True
    else:
        return False



import pygame
import math

def orbit_ship(obj, orbit_obj, orbit_speed, direction):
    if not orbit_obj:
        return

    if hasattr(obj, "enemy"):
        orbit_speed = orbit_speed / 5

    # Calculate the position difference between the orbiting object and the object
    pos_diff = pygame.math.Vector2(orbit_obj.world_x, orbit_obj.world_y) - pygame.math.Vector2(obj.world_x, obj.world_y)

    # # Calculate the most common direction based on the relative position
    # if pos_diff.x > 0:  # Orbiting object is to the right
    #     if pos_diff.y > 0:  # Orbiting object is above
    #         direction = -1  # Clockwise
    #     else:  # Orbiting object is below
    #         direction = 1  # Counterclockwise
    # else:  # Orbiting object is to the left
    #     if pos_diff.y > 0:  # Orbiting object is above
    #         direction = 1  # Counterclockwise
    #     else:  # Orbiting object is below
    #         direction = -1  # Clockwise

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
    obj.orbit_angle += orbit_speed * direction * global_params.game_speed
    obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

    # Calculate the new position based on the orbit radius and angle
    pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

    # Gradually move the object towards the desired initial orbit position
    if get_distance((obj.world_x, obj.world_y), (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y)) > 10:
        gradually_move_towards(obj, (obj.world_x, obj.world_y), (orbit_obj.world_x + pos.x, orbit_obj.world_y + pos.y))
    else:
        # Update the object's world position
        obj.world_x = orbit_obj.world_x + pos.x
        obj.world_y = orbit_obj.world_y + pos.y

def gradually_move_towards(obj, current_pos, target_pos):
    # Calculate the direction from the current position to the target position
    direction = (target_pos[0] - current_pos[0], target_pos[1] - current_pos[1])

    # Calculate the distance between the current position and the target position
    distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

    # Normalize the direction vector
    if distance != 0:
        direction = (direction[0] / distance, direction[1] / distance)

    # Calculate the displacement vector for each time step
    displacement = (direction[0] * obj.speed * global_params.game_speed, direction[1] * obj.speed * global_params.game_speed)

    # Move the object towards the target position with a constant speed
    obj.world_x += displacement[0]
    obj.world_y += displacement[1]

    # Check if the object has reached the target position
    if distance <= obj.speed * global_params.game_speed:
        return True  # Object has reached the target position
    else:
        return False  # Object is still moving towards the target position



"""
if obj is left of orbit_obj and upon orbit_obj: direction must be counterclockwise
if obj is right of orbit_obj and upon orbit_obj: direction must be clockwise
if obj is left of orbit_obj and below orbit_obj: direction must be clockwise
if obj is right of orbit_obj and below orbit_obj: direction must be counterclockwise
"""