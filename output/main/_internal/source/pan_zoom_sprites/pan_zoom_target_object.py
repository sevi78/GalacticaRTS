from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite

from source.utils import global_params


class PanZoomTargetObject(PanZoomSprite):
    """this is a target object the ships are flying to if not any other target is selected"""

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.world_width = width
        self.world_height = height
        self.name = "target_object"
        self.property = "target_object"
        self.parent = kwargs.get("parent")
        self.hide()

    def update(self):
        if global_params.game_paused:
            return

        self.update_pan_zoom_sprite()
        if not self.parent:
            self.kill()
            return
