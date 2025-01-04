from random import choice, randint, uniform



from source.handlers.color_handler import get_average_color
from source.multimedia_library.images import get_image_names_from_folder, get_image
from source.pan_zoom_quadtree.model.quad_tree import QuadTree
from source.qt_universe.view.game_objects.qt_game_object import GameObject
from source.qt_universe.model.qt_game_object_manager import game_object_manager

planet_images = get_image_names_from_folder("planets")
sun_images = get_image_names_from_folder("suns")
moon_images = ["moon.gif", "moon1.gif", "moon_alien.gif"]
star_images = get_image_names_from_folder("stars")

images = planet_images + sun_images + moon_images + star_images








def add_random_game_object(x: int, y: int, game_object_manager) -> None:
    image_name = choice(images)
    image = get_image(image_name)
    w, h = image.get_rect().width, image.get_rect().height
    color = get_average_color(image, consider_alpha=True)
    orbit_angle = randint(0, 360)
    orbit_speed = uniform(0.001, 0.005)

    type_ = "sun"
    if image_name in sun_images:
        type_ = "sun"
    elif image_name in planet_images:
        type_ = "planet"
    elif image_name in moon_images:
        type_ = "moon"
    elif image_name in star_images:
        type_ = "star"

    new_object = GameObject(
            x=x,
            y=y,
            width=w,
            height=h,
            image_name=image_name,
            color=color,
            type=type_,
            orbit_angle=orbit_angle,
            orbit_speed=orbit_speed)

    game_object_manager.add_object(new_object)

    if new_object.type == "planet":
        nearest_sun = game_object_manager.get_nearest_orbit_object(game_object_manager._qtree, x, y, "sun")
        if nearest_sun:
            new_object.orbit_object = nearest_sun

    if new_object.type == "moon":
        nearest_planet = game_object_manager.get_nearest_orbit_object(game_object_manager._qtree, x, y, "planet")
        if nearest_planet:
            new_object.orbit_object = nearest_planet


def add_random_game_objects(qtree: QuadTree, amount: int) -> None:
    for i in range(amount):
        x, y = randint(0, qtree.boundary.w), randint(0, qtree.boundary.h)
        add_random_game_object(x, y, game_object_manager)

    game_object_manager.set_orbit_object(qtree)



