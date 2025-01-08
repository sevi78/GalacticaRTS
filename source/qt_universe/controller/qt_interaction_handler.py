import pygame
from pygame import MOUSEBUTTONDOWN, Rect


from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_model_config.qt_config import QT_WIDTH, QT_HEIGHT, QT_RECT
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.view import qt_draw


class InteractionHandler:
    def __init__(self, game):
        self.game = game
        self._qtree = self.game.game_object_manager._qtree
        self._qt_rect = self.game.qt_renderer.screen_rect
        self.show_qtree = False

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_event(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)

    def handle_mouse_event(self, event):
        pass

    def handle_key_event(self, event):
        print(event.key)
        # if event.key == pygame.K_r:
        #     self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
        #     add_random_game_objects(self._qtree, POINTS_AMOUNT)
        # elif event.key == pygame.K_c:
        #     self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
        #     self._qtree.clear()
        if event.key == pygame.K_q:
            self.show_qtree = not self.show_qtree

        elif event.key == 1073741911:  # plus
            time_handler.set_game_speed(time_handler.game_speed + 1)
        elif event.key == 1073741910:  # pygame.K_MINUS:
            time_handler.set_game_speed(time_handler.game_speed - 1)

        elif event.key == pygame.K_d:
            qt_draw.DEBUG = not qt_draw.DEBUG

        elif event.key == pygame.K_s & pygame.KMOD_SHIFT:
            self.game.game_object_manager.save_load.save(self.game.game_object_manager.all_objects)

        elif event.key == pygame.K_l & pygame.KMOD_SHIFT:
            self.game.game_object_manager.save_load.load("test.json", "qt_database")

        elif event.key == pygame.K_c & pygame.KMOD_SHIFT:
            self.game.universe_factory.delete_universe()
            self.game.universe_factory.create_universe(QT_RECT)

        elif event.key == pygame.K_p:
            self.game.game_object_manager.select_objects_by_type("planet")

        elif event.key == pygame.K_m:
            self.game.game_object_manager.select_objects_by_type("moon")

        elif event.key == pygame.K_i:
            self.game.game_object_manager.select_objects_by_type("collectable_item")

        elif event.key == pygame.K_s:
            self.game.game_object_manager.select_objects_by_type("sun")



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
