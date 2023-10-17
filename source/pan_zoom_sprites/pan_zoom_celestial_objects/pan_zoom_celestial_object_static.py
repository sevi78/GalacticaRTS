import random

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import PanZoomCelestialObject

from source.utils import global_params
from source.utils.positioning import rot_center


class PanZoomCelestialObjectStatic(PanZoomCelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomCelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.rotation = random.randint(0, 360)
        # self.rotated_image, self.rotated_rect = rot_center(self.image, self.rotation, self.screen_x, self.screen_y)
        # self.image = self.rotated_image
        # self.rect = self.rotated_rect

    def draw_(self):
        self.set_screen_position()
        x, y = self.center
        if not inside_screen(self.center):
            return

        if not self._hidden:
            if self.gif:
                self.gif_handler.rect = self.rect
                self.gif_handler.draw()

            else:

                self.rect.center = self.center

                self.win.blit(self.image, self.rect)

            if global_params.debug:
                self.debug_object()

    def draw_(self):
        self.set_screen_position()
        x, y = self.center

        if not inside_screen(self.center):
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

            if global_params.debug:
                self.debug_object()

    def update(self):
        self.update_pan_zoom_sprite()
        if not inside_screen(self.rect.center):
            return

        self.draw()
