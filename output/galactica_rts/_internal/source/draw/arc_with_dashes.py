import math

import pygame


def draw_arc_with_dashes(surf, color, rect, start_angle, stop_angle, radius, dash_length=10, width=1):
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

def draw_arc_with_dashes__(surf, color, rect, start_angle, stop_angle, radius, dash_length=10, width=1):
    circumference = 2 * math.pi * radius
    arc_length = (abs(stop_angle - start_angle) / 360) * circumference
    num_dashes = int(arc_length / dash_length)

    for i in range(num_dashes):
        angle = start_angle + (abs(stop_angle - start_angle) / num_dashes) * i
        end_angle = start_angle + (abs(stop_angle - start_angle) / num_dashes) * (i + 1)
        pygame.draw.arc(surf, color, rect, math.radians(angle), math.radians(end_angle), width)
