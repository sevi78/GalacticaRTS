import math
import random

import pygame
from pygame import gfxdraw

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import UniverseLayeredUpdates
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomSpriteBase


class PanZoomFlickeringStar(PanZoomSpriteBase):
    __slots__ = (
        'colors',
        'color_index',
        'debug'
        )

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: UniverseLayeredUpdates = None
            ) -> None:
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group)

        # Generate a list of random colors
        # TODO: use colores precalculated somewhere
        self.colors = [(random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
                        random.randint(0, config.star_brightness)) for _ in range(10)]

        # Initialize the color index
        self.color_index = 0

    def draw(self) -> None:
        """
        Draw the flickering star on the window surface.

        This method handles the drawing of the star with a flickering effect
        by cycling through different colors.
        Note: the size is always 1 pixel!, doesn't matter what world_width, world_height is set
        """
        if self.inside_screen:
            # Get the current color from the colors list
            color = self.colors[self.color_index]

            # Update the color index for the next iteration
            self.color_index = (self.color_index + 1) % len(self.colors)

            # Draw the flickering star using the current color
            # TODO: check if any other method  would be faster, also precalculate the line points
            pygame.draw.lines(
                    self.win,
                    color,
                    True,
                    [(self.rect.x + 1, self.rect.y), (self.rect.x + 1, self.rect.y)])


class PanZoomPulsatingStar(PanZoomSpriteBase):
    __slots__ = (
        'start_pulse',
        'pulsating_star_size',
        'pulsating_star_color',
        'pulse_time'
        )

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: UniverseLayeredUpdates = None
            ) -> None:
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group)

        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = self.world_width  # random.randint(1, 3)
        self.pulsating_star_color = (
            random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
            random.randint(0, config.star_brightness))

    def draw(self) -> None:
        """
        Draw the pulsating star on the window surface.

        This method handles the drawing of the star with a pulsating effect
        by varying its size and brightness over time.
        """
        if self.inside_screen:
            # TODO: check if any other method  would be faster, specially the color calculation could be precalculated
            t = pygame.time.get_ticks() % (self.pulse_time * 1000) / (self.pulse_time * 1000)
            c = int(config.star_brightness / 2 * max(0.5, 1 + math.cos(2 * math.pi * t)))
            gfxdraw.filled_circle(
                    self.win,
                    int(self.rect.x),
                    int(self.rect.y),
                    int(self.pulsating_star_size * pan_zoom_handler.zoom),
                    (c, c, c))
