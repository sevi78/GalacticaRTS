from source.configuration.game_config import config
from source.draw.arrow import ArrowCrossAnimatedArray
from source.handlers.color_handler import colors
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite


class PanZoomTargetObject(PanZoomSprite):
    """this is a target object the ships are flying to if not any other target is selected"""

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomSprite.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.world_width = width
        self.world_height = height
        self.name = "target_object"
        self.property = "target_object"
        self.type = "target object"
        self.parent = kwargs.get("parent")

        self.target_cross = ArrowCrossAnimatedArray(
                self.win,
                colors.frame_color,
                (400, 300),
                40,
                0,
                8,
                1,
                3,
                5,
                0.8,
                -1)
        self.hide()

    def update(self):
        # make shure the gif is hidden
        self.hide()

        # only draw if the target is set
        if self.parent.target and self.parent.selected:
            self.target_cross.set_center_distance(self.parent.target.rect.width)
            self.target_cross.update(self.parent.target.rect.center)
            self.target_cross.draw()

        if config.game_paused:
            return

        self.update_pan_zoom_sprite()

        if not self.parent:
            self.kill()
            return
