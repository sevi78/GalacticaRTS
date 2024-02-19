import pygame

from source.draw.dashed_line import draw_dashed_line


def draw_cross_in_circle(win, color, center, radius):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle

    # Draw the vertical line of the cross
    pygame.draw.line(win, color, (center[0], center[1] - cross_length), (center[0], center[1] + cross_length), 1)

    # Draw the horizontal line of the cross
    pygame.draw.line(win, color, (center[0] - cross_length, center[1]), (center[0] + cross_length, center[1]), 1)


def draw_dashed_cross_in_circle__(win, color, center, radius, width,dash_length ):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle

    # Draw the vertical line of the cross
    draw_dashed_line(win, color, (center[0], center[1] - cross_length), (center[0], center[1] + cross_length), width, dash_length)

    # Draw the horizontal line of the cross
    draw_dashed_line(win, color, (center[0] - cross_length, center[1]), (center[0] + cross_length, center[1]), width, dash_length)


def draw_dashed_cross_in_circle(win, color, center, radius, width, dash_length):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle
    third_length = cross_length / 3  # Divide the cross length into three parts

    # Draw the vertical line of the cross
    draw_dashed_line(win, color, (center[0], center[1] - cross_length), (center[0], center[1] - third_length), width, dash_length)
    draw_dashed_line(win, color, (center[0], center[1] + third_length), (center[0], center[1] + cross_length), width, dash_length)

    # Draw the horizontal line of the cross
    draw_dashed_line(win, color, (center[0] - cross_length, center[1]), (center[0] - third_length, center[1]), width, dash_length)
    draw_dashed_line(win, color, (center[0] + third_length, center[1]), (center[0] + cross_length, center[1]), width, dash_length)
