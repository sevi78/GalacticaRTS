import pygame
import sys

from source.draw.arrow import draw_arrows_on_line_from_start_to_end


# Define the draw_arrows_on_line_from_start_to_end function as provided


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Arrow Drawing Example")



    # Main game loop
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
        draw_arrows_on_line_from_start_to_end(
            surf=screen,
            color=(0, 0, 0),
            start_pos=(screen_width // 2, screen_height // 2),
            end_pos=mouse_pos,
            width=1,
            dash_length=55,
            arrow_size=(2, 10)
            )

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()