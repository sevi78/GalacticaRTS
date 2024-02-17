import math

import pygame


def draw_arrow(screen, start_pos, target_pos, color, arrow_size):
    """
    This function draws an arrow that moves towards a target position.

    Parameters:
    screen (pygame.Surface): The surface to draw the arrow on.
    start_pos (tuple): The starting position of the arrow.
    target_pos (tuple): The target position of the arrow.
    color (tuple): The color of the arrow.
    arrow_size (int): The size of the arrow.
    """

    # Calculate the angle to the target position
    dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
    angle = math.atan2(dy, dx)

    # Calculate the end position of the arrow
    end_pos = (start_pos[0] + arrow_size * math.cos(angle), start_pos[1] + arrow_size * math.sin(angle))

    # Draw the arrow
    pygame.draw.line(screen, color, start_pos, end_pos, 2)
    pygame.draw.polygon(screen, color, [end_pos, (
    end_pos[0] - 10 * math.cos(angle - math.pi / 6), end_pos[1] - 10 * math.sin(angle - math.pi / 6)), (
                                        end_pos[0] - 10 * math.cos(angle + math.pi / 6),
                                        end_pos[1] - 10 * math.sin(angle + math.pi / 6))])
