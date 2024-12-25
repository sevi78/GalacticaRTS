import pygame

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image, rotate_image_cached, underblit_image


def calculate_weapon_positions(spaceship_size, rocket_size, level):
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
    rect = spaceship_image.get_rect()
    spaceship_size = spaceship_image.get_rect().size
    rocket_size = weapon_image.get_rect().size
    positions = calculate_weapon_positions(spaceship_size, rocket_size, level)

    for position in positions:
        spaceship_image = underblit_image(spaceship_image, weapon_image,
                position[0] - rocket_size[0] / 2, position[1] - rocket_size[1] / 2)

    return spaceship_image


def main():
    # screen
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Spaceship Test")

    spaceship_image = get_image("spacehunter.png")
    weapon_name = "phaser"
    weapon = get_image(weapon_name + "_attached.png")

    weapon_size = (17, 42)
    weapon = pygame.transform.scale(weapon, weapon_size)
    # weapon_offsets = {"rocket": (0, weapon_size[1]), "laser": (0, -4), "phaser": (0, -4)}

    surf = draw_weapons_onto_ship_image(spaceship_image, weapon, 2)
    rot = 0

    scale_dir = 1
    scale = 200
    scale_min = 200
    scale_max = 400
    clock = pygame.time.Clock()

    x, y = screen_width // 2, screen_height // 2

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

        # scale_factor = scale / 200
        scale_factor = pan_zoom_handler.zoom
        scaled_surf = pygame.transform.scale(surf, (
            int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))

        rot += -1
        rot_image = rotate_image_cached(scaled_surf, rot)

        screen.blit(rot_image, rot_image.get_rect(center=(x, y)))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

