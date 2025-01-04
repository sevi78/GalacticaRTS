import random
import time

from pygame import Vector2

from source.configuration.game_config import config
from source.multimedia_library.images import get_gif_duration
from source.qt_universe.view.game_objects.qt_points import Point
#
# PanZoomMovingRotatingImage(
#                     win=self.win,
#                     world_x=x,
#                     world_y=y,
#                     world_width=w,
#                     world_height=h,
#                     layer=ASTEROID_LAYER,
#                     group=all_sprites,
#                     image_name=image_name,
#                     image_alpha=None,
#                     rotation_angle=r,
#                     rotation_speed=rotation_speed,
#                     movement_speed=movement_speed,
#                     direction=Vector2(dx, dy),
#                     world_rect=self.world_rect
#                     ))
class QTImage(Point):
    def __init__(self, x, y, width, height, layer, image_name, image_alpha, color, type_, rotation_angle, **kwargs):
        super().__init__(x, y, width, height, layer)
        # args
        self.color = color
        self.image_name = image_name
        self.image_alpha = image_alpha
        self.type = type_
        self.rotation_angle = rotation_angle

        # kwargs
        self.align_image = kwargs.get("align_image", "center")

        # attributes
        self.lod = 0


class QTMovingImage(QTImage):
    def __init__(self, x, y, width, height, layer, image_name, image_alpha, color, type_, rotation_angle,rotation_speed, movement_speed, direction,wrap_around, **kwargs):
        super().__init__(x, y, width, height, layer, image_name, image_alpha, color, type_, rotation_angle, **kwargs)
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.direction = Vector2(direction)
        self.wrap_around = wrap_around



class QTGif(Point):
    def __init__(
            self, x, y, width, height, layer, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop,
            image_alpha, color, type_, rotation_angle, **kwargs
            ):
        super().__init__(x, y, width, height, layer)
        # args
        self.gif_name = gif_name
        self.gif_index = gif_index

        # if gif_animation_time is not set, use the duration of the first frame
        self.gif_animation_time = gif_animation_time
        self.gif_animation_time = get_gif_duration(self.gif_name) / 1000 if not self.gif_animation_time else self.gif_animation_time
        self.loop_gif = loop_gif
        self.kill_after_gif_loop = kill_after_gif_loop
        self.image_alpha = image_alpha
        self.color = color
        self.type = type_
        self.rotation_angle = rotation_angle

        # kwargs
        self.align_image = kwargs.get("align_image", "center")

        # attributes
        self.lod = 0
        self.gif_start = time.time()

class QTMovingGif(QTGif):
    def __init__(
            self, x, y, width, height, layer, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop,
            image_alpha, color, type_, rotation_angle,rotation_speed, movement_speed, direction,wrap_around, **kwargs):
        super().__init__(x, y, width, height, layer, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop,
                         image_alpha, color, type_, rotation_angle, **kwargs)
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.direction = Vector2(direction)
        self.wrap_around = wrap_around


class QTFlickeringStar(Point):
    def __init__(self, x, y, width, height, layer, colors, type_):
        super().__init__(x, y, width, height, layer)
        self.colors = colors
        self.color_index = 0
        self.type = type_


class QTPulsatingStar(Point):
    def __init__(self, x, y, width, height, layer, type_):
        super().__init__(x, y, width, height, layer)
        self.color_index = 0
        self.type = type_

        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = self.width  # random.randint(1, 3)
        self.pulsating_star_color = (
            random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
            random.randint(0, config.star_brightness))

#
#
# class PanZoomPulsatingStar(PanZoomSpriteBase):
#     __slots__ = (
#         'start_pulse',
#         'pulsating_star_size',
#         'pulsating_star_color',
#         'pulse_time'
#         )
#
#     def __init__(
#             self,
#             win: pygame.Surface,
#             world_x: int,
#             world_y: int,
#             world_width: int,
#             world_height: int,
#             layer: int = 0,
#             group: UniverseLayeredUpdates = None
#             ) -> None:
#         super().__init__(win, world_x, world_y, world_width, world_height, layer, group)
#
#         # start pulse
#         self.start_pulse = random.random()
#         self.pulse_time = random.uniform(0.5, 3.0)
#         self.pulsating_star_size = self.world_width  # random.randint(1, 3)
#         self.pulsating_star_color = (
#             random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
#             random.randint(0, config.star_brightness))
#
#         # self.image = pygame.surface.Surface((1, 1))
#
#     def draw(self) -> None:
#         """
#         Draw the pulsating star on the window surface.
#
#         This method handles the drawing of the star with a pulsating effect
#         by varying its size and brightness over time.
#         """
#         if self.inside_screen:
#             # TODO: check if any other method  would be faster, specially the color calculation could be precalculated
#             t = pygame.time.get_ticks() % (self.pulse_time * 1000) / (self.pulse_time * 1000)
#             c = int(config.star_brightness / 2 * max(0.5, 1 + math.cos(2 * math.pi * t)))
#             gfxdraw.filled_circle(
#                     self.win,
#                     int(self.rect.x),
#                     int(self.rect.y),
#                     int(self.pulsating_star_size * pan_zoom_handler.zoom),
#                     (c, c, c))
