# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# win = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Background Gradient")
#
# # Define the colors for the gradient
# color1 = (255, 0, 0)  # Red
# color2 = (0, 0, 255)  # Blue
#
# # Draw the background gradient using geometric primitives and color blending
# for y in range(600):
#     # Interpolate the color based on the vertical position
#     color = (int(color1[0] * (1 - y / 600) + color2[0] * (y / 600)),
#              int(color1[1] * (1 - y / 600) + color2[1] * (y / 600)),
#              int(color1[2] * (1 - y / 600) + color2[2] * (y / 600)))
#     # Draw a horizontal line at the current vertical position with the interpolated color
#     pygame.draw.line(win, color, (0, y), (800, y))
#
# # Update the display
# pygame.display.flip()
#
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
# # Quit Pygame
# pygame.quit()

#
# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the display
# win = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Background Gradient")
#
# # Create a surface for the background gradient
# background = pygame.Surface((800, 600))
#
# # Define the colors for the gradient
# black = (0, 0, 0)
# transparent = (0, 0, 0, 0)
#
# # Fill the surface with a black color
# background.fill(black)
#
# # Create a transparent rectangle in the center
# center_rect = pygame.Rect(50, 50, 700, 500)
# pygame.draw.rect(background, transparent, center_rect)
#
# # Draw the background surface onto the display
# win.blit(background, (0, 0))
#
# # Update the display
# pygame.display.flip()
#
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
# # Quit Pygame
# pygame.quit()
import pygame


def draw_gradient(win, x, y, width, height, fade_range, color):
    # Create a surface for the background gradient
    background = pygame.Surface((width, height))

    # Define the colors for the gradient
    transparent = (0, 0, 0, 0)

    # Fill the surface with a black color
    background.fill(color)

    # Create a transparent rectangle in the center
    center_rect = pygame.Rect(fade_range, fade_range, width - fade_range * 2, height - fade_range * 2)
    pygame.draw.rect(background, transparent, center_rect)

    # Draw the background surface onto the display
    win.blit(background, (x, y))


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up the display
    win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Background Gradient")

    # Main loop
    running = True
    while running:

        draw_gradient(win, 50, 50, 800, 600, 50, (155, 0, 0))

        # Update the display
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Quit Pygame
    pygame.quit()
