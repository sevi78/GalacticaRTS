import numpy as np
import pygame

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image, rotate_image_cached, underblit_image


def find_color_pixels(surface, color='darkest', threshold=50, max_points=4):
    """
    Find pixels of a specific color or the darkest pixels in a surface.

    :param surface: Pygame surface to search
    :param color: 'red', 'green', 'blue', or 'darkest'
    :param threshold: Threshold for color intensity or darkness
    :param max_points: Maximum number of points to return
    :return: List of (x, y) coordinates
    """
    # Convert surface to a 3D numpy array (width, height, 3)
    arr = pygame.surfarray.pixels3d(surface)

    if color == 'darkest':
        # Calculate brightness (simple average of RGB values)
        intensity = np.mean(arr, axis=2)
        # Find coordinates of dark pixels
        pixels = np.argwhere(intensity < threshold)
        # Sort by brightness (darkest first)
        sorted_pixels = sorted(pixels, key=lambda x: intensity[x[0], x[1]])
    else:
        # Select the appropriate color channel
        color_index = {'red': 0, 'green': 1, 'blue': 2}[color]
        # Find coordinates of pixels with high intensity in the selected channel
        pixels = np.argwhere(arr[:, :, color_index] > threshold)
        # Sort by color intensity (highest first)
        sorted_pixels = sorted(pixels, key=lambda x: arr[x[0], x[1], color_index], reverse=True)

    # Take top max_points
    selected_pixels = sorted_pixels[:max_points]

    # Return as (x, y) tuples (Pygame uses (x, y) format)
    return [(int(x[1]), int(x[0])) for x in selected_pixels]


def calculate_weapon_positions(spaceship_size, weapon_size, level):
    offset_x = (spaceship_size[0] - weapon_size[0] * 2) / 6
    offset_y = (spaceship_size[1] - weapon_size[1]) / 4

    positions = []
    if level == 0:
        positions.append((offset_x + weapon_size[0] / 2, offset_y + weapon_size[1] / 2))
    elif level == 1:
        positions.append((offset_x + weapon_size[0] / 2, offset_y + weapon_size[1] / 2))
        positions.append((spaceship_size[0] - offset_x - weapon_size[0] / 2, offset_y + weapon_size[1] / 2))
    elif level == 2:
        positions.extend([
            (offset_x + 5 + weapon_size[0] / 2, offset_y - 10 + weapon_size[1] / 2),
            (spaceship_size[0] - offset_x - weapon_size[0] / 2 - 5, offset_y - 10 + weapon_size[1] / 2),
            (offset_x - 5 + weapon_size[0] / 2, offset_y + weapon_size[1] / 2),
            (spaceship_size[0] - offset_x - weapon_size[0] / 2 + 5, offset_y + weapon_size[1] / 2)
            ])

    return positions


def draw_weapons_onto_ship_image(
        spaceship_image: pygame.surface, weapon_image: pygame.surface, level: int
        ) -> pygame.surface.Surface:
    spaceship_size = spaceship_image.get_rect().size
    weapon_size = weapon_image.get_rect().size

    positions = calculate_weapon_positions(spaceship_size, weapon_size, level)

    surf = spaceship_image
    for position in positions:
        surf = underblit_image(surf, weapon_image, position[0] - weapon_size[0] / 2, position[1] - weapon_size[1] / 2)

    return surf


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Spaceship Test")
    x, y = screen_width // 2, screen_height // 2
    spaceship_image = get_image("spacehunter.png")
    print(f"spaceship_image.size: {spaceship_image.get_rect().size}")

    weapon_size = (17, 42)
    weapon_name = "phaser"
    weapon = get_image(weapon_name + "_attached.png")
    weapon = pygame.transform.scale(weapon, weapon_size)

    surf = draw_weapons_onto_ship_image(spaceship_image, weapon, 2)
    rot = 0

    scale_dir = 1
    scale = 200
    scale_min = 200
    scale_max = 400
    clock = pygame.time.Clock()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        pan_zoom_handler.listen(events)
        screen.fill((0, 0, 100))

        scale += scale_dir
        if scale >= scale_max:
            scale_dir = -1
        elif scale <= scale_min:
            scale_dir = 1

        scale_factor = pan_zoom_handler.zoom
        scaled_surf = pygame.transform.scale(surf, (
            int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))

        rot += 0#-1
        rot_image = rotate_image_cached(scaled_surf, rot)

        # Get the position where the rotated image will be drawn
        rot_rect = rot_image.get_rect(center=(x, y))
        screen.blit(rot_image, rot_rect)

        # Find red pixels in the rotated image
        red_pixels = find_color_pixels(rot_image, "green", threshold=200, max_points=4)

        # Draw circles at the red pixel positions
        for px, py in red_pixels:
            # Adjust pixel position to screen coordinates
            screen_x = rot_rect.left + px
            screen_y = rot_rect.top + py
            pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 5)

        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

    pygame.quit()


if __name__ == "__main__":
    main()
