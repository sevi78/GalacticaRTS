from source.configuration.game_config import config
from source.gui.lod import level_of_detail
# from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import CelestialObject


from unused2.celestial_objects.celestial_object import CelestialObject


class Comet(CelestialObject):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

    def draw(self):
        self.set_screen_position()

        x, y = self.center
        if not level_of_detail.inside_screen(self.center):
            return

        if not self._hidden:
            if self.image:
                nsx, nsy = (self.size_x * self.get_zoom(), self.size_y * self.get_zoom())
                self.rect.width = nsx
                self.rect.height = nsy
                self.rect.x = self.get_screen_x() + self.image.get_size()[0] / 2 * self.get_zoom()
                self.rect.y = self.get_screen_y() + self.image.get_size()[1] / 2 * self.get_zoom()

                self.move(direction=None)
                if not self.gif:
                    self.win.blit(self.image, self.rect)

            if config.debug:
                self.debug_object()
