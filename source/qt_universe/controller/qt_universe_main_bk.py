import pygame

from source.math.math_handler import ndigits
from source.qt_universe.controller.qt_box_selection import BoxSelection
from source.qt_universe.controller.qt_interaction_handler import InteractionHandler
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_game_object_manager import GameObjectManager
from source.qt_universe.model.qt_model_config.qt_config import *
from source.qt_universe.model.qt_time_handler import time_handler
from source.qt_universe.model.qt_universe_factory import UniverseFactory
from source.qt_universe.view.qt_debugger import draw_debug_text
from source.qt_universe.view.qt_draw import draw_objects
from source.qt_universe.view.qt_draw_methods import draw_quadtree, draw_quadtree_boundary


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = FPS
        self._rect = Rect(0, 0, 1920, 1080)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h], pygame.RESIZABLE)
        self.universe_surface = pygame.Surface(self._screen.get_size())
        self._screen_search_area = self.get_screen_search_area()

        # pan_zoom_handler.zoom_min = 0.0002
        # pan_zoom_handler.zoom_max = 2.0
        # pan_zoom_handler.center_pan_zoom_handler(Rect(QT_RECT.x + QT_RECT.width / 2, QT_RECT.y + QT_RECT.height / 2,QT_RECT.width, QT_RECT.height))
        # x,y = pan_zoom_handler.screen_2_world(self._screen.get_width() / 2, 0)
        # navigate_to_position(x,y)
        # add_random_game_objects(game_object_manager._qtree, POINTS_AMOUNT)

        self.game_object_manager = GameObjectManager(QT_RECT, self)
        self.interaction_handler = InteractionHandler(self)
        self.box_selection = BoxSelection(self._screen, self.game_object_manager.all_objects)
        self.universe_factory = UniverseFactory(self._screen, QT_RECT, self.game_object_manager)
        self.universe_factory.create_universe(QT_RECT, collectable_items_amount=0)

        self.setup_pan_zoom_handler()

    def setup_pan_zoom_handler(self) -> None:
        # calculate the min zoom factor
        pan_zoom_handler.zoom_min = 1000 / QT_WIDTH#self.data["globals"]["width"]

        # set zoom
        pan_zoom_handler.set_zoom(pan_zoom_handler.zoom_min)

        pan_zoom_handler.world_offset_x= 1000

        # navigate zo center of the level
        # navigate_to_position(QT_WIDTH / 2 * pan_zoom_handler.get_zoom(), QT_HEIGHT / 2 * pan_zoom_handler.get_zoom())#navigate_to_position(QT_WIDTH / 2,QT_HEIGHT / 2)

    def event_loop(self):
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        self.interaction_handler.handle_events(events)
        self.box_selection.listen(events)
        # self.box_selection.set_selectable_objects(self.game_object_manager._qtree.query(self._screen_search_area))
        self.box_selection.set_selectable_objects(self.game_object_manager.all_objects)

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._running = False

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

        # draw the box selection
        self.box_selection.draw()

        # Draw the qtree on the universe surface
        draw_quadtree_boundary(self.game_object_manager._qtree, self._screen, pan_zoom_handler)
        if self.interaction_handler.show_qtree:
            draw_quadtree(self.game_object_manager._qtree, self._screen, pan_zoom_handler)

        # Draw debug text directly on the screen (assuming it's UI)
        draw_debug_text(self._screen, {
            "fps": self._clock.get_fps(),
            "game_speed": time_handler.game_speed,
            "point_count": self.game_object_manager._qtree.count(),
            "dynamic_object_count": len(self.game_object_manager.dynamic_objects),
            "zoom:": pan_zoom_handler.get_zoom(),
            "lod:":ndigits(pan_zoom_handler.get_zoom(), 4)})

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
