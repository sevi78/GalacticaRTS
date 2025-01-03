import math

import pygame
from pygame import gfxdraw

from source.gui.lod import level_of_detail
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import CelestialObject


class PanZoomFlickeringStar(CelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)

    def draw(self):
        if self._hidden:
            return

        # Get the current color from the colors list
        color = self.colors[self.color_index]

        # Update the color index for the next iteration
        self.color_index = (self.color_index + 1) % len(self.colors)

        # Draw the flickering star using the current color
        pygame.draw.lines(self.win, color, True, [(self.rect.centerx + 1, self.rect.centery),
                                                  (self.rect.centerx + 1, self.rect.centery)])

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return
        self.draw()


class PanZoomPulsatingStar(CelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)

    def draw(self):
        if self._hidden:
            return
        t = pygame.time.get_ticks() % (self.pulse_time * 1000) / (self.pulse_time * 1000)
        s = 2 * math.pi * (t + self.start_pulse)
        c = int(127 * max(0.5, 1 + math.cos(2 * math.pi * t)))
        gfxdraw.filled_circle(self.win, self.rect.centerx, self.rect.centery, int(self.pulsating_star_size * self.get_zoom()), (
            c, c, c))

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()
