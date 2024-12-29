from random import choice, randint, uniform

from pygame import Rect

from source.handlers.color_handler import get_average_color
from source.multimedia_library.images import get_image_names_from_folder, get_image
from source.pan_zoom_quadtree.model.quad_tree import QuadTree
from source.qt_universe.model.game_object import GameObject

planet_images = get_image_names_from_folder("planets")
sun_images = get_image_names_from_folder("suns")


images = planet_images + sun_images


def get_nearest_sun(qtree, x, y):
    search_radius = max(qtree.boundary.width, qtree.boundary.height)
    search_area = Rect(x - search_radius, y - search_radius, search_radius * 2, search_radius * 2)
    nearby_objects = qtree.query(search_area)

    nearest_sun = None
    min_distance = float('inf')

    for obj in nearby_objects:
        if obj.type == "sun":
            distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_sun = obj

    return nearest_sun


def add_random_game_object_(x: int, y: int, qtree: QuadTree) -> None:
    image_name = choice(images)
    image = get_image(image_name)
    w, h = image.get_rect().width, image.get_rect().height
    color = get_average_color(image, consider_alpha=True)
    point = GameObject(x, y, w, h, image_name, color, type="planet" if image_name in planet_images else "sun")

    qtree.insert(point)


def add_random_game_object(x: int, y: int, qtree: QuadTree) -> None:
    image_name = choice(images)
    image = get_image(image_name)
    w, h = image.get_rect().width, image.get_rect().height
    color = get_average_color(image, consider_alpha=True)
    orbit_angle = randint(0, 360)
    orbit_speed = uniform(0.001, 0.005)
    new_object = GameObject(
            x=x,
            y=y,
            width=w,
            height=h,
            image_name= image_name,
            color=color,
            type="planet" if image_name in planet_images else "sun",
            orbit_angle=orbit_angle,
            orbit_speed=orbit_speed)

    qtree.insert(new_object)

    if new_object.type == "planet":
        nearest_sun = get_nearest_sun(qtree, x, y)
        if nearest_sun:
            new_object.orbit_object = nearest_sun
        #     print(f"Planet at ({x}, {y}) is now orbiting Sun at ({nearest_sun.x}, {nearest_sun.y})")
        # else:
        #     print(f"No sun found for planet at ({x}, {y})")




def add_random_game_objects(qtree: QuadTree, amount: int) -> None:
    for i in range(amount):
        x, y = randint(0, qtree.boundary.w), randint(0, qtree.boundary.h)
        add_random_game_object(x, y, qtree)
