from pygame import Rect

from source.qt_universe.model.config.qt_config import QT_CAPACITY


class QuadTree:# original
    def __init__(self, boundary: Rect, capacity: int = QT_CAPACITY) -> None:
        self.boundary = boundary
        self.southEast = None
        self.southWest = None
        self.northEast = None
        self.northWest = None

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

    def remove(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        for i, p in enumerate(self.points):
            if p is point:
                self.points.pop(i)
                self.check_collapse()
                return True

        if self.divided:
            removed = any([
                self.northWest.remove(point),
                self.northEast.remove(point),
                self.southWest.remove(point),
                self.southEast.remove(point)
                ])
            if removed:
                self.check_collapse()
            return removed

        return False

    def clear(self):
        self.points = []
        if self.divided:
            self.northEast.clear()
            self.northWest.clear()
            self.southEast.clear()
            self.southWest.clear()

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

    def check_collapse(self):
        if self.divided:
            total_points = len(self.points) + sum(
                    child.count() for child in [self.northWest, self.northEast, self.southWest, self.southEast])
            if total_points <= self.capacity:
                self.collapse()

    def collapse(self):
        if self.divided:
            for child in [self.northWest, self.northEast, self.southWest, self.southEast]:
                self.points.extend(child.points)
            self.northWest = self.northEast = self.southWest = self.southEast = None
            self.divided = False



# class QuadTree__:# old
#     def __init__(self, boundary: Rect, capacity: int = QT_CAPACITY) -> None:
#         self.boundary = boundary
#         self.southEast = None
#         self.southWest = None
#         self.northEast = None
#         self.northWest = None
#
#         self.capacity = capacity
#         self.divided = False
#         self.points = []
#
#     def count(self):
#         cnt = len(self.points)
#         if not self.divided:
#             return cnt
#         else:
#             cnt += self.northEast.count()
#             cnt += self.northWest.count()
#             cnt += self.southEast.count()
#             cnt += self.southWest.count()
#         return cnt
#
#     def insert(self, point):
#         if not self.boundary.collidepoint(point.x, point.y):
#             return False
#
#         if len(self.points) < self.capacity:
#             self.points.append(point)
#             return True
#         else:
#             if not self.divided:
#                 self.subdivide()
#
#             if self.northEast.insert(point):
#                 return True
#             elif self.northWest.insert(point):
#                 return True
#             elif self.southEast.insert(point):
#                 return True
#             elif self.southWest.insert(point):
#                 return True
#
#     def remove(self, point):
#         if not self.boundary.collidepoint(point.x, point.y):
#             return False
#
#         for i, p in enumerate(self.points):
#             if p is point:
#                 self.points.pop(i)
#                 self.check_collapse()
#                 return True
#
#         if self.divided:
#             removed = any([
#                 self.northWest.remove(point),
#                 self.northEast.remove(point),
#                 self.southWest.remove(point),
#                 self.southEast.remove(point)
#                 ])
#             if removed:
#                 self.check_collapse()
#             return removed
#
#         return False
#
#     def clear(self):
#         self.points = []
#         if self.divided:
#             self.northEast.clear()
#             self.northWest.clear()
#             self.southEast.clear()
#             self.southWest.clear()
#
#     def query(self, area: Rect):
#         found = []
#         if not self.boundary.colliderect(area):
#             return found
#
#         for p in self.points:
#             if area.collidepoint(p.x, p.y):
#                 found.append(p)
#
#         if self.divided:
#             found.extend(self.northWest.query(area))
#             found.extend(self.northEast.query(area))
#             found.extend(self.southWest.query(area))
#             found.extend(self.southEast.query(area))
#
#         return found
#
#     def subdivide(self):
#         x = self.boundary.x
#         y = self.boundary.y
#         w = self.boundary.width
#         h = self.boundary.height
#
#         nw = Rect(x, y, w / 2, h / 2)
#         ne = Rect(x + w / 2, y, w / 2, h / 2)
#         sw = Rect(x, y + h / 2, w / 2, h / 2)
#         se = Rect(x + w / 2, y + h / 2, w / 2, h / 2)
#
#         self.northWest = QuadTree(boundary=nw, capacity=self.capacity)
#         self.northEast = QuadTree(boundary=ne, capacity=self.capacity)
#         self.southWest = QuadTree(boundary=sw, capacity=self.capacity)
#         self.southEast = QuadTree(boundary=se, capacity=self.capacity)
#
#         self.divided = True
#
#     def check_collapse(self):
#         if self.divided:
#             total_points = len(self.points) + sum(
#                     child.count() for child in [self.northWest, self.northEast, self.southWest, self.southEast])
#             if total_points <= self.capacity:
#                 self.collapse()
#
#     def collapse(self):
#         if self.divided:
#             for child in [self.northWest, self.northEast, self.southWest, self.southEast]:
#                 self.points.extend(child.points)
#             self.northWest = self.northEast = self.southWest = self.southEast = None
#             self.divided = False