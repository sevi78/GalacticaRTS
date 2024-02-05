import random

import pygame
from pygame_widgets.util import drawText

from source.configuration import global_params
from source.gui.lod import inside_screen
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.multimedia_library.gif_handler import GifHandler


class CelestialObject(WidgetBase):
    # __slots__ = WidgetBase.__slots__
    # __slots__ += (
    #     'speed', 'direction', 'rotation', 'rotation_direction', 'rotation_speed', 'layer', 'type', 'world_x', 'world_y',
    #     'world_width', 'height', 'image', 'image_raw', 'rect', 'rotateable', 'colors', 'start_pulse', 'pulse_time',
    #     'pulsating_star_size', 'pulsating_star_color', 'color_index', 'gif', 'gif_handler', 'parent', 'ui_parent',
    #     'zoomable')
    possible_directions = [-1, 1]

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.speed = random.uniform(0.1, 1.5)
        self.direction = (random.uniform(-self.speed, self.speed), random.uniform(-self.speed, self.speed))
        self.rotation = 0
        self.rotation_direction = random.choice(CelestialObject.possible_directions)
        self.rotation_speed = random.uniform(0.1, 1.0)
        self.layer = kwargs.get("layer", 3)
        self.type = kwargs.get("type", "star")
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height
        self.display_border = max(self.world_width, self.world_height)
        self.image = kwargs.get("image", None)
        self.image_raw = self.image
        self.rect = None
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

        if self.image:
            if self.type in self.rotateable:
                self.image = pygame.transform.rotate(self.image_raw, random.randint(-360, 360))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        self.gif = kwargs.get("gif", None)
        self.gif_handler = None

        if self.gif:
            self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.0)

        self.parent = kwargs.get("parent")
        self.ui_parent = kwargs.get("ui_parent")
        self.zoomable = True

        # append to list
        # getattr(self.parent, self.type).append(self)

    def move(self, direction):
        if direction:
            self.world_x += direction[0] * global_params.game_speed
            self.world_y += direction[1] * global_params.game_speed
        else:
            self.world_x -= self.speed * global_params.game_speed
            self.world_y += self.speed * global_params.game_speed / 2

        if self.world_x > global_params.app.level_handler.data["globals"]["width"] * global_params.quadrant_amount:
            self.world_x = 0
        if self.world_x < 0:
            self.world_x = global_params.app.level_handler.data["globals"]["width"] * global_params.quadrant_amount

        if self.world_y > global_params.app.level_handler.data["globals"]["height"] * global_params.quadrant_amount:
            self.world_y = 0
        if self.world_y < 0:
            self.world_y = global_params.app.level_handler.data["globals"]["height"] * global_params.quadrant_amount

    def draw(self):
        self.set_screen_position()
        # x, y = self.center
        #
        if not inside_screen(self.center, border=0):
            return
        #
        if not self._hidden:
            if self.image:
                nsx, nsy = (self.size_x * self.get_zoom(), self.size_y * self.get_zoom())
                self.rect.width = nsx
                self.rect.height = nsy

                self.rect.x = self.get_screen_x() + self.image.get_size()[0] / 2 * self.get_zoom()
                self.rect.y = self.get_screen_y() + self.image.get_size()[1] / 2 * self.get_zoom()

            self.debug_object()

    def debug_object(self):
        if self.rect:
            pygame.draw.rect(self.win, self.frame_color, self.rect, 1)
        else:
            pygame.draw.rect(self.win, self.frame_color, (
                self.get_screen_x(), self.get_screen_y(), self.get_screen_width(), self.get_screen_height()), 1)

        font = pygame.font.SysFont(global_params.font_name, 18)
        text = self.type
        drawText(global_params.app.win, text, self.frame_color, (
            self.get_screen_x(), self.get_screen_y(), 400, 30), font, "left")
