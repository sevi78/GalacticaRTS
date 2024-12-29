from random import randint

import pygame
from pygame import Rect

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_quadtree.model.points import Point
from source.pan_zoom_quadtree.model.quad_tree import QuadTree
from source.pan_zoom_quadtree.view.draw import draw_quadtree, draw_quadtree_boundary, draw_points_inside_screen_rect

POINTS_AMOUNT = 2000
QT_WIDTH = 500000
QT_HEIGHT = 500000


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = 3000
        self._rect = Rect(0, 0, 1900, 1080)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h], pygame.RESIZABLE)

        self._qt_rect = Rect(0, 0, QT_WIDTH, QT_HEIGHT)
        self._qtree = QuadTree(self._qt_rect, 4)
        self.show_qtree = False

        pan_zoom_handler.zoom_min = 0.0002
        pan_zoom_handler.zoom_max = 2.0
        self.lod = pan_zoom_handler.get_zoom()

        self.add_random_points(POINTS_AMOUNT)

    def add_random_points(self, amount):
        min_size = 5
        max_size = 200
        for i in range(amount):
            size = randint(min_size, max_size)
            point = Point(randint(0, self._qt_rect.w), randint(0, self._qt_rect.h), size, size)

            self._qtree.insert(point)

    def draw(self) -> None:
        self._screen.fill((0, 0, 0))

        visible_rect = Rect(pan_zoom_handler.world_offset_x, pan_zoom_handler.world_offset_y,
                self._rect.w / pan_zoom_handler.get_zoom(), self._rect.h / pan_zoom_handler.get_zoom())

        # draw_points_inside_visible_rect(self._screen, self._qtree, visible_rect)

        # draw_points_selection(self._screen, self._qtree)

        draw_points_inside_screen_rect(self._screen, self._qtree)

        if self.show_qtree:
            draw_quadtree(self._qtree, self._screen, pan_zoom_handler)

        draw_quadtree_boundary(self._qtree, self._screen, pan_zoom_handler)

        pygame.display.update()

    def event_loop(self):
        events = pygame.event.get()
        pan_zoom_handler.listen(events)

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False

            # if event.type == MOUSEBUTTONDOWN and event.button == 1:
            #     mX, mY = pygame.mouse.get_pos()
            #     world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
            #
            #     min_size = 5
            #     max_size = 200
            #
            #     size = randint(min_size, max_size)
            #
            #     point = Planet(int(world_x), int(world_y), size, size)
            #
            #     self._qtree.insert(point)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False

                if event.key == pygame.K_r:
                    self._qtree = QuadTree(self._qt_rect, 4)
                    self.add_random_points(POINTS_AMOUNT)

                if event.key == pygame.K_c:
                    self._qtree = QuadTree(self._qt_rect, 4)
                    self._qtree.clear()

                if event.key == pygame.K_q:
                    self.show_qtree = not self.show_qtree

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self.draw()
            self._clock.tick(self._fps)
            self.lod = pan_zoom_handler.get_zoom()
            pygame.display.set_caption(
                    f"Point Quadtree: {self._clock.get_fps()} fps, panzoom: {pan_zoom_handler.get_zoom()}/{pan_zoom_handler.zoom_min}/{pan_zoom_handler.zoom_max}, lod: {self.lod}")

        pygame.quit()


Game().loop()
pygame.quit()
