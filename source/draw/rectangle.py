import pygame.draw

from source.draw.arc_with_dashes import draw_arc_with_dashes
from source.draw.dashed_line import draw_dashed_line
from source.handlers.pan_zoom_handler import pan_zoom_handler


def draw_transparent_rounded_rect(surface, color, rect, radius, alpha):
    # Create a Surface with the correct dimensions and with per-pixel alpha enabled
    rect_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    # Draw a transparent rounded rectangle on the created Surface
    pygame.draw.rect(rect_surface, color + (alpha,), (0, 0, rect[2], rect[3]), border_radius=radius)
    # Blit the transparent rounded rectangle onto the target surface at the correct position
    surface.blit(rect_surface, rect[:2])

    return rect_surface


def draw_dashed_rounded_rectangle__(
        surf, color, rect, width, border_radius, dash_length
        ):  # original, scaling issues with the borders
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


def draw_dashed_rounded_rectangle(
        surf, color, rect, width, border_radius, dash_length
        ):  # fixed scaling,still issues
    x, y, w, h = rect

    # Adjust border_radius if it exceeds half of the rectangle's dimensions
    if w < 2 * border_radius:
        border_radius = w // 2
    if h < 2 * border_radius:
        border_radius = h // 2

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
    draw_arc_with_dashes(surf, color, (x + w - 2 * border_radius, y + h - 2 * border_radius), 0, 90,
            border_radius,
            dash_length,
            width)  # Bottom-right





#
# def draw_grid_lines(surf, rect, width, dash_length):
#     """Draws a grid pattern on the given surface and returns the coordinates of the lines."""
#     x, y, w, h = rect
#     grid_color = (123, 0, 0, 122)  # Color for the grid lines (green for debugging)
#
#     # Draw horizontal dashes
#     for j in range(y +dash_length, y + h, dash_length + width):
#         for i in range(x, x + w, dash_length + width):
#             if not j == rect.bottom:
#                 pygame.draw.line(surf, grid_color, (i, j), (i + dash_length, j), width)
#
#     # # Draw vertical dashes
#     # for i in range(x + dash_length, x + w, dash_length + width):
#     #     for j in range(y, y + h, dash_length + width):
#     #         pygame.draw.line(surf, grid_color, (i, j), (i, j + dash_length), width)
#
#
#
# # Example usage in your main application loop would remain unchanged.
#
# def draw_dashed_rounded_rectangle(surf, color, rect, width, border_radius, dash_length):
#     x, y, w, h = rect
#
#     # Adjust border_radius if it exceeds half of the rectangle's dimensions
#     if w < 2 * border_radius:
#         border_radius = w // 2
#     if h < 2 * border_radius:
#         border_radius = h // 2
#
#     # Create a new surface for the rounded rectangle with per-pixel alpha
#     rounded_rect_surface = pygame.Surface((w, h), pygame.SRCALPHA)
#
#     # Draw the filled rounded rectangle on the new surface
#     pygame.draw.rect(rounded_rect_surface, color,
#             (0, 0, w, h), border_radius=border_radius, width=1)
#
#     # Call the grid drawing function to overlay a grid pattern
#     draw_grid_lines(rounded_rect_surface, Rect(0, 0, w, h), width=width // 2, dash_length=dash_length)
#
#     # Blit the rounded rectangle surface onto the main surface at the correct position
#     surf.blit(rounded_rect_surface, (x, y))





def draw_zoomable_rect(surface, color, world_x, world_y, width, height, **kwargs):
    border_radius = kwargs.get("border_radius", 0)
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    rect = pygame.Rect(screen_x, screen_y, width * pan_zoom_handler.zoom, height * pan_zoom_handler.zoom)
    pygame.draw.rect(surface, color, rect, 1, border_radius)


def main():
    # Initialize Pygame
    pygame.init()

    # Constants for the window size and colors
    WINDOW_SIZE = (800, 600)
    BACKGROUND_COLOR = (255, 255, 255)
    DASHED_RECT_COLOR = (0, 0, 255)
    DASH_LENGTH = 10
    LINE_WIDTH = 3

    # Create the main window
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Dashed Rounded Rectangle Test")

    # Main loop flag
    running = True

    # Initial sizes for rectangles
    base_width = 100
    base_height = 50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle key presses for size adjustment
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Plus key (+)
                    base_width += 10
                    base_height += 5
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Minus key (-)
                    base_width = max(10, base_width - 10)  # Prevent negative or zero size
                    base_height = max(10, base_height - 5)

                elif event.key == pygame.K_LEFT:  # Minus key (-)
                    DASH_LENGTH -= 1  # Prevent negative or zero size

                elif event.key == pygame.K_RIGHT:  # Minus key (-)
                    DASH_LENGTH += 1

                elif event.key == pygame.K_UP:  # Minus key (-)
                    LINE_WIDTH += 1  # Prevent negative or zero size

                elif event.key == pygame.K_DOWN:  # Minus key (-)
                    LINE_WIDTH -= 1

        screen.fill(BACKGROUND_COLOR)

        # Draw a single dashed rounded rectangle at the center of the screen with current sizes
        x = (WINDOW_SIZE[0] - base_width) // 2
        y = (WINDOW_SIZE[1] - base_height) // 2

        draw_dashed_rounded_rectangle(
                surf=screen,
                color=DASHED_RECT_COLOR,
                rect=(x, y, base_width, base_height),
                width=LINE_WIDTH,
                border_radius=15,
                dash_length=DASH_LENGTH)

        # print(f"x: {x}, y: {y}, width: {base_width}, height: {base_height}")

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


# This allows the module to be run as a script or imported without executing the main function.
if __name__ == "__main__":
    main()
