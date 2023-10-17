import random

import pygame
from pygame_widgets.util import drawText

from source.gui.lod import inside_screen

from source.multimedia_library.gif_handler import GifHandler
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from source.utils import global_params


class PanZoomCelestialObject(PanZoomSprite):
    # __slots__ = WidgetBase.__slots__
    # __slots__ += (
    #     'speed', 'direction', 'rotation', 'rotation_direction', 'rotation_speed', 'layer', 'type', 'world_x', 'world_y',
    #     'world_width', 'height', 'image', 'image_raw', 'rect', 'rotateable', 'colors', 'start_pulse', 'pulse_time',
    #     'pulsating_star_size', 'pulsating_star_color', 'color_index', 'gif', 'gif_handler', 'parent', 'ui_parent',
    #     'zoomable')
    possible_directions = [-1, 1]

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        # WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = random.uniform(0.1, 1.5)
        self.direction = (random.uniform(-self.speed, self.speed), random.uniform(-self.speed, self.speed))
        self.rotation = 0
        self.rotation_direction = random.choice(PanZoomCelestialObject.possible_directions)
        self.rotation_speed = random.uniform(0.1, 1.0)
        self.type = kwargs.get("type", "star")
        self.rotateable = ["galaxy", "nebulae", "asteroid", "comet"]

        # colors
        # Generate a list of random colors
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]

        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = random.randint(1, 3)
        self.pulsating_star_color = (random.randint(110, 255), random.randint(110, 255), random.randint(110, 255))

        # Initialize the color index
        self.color_index = 0
        self.zoomable = True

    def move(self, direction):
        if direction:
            self.world_x += direction[0] * global_params.time_factor
            self.world_y += direction[1] * global_params.time_factor
        else:
            self.world_x -= self.speed * global_params.time_factor
            self.world_y += self.speed * global_params.time_factor / 2

        if self.world_x > global_params.scene_width * global_params.quadrant_amount:
            self.world_x = 0
        if self.world_x < 0:
            self.world_x = global_params.scene_width * global_params.quadrant_amount

        if self.world_y > global_params.scene_height * global_params.quadrant_amount:
            self.world_y = 0
        if self.world_y < 0:
            self.world_y = global_params.scene_height * global_params.quadrant_amount

        self.set_world_position((self.world_x, self.world_y))

    def update(self):
        self.update_pan_zoom_sprite()
        if not inside_screen(self.rect.center):
            return

        # if inside_screen(self.rect.center):
        self.draw()

    def draw(self):
        if self._hidden:
            return
        if not self.image_name == "no_image.png":
            self.win.blit(self.image, self.rect)
        # print ("PanZoomCelestialObject.update")

    # def draw_(self):
    #     self.set_screen_position()
    #     x, y = self.center
    #
    #     if not inside_screen(self.center):
    #         return
    #
    #     if not self._hidden:
    #         if self.image:
    #             nsx, nsy = (self.size_x * self.get_zoom(), self.size_y * self.get_zoom())
    #             self.rect.width = nsx
    #             self.rect.height = nsy
    #
    #             self.rect.x = self.get_screen_x() + self.image.get_size()[0] / 2 * self.get_zoom()
    #             self.rect.y = self.get_screen_y() + self.image.get_size()[1] / 2 * self.get_zoom()

    # def debug_object__(self):
    #     if self.rect:
    #         pygame.draw.rect(self.win, self.frame_color, self.rect, 1)
    #     else:
    #         pygame.draw.rect(self.win, self.frame_color, (
    #         self.get_screen_x(), self.get_screen_y(), self.get_screen_width(), self.get_screen_height()), 1)
    #
    #     font = pygame.font.SysFont(global_params.font_name, 18)
    #     text = self.type
    #     drawText(global_params.app.win, text, self.frame_color, (
    #     self.get_screen_x(), self.get_screen_y(), 400, 30), font, "left")

# class Quadrant(CelestialObject):
#     def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
#         CelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
#
#     def draw(self):
#         self.set_screen_position()
#         x, y = self.center
#         if not inside_screen(self.center):
#             return
#
#         if not self._hidden:
#             # x, y = pan_zoom_handler.world_2_screen(self.world_x, self.world_y)
#             # pygame.draw.rect(self.win, self.frame_color, (
#             #     x, y, self.get_screen_width() / self.get_zoom(), self.get_screen_height() / self.get_zoom()), 1)
#
#             if global_params.debug:
#                 pygame.draw.rect(self.win, self.frame_color, self.rect, 1)
