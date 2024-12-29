from random import randint
import pygame
from pygame import draw, Rect, Surface
from pygame import gfxdraw, MOUSEBUTTONDOWN
from source.handlers.pan_zoom_handler import pan_zoom_handler


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point(x={self.x}, y={self.y})"


class QuadTree:
    def __init__(self, boundary: Rect, capacity: int = 4) -> None:
        self.boundary = boundary
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

    def draw(self, surface: Surface, pan_zoom_handler):
        screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
        boundary_screen = pan_zoom_handler.world_2_screen(self.boundary.x, self.boundary.y)
        boundary_screen_width = self.boundary.width * pan_zoom_handler.get_zoom()
        boundary_screen_height = self.boundary.height * pan_zoom_handler.get_zoom()
        boundary_screen_rect = Rect(
                boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

        if screen_rect.colliderect(boundary_screen_rect):
            draw_rect_border(surface, boundary_screen_rect, (255, 255, 255))
            if self.divided:
                self.northEast.draw(surface, pan_zoom_handler)
                self.northWest.draw(surface, pan_zoom_handler)
                self.southEast.draw(surface, pan_zoom_handler)
                self.southWest.draw(surface, pan_zoom_handler)

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


def draw_rect_border(screen: Surface, r: Rect, color) -> None:
    draw.line(screen, color, (r.x, r.y), (r.x + r.w, r.y))
    draw.line(screen, color, (r.x, r.y), (r.x, r.y + r.h))
    draw.line(screen, color, (r.x + r.w, r.y), (r.x + r.w, r.y + r.h))
    draw.line(screen, color, (r.x, r.y + r.h), (r.x + r.w, r.y + r.h))


RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._fps = 3000
        self._rect = Rect(0, 0, 1200, 800)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h], pygame.RESIZABLE)
        self._points = []
        self._qtree = QuadTree(self._rect, 4)

        for i in range(2000):
            point = Point(randint(0, self._rect.w), randint(0, self._rect.h))
            self._points.append(point)
            self._qtree.insert(point)

    def draw(self) -> None:
        self._screen.fill((0, 0, 0))

        visible_rect = Rect(pan_zoom_handler.world_offset_x, pan_zoom_handler.world_offset_y,
                self._rect.w / pan_zoom_handler.get_zoom(), self._rect.h / pan_zoom_handler.get_zoom())

        for p in self._points:
            if visible_rect.collidepoint(p.x, p.y):
                screen_position_x, screen_position_y = pan_zoom_handler.world_2_screen(p.x, p.y)
                gfxdraw.pixel(self._screen, int(screen_position_x), int(screen_position_y), RED)

        mX, mY = pygame.mouse.get_pos()
        world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
        search_size = 200 / pan_zoom_handler.get_zoom()
        search_area = Rect(world_x - search_size / 2, world_y - search_size / 2, search_size, search_size)

        found = self._qtree.query(search_area)

        screen_search_area = Rect(mX - 100, mY - 100, 200, 200)
        draw_rect_border(self._screen, screen_search_area, GREEN)

        for point in found:
            screen_x, screen_y = pan_zoom_handler.world_2_screen(point.x, point.y)
            draw.circle(self._screen, GREEN, (int(screen_x), int(screen_y)), 3)

        self._qtree.draw(self._screen, pan_zoom_handler)

        pygame.display.update()

    def event_loop(self):
        events = pygame.event.get()
        pan_zoom_handler.listen(events)

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mX, mY = pygame.mouse.get_pos()
                world_x, world_y = pan_zoom_handler.screen_2_world(mX, mY)
                point = Point(int(world_x), int(world_y))
                self._points.append(point)
                self._qtree.insert(point)

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self.draw()
            self._clock.tick(self._fps)
            pygame.display.set_caption(f"Point Quadtree: {self._clock.get_fps()} fps")

        pygame.quit()


Game().loop()
pygame.quit()
