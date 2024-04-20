from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject

MISSILE_SPEED = 1.0
MISSILE_POWER = 50
MISSILE_RANGE = 3000


class PanZoomMissile(PanZoomGameObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.explode_if_target_reached = True
        self.target = kwargs.get("target")
        self.speed = MISSILE_SPEED
        self.missile_power = kwargs.get("missile_power", MISSILE_POWER)

    def damage(self):
        if not self.target:
            return
        self.target.energy -= self.missile_power
        self.target.weapon_handler.draw_moving_image(self.target, self.missile_power)

        # if self.target.energy <= 0:
        #     self.explode()
