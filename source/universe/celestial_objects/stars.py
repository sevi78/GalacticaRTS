import math

import pygame
from pygame import gfxdraw

from source.gui.lod import level_of_detail
from source.universe.celestial_objects.celestial_object import CelestialObject


class FlickeringStar(CelestialObject):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

    def draw(self):
        self.set_screen_position()
        x, y = self.center
        if not level_of_detail.inside_screen(self.center):
            return

        if not self._hidden:
            """
                    Draw a flickering star on the screen.
                    """
            # Get the current color from the colors list
            color = self.colors[self.color_index]

            # Update the color index for the next iteration
            self.color_index = (self.color_index + 1) % len(self.colors)

            # Draw the flickering star using the current color
            pygame.draw.lines(self.win, color, True, [(self.screen_x + 1, self.screen_y),
                                                      (self.screen_x + 1, self.screen_y)])


class PulsatingStar(CelestialObject):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

    def draw(self):
        self.set_screen_position()
        x, y = self.center
        if not level_of_detail.inside_screen(self.center):
            return

        if not self._hidden:
            t = pygame.time.get_ticks() % (self.pulse_time * 1000) / (self.pulse_time * 1000)
            s = 2 * math.pi * (t + self.start_pulse)
            c = int(127 * max(0.5, 1 + math.cos(2 * math.pi * t)))
            gfxdraw.filled_circle(self.win, int(self.get_screen_x()), int(self.get_screen_y()), int(self.pulsating_star_size * self.get_zoom()), (
                c, c, c))

            # self.debug_object()
