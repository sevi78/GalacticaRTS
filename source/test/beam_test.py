# import random
# import pygame
# from typing import Tuple
#
# def draw_zigzag_line(surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int], num_segments: int) -> None:
#     dx = (end_pos[0] - start_pos[0]) / num_segments
#     dy = (end_pos[1] - start_pos[1]) / num_segments
#
#     for i in range(num_segments):
#         rx = random.randint(-10, 10)
#         ry = random.randint(-10, 10)
#
#         if i % 2 == 0:
#             start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
#             end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
#         else:
#             start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
#             end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
#
#         pygame.draw.line(surface, color, start, end)
#
# def draw_zigzag_line1(surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int], num_segments: int) -> None:
#     dx = (end_pos[0] - start_pos[0]) / num_segments
#     dy = (end_pos[1] - start_pos[1]) / num_segments
#
#     for i in range(num_segments):
#         rx = random.randint(-10, 10)
#         ry = random.randint(-10, 10)
#
#         if i % 2 == 0:
#             start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
#             end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
#         else:
#             start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
#             end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
#
#         pygame.draw.line(surface, color, start, end)
#
# def draw_beam_line(surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int], num_segments: int) -> None:
#     for i in range(num_segments):
#         progress = (i + 1) / num_segments
#         segment_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
#         segment_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
#
#         rx = random.randint(-10, 10)
#         ry = random.randint(-10, 10)
#         segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))
#
#         pygame.draw.line(surface, color, start_pos, segment_end)
#
# def draw_segmented_beam(surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int], num_lines: int, segments_per_line: int) -> None:
#     for line in range(num_lines):
#         progress = (line + 1) / num_lines
#         line_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
#         line_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
#         line_end = (int(line_end_x), int(line_end_y))
#
#         current_pos = start_pos
#         for segment in range(segments_per_line):
#             segment_progress = (segment + 1) / segments_per_line
#             segment_end_x = start_pos[0] + (line_end[0] - start_pos[0]) * segment_progress
#             segment_end_y = start_pos[1] + (line_end[1] - start_pos[1]) * segment_progress
#
#             rx = random.randint(-5, 5)
#             ry = random.randint(-5, 5)
#             segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))
#
#             if segment % 2 == 0:
#                 pygame.draw.line(surface, color, current_pos, segment_end)
#             else:
#                 pygame.draw.line(surface, color, segment_end, current_pos)
#
#             current_pos = segment_end
#
# def main():
#     pygame.init()
#     window = pygame.display.set_mode((800, 600))
#     clock = pygame.time.Clock()
#
#     # Initial number of segments for each function
#     num_segments = 24
#     segments_per_line = 24
#
#     run = True
#     while run:
#         clock.tick(60)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#
#             # Adjust num_segments with keyboard input
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
#                     num_segments += 2
#                 elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
#                     num_segments -= 2
#                     if num_segments < 2:   # Ensure at least two segments
#                         num_segments = 2
#
#         window.fill("black")
#
#         # Draw the functions stacked from top left to bottom left
#         color = random.choice(list(pygame.color.THECOLORS.keys()))
#
#         draw_zigzag_line(window, color, (100, 50), (300, 150), num_segments)
#         draw_zigzag_line1(window, color, (100, 200), (300, 300), num_segments)
#         draw_beam_line(window, color, (100, 350), (300, 450), num_segments)
#         draw_segmented_beam(window, color, (100, 500), (300, 600), 1 ,num_segments)
#
#         # Display text information about each function's attributes
#         font = pygame.font.Font(None, 36)
#
#         text_surface_1 = font.render(f"Zigzag Line | Segments: {num_segments}", True,(255 ,255 ,255))
#         window.blit(text_surface_1,(20 ,20))
#
#         text_surface_2 = font.render(f"Zigzag Line 1 | Segments: {num_segments}", True,(255 ,255 ,255))
#         window.blit(text_surface_2,(20 ,170))
#
#         text_surface_3 = font.render(f"Beam Line | Segments: {num_segments}", True,(255 ,255 ,255))
#         window.blit(text_surface_3,(20 ,320))
#
#         text_surface_4 = font.render(f"Segmented Beam | Lines: {4}, Segments per Line: {num_segments}", True,(255 ,255 ,255))
#         window.blit(text_surface_4,(20 ,470))
#
#         pygame.display.flip()
#
#     pygame.quit()
#     exit()
#
# if __name__ == "__main__":
#     main()


