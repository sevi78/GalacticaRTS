import pygame

from source.qt_universe.controller.qt_interaction_handler import InteractionHandler
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.config.qt_config import *
from source.qt_universe.model.qt_game_object_manager import GameObjectManager
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.model.qt_universe_factory import UniverseFactory
from source.qt_universe.view.qt_draw import draw_quadtree_boundary, \
    draw_quadtree, draw_objects

font = pygame.font.SysFont(None, 12)

FPS = 30000

"""
TODO: 
clean unused stuff. 
update: when , why and what to update ... 

make cmments !!

rename funcitons like draw_points_inside_screen_rect_with_lod

"""


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = FPS
        self._rect = Rect(0, 0, 1900, 1080)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h], pygame.RESIZABLE)
        self.universe_surface = pygame.Surface(self._screen.get_size())
        self._screen_search_area = self.get_screen_search_area()

        pan_zoom_handler.zoom_min = 0.0002
        pan_zoom_handler.zoom_max = 2.0
        pan_zoom_handler.center_pan_zoom_handler(QT_RECT)
        # add_random_game_objects(game_object_manager._qtree, POINTS_AMOUNT)

        self.game_object_manager = GameObjectManager(QT_RECT, self)
        self.interaction_handler = InteractionHandler(self.game_object_manager._qtree, self._rect)
        self.universe_factory = UniverseFactory(self._screen, QT_RECT, self.game_object_manager)
        self.universe_factory.create_universe(QT_RECT, collectable_items_amount=0)

    def event_loop(self):
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        self.interaction_handler.handle_events(events)

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._running = False

    def draw_debug_text(self):
        text_ = (
            f"Point Quadtree: {self._clock.get_fps()} fps, game_speed: {time_handler.game_speed}")
        text = font.render(text_, True, (255, 255, 255))
        self._screen.blit(text, (10, 10))

    def get_screen_search_area(self):
        border = 50
        screen_search_area = Rect(border, border, self._screen.get_width() - (border * 2), self._screen.get_height() - (
                border * 2))
        return screen_search_area

    def draw(self) -> None:
        # Clear the screen
        self._screen.fill((0, 0, 0))

        # Clear the universe surface
        self.universe_surface.fill((0, 0, 0))

        # Draw the points onto the universe surface
        draw_objects(self.universe_surface, self.game_object_manager._qtree, self._screen_search_area)

        # Draw the universe surface onto the main screen
        self._screen.blit(self.universe_surface, (0, 0))

        # Draw the qtree on the universe surface
        draw_quadtree_boundary(self.game_object_manager._qtree, self._screen, pan_zoom_handler)
        if self.interaction_handler.show_qtree:
            draw_quadtree(self.game_object_manager._qtree, self._screen, pan_zoom_handler)

        # Draw debug text directly on the screen (assuming it's UI)
        self.draw_debug_text()

        # Finally, update the screen
        # pygame.display.flip()
        pygame.display.update()

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self.game_object_manager.update()
            self.interaction_handler._qtree = self.game_object_manager._qtree
            self.draw()
            self._clock.tick(self._fps)
        pygame.quit()


game = Game()
game.loop()
pygame.quit()
