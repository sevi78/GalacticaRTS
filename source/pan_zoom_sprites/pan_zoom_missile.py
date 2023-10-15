from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject

MISSILE_SPEED = 1.5
MISSILE_POWER = 50
MISSILE_RANGE = 3000


class PanZoomMissile(PanZoomGameObject):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.speed = MISSILE_SPEED
        self.explode_if_target_reached = True

    def damage(self):
        if not self.target:
            return
        self.target.energy -= MISSILE_POWER
        if self.target.energy <= 0:
            self.explode()
    # def update(self):
    #     self.update_pan_zoom_game_object()
    #     #print (self.rect.center, self.target.rect.center)
