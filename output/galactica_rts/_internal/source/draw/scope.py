import math

import pygame

from source.configuration.game_config import config
from source.debug.function_disabler import disabler, auto_disable
from source.draw.circles import draw_dashed_circle
from source.draw.dashed_line import draw_dashed_line
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image
from source.text.text_formatter import format_number

SCOPE_SIZE = 30
SCOPE_TEXT_SIZE = 12


#
# disabled_functions = ["draw_range"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable

class Scope:
    def __init__(self, win: pygame.surface.Surface):
        self.win = win
        self.font_size = SCOPE_TEXT_SIZE
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.text = ""
        self.base_color = colors.ui_darker
        self.hover_color = colors.hover_color
        self.warn_color = pygame.color.THECOLORS.get("red")
        self.current_color = self.base_color
        self.warn_image = get_image("warning.png")
        self.distance = 1
        self.inner_circle_dash_lenght = config.ui_scope_inner_circle_dash_length
        self.outer_circle_dash_lenght = config.ui_scope_outer_circle_dash_length
        self.dash_lenght = 0
        self.dash_lenght_max = 12
        self.dir = 1

    def update_dash_lenght(self):
        # Adjust dash_length and change direction if limits are reached
        if self.dash_lenght >= self.dash_lenght_max or self.dash_lenght <= 1.0:
            self.dir *= -1  # Reverse the direction
        # Update dash_length based on the current direction
        self.dash_lenght += 0.15 * self.dir
        # Ensure dash_length does not go out of bounds
        self.dash_lenght = max(1.0, min(self.dash_lenght, self.dash_lenght_max))

    def handle_color(self, hit_object, is_inside_range):
        # if has target and hover over target -> green
        # if hover anywhere else than possible target-> blue
        if hit_object:
            color = self.hover_color
        else:
            color = self.base_color

        if not is_inside_range:
            color = self.warn_color

        self.current_color = color

    def handle_hit_object(self, lists):
        if lists:
            hit_object = sprite_groups.get_hit_object(lists=lists)
        else:
            hit_object = sprite_groups.get_hit_object()
        return hit_object

    def is_in_range(self, mouse_pos, range_, start_pos):
        self.distance = math.dist(start_pos, mouse_pos) / pan_zoom_handler.zoom
        # handle range
        is_inside_range = self.distance <= range_
        return is_inside_range

    def draw_text(self, x, y, color, text: str):
        text = self.font.render(text, 1, color)
        self.win.blit(text, (x, y))

    def draw_info_texts(self, info, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        y = 0
        self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - SCOPE_SIZE - self.font_size - 2, self.current_color, f"distance: {format_number(self.distance * 1000, 1)}")
        for key, value in info.items():
            self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - y - SCOPE_SIZE, self.current_color, f"{key}: {value}")
            y += SCOPE_SIZE

    def draw_warning_image(self, x, y):
        self.win.blit(self.warn_image, (x, y))

    def draw_range(self, obj):
        """
        draw the range of the object with dashed circle:

        this is a bottleneck, because the circle can be very big

        """

        max_range = obj.energy / obj.energy_use
        radius = max_range * pan_zoom_handler.zoom
        # if radius > config.width / 2:
        #     return

        draw_dashed_circle(self.win, self.base_color, obj.rect.center, radius, 25)

    def draw_lines_from_startpos_to_mouse_pos(self, mouse_pos, start_pos):
        # draw line from selected object to mouse cursor
        draw_dashed_line(self.win, self.current_color, start_pos, mouse_pos, width=1, dash_length=10)  # self.dash_lenght)

    def draw_scope_circles(self, mouse_pos):
        size_x = SCOPE_SIZE
        size_y = SCOPE_SIZE
        # draw circles
        draw_dashed_circle(self.win, self.current_color, mouse_pos, size_x / 2, width=1, dash_length=int(self.dash_lenght))
        draw_dashed_circle(self.win, self.current_color, mouse_pos, size_x, width=1, dash_length=int(self.dash_lenght))
        # horizontal line
        factor = size_x / 12
        mouse_x, mouse_y = mouse_pos
        x = mouse_x - size_x * factor / 2
        y = mouse_y
        x1 = x + size_x * factor
        y1 = y
        draw_dashed_line(self.win, self.current_color, (x, y), (x1, y1), width=1, dash_length=self.dash_lenght)
        # vertical line
        x = mouse_x
        y = mouse_y - size_x * factor / 2
        x1 = x
        y1 = y + size_x * factor
        draw_dashed_line(self.win, self.current_color, (x, y), (x1, y1), width=1, dash_length=self.dash_lenght)

    def update_scope(self, start_pos: tuple, range_: float, **kwargs) -> None:
        """
        draws line to mouse position and draws the scope and some info text
        use kwargs('lists') to filter which hit object get accepted to make the scope green
        """
        lists = kwargs.get("lists", [])
        # update dash_lenght
        self.update_dash_lenght()

        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # check if mouse is in range
        is_inside_range = self.is_in_range(mouse_pos, range_, start_pos)

        # handle hit object
        hit_object = self.handle_hit_object(lists)

        # handle different colors depending on distance and hover object
        self.handle_color(hit_object, is_inside_range)

        # # draw the lines from selected object to mouse cursor
        # self.draw_lines_from_startpos_to_mouse_pos(mouse_pos, start_pos)
        #
        # # draw scope circles including text
        # self.draw_scope_circles_with_text_and_warning_image(info, mouse_pos, is_inside_range)

    def draw_scope_circles_with_text_and_warning_image(self, info, mouse_pos, is_inside_range):
        # scope
        self.draw_scope_circles(mouse_pos)
        # text
        self.draw_info_texts(info, mouse_pos)

        # if distance outside range_
        if not is_inside_range:
            mouse_x, mouse_y = mouse_pos
            self.draw_warning_image(mouse_x, mouse_y - SCOPE_SIZE * 2)


scope = Scope(config.win)
