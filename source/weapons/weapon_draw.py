import os

import pygame

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.weapons.weapon_rack import create_weapon_rack
from source.multimedia_library.images import get_image, rotate_image_cached, underblit_image


def generate_weaponized_spacehip_image(ship_name, spaceship_size, weapon_name, weapon_size, level, save=False):
    spaceship_image = get_image(ship_name + ".png")
    weapon_image_raw = get_image(weapon_name + "_attached.png")
    weapon_image = pygame.transform.scale(weapon_image_raw, weapon_size)

    rack = create_weapon_rack(spaceship_size, weapon_size, level)
    spaceship_image = draw_weapons_under_ship_image(rack, spaceship_image, weapon_image, weapon_size)

    if save:
        filename = f"{ship_name}_{weapon_name}_{level}.png"
        path = r'/assets/pictures/ships'
        save_file = os.path.join(path, filename)
        pygame.image.save(spaceship_image, save_file)
    return rack, spaceship_image


def generate_weaponized_spacehip_images(ship_names, spaceship_size, weapon_names, weapon_size, levels):
    for ship_name in ship_names:
        for weapon_name in weapon_names:
            for level in levels:
                generate_weaponized_spacehip_image(ship_name, spaceship_size, weapon_name, weapon_size, level)


def draw_weapons_under_ship_image(rack, spaceship_image, weapon_image, weapon_size):
    # underbilt image
    for point in rack.points:
        spaceship_image = underblit_image(spaceship_image, weapon_image, point[0] - weapon_size[0] / 2, point[1] - 7)
    return spaceship_image


def handle_events(angle, events, running, x, y):
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RIGHT:
                x += 10
            if event.key == pygame.K_LEFT:
                x -= 10
            if event.key == pygame.K_UP:
                y -= 10
            if event.key == pygame.K_DOWN:
                y += 10

            if event.key == pygame.K_RIGHT and event.mod & pygame.KMOD_SHIFT:
                angle += 10
            if event.key == pygame.K_LEFT and event.mod & pygame.KMOD_SHIFT:
                angle -= 10
    return angle, running


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # init
    ship_name = "spaceship"
    weapon_name = "phaser"
    weapon_size = (17, 42)
    spaceship_size = (64, 64)
    resize_factor = 1/spaceship_size[0] * 30
    level = 0

    # rack, spaceship_image = generate_weaponized_spacehip_image(ship_name, spaceship_size, weapon_name, weapon_size, level, save=False)
    rack = create_weapon_rack(spaceship_size, weapon_size, level, resize_factor=resize_factor)
    rack.set_level(2)
    # rack = create_rack(spaceship_size, weapon_size, level)

    spaceship_image = draw_weapons_under_ship_image(
            rack,
            get_image(ship_name + ".png"),
            pygame.transform.scale(get_image(weapon_name + "_attached.png"), weapon_size),
            weapon_size)

    levels = [0, 1, 2]
    ship_names = ["spaceship", "spacehunter"]
    weapon_names = ["rocket", "laser", "phaser"]
    # generate_weaponized_spacehip_images(ship_names,spaceship_size, weapon_names, weapon_size, levels)

    # test
    pan_zoom_handler.zoom_min = 0.0001
    pan_zoom_handler.zoom_max = 10
    x_raw, y_raw = screen_width // 2, screen_height // 2
    spaceship_size_raw = (64, 64)
    angle = 0

    # main loop
    running = True
    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        x, y = pan_zoom_handler.world_2_screen(x_raw, y_raw)
        angle, running = handle_events(angle, events, running, x, y)

        screen.fill((0, 0, 0))
        spaceship_size = [pan_zoom_handler.zoom * spaceship_size_raw[0], pan_zoom_handler.zoom * spaceship_size_raw[1]]

        scaled_image = pygame.transform.scale(spaceship_image, (spaceship_size[0], spaceship_size[1]))
        rotated_image = rotate_image_cached(scaled_image, angle)
        rot_rect = rotated_image.get_rect(center=(x, y))

        screen.blit(rotated_image, rot_rect)
        pygame.draw.rect(screen, (55, 20, 200), rot_rect, 1)
        pygame.draw.circle(screen, (0, 255, 0), rot_rect.center, 10, 1)

        # print(spaceship_size[0], spaceship_size[1])
        rack.update(
                x=rot_rect.centerx,
                y=rot_rect.centery,
                width=spaceship_size[0],
                height=spaceship_size[1],
                pivot=rot_rect.center,
                angle=angle,
                scale=pan_zoom_handler.zoom)

        rack.draw(screen)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

"""

You're correct in identifying the source of the error. The mismatch between the initialization size and the update size is causing the calculations to fail. To address this issue and make it possible to initialize a rack with a different size than the original image, we can modify the WeaponRack class in the weapon_draw3.py file. Here's how we can adjust it:

    Modify the WeaponRack class initialization to accept both original and display sizes:

python
class WeaponRack(Rack):
    def __init__(self, original_width, original_height, display_width, display_height, pivot: tuple, points_by_level: dict):
        self.level = 0
        self.points_by_level = points_by_level
        self.levels = list(points_by_level.keys())
        self.original_width = original_width
        self.original_height = original_height
        self.display_width = display_width
        self.display_height = display_height
        super().__init__(display_width, display_height, pivot, self.points_by_level[self.level])

    Update the update method in the Rack class to handle scaling:

python
def update(self, x=None, y=None, width=None, height=None, pivot=None, points=None, scale=None, angle=None):
    self.x = x if x is not None else self.x
    self.y = y if y is not None else self.y
    self.width = width if width is not None else self.width
    self.height = height if height is not None else self.height
    self.pivot = pivot if pivot is not None else self.pivot
    self.points = points if points is not None else self.points
    self.scale = scale if scale is not None else self.scale
    self.angle = angle if angle is not None else self.angle

    # Calculate scaling factors
    scale_x = self.width / self.original_width
    scale_y = self.height / self.original_height

    # Update positions, width, height, rotation
    self.update_points(scale_x, scale_y)

    Modify the update_points method to use the scaling factors:

python
def update_points(self, scale_x, scale_y):
    self.points = []
    for point in self.points_raw:
        scaled_x = int(point[0] * scale_x)
        scaled_y = int(point[1] * scale_y)
        self.points.append((scaled_x, scaled_y))

    pts = [(Vector2(p) - self.pivot).rotate(-self.angle) + self.pivot for p in self.points]
    self.points = pts

Now, in your WeaponHandler class, you can initialize the WeaponRack with both the original and display sizes:

python
self.weapon_rack = WeaponRack(
    original_width=self.spaceship_size[0],
    original_height=self.spaceship_size[1],
    display_width=self.spaceship_size[0],
    display_height=self.spaceship_size[1],
    pivot=(self.spaceship_size[0] / 2, self.spaceship_size[1] / 2),
    points_by_level=copy.copy(self.all_level_rack_positions)
)

In the update_gun_positions method, you can now update the rack with the current display size:

python
def update_gun_positions(self):
    self.weapon_rack.update(
        x=self.parent.rect.centerx,
        y=self.parent.rect.centery,
        width=self.parent.screen_width,
        height=self.parent.screen_height,
        pivot=self.parent.rect.center,
        angle=self.parent.angle,
        scale=pan_zoom_handler.zoom
    )

These changes allow the WeaponRack to maintain the correct proportions and positions of the weapon points, even when the display size differs from the original image size
"""
