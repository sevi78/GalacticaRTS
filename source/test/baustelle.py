# Calculate direction vector
import math

import pygame


# def degrees_to_vector2(rotation_angle:float, movement_speed:float)->pygame.math.Vector2:
#     angle_radians = math.radians(rotation_angle)
#     x_component = math.cos(angle_radians) * movement_speed
#     y_component = math.sin(angle_radians) * movement_speed
#     direction = pygame.math.Vector2(x_component, y_component)
#
#     return direction


import math
import pygame

# def degrees_to_vector2(rotation_angle: float, movement_speed: float) -> pygame.math.Vector2:
#     angle_radians = math.radians(rotation_angle)
#     x_component = -math.sin(angle_radians) * movement_speed
#     y_component = -math.cos(angle_radians) * movement_speed
#     return pygame.math.Vector2(x_component, y_component)

import math
import pygame
from pygame import Vector2

#
# def degrees_to_vector2(rotation_angle: float, movement_speed: float) -> pygame.math.Vector2:
#     angle_radians = math.radians(rotation_angle)
#     x_component = -math.sin(angle_radians) * movement_speed
#     y_component = math.cos(angle_radians) * movement_speed
#     return pygame.math.Vector2(x_component, y_component)
#
# for i in range (360):
#     print (f"rotation_angle = {i}, direction = {degrees_to_vector2(i, 10)}")



p = Vector2(12,  0)

print (p.x)
