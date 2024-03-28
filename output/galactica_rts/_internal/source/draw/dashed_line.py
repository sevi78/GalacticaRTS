import math

import pygame


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    dashes = int(distance / dl)
    if dashes == 0:
        return

    dx_dash = dx / dashes
    dy_dash = dy / dashes

    for i in range(dashes):
        start = x1 + dx_dash * i, y1 + dy_dash * i
        end = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
        pygame.draw.line(surf, color, start, end, width)
