from source.gui.lod import inside_screen
from source.universe.celestial_objects.celestial_object import CelestialObject
from source.configuration import global_params
from source.handlers.position_handler import rot_center


class Asteroid(CelestialObject):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

    def draw(self):
        self.move(self.direction)
        self.set_screen_position()

        if not inside_screen(self.center):
            if self.gif_handler:
                self.gif_handler._hidden = True
            return
        else:
            if self.gif_handler:
                self.gif_handler._hidden = False

        if not self._hidden:
            if self.gif:
                self.gif_handler.rect = self.rect

            rotated_image, new_rect = rot_center(self.image, self.rotation, self.screen_x, self.screen_y)
            self.image = rotated_image
            self.rect = new_rect

            if not self.gif:
                self.win.blit(self.image, self.rect)
            self.rotation += self.rotation_speed * self.rotation_direction

            if global_params.debug:
                self.debug_object()
