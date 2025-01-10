import pygame

from source.qt_universe.controller.qt_box_selection import BoxSelection
from source.qt_universe.controller.qt_interaction_handler import InteractionHandler
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.model.qt_game_object_manager import GameObjectManager
from source.qt_universe.model.qt_model_config.qt_config import *
from source.qt_universe.model.qt_universe_factory import UniverseFactory
from source.qt_universe.view.qt_renderer import QTRenderer


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = FPS
        self._running = True

        # Initialize QTRenderer
        self.qt_renderer = QTRenderer(self)

        # Initialize managers and handlers
        self.setup_pan_zoom_handler()
        self.game_object_manager = GameObjectManager(QT_RECT, self)
        self.interaction_handler = InteractionHandler(self)
        self.box_selection = BoxSelection(self.qt_renderer.screen, self.game_object_manager.all_objects)

        # Create universe
        self.universe_factory = UniverseFactory(self.qt_renderer.screen, QT_RECT, self.game_object_manager)
        self.universe_factory.create_universe(QT_RECT, collectable_items_amount=0)

    def setup_pan_zoom_handler(self) -> None:
        pan_zoom_handler.zoom_min = 1000 / QT_WIDTH  # Example zoom factor calculation
        # pan_zoom_handler.set_zoom(pan_zoom_handler.zoom_min)
        pan_zoom_handler.set_zoom_at_position(pan_zoom_handler.zoom_min, (self.qt_renderer.screen.get_width() // 2, self.qt_renderer.screen.get_height() // 2))
        pan_zoom_handler.world_offset_x = 1000

    def event_loop(self):
        events = pygame.event.get()
        pan_zoom_handler.listen(events)
        self.interaction_handler.handle_events(events)
        self.box_selection.listen(events)

        # Set selectable objects for box selection
        self.box_selection.set_selectable_objects(self.game_object_manager.all_objects)

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._running = False

    def get_screen_search_area(self):
        border = 50
        screen_search_area = Rect(border, border,
                self.qt_renderer.screen.get_width() - (border * 2),
                self.qt_renderer.screen.get_height() - (border * 2))
        return screen_search_area

    def loop(self) -> None:
        while self._running:
            # self.event_loop()
            self.game_object_manager.update()
            self.interaction_handler._qtree = self.game_object_manager._qtree

            # Use QTRenderer to draw
            self.qt_renderer.draw()

            self._clock.tick(self._fps)
            self.event_loop()

            pygame.display.flip()

        pygame.quit()


# Start the game loop
game = Game()
game.loop()
pygame.quit()
