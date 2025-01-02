from source.pan_zoom_sprites.rack import Rack


class WeaponRack(Rack):
    def __init__(self, width, height, pivot: tuple, points_by_level: dict):
        self.level = 0

        self.points_by_level = points_by_level
        self.levels = list(points_by_level.keys())
        super().__init__(width, height, pivot, self.points_by_level[self.level])

    def set_level(self, level):
        self.level = level
        self.points_raw = self.points_by_level[level]
        self.points = self.points_by_level[level]


def calculate_weapon_positions(spaceship_size, rocket_size, levels, resize_factor):
    # Apply resize_factor to spaceship and rocket sizes
    adjusted_spaceship_size = (spaceship_size[0] * resize_factor, spaceship_size[1] * resize_factor)
    adjusted_rocket_size = (rocket_size[0] * resize_factor, rocket_size[1] * resize_factor)

    offset_x = (adjusted_spaceship_size[0] - adjusted_rocket_size[0] * 2) / 6
    offset_y = 16 * resize_factor

    positions = {}
    for level in levels:
        if level == 0:
            positions[level] = [(offset_x + adjusted_rocket_size[0] / 2, offset_y)]
        elif level == 1:
            positions[level] = [
                (offset_x + adjusted_rocket_size[0] / 2, offset_y),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2, offset_y)
                ]
        elif level == 2:
            outside_offset = 3 * resize_factor
            outer_y_offset = 5 * resize_factor
            inner_y_offset = outer_y_offset - 5 * resize_factor
            positions[level] = [
                (offset_x + outside_offset + adjusted_rocket_size[0] / 2, offset_y - outer_y_offset),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2 - outside_offset,
                 offset_y - outer_y_offset),
                (offset_x - outside_offset + adjusted_rocket_size[0] / 2, offset_y - inner_y_offset),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2 + outside_offset,
                 offset_y - inner_y_offset)
                ]

    return positions


def create_weapon_rack(spaceship_size, weapon_size, levels, resize_factor):
    positions = calculate_weapon_positions(spaceship_size, weapon_size, [0, 1, 2], resize_factor)
    rack = WeaponRack(
            width=spaceship_size[0],
            height=spaceship_size[1],
            pivot=(spaceship_size[0] / 2, spaceship_size[1] / 2),
            points_by_level=positions
            )
    return rack
