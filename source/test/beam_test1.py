import random
from typing import Tuple

import pygame

start_color = (0, 0, 0)
end_color = (255, 255, 255)
num_points = 10
num_lines = 5
num_turns = 5


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


def draw_wavy_line(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    amplitude = 20
    frequency = 5
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        x_offset = amplitude * random.choice([-1, 1]) * (i % frequency == 0)
        y_offset = amplitude * random.choice([-1, 1])

        start = (start_pos[0] + i * dx + x_offset, start_pos[1] + i * dy + y_offset)
        end = (start_pos[0] + (i + 1) * dx + x_offset, start_pos[1] + (i + 1) * dy + y_offset)

        pygame.draw.line(surface, color, start, end)


def draw_dotted_line(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    dot_radius = 5
    dx = (end_pos[0] - start_pos[0]) / num_segments
    dy = (end_pos[1] - start_pos[1]) / num_segments

    for i in range(num_segments):
        x_offset = random.randint(-spreading // 2, spreading // 2)
        y_offset = random.randint(-spreading // 2, spreading // 2)

        dot_position = (
            int(start_pos[0] + i * dx + x_offset),
            int(start_pos[1] + i * dy + y_offset)
            )

        pygame.draw.circle(surface, color, dot_position, dot_radius)


def draw_solid_line(
        surface: pygame.Surface, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    pygame.draw.line(surface, color, start_pos, end_pos)


def draw_curved_line(
        surface: pygame.Surface, color: Tuple[int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int],
        num_segments: int, spreading: int
        ) -> None:
    points = []
    for i in range(num_segments):
        t = i / num_segments
        x = (1 - t) ** 2 * start_pos[0] + 2 * (1 - t) * t * random.randint(
                start_pos[0] - 50, start_pos[0] + 50) + t ** 2 * end_pos[0]
        y = (1 - t) ** 2 * start_pos[1] + 2 * (1 - t) * t * random.randint(
                start_pos[1] - 50, start_pos[1] + 50) + t ** 2 * end_pos[1]
        points.append((int(x), int(y)))

    for i in range(len(points) - 1):
        pygame.draw.line(surface, color, points[i], points[i + 1])


def draw_spiral_line(
        surface: pygame.Surface, color: Tuple[int, int, int], center_position: Tuple[int, int], radius: int,
        num_turns: int, num_points: int
        ) -> None:
    prev_x, prev_y = center_position
    for i in range(num_points):
        angle = i * (num_turns * 2 * 3.14159 / num_points)
        x = center_position[0] + radius * angle * random.uniform(0.8, 1.2) * random.choice([-1, 1])
        y = center_position[1] + radius * angle * random.uniform(0.8, 1.2) * random.choice([-1, 1])

        if i > 0:
            pygame.draw.line(surface, color, (prev_x, prev_y), (int(x), int(y)))

        prev_x, prev_y = x, y


def draw_fade_line(
        surface: pygame.Surface,
        color: Tuple[int, int, int],
        start_position: Tuple[int, int],
        end_position: Tuple[int, int],
        num_segments: int,
        spreading: int
        ) -> None:
    for i in range(num_segments):
        alpha = max(255 - (255 // num_segments) * i, 0)
        # Ensure that color is a tuple of 4 elements (R, G, B, A)
        segment_color = (color[0], color[1], color[2], alpha)

        segment_start_x = start_position[0] + ((end_position[0] - start_position[0]) / num_segments) * i
        segment_start_y = start_position[1] + ((end_position[1] - start_position[1]) / num_segments) * i

        segment_end_x = segment_start_x + ((end_position[0] - start_position[0]) / num_segments)
        segment_end_y = segment_start_y + ((end_position[1] - start_position[1]) / num_segments)

        # Debugging output
        print(f"Segment Color: {segment_color}")  # Check color values
        pygame.draw.line(surface, segment_color, (segment_start_x, segment_start_y), (segment_end_x, segment_end_y))


def draw_rainbow_line(
        surface: pygame.Surface, color_list: list[start_color:int, end_color:int, num_points:int]
        ) -> None:
    for j in range(num_points):
        color_index = j % len(color_list)

        for k in range(len(color_list) - 1):
            r = color_list[color_index][0]
            g = color_list[color_index][1]
            b = color_list[color_index][2]

            pygame.draw.circle(surface, (r, g, b), (100 + j * 10, k * 10), 5)


def draw_random_lines(
        surface: pygame.Surface, color_tuple: list[start_color:int, end_color:int, num_lines:int]
        ) -> None:
    for _ in range(num_lines):
        start_x = random.randint(100, 1820)
        start_y = random.randint(100, 980)

        end_x = random.randint(100, 1820)
        end_y = random.randint(100, 980)

        pygame.draw.line(surface, (255, 255, 255), (start_x, start_y), (end_x, end_y))


def main():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0), (0, 255, 0),
                      (0, 255, 127), (0, 255, 255), (0, 127, 255), (0, 0,
                                                                    255), (127, 0, 255), (255,
                                                                                          0,
                                                                                          255)]

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

        draw_zigzag_line(window, color, (100, 50), (300, 150), num_segments, spreading)
        draw_wavy_line(window, color, (100, 200), (300, 300), num_segments, spreading)
        draw_dotted_line(window, color, (100, 350), (300, 450), num_segments, spreading)
        draw_solid_line(window, color, (100, 500), (300, 600), num_segments, spreading)
        draw_curved_line(window, color, (100, 650), (300, 750), num_segments, spreading)

        # Spiral Line Drawing Example
        # draw_spiral_line(window, color, (500, 200), 50, num_turns, num_points)

        # Fade Line Drawing Example
        # draw_fade_line(window, color, (500, 400), (800, 400), num_segments, spreading)

        # Rainbow Line Drawing Example

        # draw_rainbow_line(window, rainbow_colors)

        # Random Lines Drawing Example
        # draw_random_lines(window, (255,255,255),)

        # Display text information about each function's attributes

        draw_function_texts(font, num_segments, rainbow_colors, spreading, window)

        pygame.display.update()

    pygame.quit()
    exit()


def draw_function_texts(font, num_segments, rainbow_colors, spreading, window):
    text_surface_1 = font.render(f"Zigzag Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_1, (20,
                                 20))
    text_surface_2 = font.render(f"Wavy Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_2, (20,
                                 170))
    text_surface_3 = font.render(f"Dotted Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_3, (20,
                                 320))
    text_surface_4 = font.render(f"Solid Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_4, (20,
                                 470))
    text_surface_5 = font.render(f"Curved Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_5, (20,
                                 620))
    text_surface_6 = font.render(f"Spiral Line | Radius:{50}, Turns:{num_segments}", True,
            (255,
             255,
             255))
    window.blit(text_surface_6, (20,
                                 770))
    text_surface_7 = font.render(f"Fade Line | Segments:{num_segments}, Spreading:{spreading}", True,
            (255,
             255,
             255))
    window.blit(text_surface_7, (20,
                                 920))
    text_surface_8 = font.render(f"Rainbow Line | Colors Count:{len(rainbow_colors)}", True,
            (255,
             255,
             255))
    window.blit(text_surface_8, (20,
                                 1070))
    text_surface_9 = font.render(f"Random Lines | Count:{10}", True,
            (255,
             255,
             255))
    window.blit(text_surface_9, (20,
                                 1175))


if __name__ == "__main__":
    main()
