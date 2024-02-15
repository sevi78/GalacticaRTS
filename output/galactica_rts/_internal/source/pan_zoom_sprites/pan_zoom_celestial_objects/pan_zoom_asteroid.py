from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import PanZoomCelestialObject

from source.configuration import global_params
from source.handlers.position_handler import rot_center


class PanZoomAsteroid(PanZoomCelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomCelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)

    # def draw_(self):
    #     self.move(self.direction)
    #     self.set_screen_position()
    #     x, y = self.center
    #     if not inside_screen(self.center):
    #         return
    #
    #     if not self._hidden:
    #         if self.gif:
    #             self.gif_handler.rect = self.rect
    #             self.gif_handler.draw()
    #
    #         rotated_image, new_rect = rot_center(self.image, self.rotation, self.screen_x, self.screen_y)
    #         self.image = rotated_image
    #         self.rect = new_rect
    #
    #         if not self.gif:
    #             self.win.blit(self.image, self.rect)
    #         self.rotation += self.rotation_speed * self.rotation_direction
    #
    #         if global_params.debug:
    #             self.debug_object()
    #
    # def update__(self):
    #     self.update_pan_zoom_sprite()
    #     # if not inside_screen(self.rect.center):
    #     #     return
    #
    #     # if inside_screen(self.rect.center):
    #     #self.draw()
    #     # print ("PanZoomAsteroid.update")
