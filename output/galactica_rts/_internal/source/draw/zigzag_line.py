import random
from typing import Tuple

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


def draw_zigzag_line1(
        surface: pygame.Surface,
        color: Tuple[int, int, int],
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        num_segments: int
        ) -> None:

    # Calculate the change in x and y for each segment
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        # Add random offset to each point for a more natural look
        rx = random.randint(-10, 10)
        ry = random.randint(-10, 10)

        if i % 2 == 0:
            # Even segments: draw from left to right
            start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
            end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
        else:
            # Odd segments: draw from right to left (creating the zigzag)
            start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
            end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)

        # Draw the line segment
        pygame.draw.line(surface, color, start, end)


def draw_beam_line(
        surface: pygame.Surface,
        color: Tuple[int, int, int],
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        num_segments: int
        ) -> None:

    for i in range(num_segments):
        # Calculate the end point for each segment
        progress = (i + 1) / num_segments
        segment_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        segment_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

        # Add random offset to the end point for a more natural look
        rx = random.randint(-10, 10)
        ry = random.randint(-10, 10)
        segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))

        # Draw the line segment from the start position to the calculated end position
        pygame.draw.line(surface, color, start_pos, segment_end)


def draw_segmented_beam(
        surface: pygame.Surface,
        color: Tuple[int, int, int],
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        num_lines: int,
        segments_per_line: int
        ) -> None:

    for line in range(num_lines):
        # Calculate the end point for this line
        progress = (line + 1) / num_lines
        line_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        line_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        line_end = (int(line_end_x), int(line_end_y))

        # Draw a zigzag line from start_pos to line_end
        current_pos = start_pos
        for segment in range(segments_per_line):
            # Calculate the end of this segment
            segment_progress = (segment + 1) / segments_per_line
            segment_end_x = start_pos[0] + (line_end[0] - start_pos[0]) * segment_progress
            segment_end_y = start_pos[1] + (line_end[1] - start_pos[1]) * segment_progress

            # Add randomness
            rx = random.randint(-5, 5)
            ry = random.randint(-5, 5)
            segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))

            # Alternate the direction for zigzag effect
            if segment % 2 == 0:
                pygame.draw.line(surface, color, current_pos, segment_end)
            else:
                pygame.draw.line(surface, color, segment_end, current_pos)

            current_pos = segment_end


def main():
    window = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill("black")

        color = random.choice(list(pygame.color.THECOLORS.keys()))
        draw_zigzag_line(window, color, (100, 500), (300, 800), 24)

        draw_zigzag_line1(window, color, (200, 700), (500, 400), 24)

        draw_beam_line(window, color, (200, 700), (500, 400), 24)

        draw_segmented_beam(window, color, (200, 700), (500, 400), 1, 24)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
