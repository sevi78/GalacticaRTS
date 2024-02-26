import pygame

from source.draw.rect import draw_transparent_rounded_rect
from source.handlers.color_handler import colors

config = {
    "ui_panel_alpha": 220,
    "ui_rounded_corner_big_thickness": 3,
    "ui_rounded_corner_radius_big": 30,
    "ui_rounded_corner_radius_small": 9,
    "ui_rounded_corner_small_thickness": 1
    }


class Frame:
    def __init__(self, win, x, y, width, height):
        self.win = win
        self.world_y = x
        self.world_x = y
        self.world_width = width
        self.world_height = height
        self.frame_color = colors.ui_dark
        self.surface = pygame.surface.Surface((self.world_width, self.world_height))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = self.world_x, self.world_y
        self.ui_rounded_corner_radius_big = config["ui_rounded_corner_radius_big"]
        self.ui_rounded_corner_radius_small = config["ui_rounded_corner_radius_small"]
        self.ui_rounded_corner_big_thickness = config["ui_rounded_corner_big_thickness"]
        self.ui_rounded_corner_small_thickness = config["ui_rounded_corner_small_thickness"]
        self.ui_panel_alpha = config["ui_panel_alpha"]
        self.ui_rounded_corner_radius = config["ui_rounded_corner_radius_small"]
        self.ui_rounded_corner_thickness = config["ui_rounded_corner_small_thickness"]
        self.frame_border = 10

    def update_position(self, pos):
        self.world_x = pos[0] - self.frame_border / 2
        self.world_y = pos[1] - self.frame_border / 2
        self.rect.x, self.rect.y = self.world_x + self.frame_border, self.world_y + self.frame_border

    def update_size(self, size: tuple[int, int]):
        self.world_width = size[0]
        self.world_height = size[1]
        self.rect.width, self.rect.height = self.world_width, self.world_height

    def update(self, x, y, width, height):
        self.update_position((x, y))
        self.update_size((width, height))

    def draw(self):
        self.surface = pygame.transform.scale(self.surface, (self.world_width, self.world_height))
        rect = (self.world_x, self.world_y, self.surface.get_rect().width, self.surface.get_rect().height)
        draw_transparent_rounded_rect(
            self.win,
            (0, 0, 0),
            rect,
            self.ui_rounded_corner_radius,
            self.ui_panel_alpha)

        pygame.draw.rect(
            self.win,
            self.frame_color,
            rect,
            self.ui_rounded_corner_thickness,
            self.ui_rounded_corner_radius)
