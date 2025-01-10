import pygame
from pygame import Rect

from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_model_config.qt_config import QT_CAPACITY


class QuadTree:  # original
    def __init__(self, boundary: Rect, capacity: int = QT_CAPACITY) -> None:
        self.boundary = boundary
        self.southEast = None
        self.southWest = None
        self.northEast = None
        self.northWest = None

        self.capacity = capacity
        self.divided = False
        self.points = []

    def count(self):
        cnt = len(self.points)
        if not self.divided:
            return cnt
        else:
            cnt += self.northEast.count()
            cnt += self.northWest.count()
            cnt += self.southEast.count()
            cnt += self.southWest.count()
        return cnt

    def insert(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northEast.insert(point):
                return True
            elif self.northWest.insert(point):
                return True
            elif self.southEast.insert(point):
                return True
            elif self.southWest.insert(point):
                return True

    # def insert(self, point):
    #     if len(self.points) < self.capacity:
    #         self.points.append(point)
    #         return True
    #     else:
    #         if not self.divided:
    #             self.subdivide()
    #
    #         return (self.northEast.insert(point) or
    #                 self.northWest.insert(point) or
    #                 self.southEast.insert(point) or
    #                 self.southWest.insert(point))

    def remove(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        for i, p in enumerate(self.points):
            if p is point:
                self.points.pop(i)
                self.check_collapse()
                return True

        if self.divided:
            removed = any([
                self.northWest.remove(point),
                self.northEast.remove(point),
                self.southWest.remove(point),
                self.southEast.remove(point)
                ])
            if removed:
                self.check_collapse()
            return removed

        return False

    def clear(self):
        self.points = []
        if self.divided:
            self.northEast.clear()
            self.northWest.clear()
            self.southEast.clear()
            self.southWest.clear()

    def get_all_points(self):
        all_points = self.points.copy()
        if self.divided:
            all_points.extend(self.northEast.get_all_points())
            all_points.extend(self.northWest.get_all_points())
            all_points.extend(self.southEast.get_all_points())
            all_points.extend(self.southWest.get_all_points())
        return all_points

    def query(self, area: Rect):
        found = []
        if not self.boundary.colliderect(area):
            return found

        for p in self.points:
            if area.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            found.extend(self.northWest.query(area))
            found.extend(self.northEast.query(area))
            found.extend(self.southWest.query(area))
            found.extend(self.southEast.query(area))

        return found

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width
        h = self.boundary.height

        nw = Rect(x, y, w / 2, h / 2)
        ne = Rect(x + w / 2, y, w / 2, h / 2)
        sw = Rect(x, y + h / 2, w / 2, h / 2)
        se = Rect(x + w / 2, y + h / 2, w / 2, h / 2)

        self.northWest = QuadTree(boundary=nw, capacity=self.capacity)
        self.northEast = QuadTree(boundary=ne, capacity=self.capacity)
        self.southWest = QuadTree(boundary=sw, capacity=self.capacity)
        self.southEast = QuadTree(boundary=se, capacity=self.capacity)

        self.divided = True

    def check_collapse(self):
        if self.divided:
            total_points = len(self.points) + sum(
                    child.count() for child in [self.northWest, self.northEast, self.southWest, self.southEast])
            if total_points <= self.capacity:
                self.collapse()

    def collapse(self):
        if self.divided:
            for child in [self.northWest, self.northEast, self.southWest, self.southEast]:
                self.points.extend(child.points)
            self.northWest = self.northEast = self.southWest = self.southEast = None
            self.divided = False


def get_world_search_area() -> Rect:
    screen_rect = pygame.display.get_surface().get_rect()
    screen_search_area = screen_rect.inflate(-200, -200)  # Inflate by 200 pixels on each side
    world_x1, world_y1 = pan_zoom_handler.screen_2_world(screen_search_area.left, screen_search_area.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(screen_search_area.right, screen_search_area.bottom)
    return pygame.Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)


def get_search_area(rect: Rect) -> Rect:
    world_x1, world_y1 = pan_zoom_handler.screen_2_world(rect.left, rect.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(rect.right, rect.bottom)
    return pygame.Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)


def get_nearest_object(
        q_tree: QuadTree, screen_x: int or float, screen_y: int or float, type_: str or list[str],
        distance: int or float
        ):
    """
    Returns the nearest object of a certain type in a certain distance from the given coordinates,
    or None if no object is found

    Use screen coordinates like mouse.get_pos() or obj.rect!

    :param q_tree: The quad tree
    :param screen_x: The x coordinate
    :param screen_y: The y coordinate
    :param type_: The type of the object: either a string or a list of strings
    :param distance: The distance
    """

    # Define the search area rectangle
    search_area_rect = Rect(screen_x - distance / 2, screen_y - distance / 2, distance, distance)

    # Convert the search area rectangle to world coordinates
    world_search_area = get_search_area(search_area_rect)

    # Query the quad tree for objects within the search area
    visible_objects = q_tree.query(world_search_area)

    # Check if type_ is a string or a list of strings
    if isinstance(type_, str):
        # Filter the objects by type
        typed_visible_objects = [obj for obj in visible_objects if obj.type == type_]

        # Find the nearest object
        if not typed_visible_objects:
            return None
        nearest_object = min(typed_visible_objects, key=lambda obj: (obj.x - screen_x) ** 2 + (obj.y - screen_y) ** 2)

        return nearest_object
    elif isinstance(type_, list):
        # Iterate over the types in the list
        for obj_type in type_:
            # Filter the objects by type
            typed_visible_objects = [obj for obj in visible_objects if obj.type == obj_type]

            # Find the nearest object
            if typed_visible_objects:
                nearest_object = min(typed_visible_objects, key=lambda obj: (obj.x - screen_x) ** 2 + (
                        obj.y - screen_y) ** 2)
                return nearest_object

        # If no objects are found for any type, return None
        return None
    else:
        raise ValueError("type_ must be a string or a list of strings")
