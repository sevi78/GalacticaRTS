import pygame
from pygame import Rect

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_quadtree.model.quad_tree import QuadTree
from source.pan_zoom_quadtree.view.draw import draw_quadtree, draw_quadtree_boundary
from source.qt_universe.controller.interaction_handler import InteractionHandler
from source.qt_universe.model.qt_config import *
from source.qt_universe.model.qt_game_object_factory import add_random_game_objects
from source.qt_universe.model.time_handler import time_handler
from source.qt_universe.view.draw import draw_points_inside_screen_rect_with_lod

font = pygame.font.SysFont(None, 12)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = 3000
        self._rect = Rect(0, 0, 1900, 1080)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h], pygame.RESIZABLE)
        self._qt_rect = Rect(0, 0, QT_WIDTH, QT_HEIGHT)
        self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)
        self.interaction_handler = InteractionHandler(self._qtree, self._qt_rect)

        pan_zoom_handler.zoom_min = 0.0002
        pan_zoom_handler.zoom_max = 2.0
        add_random_game_objects(self._qtree, POINTS_AMOUNT)

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
        draw_points_inside_screen_rect_with_lod(self._screen, self._qtree, self.get_screen_search_area())

        if self.interaction_handler.show_qtree:
            draw_quadtree(self._qtree, self._screen, pan_zoom_handler)

        draw_quadtree_boundary(self._qtree, self._screen, pan_zoom_handler)
        self.draw_debug_text()

    def update(self) -> None:
        # Update positions
        points = self._qtree.query(self._qt_rect)
        for point in points:
            point.update()
            # if point.type == "planet":
            #     if point.orbit_object:
            #         pygame.draw.line(self._screen,(255, 255, 255), point.rect.center, point.orbit_object.rect.center, 1)
            #     point.x += 10
            #     point.y += 10
            #     # self.wraparound(point)

        # Rebuild the quadtree with updated positions, because clear doesn't work properly
        self._qtree = QuadTree(self._qt_rect, QT_CAPACITY)

        for point in points:
            self._qtree.insert(point)

        self.interaction_handler._qtree = self._qtree

    def wraparound(self, point):
        point.x = point.x % self._qt_rect.width
        point.y = point.y % self._qt_rect.height

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self._screen.fill((0, 0, 0))
            self.draw()
            self.update()
            self._clock.tick(self._fps)
            pygame.display.update()
        pygame.quit()


Game().loop()
pygame.quit()
