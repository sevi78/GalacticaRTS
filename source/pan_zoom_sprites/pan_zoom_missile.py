import random

import pygame

from source.configuration.game_config import config
from source.gui.widgets.moving_image import MovingImage
from source.multimedia_library.images import get_image
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
        if self.target.property in ["ship", "ufo"]:
            self.target.energy -= self.missile_power
            self.target.weapon_handler.draw_moving_image(self.target, self.missile_power)
        if self.target.property == "planet":
            print ("attacking planet")

            MovingImage(
                config.app.win,
                self.target.rect.top,
                self.target.rect.right,
                18,
                18,
                get_image("energy_25x25.png"),
                1,
                (random.randint(-2, 2), random.randint(-2, 2)),
                f"-{self.missile_power}", pygame.color.THECOLORS["red"],
                "georgiaproblack", 1, self.target, target=None)

        # if self.target.energy <= 0:
        #     self.explode()
