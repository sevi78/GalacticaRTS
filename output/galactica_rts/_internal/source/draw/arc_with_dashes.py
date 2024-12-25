import math

import pygame

from source.handlers.time_handler import time_handler


def draw_arc_with_dashes_original(
        surf, color, rect, start_angle, stop_angle, radius, dash_length=10,
        width=1
        ):  # original
    # Calculate the total angle and the number of dashes
    total_angle = stop_angle - start_angle
    circumference = 2 * math.pi * radius
    arc_length = (total_angle / 360) * circumference
    num_dashes = int(arc_length / dash_length)

    for i in range(num_dashes):
        angle = start_angle + (total_angle / num_dashes) * i
        start = rect[0] + radius + radius * math.cos(math.radians(angle)), rect[
            1] + radius + radius * math.sin(math.radians(angle))
        angle += total_angle / (2 * num_dashes)
        end = rect[0] + radius + radius * math.cos(math.radians(angle)), rect[
            1] + radius + radius * math.sin(math.radians(angle))
        pygame.draw.line(surf, color, start, end, width)


def draw_arc_with_dashes(surf, color, rect, start_angle, stop_angle, radius, dash_length=10, width=1):
    # Calculate the total angle and the number of dashes
    total_angle = stop_angle - start_angle
    circumference = 2 * math.pi * radius
    arc_length = (total_angle / 360) * circumference
    if arc_length == 0:
        return  # No need to draw dashes if the arc length is 0

    num_dashes = int(arc_length / dash_length)
    if num_dashes == 0:
        return  # No need to draw dashes if there are no dashes to draw

    angle_increment = total_angle / num_dashes
    start_angle_rad = math.radians(start_angle)
    angle_increment_rad = math.radians(angle_increment)

    for i in range(num_dashes):
        angle = start_angle_rad + angle_increment_rad * i
        start = rect[0] + radius + radius * math.cos(angle), rect[1] + radius + radius * math.sin(angle)
        angle += angle_increment_rad / 2
        end = rect[0] + radius + radius * math.cos(angle), rect[1] + radius + radius * math.sin(angle)
        pygame.draw.line(surf, color, start, end, width)


def draw_arc_with_dashes_copilot(surf, color, rect, start_angle, stop_angle, radius, dash_length=10, width=1):
    # Calculate the total angle and the number of dashes
    total_angle = stop_angle - start_angle
    circumference = 2 * math.pi * radius
    arc_length = (total_angle / 360) * circumference
    num_dashes = int(arc_length / dash_length)

    # Precompute as much as possible outside the loop
    angle_step = total_angle / num_dashes
    half_angle_step = angle_step / 2
    start_rad = math.radians(start_angle)
    step_rad = math.radians(angle_step)
    half_step_rad = math.radians(half_angle_step)
    center_x, center_y = rect[0] + radius, rect[1] + radius

    # Use a list to store line segments and draw them in a batch
    lines = []
    for i in range(num_dashes):
        # Calculate start point
        start_rad += step_rad
        start_x = center_x + radius * math.cos(start_rad)
        start_y = center_y + radius * math.sin(start_rad)

        # Calculate end point
        end_rad = start_rad + half_step_rad
        end_x = center_x + radius * math.cos(end_rad)
        end_y = center_y + radius * math.sin(end_rad)

        # Append line segment to list
        lines.append(((int(start_x), int(start_y)), (int(end_x), int(end_y))))

    # Draw all lines in a batch
    for line in lines:
        pygame.draw.line(surf, color, line[0], line[1], width)


# Example usage:
# Assuming 'screen' is a pygame.Surface object
# draw_arc_with_dashes(screen, (255, 255, 255), (100, 100, 200, 200), 0, 180, 100)


def main():
    pygame.init()
    win = pygame.display.set_mode((600, 600))
    test_loops = 1000000
    start_original = time_handler.time
    for i in range(test_loops):
        draw_arc_with_dashes_original(win, (
            100, 100, 100), pygame.Rect(10, 10, 100, 100), 90, 180, 20, dash_length=10, width=1)
    end_original = time_handler.time
    print(f"Original: {end_original - start_original} seconds for {test_loops} loops")

    start_codium = time_handler.time
    for i in range(test_loops):
        draw_arc_with_dashes(win, (100, 100, 100), pygame.Rect(10, 10, 100, 100), 90, 180, 20, dash_length=10, width=1)
    end_codium = time_handler.time
    print(f"Codium: {end_codium - start_codium} seconds for {test_loops} loops")

    start_copilot = time_handler.time
    for i in range(test_loops):
        draw_arc_with_dashes_copilot(win, (
            100, 100, 100), pygame.Rect(10, 10, 100, 100), 90, 180, 20, dash_length=10, width=1)
    end_copilot = time_handler.time
    print(f"Copilot: {end_copilot - start_copilot} seconds for {test_loops} loops")


"""
result:
Original: 6.172613143920898 seconds for 1000000 loops
Codium: 5.6729700565338135 seconds for 1000000 loops
Copilot: 6.202739953994751 seconds for 1000000 loops
coduium is fastest
"""

if __name__ == '__main__':
    main()
