import random

from source.gui.lod import level_of_detail
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import PanZoomCelestialObject


class PanZoomCelestialObjectStatic(PanZoomCelestialObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomCelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.rotation = random.randint(0, 360)

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()
