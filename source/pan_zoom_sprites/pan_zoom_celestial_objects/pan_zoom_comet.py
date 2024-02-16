from source.gui.lod import level_of_detail
from source.pan_zoom_sprites.pan_zoom_celestial_objects.pan_zoom_celestial_object import PanZoomCelestialObject


class PanZoomComet(PanZoomCelestialObject):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        PanZoomCelestialObject.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

    def update(self):
        self.update_pan_zoom_sprite()
        self.move(direction=None)
        if not level_of_detail.inside_screen(self.rect.center):
            return

        self.draw()
