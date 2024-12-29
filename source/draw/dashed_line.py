import math
import random
from functools import lru_cache

import pygame
from pygame import Rect

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEBUG = False
DEBUG_BORDER = 0 if not DEBUG else 50


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
    border = DEBUG_BORDER
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
