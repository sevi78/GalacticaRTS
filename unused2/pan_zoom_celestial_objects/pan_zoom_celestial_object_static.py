import random

from source.gui.lod import level_of_detail
# from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import CelestialObject


class CelestialObjectStatic_(CelestialObject):
    def __init__(self, win, x, y, width, height, image, **kwargs):
        CelestialObject.__init__(self, win, x, y, width, height, image, **kwargs)
        self.rotation = random.randint(0, 360)

    def update(self):
        self.update_pan_zoom_sprite()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()
