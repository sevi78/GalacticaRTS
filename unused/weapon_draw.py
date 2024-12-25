import pygame
from pygame import Vector2

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image, rotate_image_cached, underblit_image



def calculate_weapon_positions_(spaceship_size, rocket_size, level):
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

def calculate_weapon_positions(spaceship_size, rocket_size, levels):
    offset_x = (spaceship_size[0] - rocket_size[0] * 2) / 6
    offset_y = (spaceship_size[1] - rocket_size[1]) / 4

    positions = {}
    for level in levels:
        if level == 0:
            positions[level] = [(offset_x + rocket_size[0] / 2, offset_y + rocket_size[1] / 2)]
        elif level == 1:
            positions[level] = [
                (offset_x + rocket_size[0] / 2, offset_y + rocket_size[1] / 2),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2, offset_y + rocket_size[1] / 2)
            ]
        elif level == 2:
            positions[level] = [
                (offset_x + 5 + rocket_size[0] / 2, offset_y - 10 + rocket_size[1] / 2),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2 - 5, offset_y - 10 + rocket_size[1] / 2),
                (offset_x - 5 + rocket_size[0] / 2, offset_y + rocket_size[1] / 2),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2 + 5, offset_y + rocket_size[1] / 2)
            ]

    return positions



def create_rack(rect_: pygame.Rect, pivot: tuple, angle: int, points: dict, scale: float) -> dict:
    rect_center = Vector2(rect_.center)
    rotated_points = {}
    levels = [0, 1, 2]
    for level in levels:
        rotated_points[level] = []
        for point in points[level]:

            scaled_point = Vector2(point) * scale
            global_point = scaled_point + rect_center
            rotated_point = (global_point - Vector2(pivot)).rotate(-angle) + Vector2(pivot)
            rotated_points[level].append((int(rotated_point.x), int(rotated_point.y)))

    return rotated_points

def draw_weapons_onto_ship_image(
        spaceship_image: pygame.surface, weapon_image: pygame.surface, level: int
        ) -> tuple[pygame.surface.Surface, dict[str, tuple[int, int]]]:
    rect = spaceship_image.get_rect()
    spaceship_size = spaceship_image.get_rect().size
    rocket_size = weapon_image.get_rect().size
    positions = calculate_weapon_positions(spaceship_size, rocket_size, [0, 1, 2])

    for position in positions[level]:
        spaceship_image = underblit_image(spaceship_image, weapon_image,
                position[0] - rocket_size[0] / 2, position[1] - rocket_size[1] / 2)

    rack_points = create_rack(
            rect_=rect,
            pivot=rect.center,
            angle=0,
            points=positions,
            scale=pan_zoom_handler.zoom
            )

    return spaceship_image, rack_points


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Spaceship Test")
    x, y = screen_width // 2, screen_height // 2
    spaceship_image = get_image("spacehunter.png")
    # print (f"spaceship_image.size: {spaceship_image.get_rect().size}")

    weapon_size = (17, 42)
    weapon_name = "phaser"
    weapon = get_image(weapon_name + "_attached.png")
    weapon = pygame.transform.scale(weapon, weapon_size)
    weapon_offsets = {"rocket": (0, weapon_size[1]), "laser": (0, -4), "phaser": (0, -4)}

    surf, rack_points = draw_weapons_onto_ship_image(spaceship_image, weapon, 2)
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

        # scale_factor = scale / 200
        scale_factor = pan_zoom_handler.zoom
        spaceship_size = (
            int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor))
        scaled_surf = pygame.transform.scale(surf, spaceship_size)

        rot += 1
        rot_image = rotate_image_cached(scaled_surf, rot)

        screen.blit(rot_image, rot_image.get_rect(center=(x, y)))

        # debug rect_points
        pos = rot_image.get_rect().center
        new_rackpoints =  update_rect_points(rack_points, pos, pan_zoom_handler.zoom)
        # for key ,pointlist in new_rackpoints.items():
        #     for point in pointlist:

        for point in new_rackpoints[2]:
            pygame.draw.circle(screen, (255, 0, 0), point, 3, 1)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()




def update_rect_points(rack_points_, pos,  zoom):
    updated_rackpoints = {}
    levels = [0, 1, 2]
    x,y = pos
    for level in levels:
        updated_rackpoints[level] = []
        for point in rack_points_[level]:
            updated_rackpoints[level].append(
                    # (point[0] + x - spaceship_size[0] - , point[1] + y - spaceship_size[1])
                    (point[0] + x , point[1] + y )
                    )


        print (updated_rackpoints)
    return updated_rackpoints


if __name__ == "__main__":
    main()
