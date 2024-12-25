# import math
#
# import pygame
#
#
# def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
#     x1, y1 = start_pos
#     x2, y2 = end_pos
#     dl = dash_length
#
#     dx = x2 - x1
#     dy = y2 - y1
#     distance = math.hypot(dx, dy)
#     if distance == 0:
#         return
#     dashes = int(distance / dl)
#     if dashes == 0:
#         return
#
#     dx_dash = dx / dashes
#     dy_dash = dy / dashes
#
#     for i in range(dashes):
#         start = x1 + dx_dash * i, y1 + dy_dash * i
#         end = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
#         pygame.draw.line(surf, color, start, end, width)
# import pygame
# import math
# import random
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# pygame.display.set_caption("Dashed Lines Test")
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
#
# def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
#     x1, y1 = start_pos
#     x2, y2 = end_pos
#     dl = dash_length
#
#     dx = x2 - x1
#     dy = y2 - y1
#     distance = math.hypot(dx, dy)
#     if distance == 0:
#         return
#     dashes = int(distance / dl)
#     if dashes == 0:
#         return
#
#     dx_dash = dx / dashes
#     dy_dash = dy / dashes
#
#     for i in range(dashes):
#         start = x1 + dx_dash * i, y1 + dy_dash * i
#         end = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
#         pygame.draw.line(surf, color, start, end, width)
#
# # Main game loop
# running = True
# clock = pygame.time.Clock()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.VIDEORESIZE:
#             # Handle window resize event
#             width, height = event.size
#             screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
#
#     # Fill the screen with white
#     screen.fill(WHITE)
#
#     # Draw 10 dashed lines with different lengths
#     for i in range(100):
#         start_pos = (50, 50 + i * (height // 11))
#         end_pos = (50 + random.randint(100, width - 100), 50 + i * (height // 11))
#         color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         line_width = random.randint(1, 3)
#         dash_length = random.randint(5, 20)
#
#         draw_dashed_line(screen, color, start_pos, end_pos, line_width, dash_length)
#
#     # Update the display
#     pygame.display.flip()
#
#     # Cap the frame rate and update FPS in caption
#     fps = clock.get_fps()
#     pygame.display.set_caption(f"Dashed Lines Test - FPS: {fps:.2f}")
#     clock.tick(60)
#
# # Quit Pygame
# pygame.quit()

#
# import pygame
# import math
# import random
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# pygame.display.set_caption("Dashed Lines Test")
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
#
# def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
#     x1, y1 = start_pos
#     x2, y2 = end_pos
#     dl = dash_length
#
#     dx = x2 - x1
#     dy = y2 - y1
#     distance = math.hypot(dx, dy)
#     if distance == 0:
#         return
#     dashes = int(distance / dl)
#     if dashes == 0:
#         return
#
#     dx_dash = dx / dashes
#     dy_dash = dy / dashes
#
#     for i in range(dashes):
#         start = x1 + dx_dash * i, y1 + dy_dash * i
#         end = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
#         pygame.draw.line(surf, color, start, end, width)
#
# # Generate consistent properties for each line
# line_properties = []
# for i in range(10):
#     color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     line_width = random.randint(1, 3)
#     dash_length = random.randint(5, 20)
#     length_factor = random.uniform(0.3, 0.9)  # Factor to determine line length
#     line_properties.append((color, line_width, dash_length, length_factor))
#
# # Main game loop
# running = True
# clock = pygame.time.Clock()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.VIDEORESIZE:
#             # Handle window resize event
#             width, height = event.size
#             screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
#
#     # Fill the screen with white
#     screen.fill(WHITE)
#
#     # Draw 10 dashed lines with consistent properties
#     for i, (color, line_width, dash_length, length_factor) in enumerate(line_properties):
#         start_pos = (50, 50 + i * (height // 11))
#         end_pos = (55050 + int(length_factor * (width - 100)), 50 + i * (height // 11))
#         draw_dashed_line(screen, color, start_pos, end_pos, line_width, dash_length)
#
#     # Update the display
#     pygame.display.flip()
#
#     # Cap the frame rate and update FPS in caption
#     fps = clock.get_fps()
#     pygame.display.set_caption(f"Dashed Lines Test - FPS: {fps:.2f}")
#     clock.tick(60)
#
# # Quit Pygame
# pygame.quit()


# The rest of your code remains the same


import random

from pygame import Rect

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


