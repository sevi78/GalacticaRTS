from source.qt_universe.view.game_objects.qt_game_objects import *

#
# def create_point(x, y, width, height, layer, id_):
#     return Point(x, y, width, height, layer, id_)
#
# def create_qt_image(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, **kwargs):
#     return QTImage(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, **kwargs)
#
# def create_qt_gif(x, y, width, height, layer, id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, color, type_, rotation_angle, **kwargs):
#     return QTGif(x, y, width, height, layer, id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, color, type_, rotation_angle, **kwargs)
#
# def create_qt_moving_image(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs):
#     return QTMovingImage(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs)
#
# def create_qt_moving_gif(x, y, width, height, layer,id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop,
#             image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs):
#     return QTMovingGif(x, y, width, height, layer,id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop,
#             image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs)
#
# def create_qt_flickering_star(x, y, width, height, layer, id_,  colors, type_):
#     return QTFlickeringStar(x, y, width, height, layer, id_, colors, type_ )
#
# def create_qt_pulsating_star(x, y, width, height, layer, id_, type_):
#     return QTPulsatingStar(x, y, width, height, layer, id_, type_ )



from typing import List, Tuple, Optional, Any

def create_point(x: int, y: int, width: int, height: int, layer: int, id_: int) -> Point:
    return Point(x, y, width, height, layer, id_)

def create_qt_image(x: int, y: int, width: int, height: int, layer: int, id_: int, image_name: str, image_alpha: float, color: Tuple[int, int, int], type_: str, rotation_angle: float, **kwargs: Any) -> QTImage:
    return QTImage(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, **kwargs)

def create_qt_gif(x: int, y: int, width: int, height: int, layer: int, id_: int, gif_name: str, gif_index: int, gif_animation_time: Optional[float], loop_gif: bool, kill_after_gif_loop: bool, image_alpha: float, color: Tuple[int, int, int], type_: str, rotation_angle: float, **kwargs: Any) -> QTGif:
    return QTGif(x, y, width, height, layer, id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, color, type_, rotation_angle, **kwargs)

def create_qt_moving_image(x: int, y: int, width: int, height: int, layer: int, id_: int, image_name: str, image_alpha: float, color: Tuple[int, int, int], type_: str, rotation_angle: float, rotation_speed: float, movement_speed: float, direction: Tuple[float, float], wrap_around: bool, **kwargs: Any) -> QTMovingImage:
    return QTMovingImage(x, y, width, height, layer, id_, image_name, image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs)

def create_qt_moving_gif(x: int, y: int, width: int, height: int, layer: int, id_: int, gif_name: str, gif_index: int, gif_animation_time: Optional[float], loop_gif: bool, kill_after_gif_loop: bool, image_alpha: float, color: Tuple[int, int, int], type_: str, rotation_angle: float, rotation_speed: float, movement_speed: float, direction: Tuple[float, float], wrap_around: bool, **kwargs: Any) -> QTMovingGif:
    return QTMovingGif(x, y, width, height, layer, id_, gif_name, gif_index, gif_animation_time, loop_gif, kill_after_gif_loop, image_alpha, color, type_, rotation_angle, rotation_speed, movement_speed, direction, wrap_around, **kwargs)

def create_qt_flickering_star(x: int, y: int, width: int, height: int, layer: int, id_: int, colors: List[Tuple[int, int, int]], type_: str) -> QTFlickeringStar:
    return QTFlickeringStar(x, y, width, height, layer, id_, colors, type_)

def create_qt_pulsating_star(x: int, y: int, width: int, height: int, layer: int, id_: int, type_: str) -> QTPulsatingStar:
    return QTPulsatingStar(x, y, width, height, layer, id_, type_)




