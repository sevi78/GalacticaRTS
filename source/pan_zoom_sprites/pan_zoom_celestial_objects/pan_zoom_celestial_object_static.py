import random

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import PanZoomCelestialObject


class PanZoomCelestialObjectStatic(PanZoomCelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomCelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.rotation = random.randint(0, 360)

    def draw_(self):
        self.set_screen_position()
        x, y = self.center
        if not level_of_detail.inside_screen(self.center):
            return

        if not self._hidden:
            if self.gif:
                self.gif_handler.rect = self.rect
                self.gif_handler.draw()

            else:

                self.rect.center = self.center

                self.win.blit(self.image, self.rect)

            if config.debug:
                self.debug_object()

    def draw_(self):
        self.set_screen_position()
        x, y = self.center

        if not level_of_detail.inside_screen(self.center):
            return

        if not self._hidden:
            if self.gif:
                self.gif_handler.rect = self.rect
                self.gif_handler.draw()

            else:
                nsx, nsy = (self.size_x * self.get_zoom(), self.size_y * self.get_zoom())
                self.rect.width = nsx
                self.rect.height = nsy

                self.rect.x = self.get_screen_x() + self.image.get_size()[0] / 2 * self.get_zoom()
                self.rect.y = self.get_screen_y() + self.image.get_size()[1] / 2 * self.get_zoom()
                self.win.blit(self.image, self.rect)

            if config.debug:
                self.debug_object()

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()
