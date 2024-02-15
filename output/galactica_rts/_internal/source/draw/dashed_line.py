import math

import pygame

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx ** 2 + dy ** 2)
    dashes = int(distance / dl)

    for i in range(dashes):
        start = x1 + (dx / dashes) * i, y1 + (dy / dashes) * i
        end = x1 + (dx / dashes) * (i + 0.5), y1 + (dy / dashes) * (i + 0.5)
        pygame.draw.line(surf, color, start, end, width)