#
#
def draw_dashed_line_(surf, color, start_pos, end_pos, width=1, dash_length=10):  # origiona
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    # Get screen boundaries
    clip_rect = surf.get_clip()

    # Calculate the line equation: y = mx + b
    if abs(x2 - x1) > 1e-6:  # Check if the line is not vertical
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
    else:
        m = None
        b = None

    # Clip line to screen boundaries
    if m is not None:
        # Check left and right boundaries
        if x1 < clip_rect.left:
            y1 = m * clip_rect.left + b
            x1 = clip_rect.left
        elif x1 > clip_rect.right:
            y1 = m * clip_rect.right + b
            x1 = clip_rect.right
        if x2 < clip_rect.left:
            y2 = m * clip_rect.left + b
            x2 = clip_rect.left
        elif x2 > clip_rect.right:
            y2 = m * clip_rect.right + b
            x2 = clip_rect.right

        # Check top and bottom boundaries
        if abs(m) > 1e-6:  # Avoid division by very small numbers
            if y1 < clip_rect.top:
                x1 = (clip_rect.top - b) / m
                y1 = clip_rect.top
            elif y1 > clip_rect.bottom:
                x1 = (clip_rect.bottom - b) / m
                y1 = clip_rect.bottom
            if y2 < clip_rect.top:
                x2 = (clip_rect.top - b) / m
                y2 = clip_rect.top
            elif y2 > clip_rect.bottom:
                x2 = (clip_rect.bottom - b) / m
                y2 = clip_rect.bottom
        else:
            # Nearly horizontal line
            y1 = y2 = max(clip_rect.top, min(y1, clip_rect.bottom))
    else:
        # Vertical line
        x1 = x2 = max(clip_rect.left, min(x1, clip_rect.right))
        y1 = max(clip_rect.top, min(y1, clip_rect.bottom))
        y2 = max(clip_rect.top, min(y2, clip_rect.bottom))

    # Ensure x1, y1, x2, y2 are within the clip rect
    x1 = max(clip_rect.left, min(x1, clip_rect.right))
    y1 = max(clip_rect.top, min(y1, clip_rect.bottom))
    x2 = max(clip_rect.left, min(x2, clip_rect.right))
    y2 = max(clip_rect.top, min(y2, clip_rect.bottom))

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance < 1:  # If the line is too short, don't draw anything
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


import pygame
import math
from functools import lru_cache


@lru_cache(maxsize=1000)
def calculate_dash_points(start_pos, end_pos, dash_length, clip_rect):
    x1, y1 = end_pos
    x2, y2 = start_pos
    dl = dash_length
    left, top, right, bottom = clip_rect

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance < 1:
        return []

    dashes = int(distance / dl)
    if dashes == 0:
        return []

    dx_dash = dx / dashes
    dy_dash = dy / dashes

    points = []
    for i in range(dashes):
        end = x1 + dx_dash * i, y1 + dy_dash * i
        start = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)

        # Check if the dash is within the clip rect
        if (left <= start[0] <= right and top <= start[1] <= bottom and
                left <= end[0] <= right and top <= end[1] <= bottom):
            points.append((start, end))

    return tuple(points)


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    clip_rect_ = surf.get_clip()
    border = 50
    clip_rect = Rect(
            clip_rect_[0] + border, clip_rect_[1] + border, clip_rect_[2] - border * 2, clip_rect_[3] - border * 2)
    points = calculate_dash_points(start_pos, end_pos, dash_length,
            (clip_rect.left, clip_rect.top, clip_rect.right, clip_rect.bottom))

    draw_line = pygame.draw.line
    for start, end in points:
        draw_line(surf, color, start, end, width)


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Dashed Lines Test")

    # Generate consistent properties for each line
    line_properties = []
    for i in range(10):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        line_width = random.randint(1, 3)
        dash_length = random.randint(5, 20)
        length_factor = random.uniform(0.3, 0.9)  # Factor to determine line length
        line_properties.append((color, line_width, dash_length, length_factor))

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize event
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Fill the screen with white
        screen.fill(WHITE)

        pygame.draw.rect(screen, (123, 123, 123), (30, 30, 200, 200))
        # Draw 10 dashed lines with consistent properties
        for i, (color, line_width, dash_length, length_factor) in enumerate(line_properties):
            start_pos = (50, 50 + i * (height // 11))
            end_pos = (55050 + int(length_factor * (width - 100)), 50 + i * (height // 11))
            draw_dashed_line(screen, color, start_pos, end_pos, line_width, dash_length)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate and update FPS in caption
        fps = clock.get_fps()
        pygame.display.set_caption(f"Dashed Lines Test - FPS: {fps:.2f}")
        clock.tick(60)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
