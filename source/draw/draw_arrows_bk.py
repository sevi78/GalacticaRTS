import pygame
import sys
import math


# Define the draw_arrows function as provided
def draw_arrows(surf, color, start_pos, end_pos, width=1, dash_length=10, arrow_size=(4, 6)):
    x1, y1 = end_pos
    x2, y2 = start_pos
    dl = dash_length

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    dashes = int(distance / dl)
    if dashes == 0:
        return

    dx_dash = dx / dashes
    dy_dash = dy / dashes

    arrow_width, arrow_height = arrow_size

    for i in range(dashes):
        end = x1 + dx_dash * i, y1 + dy_dash * i
        start = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
        pygame.draw.line(surf, color, start, end, width)

        # Calculate the angle of the dash
        angle = math.atan2(dy_dash, dx_dash)

        # Calculate the points of the arrowhead
        right = end[0] + arrow_height * math.cos(angle - math.pi / 6), end[
            1] + arrow_height * math.sin(angle - math.pi / 6)
        left = end[0] + arrow_height * math.cos(angle + math.pi / 6), end[
            1] + arrow_height * math.sin(angle + math.pi / 6)
        tip = end[0] + arrow_width * math.cos(angle), end[1] + arrow_width * math.sin(angle)

        # Draw the arrowhead
        pygame.draw.polygon(surf, color, [right, tip, left])

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
        draw_arrows(
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
