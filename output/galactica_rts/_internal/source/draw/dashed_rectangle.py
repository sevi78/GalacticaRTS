import pygame

from source.draw.arc_with_dashes import draw_arc_with_dashes
from source.draw.dashed_line import draw_dashed_line


def draw_dashed_rounded_rectangle(surf, color, rect, width,  border_radius, dash_length):
    x, y, w, h = rect
    # Draw the straight dashed edges
    draw_dashed_line(surf, color, (x + border_radius, y), (x + w - border_radius, y), width, dash_length)  # Top
    draw_dashed_line(surf, color, (x + border_radius, y + h), (
        x + w - border_radius, y + h), width, dash_length)  # Bottom
    draw_dashed_line(surf, color, (x, y + border_radius), (x, y + h - border_radius), width, dash_length)  # Left
    draw_dashed_line(surf, color, (x + w, y + border_radius), (
        x + w, y + h - border_radius), width, dash_length)  # Right

    # Draw the dashed rounded corners
    draw_arc_with_dashes(surf, color, (x, y), 180, 270, border_radius, dash_length, width)  # Top-left
    draw_arc_with_dashes(surf, color, (
        x + w - 2 * border_radius, y), 270, 360, border_radius, dash_length, width)  # Top-right
    draw_arc_with_dashes(surf, color, (
        x, y + h - 2 * border_radius), 90, 180, border_radius, dash_length, width)  # Bottom-left
    draw_arc_with_dashes(surf, color, (
        x + w - 2 * border_radius, y + h - 2 * border_radius), 0, 90, border_radius, dash_length, width)  # Bottom-right


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))  # Fill the screen with black
        draw_dashed_rounded_rectangle(screen, (255, 255, 255), (
            100, 100, 500, 300), 1, 15, 5)  # Draw a dashed rounded rectangle

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
