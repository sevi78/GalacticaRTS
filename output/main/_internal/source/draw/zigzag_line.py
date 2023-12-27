import random
import pygame


def draw_zigzag_line(surface, color, start_pos, end_pos, num_segments):  # orig
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        rx = random.randint(-10, 10)
        ry = random.randint(-10, 10)
        if i % 2 == 0:
            start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
            end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
        else:
            start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
            end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
        pygame.draw.line(surface, color, start, end)


def draw_zigzag_line__(surface, color, start_pos, end_pos, num_segments, pan_zoom_handler):
    zoom = pan_zoom_handler.zoom
    start_pos = (start_pos[0] * zoom, start_pos[1] * zoom)
    end_pos = (end_pos[0] * zoom, end_pos[1] * zoom)
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        rx = random.randint(-10, 10) * zoom
        ry = random.randint(-10, 10) * zoom
        if i % 2 == 0:
            start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
            end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
        else:
            start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
            end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
        pygame.draw.line(surface, color, start, end)
