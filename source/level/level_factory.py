import pygame.display

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_quadrant import Quadrant
from source.utils import global_params

QUADRANT_AMOUNT = global_params.quadrant_amount


class LevelFactory:
    def __init__(self, win, quadrant_amount):
        self.quadrant_amount = quadrant_amount
        self.win = win
        self.left = 0
        self.top = 0

    def create_quadrant(self, x, y, width, height):
        quadrant = Quadrant(self.win, x, y, width, height, pan_zoom_handler, None,
            debug=False, group="quadrants")
        return quadrant

    def create_quadrants(self):
        quadrants = {}
        left, top = self.left, self.top
        width, height = global_params.scene_width, global_params.scene_height

        for x in range(self.quadrant_amount):
            left = self.left + (x * width)

            for y in range(self.quadrant_amount):
                top = self.top + (y * height)
                key = f"{x}_{y}"
                quadrant = level_factory.create_quadrant(left, top, width, height)

                print("key", key)

                quadrants[key] = quadrant

        return quadrants


level_factory = LevelFactory(pygame.display.get_surface(), QUADRANT_AMOUNT)


class Level:
    def __init__(self):
        self.quadrants = {}
        # self.quadrants = level_factory.create_quadrants()


level = Level()
