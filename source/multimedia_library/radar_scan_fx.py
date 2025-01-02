import time

import pygame

from source.multimedia_library.images import rounded_surface

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

GLOW_CYCLE_TIME = 5


class RadarScanFX:
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, corner_radius: int = 0):
        """
        Initialize the RadarScanFX object.

        Args:
        surface (pygame.Surface): The surface to draw on.
        x (int): The top-left x position of the radar.
        y (int): The top-left y position of the radar.
        width (int): The width of the radar.
        height (int): The height of the radar.
        corner_radius (int): The radius for rounded corners. If 0, no rounding is applied.
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = corner_radius

        # Create a surface for the frame content with per-pixel alpha
        self.frame_content = pygame.Surface((width, height), pygame.SRCALPHA)

        # Initialize other attributes
        self.glow_position = 0.0
        self.glow_width = 100  # This can be adjusted based on width if needed
        self.glow_start_time = time.time()

    def scale(self, x: int, y: int, width: int, height: int) -> None:
        """
        Update the size and position of the radar.

        Args:
        x (int): The new x position for the radar.
        y (int): The new y position for the radar.
        width (int): The new width for the radar.
        height (int): The new height for the radar.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Update frame content size
        self.frame_content = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Optionally adjust glow width or other attributes based on size changes
        self.glow_width = int(self.width * 0.5)  # Example adjustment

    def draw_frame(self) -> None:
        """Draw the radar frame with glow effect."""

        # Clear the frame content surface
        self.frame_content.fill((0, 0, 0, 255))  # Fill with opaque black

        # Calculate glow position (5 second cycle)
        current_time = time.time()
        elapsed_time = current_time - self.glow_start_time
        self.glow_position = (elapsed_time % GLOW_CYCLE_TIME) / GLOW_CYCLE_TIME * self.width

        # Create and draw the radar glow effect
        glow_surface = pygame.Surface((self.glow_width, self.height), pygame.SRCALPHA)

        for x in range(self.glow_width):
            alpha = 255 if x == self.glow_width // 2 else int(255 * (
                    1 - abs(x - self.glow_width // 2) / (self.glow_width // 2)))
            pygame.draw.line(glow_surface, (0, 255, 0, alpha), (x, 0), (x, self.height))

        # Draw the glow on the frame content surface
        glow_x = int(self.glow_position - self.glow_width // 2)

        # Blit glow effect onto frame content
        self.frame_content.blit(glow_surface, (glow_x, 0))

    def update(self) -> None:
        """Update and draw the radar display."""

        # Draw frame with effects onto main surface
        self.draw_frame()

        if self.corner_radius > 0:
            # start = time.time()
            rounded_content = rounded_surface(self.frame_content, corner_radius=self.corner_radius)
            self.surface.blit(rounded_content, (self.x, self.y))
            # end = time.time()
            # print(f"Rounded surface in {end - start} seconds")
        else:
            self.surface.blit(self.frame_content, (self.x, self.y))


def main() -> None:
    """Main function to run the Pygame application."""

    # Initialize Pygame and set up display
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mini-Map with Radar Glow and Scaling")

    clock = pygame.time.Clock()

    # Create two radar instances: one with rounded corners and one without
    mini_map_rounded = RadarScanFX(screen, 50, 50, 200, 200, corner_radius=20)
    mini_map_square = RadarScanFX(screen, 300, 50, 200, 200)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse wheel events for scaling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up to zoom in
                    mini_map_rounded.scale(mini_map_rounded.x,
                            mini_map_rounded.y - 10,
                            mini_map_rounded.width * 1.1,
                            mini_map_rounded.height * 1.1)
                    mini_map_square.scale(mini_map_square.x,
                            mini_map_square.y - 10,
                            mini_map_square.width * 1.1,
                            mini_map_square.height * 1.1)
                elif event.button == 5:  # Scroll down to zoom out
                    mini_map_rounded.scale(mini_map_rounded.x,
                            mini_map_rounded.y + 10,
                            mini_map_rounded.width * 0.9,
                            mini_map_rounded.height * 0.9)
                    mini_map_square.scale(mini_map_square.x,
                            mini_map_square.y + 10,
                            mini_map_square.width * 0.9,
                            mini_map_square.height * 0.9)

        screen.fill((255, 255, 255))  # Clear screen with white background

        mini_map_rounded.update()  # Update and draw rounded map
        mini_map_square.update()  # Update and draw square map

        pygame.display.flip()  # Refresh display

        clock.tick(60)  # Limit to FPS

    pygame.quit()  # Clean up Pygame resources


if __name__ == "__main__":
    main()

#
#
# def rounded_surface(surface: pygame.Surface, corner_radius: int) -> pygame.Surface:
#     """
#     Create a rounded version of the given surface.
#
#     Args:
#     surface (pygame.Surface): The original surface to round.
#     corner_radius (int): The radius of the rounded corners.
#
#     Returns:
#     pygame.Surface: A new surface with rounded corners.
#     """
#     size = surface.get_size()
#     rounded = pygame.Surface(size, pygame.SRCALPHA)
#
#     mask = pygame.Surface(size, pygame.SRCALPHA)
#     mask.fill((255, 255, 255, 0))
#     pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=corner_radius)
#
#     rounded.blit(surface, (0, 0))
#     mask_alpha = pygame.surfarray.array_alpha(mask)
#     surface_alpha = pygame.surfarray.pixels_alpha(rounded)
#     surface_alpha[:] = np.minimum(surface_alpha, mask_alpha)
#     del surface_alpha  # Release the surface lock
#
#     return rounded
#
#
# class RadarScanFX__: # should be optimized but i crap
#     def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, corner_radius: int = 0):
#         """
#         Initialize the RadarScanFX object.
#
#         Args:
#         surface (pygame.Surface): The surface to draw on.
#         x (int): The top-left x position of the radar.
#         y (int): The top-left y position of the radar.
#         width (int): The width of the radar.
#         height (int): The height of the radar.
#         corner_radius (int): The radius for rounded corners. If 0, no rounding is applied.
#         """
#         self.surface = surface
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.corner_radius = corner_radius
#
#         # Create a surface for the frame content with per-pixel alpha
#         self.frame_content = pygame.Surface((width, height), pygame.SRCALPHA)
#
#         # Initialize other attributes
#         self.glow_position = 0.0
#         self.glow_width = 100  # This can be adjusted based on width if needed
#         self.glow_start_time = time.time()
#
#         # Store the rounded surface and a flag to check if it needs updating
#         self.rounded_surface_cache = None
#         self.needs_redraw = True
#
#     def scale(self, x: int, y: int, width: int, height: int) -> None:
#         """
#         Update the size and position of the radar.
#
#         Args:
#         x (int): The new x position for the radar.
#         y (int): The new y position for the radar.
#         width (int): The new width for the radar.
#         height (int): The new height for the radar.
#         """
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#
#         # Update frame content size and set redraw flag
#         self.frame_content = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
#
#         # Optionally adjust glow width or other attributes based on size changes
#         self.glow_width = int(self.width * 0.5)  # Example adjustment
#
#         # Mark that we need to recreate the rounded surface
#         self.needs_redraw = True
#
#     def draw_frame(self) -> None:
#         """Draw radar frame with glow effect."""
#
#         # Clear the frame content surface
#         self.frame_content.fill((0, 0, 0, 255))  # Fill with opaque black
#
#         # Calculate glow position (5 second cycle)
#         current_time = time.time()
#         elapsed_time = current_time - self.glow_start_time
#         self.glow_position = (elapsed_time % 5) / 5 * self.width
#
#         # Create and draw radar glow effect
#         glow_surface = pygame.Surface((self.glow_width, self.height), pygame.SRCALPHA)
#
#         for x in range(self.glow_width):
#             alpha = 255 if x == self.glow_width // 2 else int(255 * (
#                     1 - abs(x - self.glow_width // 2) / (self.glow_width // 2)))
#             pygame.draw.line(glow_surface, (0, 255, 0, alpha), (x, 0), (x, self.height))
#
#         # Draw glow on frame content surface
#         glow_x = int(self.glow_position - self.glow_width // 2)
#
#         # Blit glow effect onto frame content
#         self.frame_content.blit(glow_surface, (glow_x, 0))
#
#     def update(self) -> None:
#         """Update and draw radar display."""
#
#         self.draw_frame()
#         # Draw frame only if it needs redrawing
#         if self.needs_redraw:
#
#
#             # Create rounded surface only if needed
#             if self.corner_radius > 0:
#                 self.rounded_surface_cache = rounded_surface(self.frame_content, corner_radius=self.corner_radius)
#             else:
#                 self.rounded_surface_cache = None
#
#             # Reset redraw flag after drawing
#             self.needs_redraw = False
#
#             # Blit either rounded or normal frame content to main surface
#             if self.rounded_surface_cache is not None:
#                 self.surface.blit(self.rounded_surface_cache, (self.x, self.y))
#             else:
#                 self.surface.blit(self.frame_content, (self.x, self.y))
#
#
# # Main function to run Pygame application.
# def main() -> None:
#     """Main function to run the Pygame application."""
#
#     # Initialize Pygame and set up display
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption("Mini-Map with Radar Glow and Scaling")
#
#     clock = pygame.time.Clock()
#
#     # Create two radar instances: one with rounded corners and one without
#     mini_map_rounded = RadarScanFX(screen, 50, 50, 200, 200, corner_radius=20)
#     mini_map_square = RadarScanFX(screen, 300, 50, 200, 200)
#
#     # Main game loop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             # Handle mouse wheel events for scaling
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 4:  # Scroll up to zoom in
#                     mini_map_rounded.scale(mini_map_rounded.x,
#                             mini_map_rounded.y - 10,
#                             mini_map_rounded.width * 1.1,
#                             mini_map_rounded.height * 1.1)
#                     mini_map_square.scale(mini_map_square.x,
#                             mini_map_square.y - 10,
#                             mini_map_square.width * 1.1,
#                             mini_map_square.height * 1.1)
#                 elif event.button == 5:  # Scroll down to zoom out
#                     mini_map_rounded.scale(mini_map_rounded.x,
#                             mini_map_rounded.y + 10,
#                             mini_map_rounded.width * 0.9,
#                             mini_map_rounded.height * 0.9)
#                     mini_map_square.scale(mini_map_square.x,
#                             mini_map_square.y + 10,
#                             mini_map_square.width * 0.9,
#                             mini_map_square.height * 0.9)
#
#         screen.fill((255, 255, 255))  # Clear screen with white background
#
#         mini_map_rounded.update()  # Update and draw rounded map
#         mini_map_square.update()  # Update and draw square map
#
#         pygame.display.flip()  # Refresh display
#
#         clock.tick(60)  # Limit to FPS
#
#     pygame.quit()  # Clean up Pygame resources
#
#
# if __name__ == "__main__":
#     main()
