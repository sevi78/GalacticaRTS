import math
import random

import pygame
from pygame import Vector2, Rect

from source.configuration.game_config import config
from source.gui.widgets.moving_image import MovingImage
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import UniverseLayeredUpdates
from source.math.math_handler import degrees_to_vector2
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_game_object import PanZoomGameObject
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import CurveMove, PanZoomMovingRotatingGif
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite

MISSILE_SPEED = 1.0
MISSILE_POWER = 50
MISSILE_RANGE = 3000


# class PanZoomMissile(PanZoomGameObject): # dont use this !!
#     def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
#         PanZoomGameObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
#         self.explode_if_target_reached = True
#         self.target = kwargs.get("target")
#         self.speed = MISSILE_SPEED
#         self.missile_power = kwargs.get("missile_power", MISSILE_POWER)
#         self.rotate_correction_angle = kwargs.get("rotate_correction_angle", 0)
#
#         print(self.initial_rotation)
#
#     def damage(self):
#         if not self.target:
#             return
#         if self.target.property in ["ship", "ufo"]:
#             self.target.energy -= self.missile_power
#             self.target.weapon_handler.draw_moving_image(self.target, self.missile_power)
#         if self.target.property == "planet":
#             print("attacking planet")
#
#             MovingImage(
#                     config.app.win,
#                     self.target.rect.top,
#                     self.target.rect.right,
#                     18,
#                     18,
#                     get_image("energy_25x25.png"),
#                     1,
#                     (random.randint(-2, 2), random.randint(-2, 2)),
#                     f"-{self.missile_power}", pygame.color.THECOLORS["red"],
#                     "georgiaproblack", 1, self.target.rect, target=None)
#
#         # if self.target.energy <= 0:
#         #     self.explode()


class Missile(PanZoomMovingRotatingGif):
    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group: UniverseLayeredUpdates = None,
            gif_name: str = None,
            gif_index: int = 0,
            gif_animation_time: float = None,
            loop_gif: bool = True,
            kill_after_gif_loop: bool = False,
            image_alpha: int = None,
            rotation_angle: int = 0,
            movement_speed: float = 0,
            direction: Vector2 = (0, 0),
            world_rect: Rect = Rect(0, 0, 0, 0),
            target: any = None,
            **kwargs
            ):
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, rotation_angle, movement_speed, direction, world_rect)
        self.target_reached = None
        self.target = target
        self.debug = False
        self.enable_wrap_around = False

        direction = degrees_to_vector2(-self.rotation_angle + 270, self.movement_speed)
        gravity = kwargs.get("gravity", 0.05)
        friction = kwargs.get("friction", 0.99)
        self.curve_move = CurveMove(world_x, world_y, direction, gravity, friction)

        self.exploded = False
        self.explosion_relative_gif_size = kwargs.get("explosion_relative_gif_size", 1.0)
        self.explosion_name = kwargs.get("explosion_name", "explosion.gif")
        self.explode_if_target_reached = kwargs.get("explode_if_target_reached", True)
        self.missile_power = kwargs.get("missile_power", MISSILE_POWER)

    def explode(self, **kwargs):

        # self.explode_calls += 1
        sound = kwargs.get("sound", None)
        size = kwargs.get("size", (40, 40))

        x, y = self.world_x, self.world_y
        if not self.exploded:
            explosion = PanZoomSprite(
                    self.win, x, y, size[0], size[1], pan_zoom_handler, self.explosion_name,
                    loop_gif=False, kill_after_gif_loop=True, align_image="center",
                    relative_gif_size=self.explosion_relative_gif_size,
                    layer=10, sound=sound, group="explosions", name="explosion")

            moving_image = MovingImage(
                    self.win,
                    self.target.rect.top,
                    self.target.rect.right,
                    18,
                    18,
                    get_image("energy_25x25.png"),
                    1,
                    (random.randint(-1, 1), 2),
                    f"-{self.missile_power}", pygame.color.THECOLORS["red"],
                    "georgiaproblack", 1, self.target.rect, target=None)

            self.exploded = True

        if hasattr(self, "__delete__"):
            self.__delete__(self)

        self.kill()

    def damage(self):
        self.target.energy -= self.missile_power

    def reach_target(self):
        self.target_reached = math.dist(self.rect.center, self.target.rect.center) < 10

        if self.target_reached:
            if self.explode_if_target_reached:
                self.damage()
                self.explode()

    def update(self):
        x, y = self.curve_move.get_curve_position(self, self.target)
        self.set_position(x, y)
        self.rotation_angle = -math.degrees(math.atan2(self.curve_move.direction.y, self.curve_move.direction.x))
        super().update()

        self.reach_target()