import random
import pygame
from typing import Tuple


def draw_zigzag_line(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        rx = random.randint(-spreading, spreading)
        ry = random.randint(-spreading, spreading)

        if i % 2 == 0:
            start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
            end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
        else:
            start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
            end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)

        pygame.draw.line(surface, color, start, end)


def draw_zigzag_line1(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        rx = random.randint(-spreading, spreading)
        ry = random.randint(-spreading, spreading)

        if i % 2 == 0:
            start = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)
            end = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
        else:
            start = (start_pos[0] + (i + 1) * dx + rx, start_pos[1] + (i + 1) * dy + ry)
            end = (start_pos[0] + i * dx + rx, start_pos[1] + i * dy + ry)

        pygame.draw.line(surface, color, start, end)


def draw_beam_line(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    for i in range(num_segments):
        progress = (i + 1) / num_segments
        segment_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        segment_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

        rx = random.randint(-spreading, spreading)
        ry = random.randint(-spreading, spreading)
        segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))

        pygame.draw.line(surface, color, start_pos, segment_end)


def draw_segmented_beam(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_lines: int, segments_per_line: int, spreading: int
        ) -> None:
    for line in range(num_lines):
        progress = (line + 1) / num_lines
        line_end_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        line_end_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        line_end = (int(line_end_x), int(line_end_y))

        current_pos = start_pos
        for segment in range(segments_per_line):
            segment_progress = (segment + 1) / segments_per_line
            segment_end_x = start_pos[0] + (line_end[0] - start_pos[0]) * segment_progress
            segment_end_y = start_pos[1] + (line_end[1] - start_pos[1]) * segment_progress

            rx = random.randint(-spreading // 2, spreading // 2)
            ry = random.randint(-spreading // 2, spreading // 2)
            segment_end = (int(segment_end_x + rx), int(segment_end_y + ry))

            if segment % 2 == 0:
                pygame.draw.line(surface, color, current_pos, segment_end)
            else:
                pygame.draw.line(surface, color, segment_end, current_pos)

            current_pos = segment_end


def main():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Initial number of segments and spreading value
    num_segments = 24
    segments_per_line = 24
    spreading = 20

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Adjust num_segments with keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    num_segments += 2
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    num_segments -= 2
                    if num_segments < 2:
                        num_segments = 2

                # Adjust spreading with left and right arrow keys
                if event.key == pygame.K_LEFT:
                    spreading -= 5
                    if spreading < 0:
                        spreading = 0
                elif event.key == pygame.K_RIGHT:
                    spreading += 5

        window.fill("black")

        # Draw the functions stacked from top left to bottom left
        color = random.choice(list(pygame.color.THECOLORS.keys()))
        # color = pygame.color.THECOLORS["white"]

        draw_zigzag_line(window, color, (100, 50), (300, 150), num_segments, spreading)
        draw_zigzag_line1(window, color, (100, 200), (300, 300), num_segments, spreading)
        draw_beam_line(window, color, (100, 350), (300, 450), num_segments, spreading)
        draw_segmented_beam(window, color, (100, 500), (300, 600), 1, num_segments, spreading)

        # Display text information about each function's attributes
        font = pygame.font.Font(None, 36)

        text_surface_1 = font.render(f"Zigzag Line | Segments: {num_segments}, Spreading: {spreading}", True, (
        255, 255, 255))
        window.blit(text_surface_1, (20, 20))

        text_surface_2 = font.render(f"Zigzag Line 1 | Segments: {num_segments}, Spreading: {spreading}", True, (
        255, 255, 255))
        window.blit(text_surface_2, (20, 170))

        text_surface_3 = font.render(f"Beam Line | Segments: {num_segments}, Spreading: {spreading}", True, (
        255, 255, 255))
        window.blit(text_surface_3, (20, 320))

        text_surface_4 = font.render(f"Segmented Beam | Lines: {4}, Segments per Line: {num_segments}, Spreading: {spreading}", True, (
        255, 255, 255))
        window.blit(text_surface_4, (20, 470))

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
