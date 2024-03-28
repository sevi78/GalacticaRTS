import math

import pygame

from source.configuration.game_config import config
from source.draw.circles import draw_dashed_circle
from source.draw.dashed_line import draw_dashed_line
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image
from source.text.text_formatter import format_number

SCOPE_SIZE = 30
SCOPE_TEXT_SIZE = 12


class Scope:
    def __init__(self, win: pygame.surface.Surface):
        self.win = win
        self.font_size = SCOPE_TEXT_SIZE
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.text = ""
        self.base_color = colors.frame_color
        self.hover_color = colors.hover_color
        self.warn_color = pygame.color.THECOLORS.get("red")
        self.warn_image = get_image("warning.png")
        self.distance = 1
        self.inner_circle_dash_lenght = config.ui_scope_inner_circle_dash_length
        self.outer_circle_dash_lenght = config.ui_scope_outer_circle_dash_length
        self.dash_lenght = 0
        self.dash_lenght_max = 12
        self.dir = 1

    def draw_text(self, x, y, color, text: str):
        text = self.font.render(text, 1, color)
        self.win.blit(text, (x, y))

    def draw_warning_image(self, x, y):
        self.win.blit(self.warn_image, (x, y))

    def draw_range(self, obj):
        max_range = obj.energy / obj.energy_use
        draw_dashed_circle(self.win, self.base_color, obj.rect.center, max_range * pan_zoom_handler.zoom, 25)

    def draw_scope(self, start_pos: tuple, range_: float, info: dict) -> bool:
        """
        draws line to mouse position and draws the scope and some info text
        """

        # Adjust dash_length and change direction if limits are reached
        if self.dash_lenght >= self.dash_lenght_max or self.dash_lenght <= 1.0:
            self.dir *= -1  # Reverse the direction

        # Update dash_length based on the current direction
        self.dash_lenght += 0.15 * self.dir

        # Ensure dash_length does not go out of bounds
        self.dash_lenght = max(1.0, min(self.dash_lenght, self.dash_lenght_max))

        # handle different colors depending on distance and hover object
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.distance = math.dist(start_pos, (mouse_x, mouse_y)) / pan_zoom_handler.zoom

        # handle range
        is_inside_range = self.distance <= range_

        # if hover anywhere else than possible target-> blue
        color = self.base_color

        # if has target and hover over target -> green
        hit_object = sprite_groups.get_hit_object()

        if hit_object:
            color = self.hover_color
            if hasattr(hit_object, 'info_text'):
                config.app.info_panel.set_text(hit_object.info_text)
                config.app.info_panel.set_planet_image(hit_object.image_raw)


        # if distance outside range_
        if not is_inside_range:
            color = self.warn_color
            self.draw_warning_image(mouse_x, mouse_y - SCOPE_SIZE * 2)

        # draw line from selected object to mouse cursor
        draw_dashed_line(self.win, color, start_pos, (mouse_x, mouse_y), width=1, dash_length=10)  # self.dash_lenght)

        # scope
        size_x = SCOPE_SIZE
        size_y = SCOPE_SIZE

        # draw circles
        draw_dashed_circle(self.win, color, (mouse_x, mouse_y), size_x / 2, width=1, dash_length=int(self.dash_lenght))
        draw_dashed_circle(self.win, color, (mouse_x, mouse_y), size_x, width=1, dash_length=int(self.dash_lenght))

        # horizontal line
        factor = size_x / 12
        x = mouse_x - size_x * factor / 2
        y = mouse_y
        x1 = x + size_x * factor
        y1 = y

        draw_dashed_line(self.win, color, (x, y), (x1, y1), width=1, dash_length=self.dash_lenght)

        # vertical line
        x = mouse_x
        y = mouse_y - size_x * factor / 2
        x1 = x
        y1 = y + size_x * factor

        draw_dashed_line(self.win, color, (x, y), (x1, y1), width=1, dash_length=self.dash_lenght)

        # text
        y = 0
        self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - SCOPE_SIZE - self.font_size - 2, color, f"distance: {format_number(self.distance * 1000, 1)}")
        for key, value in info.items():
            self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - y - SCOPE_SIZE, color, f"{key}: {value}")
            y += SCOPE_SIZE

        return is_inside_range


scope = Scope(config.win)
