import math

import pygame

from source.multimedia_library.images import get_image, rotate_image_cached, underblit_image


def calculate_rocket_positions(spaceship_size, rocket_size, level):
    offset_x = (spaceship_size[0] - rocket_size[0] * 2) / 6
    offset_y = (spaceship_size[1] - rocket_size[1]) / 4

    positions = []
    if level == 0:
        positions.append((offset_x + rocket_size[0] / 2, offset_y + rocket_size[1] / 2))
    elif level == 1:
        positions.append((offset_x + rocket_size[0] / 2, offset_y + rocket_size[1] / 2))
        positions.append((spaceship_size[0] - offset_x - rocket_size[0] / 2, offset_y + rocket_size[1] / 2))
    elif level == 2:
        positions.extend([
            (offset_x + 5 + rocket_size[0] / 2, offset_y - 10 + rocket_size[1] / 2),
            (spaceship_size[0] - offset_x - rocket_size[0] / 2 - 5, offset_y - 10 + rocket_size[1] / 2),
            (offset_x - 5 + rocket_size[0] / 2, offset_y + rocket_size[1] / 2),
            (spaceship_size[0] - offset_x - rocket_size[0] / 2 + 5, offset_y + rocket_size[1] / 2)
            ])

    return positions


def draw_weapons_onto_ship_image(
        spaceship_image: pygame.surface, weapon_image: pygame.surface, level: int
        ) -> pygame.surface.Surface:
    """
    draws the rockets onto the spaceship image based on the level of the rockets
    """
    spaceship_size = spaceship_image.get_rect().size
    rocket_size = weapon_image.get_rect().size

    positions = calculate_rocket_positions(spaceship_size, rocket_size, level)

    surf = spaceship_image
    for position in positions:
        surf = underblit_image(surf, weapon_image, position[0] - rocket_size[0] / 2, position[1] - rocket_size[1] / 2)

    return surf


def rotate_point(point, angle, center):
    """Rotate a point around a center"""
    angle = math.radians(-angle)  # Note the negative sign here
    cx, cy = center
    x, y = point
    nx = cx + math.cos(angle) * (x - cx) - math.sin(angle) * (y - cy)
    ny = cy + math.sin(angle) * (x - cx) + math.cos(angle) * (y - cy)
    return (nx, ny)


def adjust_and_rotate_positions(positions, spaceship_size, rotation_angle, center, weapon_size,offset, screen):
    """
    Adjust positions relative to spaceship center and rotate

    :param positions: List of original positions
    :param spaceship_size: Size of the spaceship
    :param rotation_angle: Current rotation angle
    :param center: Center to rotate around
    :return: List of adjusted and rotated positions
    """
    adjusted_positions = []
    offset_x, offset_y = offset
    for pos in positions:
        # Adjust position relative to spaceship center
        adjusted_x = pos[0] - spaceship_size[0] / 2 + offset_x
        adjusted_y = pos[1] - weapon_size[1] + offset_y  # - spaceship_size[1] / 2

        # Rotate the adjusted position
        rotated_pos = rotate_point((adjusted_x, adjusted_y), rotation_angle, (0, 0))

        # Translate back to screen coordinates
        screen_x = rotated_pos[0] + center[0]
        screen_y = rotated_pos[1] + center[1]

        adjusted_positions.append((screen_x, screen_y))

    # Draw the positions
    for position in adjusted_positions:
        r = 6
        pygame.draw.circle(screen, (255, 0, 0), (position[0], position[1]), 6, 1)

    return adjusted_positions


def main():
    pygame.init()

    # Set up the display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Spaceship Test")
    x, y = screen_width // 2, screen_height // 2
    spaceship_image = get_image("spacehunter.png")

    weapon_size = (17, 42)
    weapon_name = "phaser"
    weapon = get_image(weapon_name + "_attached.png")
    weapon = pygame.transform.scale(weapon, weapon_size)
    weapon_offsets = {"rocket": (0, weapon_size[1]), "laser": (0, -4), "phaser": (0, -4)}

    surf = draw_weapons_onto_ship_image(spaceship_image, weapon, 2)
    rot = 0

    scale_dir = 1
    scale = 200
    scale_min = 200
    scale_max = 400
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color
        screen.fill((0, 0, 100))  # Dark blue background

        # Scale the surf
        scale += scale_dir
        if scale >= scale_max:
            scale_dir = -1
        elif scale <= scale_min:
            scale_dir = 1

        scaled_surf = pygame.transform.scale(surf, (
        int(surf.get_width() * scale / 200), int(surf.get_height() * scale / 200)))

        # Rotate the spaceship surface
        rot += -1
        rot_image = rotate_image_cached(scaled_surf, rot)

        # Draw the spaceship image with the rockets
        screen.blit(rot_image, rot_image.get_rect(center=(x, y)))

        # Calculate the positions
        spaceship_size = spaceship_image.get_rect().size
        weapon_size = weapon.get_rect().size
        positions = calculate_rocket_positions(spaceship_size, weapon_size, 2)

        # Adjust positions relative to screen center and rotate
        offset = weapon_offsets[weapon_name]
        adjusted_positions = adjust_and_rotate_positions(positions, spaceship_size, rot, (
        x, y), weapon_size, offset, screen)

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
