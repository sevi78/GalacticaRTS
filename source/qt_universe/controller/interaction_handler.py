import pygame
from pygame import MOUSEBUTTONDOWN, Rect

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_quadtree.model.quad_tree import QuadTree

from source.qt_universe.model.qt_config import *
from source.qt_universe.model.qt_game_object_factory import add_random_game_objects, add_random_game_object
from source.qt_universe.model.time_handler import time_handler


class InteractionHandler:
    def __init__(self, qtree, qt_rect):
        self._qtree = qtree
        self._qt_rect = qt_rect
        self.show_qtree = False

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_event(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)

    def handle_mouse_event(self, event):
        if event.button == 1:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.add_game_object()
            else:
                self.select_object(True)
        elif event.button == 3:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.remove_game_object()
            else:
                self.select_object(False)

    def handle_key_event(self, event):
        print (event.key)
        if event.key == pygame.K_r:
            self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
            add_random_game_objects(self._qtree, POINTS_AMOUNT)
        elif event.key == pygame.K_c:
            self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
            self._qtree.clear()
        elif event.key == pygame.K_q:
            self.show_qtree = not self.show_qtree

        elif event.key ==1073741911: # plus
            time_handler.set_game_speed(time_handler.game_speed + 1)
        elif event.key == 1073741910:#pygame.K_MINUS:
            time_handler.set_game_speed(time_handler.game_speed - 1)

    def select_object__(self, select):
        mX, mY = pygame.mouse.get_pos()
        world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
        visible_rect = self.get_visible_rect()
        visible_objects = self._qtree.query(visible_rect)

        for obj in visible_objects:
            obj_screen_rect = self.get_object_screen_rect(obj)
            if obj_screen_rect.collidepoint(mX, mY):
                obj.selected = select
                print(f"{'Selected' if select else 'Deselected'} object at x: {obj.x}, y: {obj.y}")
                return

        if not select:
            for obj in visible_objects:
                obj.selected = False
            print("Deselected all objects")

    def select_object(self, select):
        mX, mY = pygame.mouse.get_pos()
        world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)

        # Query the quadtree for objects in the visible area
        visible_rect = self.get_visible_rect()
        visible_objects = self._qtree.query(visible_rect)

        object_selected = False  # Track if any object is selected

        for obj in visible_objects:
            # Convert object's position to screen coordinates
            screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)

            # Calculate object's rect in screen coordinates
            obj_screen_rect = Rect(
                    screen_x - obj.width * pan_zoom_handler.get_zoom() / 2,
                    screen_y - obj.height * pan_zoom_handler.get_zoom() / 2,
                    obj.width * pan_zoom_handler.get_zoom(),
                    obj.height * pan_zoom_handler.get_zoom()
                    )

            # Check if the click (in screen coordinates) is within the object's screen rect
            if obj_screen_rect.collidepoint(mX, mY):
                obj.selected = select
                print(f"{'Selected' if select else 'Deselected'} object at x: {obj.x}, y: {obj.y}")
                object_selected = True  # Mark that we have selected an object
                break  # Exit loop after selecting one object

        if not select and not object_selected:
            # If we're deselecting and didn't click on any object, deselect all
            for obj in visible_objects:
                obj.selected = False
            print("Deselected all objects")

    def add_game_object(self):
        mX, mY = pygame.mouse.get_pos()
        world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
        add_random_game_object(world_x, world_y, self._qtree)

    def remove_game_object(self):
        mX, mY = pygame.mouse.get_pos()
        world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
        print(f"world_x: {world_x}, world_y: {world_y}")
        visible_rect = self.get_visible_rect()
        visible_game_objects = self._qtree.query(visible_rect)

        for game_object in visible_game_objects:
            planet_screen_rect = self.get_object_screen_rect(game_object)
            if planet_screen_rect.collidepoint(mX, mY):
                self._qtree.remove(game_object)
                print(f"Removed planet at x: {game_object.x}, y: {game_object.y}")
                return
        print("No planet found at the clicked position")

    def get_visible_rect(self):
        return Rect(pan_zoom_handler.world_offset_x, pan_zoom_handler.world_offset_y,
                pygame.display.get_surface().get_width() / pan_zoom_handler.get_zoom(),
                pygame.display.get_surface().get_height() / pan_zoom_handler.get_zoom())

    def get_object_screen_rect(self, obj):
        screen_x, screen_y = pan_zoom_handler.world_2_screen(obj.x, obj.y)
        return Rect(
                screen_x - obj.width * pan_zoom_handler.get_zoom() / 2,
                screen_y - obj.height * pan_zoom_handler.get_zoom() / 2,
                obj.width * pan_zoom_handler.get_zoom(),
                obj.height * pan_zoom_handler.get_zoom()
                )
