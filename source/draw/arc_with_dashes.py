import math
import time

import os
from functools import lru_cache

import psutil
import pygame
from pygame import Rect

DEBUG = False
DEBUG_BORDER = 0 if not DEBUG else 50

@lru_cache(maxsize=10000)
def calculate_arc_dash_points(rect, start_angle, stop_angle, radius, dash_length, clip_rect):
    total_angle = stop_angle - start_angle
    if total_angle == 0:
        return tuple()  # No need to draw dashes if the arc length is 0

    circumference = 2 * math.pi * radius
    arc_length = (total_angle / 360) * circumference
    num_dashes = int(arc_length / dash_length)
    if num_dashes == 0:
        return tuple()  # No need to draw dashes if there are no dashes to draw

    angle_increment = math.radians(total_angle / num_dashes)

    center_x, center_y = rect[0] + radius, rect[1] + radius
    left, top, right, bottom = clip_rect

    points = []
    for i in range(num_dashes):
        angle = math.radians(start_angle) + i * angle_increment
        start_x = center_x + radius * math.cos(angle)
        start_y = center_y + radius * math.sin(angle)
        angle += angle_increment / 2
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)

        # Check if the dash is within the clip rect
        if (left <= start_x <= right and top <= start_y <= bottom and
                left <= end_x <= right and top <= end_y <= bottom):
            points.append(((start_x, start_y), (end_x, end_y)))

    return tuple(points)


def draw_arc_with_dashes(surf, color, rect, start_angle, stop_angle, radius, dash_length=10, width=1):
    clip_rect_ = surf.get_clip()
    border = DEBUG_BORDER
    clip_rect = Rect(clip_rect_[0] + border, clip_rect_[1] + border, clip_rect_[2]-border *2, clip_rect_[3]-border *2)
    points = calculate_arc_dash_points(tuple(rect), start_angle, stop_angle, radius, dash_length,
            (clip_rect.left, clip_rect.top, clip_rect.right, clip_rect.bottom))

    draw_line = pygame.draw.line
    for start, end in points:
        draw_line(surf, color, start, end, width)



def main():
    pygame.init()
    win = pygame.display.set_mode((600, 600))
    test_loops = 1000
    radii = [10, 20, 30, 100, 200, 300, 600]
    dash_lengths = [5, 10, 15, 20, 25, 30]
    positions = [(100, 100), (200, 200), (300, 300), (600, 600)]

    fastest_function = None
    min_time = float('inf')

    for func in [draw_arc_with_dashes]:
        # win.fill((0, 0, 0))
        start_time = time.perf_counter()
        for radius in radii:
            for dash_length in dash_lengths:
                for pos in positions:
                    for i in range(test_loops):
                        func(win, (100, 100, 100), pygame.Rect(pos[0], pos[1], 100, 100), 0, 360, radius, dash_length=dash_length, width=1)
                    # pygame.display.flip()

        end_time = time.perf_counter()
        time_taken = end_time - start_time

        print(f"Function: {func.__name__}, Radius: {radius}, Dash Length: {dash_length}, Time taken: {time_taken}")

        if time_taken < min_time:
            min_time = time_taken
            fastest_function = func.__name__

    # Get memory usage of the current Python process
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_usage_mb = memory_info.rss / (1024 * 1024)  # Convert bytes to MB

    print(f"Fastest function overall: {fastest_function}, Time: {min_time}, Memory Usage: {memory_usage_mb:.2f} MB")



if __name__ == "__main__":
    main()
