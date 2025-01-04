import math

import pygame
from pygame import Rect

from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.config.qt_config import QT_CAPACITY
from source.qt_universe.model.qt_quad_tree import QuadTree
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view.game_objects.qt_stars import QTMovingImage, QTMovingGif
from source.qt_universe.view.qt_draw import get_world_search_area


class GameObjectManager:
    def __init__(self, qt_rect, game):
        self._qtree = QuadTree(qt_rect, QT_CAPACITY)
        self.game = game
        self.all_objects = []
        self.dynamic_objects = []  # For objects that need constant updating
        self._qt_rect = qt_rect  # Store the qt_rect for wraparound checks

    def add_object(self, game_object):
        self.all_objects.append(game_object)
        self._qtree.insert(game_object)
        if isinstance(game_object, QTMovingImage) or isinstance(game_object, QTMovingGif):
            self.dynamic_objects.append(game_object)

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

    def get_nearest_orbit_object(self, qtree: QuadTree, x: int, y: int, type_: str):
        search_radius = max(qtree.boundary.width, qtree.boundary.height)
        search_area = Rect(x - search_radius, y - search_radius, search_radius * 2, search_radius * 2)
        nearby_objects = qtree.query(search_area)
        nearest_orbit_object = None
        min_distance = float('inf')
        for obj in nearby_objects:
            if obj.type == type_:
                distance = ((obj.x - x) ** 2 + (obj.y - y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_orbit_object = obj
        return nearest_orbit_object

    def set_orbit_object(self, qtree: QuadTree) -> None:
        for obj in qtree.points:
            if obj.type == "planet":
                nearest_sun = self.get_nearest_orbit_object(qtree, obj.x, obj.y, "sun")
                if nearest_sun:
                    obj.orbit_object = nearest_sun
            if obj.type == "moon":
                nearest_planet = self.get_nearest_orbit_object(qtree, obj.x, obj.y, "planet")
                if nearest_planet:
                    obj.orbit_object = nearest_planet

    def wraparound(self, point):
        point.x %= self._qt_rect.width
        point.y %= self._qt_rect.height

    def update_objects_position(self, obj):
        orbitable_objects = ["planet", "moon"]

        if obj.type in orbitable_objects and obj.orbit_object:
            orbit_radius = math.hypot(obj.x - obj.orbit_object.x, obj.y - obj.orbit_object.y)
            obj.orbit_angle += obj.orbit_speed * time_handler.game_speed
            obj.x = obj.orbit_object.x + orbit_radius * math.cos(obj.orbit_angle)
            obj.y = obj.orbit_object.y + orbit_radius * math.sin(obj.orbit_angle)

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

    def update_objects_rect(self, obj):
        screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)
        screen_width = obj.width * pan_zoom_handler.get_zoom()
        screen_height = obj.height * pan_zoom_handler.get_zoom()

        # Update the object's rectangle based on its position and size
        obj.rect = pygame.Rect(
                screen_x - screen_width / 2,
                screen_y - screen_height / 2,
                screen_width,
                screen_height
                )

        self.set_lod(obj)

    def update_objects_size(self, obj):
        screen_width = obj.width * pan_zoom_handler.get_zoom()
        screen_height = obj.height * pan_zoom_handler.get_zoom()

        # Adjust the size of the object's rectangle based on zoom level
        obj.rect.width = screen_width
        obj.rect.height = screen_height

    def rebuild_qtree(self):
        new_qtree = QuadTree(self._qtree.boundary, QT_CAPACITY)
        for obj in self.all_objects:
            new_qtree.insert(obj)

        self._qtree = new_qtree

    def update(self):
        # Always update dynamic objects
        for obj in self.dynamic_objects:
            self.update_objects_position(obj)
            self.update_objects_rect(obj)

        world_search_area = get_world_search_area()
        visible_objects = self._qtree.query(world_search_area)

        if pan_zoom_handler.zooming:
            for obj in visible_objects:
                self.update_objects_position(obj)
                self.update_objects_size(obj)
                self.update_objects_rect(obj)

            self.rebuild_qtree()

        elif pan_zoom_handler.panning:
            for obj in visible_objects:
                self.update_objects_position(obj)
                self.update_objects_rect(obj)

            self.rebuild_qtree()
