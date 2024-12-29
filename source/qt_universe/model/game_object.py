import math

import pygame.rect

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_quadtree.model.points import Point
from source.qt_universe.model.time_handler import time_handler
from source.qt_universe.view.draw import draw_orbit_circle


#
# class Planet_(Point):
#
#     def __init__(self, x: int, y: int, width, height, image_name, color) -> None:
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.image_name = image_name
#         self.color = color
#
#     def __str__(self):
#         return f"Point(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
#
#
#
# class Planet:
#     def __init__(self, x, y, width, height, image_name, color):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.image_name = image_name
#         self.mass = uniform(1e10, 1e12)  # Random mass between 10^10 and 10^12 kg
#         self.vx = 0  # Initial velocity in x direction
#         self.vy = 0  # Initial velocity in y direction


def calculate_mass(width, height, density=5000, scaling_factor=1e-10):
    # Assume the planet is a sphere with diameter equal to the average of width and height
    diameter = (width + height) / 2
    radius = diameter / 2

    # Calculate volume (4/3 * pi * r^3)
    volume = (4 / 3) * math.pi * (radius ** 3)

    # Calculate mass
    mass = volume * density

    # Scale the mass to be within a reasonable range for the simulation
    return mass * scaling_factor


# class GameObject__(Point):
#     def __init__(self, x, y, width, height, image_name, color, type):
#         super().__init__(x, y, width, height)
#         self.color = color
#         self.image_name = image_name
#         self.type = type
#         self.orbit_object = None
#
#         self.rect = pygame.rect.Rect(x, y, width, height)
#         self.selected = False
#
#         # Calculate mass based on size
#         self.mass = calculate_mass(self.width, self.height)
#
#         self.vx = 0  # Initial velocity in x direction
#         self.vy = 0  # Initial velocity in y direction
#
#     def update(self):
#         ???

# class GameObject(Point):
#     def __init__(self, x, y, width, height, image_name, color, type, orbit_angle, orbit_speed):
#         super().__init__(x, y, width, height)
#         self.color = color
#         self.image_name = image_name
#         self.type = type
#         self.orbit_object = None
#
#         self.rect_raw = pygame.rect.Rect(x, y, width, height)
#         self.rect = pygame.rect.Rect(0, 0, 0, 0)
#         self.selected = False
#
#         self.mass = calculate_mass(self.width, self.height)
#
#         self.vx = 0
#         self.vy = 0
#         self.lod = 0
#
#         self.orbit_angle = orbit_angle
#         self.orbit_speed = orbit_speed  # Adjust this value to change orbital speed
#
#     def set_lod(self):
#         r = self.width / 2 * pan_zoom_handler.get_zoom()
#         if r < 1:
#             self.lod = 0
#         elif r < 10:
#             self.lod = 1
#         else:
#             self.lod = 2
#
#     def update(self):
#         if self.type == "planet" and self.orbit_object:
#             # Calculate the constant orbit radius
#             orbit_radius = math.hypot(self.x - self.orbit_object.x, self.y - self.orbit_object.y)
#
#             # Update the orbit angle
#             self.orbit_angle += self.orbit_speed * time_handler.game_speed
#
#             # Calculate new position maintaining constant distance
#             self.x = self.orbit_object.x + orbit_radius * math.cos(self.orbit_angle) * time_handler.game_speed
#             self.y = self.orbit_object.y + orbit_radius * math.sin(self.orbit_angle) * time_handler.game_speed
#
#         # Update screen_rect
#         screen_x, screen_y = pan_zoom_handler.world_2_screen(self.x, self.y)
#         screen_width = self.width * pan_zoom_handler.get_zoom()
#         screen_height = self.height * pan_zoom_handler.get_zoom()
#         self.rect_raw.center = (int(self.x), int(self.y))
#         self.rect = pygame.Rect(
#                 screen_x - screen_width / 2,
#                 screen_y - screen_height / 2,
#                 screen_width,
#                 screen_height
#                 )
#
#         self.set_lod()


import math


class GameObject(Point):
    def __init__(self, x, y, width, height, image_name, color, type, orbit_angle=0, orbit_speed=0.01):
        super().__init__(x, y, width, height)
        self.color = color
        self.image_name = image_name
        self.type = type
        self.orbit_object = None

        self.rect_raw = pygame.rect.Rect(x, y, width, height)
        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.selected = False

        self.mass = calculate_mass(self.width, self.height)

        self.vx = 0
        self.vy = 0
        self.lod = 0

        self.orbit_angle = orbit_angle
        self.orbit_speed = orbit_speed  # Adjust this value to change orbital speed

    def set_lod(self):
        r = self.width / 2 * pan_zoom_handler.get_zoom()
        if r < 1:
            self.lod = 0
        elif r < 10:
            self.lod = 1
        else:
            self.lod = 2

    def update(self):
        if self.type == "planet" and self.orbit_object:
            # Calculate the constant orbit radius
            orbit_radius = math.hypot(self.x - self.orbit_object.x, self.y - self.orbit_object.y)

            # Update the orbit angle based on game speed
            self.orbit_angle += self.orbit_speed * time_handler.game_speed

            # Calculate new position maintaining constant distance
            self.x = self.orbit_object.x + orbit_radius * math.cos(self.orbit_angle)
            self.y = self.orbit_object.y + orbit_radius * math.sin(self.orbit_angle)

        # Update screen_rect
        screen_x, screen_y = pan_zoom_handler.world_2_screen(self.x, self.y)
        screen_width = self.width * pan_zoom_handler.get_zoom()
        screen_height = self.height * pan_zoom_handler.get_zoom()

        # Update rects
        self.rect_raw.center = (int(self.x), int(self.y))
        self.rect = pygame.Rect(
                screen_x - screen_width / 2,
                screen_y - screen_height / 2,
                screen_width,
                screen_height
                )

        self.set_lod()



