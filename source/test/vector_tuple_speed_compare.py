import math
import time
import pygame
from pygame.math import Vector2

def vector2_operations():
    direction = Vector2(1.0, 0.0)
    for _ in range(1000000):
        direction = direction.rotate(1)
        direction *= 1.01
        direction.normalize_ip()

def tuple_operations():
    direction = (1.0, 0.0)
    for _ in range(1000000):
        x, y = direction
        direction = (
            x * math.cos(math.radians(1)) - y * math.sin(math.radians(1)),
            x * math.sin(math.radians(1)) + y * math.cos(math.radians(1))
        )
        direction = (direction[0] * 1.01, direction[1] * 1.01)
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        direction = (direction[0] / length, direction[1] / length)

pygame.init()

start_time = time.time()
vector2_operations()
vector2_time = time.time() - start_time

start_time = time.time()
tuple_operations()
tuple_time = time.time() - start_time

print(f"Vector2 operations time: {vector2_time:.6f} seconds")
print(f"Tuple operations time: {tuple_time:.6f} seconds")
print(f"Vector2 is {tuple_time / vector2_time:.2f}x faster than tuple operations")
