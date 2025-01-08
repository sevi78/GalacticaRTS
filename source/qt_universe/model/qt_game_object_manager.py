import math
import time

import pygame
from pygame import Rect

from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_model_config.qt_config import QT_CAPACITY, QT_WIDTH
from source.qt_universe.model.qt_quad_tree import QuadTree
from source.qt_universe.model.qt_save_load import QTSaveLoad
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view.game_objects.qt_game_objects import QTMovingImage, QTMovingGif
from source.qt_universe.view.qt_draw import get_world_search_area


class GameObjectManager:
    def __init__(self, qt_rect, game):
        self._qtree = QuadTree(qt_rect, QT_CAPACITY)
        self.game = game
        self.all_objects = []
        self.dynamic_objects = []  # For objects that need constant updating
        self._qt_rect = qt_rect  # Store the qt_rect for wraparound checks

        self.save_load = QTSaveLoad(self)

    def add_object(self, game_object):
        self.all_objects.append(game_object)
        self._qtree.insert(game_object)
        if isinstance(game_object, QTMovingImage) or isinstance(game_object, QTMovingGif):
            self.dynamic_objects.append(game_object)

    def remove_object(self, game_object):
        self.all_objects.remove(game_object)
        self._qtree.remove(game_object)
        if isinstance(game_object, QTMovingImage) or isinstance(game_object, QTMovingGif):
            self.dynamic_objects.remove(game_object)

        # print ("self.object_count: ", len(self.all_objects))

    def query(self, area):
        return self._qtree.query(area)

    def set_lod(self, obj):
        r = obj.width / 2 * pan_zoom_handler.get_zoom()
        if r < 1:
            obj.lod = 0
        elif r < 10:
            obj.lod = 1
        else:
            obj.lod = 2

        # lod_ = obj.rect.width
        # print (f"obj.rect.width: {obj.rect.width})

    def get_nearest_orbit_object(self, x: int, y: int, type_: str):
        search_radius = QT_WIDTH  # max(qtree.boundary.width, qtree.boundary.height)
        search_area = Rect(x - search_radius, y - search_radius, search_radius * 2, search_radius * 2)
        nearby_objects = self.all_objects  # qtree.query(search_area)
        nearest_orbit_object = None
        min_distance = float('inf')
        for obj in nearby_objects:
            if obj.type == type_:
                distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_orbit_object = obj
        return nearest_orbit_object

    def set_orbit_object(self) -> None:
        start_time = time.time()
        for obj in self.all_objects:
            if obj.type == "planet":
                nearest_sun = self.get_nearest_orbit_object(obj.x, obj.y, "sun")
                if nearest_sun:
                    obj.orbit_object = nearest_sun
            if obj.type == "moon":
                nearest_planet = self.get_nearest_orbit_object(obj.x, obj.y, "planet")
                if nearest_planet:
                    obj.orbit_object = nearest_planet

        end_time = time.time()
        duration = end_time - start_time
        print(f"set_orbit_object took{duration:.6f} seconds")

    def set_orbit_object_by_id(self):
        for obj in self.all_objects:
            if hasattr(obj, "orbit_id"):
                obj.orbit_object = [_ for _ in self.all_objects if _.id == obj.orbit_id][0]

    def set_target_object_by_id(self):
        for obj in self.all_objects:
            if hasattr(obj, "target"):
                if obj.target:
                    obj.target = [_ for _ in self.all_objects if _.id == obj.target][0]

    def find_nearest(self, objects, target_x, target_y):
        if not objects:
            return None

        nearest = objects[0]
        min_distance = math.inf

        for obj in objects:
            distance = math.sqrt((obj.x - target_x) ** 2 + (obj.y - target_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest = obj

        return nearest

    def wraparound(self, point):
        point.x %= self._qt_rect.width
        point.y %= self._qt_rect.height

    def orbit_with_constant_distance(
            self, obj, orbit_obj, orbit_speed, direction
            ):  # used for planets, new with constant orbit distance
        if not orbit_obj:
            return

        if hasattr(obj, "enemy"):
            orbit_speed = orbit_speed / 5

        # Calculate the position difference between the orbiting object and the object
        pos_diff = pygame.math.Vector2(orbit_obj.x, orbit_obj.y) - pygame.math.Vector2(obj.x, obj.y)
        # pos_diff = obj.orbit_radius

        # Set the orbit radius based on the current distance to the orbiting object
        # obj.orbit_radius = pos_diff.length()

        # If the orbit angle is not set, calculate it based on the current position
        if not obj.orbit_angle:
            # Calculate the angle from the orbit center to the object
            obj.orbit_angle = math.degrees(math.atan2(pos_diff.y, pos_diff.x))
            # Adjust the angle for the direction of orbit
            if direction < 0:
                obj.orbit_angle += 180
            obj.orbit_angle %= 360

        # Update the orbit angle based on the orbit speed and game speed
        obj.orbit_angle += orbit_speed * direction * time_handler.game_speed
        obj.orbit_angle %= 360  # Ensure the angle stays within 0-359 degrees

        # Keep the distance constant by adjusting the position based on the orbit radius
        new_pos = pygame.math.Vector2(obj.orbit_radius, 0).rotate(-obj.orbit_angle)

        # Update the object's world position while maintaining the constant distance
        # if config.app.game_client.is_host:
        obj.x = orbit_obj.x + new_pos.x
        obj.y = orbit_obj.y + new_pos.y

    def update_objects_position(self, obj):
        orbitable_objects = ["planet", "moon"]

        if obj.type in orbitable_objects:
            if obj.orbit_object:
                self.orbit_with_constant_distance(obj, obj.orbit_object, obj.orbit_speed, obj.orbit_direction)

        elif isinstance(obj, QTMovingImage) or isinstance(obj, QTMovingGif):
            # Update position based on movement speed and direction
            movement = obj.direction * (obj.movement_speed * time_handler.game_speed)
            obj.x += movement.x
            obj.y += movement.y

            # Update rotation
            obj.rotation_angle += (obj.rotation_speed * time_handler.game_speed)
            obj.rotation_angle %= 360  # Keep the angle between 0 and 359 degrees

            # Wrap around functionality
            if getattr(obj, 'wrap_around', False):  # Check if wrap_around is set to True
                self.wraparound(obj)

    def update_objects_rect__(self, obj):
        screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)
        obj.rect.x = screen_x - obj.width/2 * pan_zoom_handler.get_zoom()
        obj.rect.y = screen_y - obj.height/2 * pan_zoom_handler.get_zoom()

    def update_objects_rect(self, obj):
        # Get the screen coordinates based on the object's world position
        screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)

        # Get the zoom level once and store it
        zoom = pan_zoom_handler.get_zoom()

        # Calculate half width and height multiplied by zoom
        half_width = obj.width / 2 * zoom
        half_height = obj.height / 2 * zoom

        # Update the object's rectangle position directly
        obj.rect.topleft = (screen_x - half_width, screen_y - half_height)

    def update_objects_size(self, obj):
        screen_width = obj.width * pan_zoom_handler.get_zoom()
        screen_height = obj.height * pan_zoom_handler.get_zoom()

        # Adjust the size of the object's rectangle based on zoom level
        obj.rect.width = screen_width
        obj.rect.height = screen_height

        self.set_lod(obj)

    def rebuild_qtree(self):
        new_qtree = QuadTree(self._qtree.boundary, QT_CAPACITY)
        for obj in self.all_objects:
            new_qtree.insert(obj)

        self._qtree = new_qtree

    def select_objects_by_type(self, object_type):
        for i in self.all_objects:
            i.selected = True if i.type.startswith(object_type) else False



    def update(self):
        # Always update dynamic objects
        for obj in self.dynamic_objects:
            self.update_objects_position(obj)
            self.update_objects_rect(obj)

        world_search_area = get_world_search_area()
        visible_objects = self._qtree.query(world_search_area)

        if pan_zoom_handler.zooming:
            for obj in visible_objects:
                if not obj.visible:
                    continue
                self.update_objects_position(obj)
                self.update_objects_size(obj)
                self.update_objects_rect(obj)

            self.rebuild_qtree()

        elif pan_zoom_handler.panning:
            for obj in visible_objects:
                if not obj.visible:
                    continue
                self.update_objects_position(obj)
                self.update_objects_rect(obj)

            self.rebuild_qtree()
