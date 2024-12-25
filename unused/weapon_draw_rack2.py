import pygame

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image, underblit_image
from source.test.rack import Rack
"""
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

"""

def draw_weapons_under_ship_image(
        rack: Rack, ship_image: pygame.Surface, weapon_image: pygame.Surface, level: int
        ) -> pygame.Surface:

    ship_size = ship_image.get_rect().size
    weapon_size = weapon_image.get_rect().size

    points = rack.get_rotated_points()

    if level == 0:
        x, y = points[level][0], points[level][1]
        ship_image = underblit_image(ship_image, weapon_image, x, y)

    if level == 1:
        x, y = points[level][0], points[level][1]
        ship_image = underblit_image(ship_image, weapon_image, x, y)

        x, y = points[level - 1][0], points[level - 1][1]
        ship_image = underblit_image(ship_image, weapon_image, x, y)

    # if level == 2:
    #     for point in rack.get_rotated_points().values():
    #         ship_image = underblit_image(ship_image, weapon_image, point[0], point[1])
    return ship_image


def main():
    pygame.init()
    window = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    x, y = 200, 200

    orig_image = get_image("spaceship.png")
    orig_rect = orig_image.get_rect(center=(x, y))
    weapon_image = pygame.transform.scale(get_image("rocket.png"), (17, 42))
    weapon_rect = weapon_image.get_rect()

    rack = Rack(
            rect=orig_rect,
            pivot=orig_rect.center,
            points={
                0: (orig_rect.left + 4, orig_rect.top),
                1: (orig_rect.right - 4, orig_rect.top),
                2: orig_rect.bottomright,
                3: orig_rect.bottomleft
                })

    # Update rack to calculate positions
    rack.update(rect=orig_rect, pivot=orig_rect.center, scale=1.0, angle=0)

    weaponised_image = draw_weapons_under_ship_image(rack, orig_image, weapon_image, 0)



    # orig_image = underblit_image(orig_image, weapon_image, 10, 0)

    # pygame.draw.circle(orig_image, (255, 233, 0), orig_rect.center,10, 5)

    # # Draw circles and blit weapon images onto orig_image
    # for point in rack.get_rotated_points().values():
    #     orig_image = underblit_image(orig_image, weapon_image, point[0]-orig_rect[0]-weapon_rect.width/2, point[1]-orig_rect[1]-weapon_rect.height/2)

    angle = 0

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        pan_zoom_handler.listen(events)
        window.fill((0, 0, 0))

        angle += 0
        scaled_image = pygame.transform.scale(weaponised_image, (
            int(weaponised_image.get_width() * pan_zoom_handler.zoom),
            int(weaponised_image.get_height() * pan_zoom_handler.zoom)
            ))

        rotated_image = pygame.transform.rotate(scaled_image, angle)

        rotated_rect = rotated_image.get_rect(center=(x, y))

        window.blit(rotated_image, rotated_rect)

        rack.update(rotated_rect, rotated_rect.center, pan_zoom_handler.zoom, angle)
        rack.draw(window)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
