import sys

import pygame

from source.draw.dashed_line import draw_dashed_line
from source.draw.arrow import draw_arrows_on_line_from_start_to_end


def draw_cross_in_circle(win, color, center, radius):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle

    # Draw the vertical line of the cross
    pygame.draw.line(win, color, (center[0], center[1] - cross_length), (center[0], center[1] + cross_length), 1)

    # Draw the horizontal line of the cross
    pygame.draw.line(win, color, (center[0] - cross_length, center[1]), (center[0] + cross_length, center[1]), 1)


def draw_dashed_cross_in_circle__(win, color, center, radius, width, dash_length):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle

    # Draw the vertical line of the cross
    draw_dashed_line(win, color, (center[0], center[1] - cross_length), (
    center[0], center[1] + cross_length), width, dash_length)

    # Draw the horizontal line of the cross
    draw_dashed_line(win, color, (center[0] - cross_length, center[1]), (
    center[0] + cross_length, center[1]), width, dash_length)


def draw_dashed_cross_in_circle(win, color, center, radius, width, dash_length):
    cross_length = radius  # The length of each arm of the cross is equal to the radius of the circle
    third_length = cross_length / 3  # Divide the cross length into three parts

    # Draw the vertical line of the cross
    draw_dashed_line(win, color, (center[0], center[1] - cross_length), (
    center[0], center[1] - third_length), width, dash_length)
    draw_dashed_line(win, color, (center[0], center[1] + third_length), (
    center[0], center[1] + cross_length), width, dash_length)

    # Draw the horizontal line of the cross
    draw_dashed_line(win, color, (center[0] - cross_length, center[1]), (
    center[0] - third_length, center[1]), width, dash_length)
    draw_dashed_line(win, color, (center[0] + third_length, center[1]), (
    center[0] + cross_length, center[1]), width, dash_length)






def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cross Drawing Example")

    # Main game loop
    arrow_pos = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a white background
        screen.fill((255, 255, 255))

        # Get the current position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        # Draw arrows from the center of the screen to the mouse position
        radius = 35

        arrow_pos += 0.01
        if arrow_pos > radius:
            arrow_pos = 0


        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
