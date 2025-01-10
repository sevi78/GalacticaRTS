import random
import time
from typing import Any, List, Tuple, Optional

from pygame import Vector2, Rect

from source.configuration.game_config import config
from source.multimedia_library.images import get_gif_duration


class Point:
    def __init__(self, x: int, y: int, width: int, height: int, layer: int, id_: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layer = layer
        self.id = id_

        self.rect = Rect(0, 0, 0, 0)
        self.selected = False
        self.visible = True
        self.class_name = self.__class__.__name__

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


class QTImage(Point):
    def __init__(
            self, x: int, y: int, width: int, height: int, layer: int, id_: int, image_name: str, image_alpha: float,
            color: Tuple[int, int, int], type_: str, rotation_angle: float, **kwargs: Any
            ) -> None:
        super().__init__(x, y, width, height, layer, id_)
        # args

        self.image_name = image_name
        self.image_alpha = image_alpha

        self.color = color
        self.normalized_color = (self.color[0] / 255, self.color[1] / 255, self.color[2] / 255, 0.0 if not self.image_alpha else 255 / self.image_alpha)

        self.type = type_
        self.rotation_angle = rotation_angle

        # kwargs
        self.align_image = kwargs.get("align_image", "center")

        # attributes
        self.lod = 0
        self.class_name = self.__class__.__name__

    def __str__(self) -> str:
        return f"{self.type}:(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


class MovingMixing:
    def __init__(
            self, rotation_speed: float, movement_speed: float, direction: Tuple[float, float], wrap_around: bool,
            **kwargs: Any
            ) -> None:
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.direction = Vector2(direction)
        self.wrap_around = wrap_around
        self.target = None
        self.orbit_object = None
        self.orbit_angle = kwargs.get("orbit_angle", 0)
        self.orbit_speed = kwargs.get("orbit_speed", 0)
        self.orbit_radius = kwargs.get("orbit_radius", 0)
        self.orbit_direction = kwargs.get("orbit_direction", 1)


class QTMovingImage(QTImage, MovingMixing):
    def __init__(
            self, x: int, y: int, width: int, height: int, layer: int, id_: int, image_name: str, image_alpha: float,
            color: Tuple[int, int, int], type_: str, rotation_angle: float, rotation_speed: float,
            movement_speed: float, direction: Tuple[float, float], wrap_around: bool, **kwargs: Any
            ) -> None:
        super().__init__(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, **kwargs)
        MovingMixing.__init__(self, rotation_speed, movement_speed, direction, wrap_around, **kwargs)
        self.class_name = self.__class__.__name__


class QTGif(Point):
    def __init__(
            self, x: int, y: int, width: int, height: int, layer: int, id_: int, gif_name: str, gif_index: int,
            gif_animation_time: Optional[float], loop_gif: bool, kill_after_gif_loop: bool, image_alpha: float,
            color: Tuple[int, int, int], type_: str, rotation_angle: float, **kwargs: Any
            ) -> None:
        super().__init__(x, y, width, height, layer, id_)
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
        self.class_name = self.__class__.__name__

    def __str__(self) -> str:
        return f"{self.type}:(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


class QTMovingGif(QTGif, MovingMixing):
    def __init__(
            self, x: int, y: int, width: int, height: int, layer: int, id_: int, gif_name: str, gif_index: int,
            gif_animation_time: Optional[float], loop_gif: bool, kill_after_gif_loop: bool, image_alpha: float,
            color: Tuple[int, int, int], type_: str, rotation_angle: float, rotation_speed: float,
            movement_speed: float, direction: Tuple[float, float], wrap_around: bool, **kwargs: Any
            ) -> None:
        super().__init__(x, y, width, height, layer, id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, color, type_, rotation_angle, **kwargs)
        MovingMixing.__init__(self, rotation_speed, movement_speed, direction, wrap_around, **kwargs)


class QTFlickeringStar(Point):
    def __init__(
            self, x: int, y: int, width: int, height: int, layer: int, id_: int, colors: List[Tuple[int, int, int]],
            type_: str
            ) -> None:
        super().__init__(x, y, width, height, layer, id_)
        self.colors = colors
        self.color_index = 0
        self.type = type_
        self.lod = 0
        self.class_name = self.__class__.__name__


class QTPulsatingStar(Point):
    def __init__(self, x: int, y: int, width: int, height: int, layer: int, id_: int, type_: str) -> None:
        super().__init__(x, y, width, height, layer, id_)
        self.color_index = 0
        self.type = type_
        self.lod = 0

        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = self.width  # random.randint(1, 3)
        self.pulsating_star_color = (
            random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
            random.randint(0, config.star_brightness))

        self.class_name = self.__class__.__name__
