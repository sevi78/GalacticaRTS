from source.gui.lod import inside_screen
from source.universe.celestial_objects.celestial_object import CelestialObject
from source.configuration import global_params


class Comet(CelestialObject):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

    def draw(self):
        self.set_screen_position()

        x, y = self.center
        if not inside_screen(self.center):
            return

        if not self._hidden:
            if self.image:
                nsx, nsy = (self.size_x * self.get_zoom(), self.size_y * self.get_zoom())
                self.rect.width = nsx
                self.rect.height = nsy
                self.rect.x = self.get_screen_x() + self.image.get_size()[0] / 2 * self.get_zoom()
                self.rect.y = self.get_screen_y() + self.image.get_size()[1] / 2 * self.get_zoom()

                self.move(direction=None)
                self.win.blit(self.image, self.rect)

            if global_params.debug:
                self.debug_object()
