from pygame import Rect

from source.qt_universe.model.qt_model_config.qt_config import QT_CAPACITY


class QuadTree:  # original
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

    # def insert(self, point):
    #     if len(self.points) < self.capacity:
    #         self.points.append(point)
    #         return True
    #     else:
    #         if not self.divided:
    #             self.subdivide()
    #
    #         return (self.northEast.insert(point) or
    #                 self.northWest.insert(point) or
    #                 self.southEast.insert(point) or
    #                 self.southWest.insert(point))

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

    def get_all_points(self):
        all_points = self.points.copy()
        if self.divided:
            all_points.extend(self.northEast.get_all_points())
            all_points.extend(self.northWest.get_all_points())
            all_points.extend(self.southEast.get_all_points())
            all_points.extend(self.southWest.get_all_points())
        return all_points

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


class QuadTree_:  # optimizied by perplexity, is slower
    __slots__ = ('boundary', 'children', 'capacity', 'divided', 'points', 'point_count')

    def __init__(self, boundary: Rect, capacity: int = QT_CAPACITY) -> None:
        self.boundary = boundary
        self.children = [None, None, None, None]  # NW, NE, SW, SE
        self.capacity = capacity
        self.divided = False
        self.points = set()
        self.point_count = 0

    def count(self):
        return self.point_count

    def insert(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        if len(self.points) < self.capacity:
            self.points.add(point)
            self.point_count += 1
            return True
        else:
            if not self.divided:
                self.subdivide()

            for i in range(4):
                if self.get_child(i).insert(point):
                    self.point_count += 1
                    return True

        return False

    def remove(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        if point in self.points:
            self.points.remove(point)
            self.point_count -= 1
            self.check_collapse()
            return True

        if self.divided:
            for i in range(4):
                if self.children[i] and self.children[i].remove(point):
                    self.point_count -= 1
                    self.check_collapse()
                    return True

        return False

    def clear(self):
        self.points.clear()
        self.point_count = 0
        if self.divided:
            for child in self.children:
                if child:
                    child.clear()
            self.children = [None, None, None, None]
            self.divided = False

    def query(self, area: Rect, found=None):
        if found is None:
            found = []
        if not self.boundary.colliderect(area):
            return found

        for p in self.points:
            if area.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            for child in self.children:
                if child:
                    child.query(area, found)

        return found

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.width / 2, self.boundary.height / 2

        self.children[0] = QuadTree(Rect(x, y, w, h), self.capacity)  # NW
        self.children[1] = QuadTree(Rect(x + w, y, w, h), self.capacity)  # NE
        self.children[2] = QuadTree(Rect(x, y + h, w, h), self.capacity)  # SW
        self.children[3] = QuadTree(Rect(x + w, y + h, w, h), self.capacity)  # SE

        self.divided = True

    def get_child(self, index):
        if not self.children[index]:
            x, y = self.boundary.x, self.boundary.y
            w, h = self.boundary.width / 2, self.boundary.height / 2
            if index == 0:  # NW
                new_boundary = Rect(x, y, w, h)
            elif index == 1:  # NE
                new_boundary = Rect(x + w, y, w, h)
            elif index == 2:  # SW
                new_boundary = Rect(x, y + h, w, h)
            else:  # SE
                new_boundary = Rect(x + w, y + h, w, h)
            self.children[index] = QuadTree(new_boundary, self.capacity)
        return self.children[index]

    def check_collapse(self):
        if self.divided and self.point_count <= self.capacity:
            self.collapse()

    def collapse(self):
        if self.divided:
            for child in self.children:
                if child:
                    self.points.update(child.points)
            self.children = [None, None, None, None]
            self.divided = False


class QuadTree__:  # about the same speed, i dont thrust the ai
    def __init__(self, boundary: Rect, capacity: int = QT_CAPACITY) -> None:
        self.boundary = boundary
        self.southEast = None
        self.southWest = None
        self.northEast = None
        self.northWest = None
        self.capacity = capacity
        self.divided = False
        self.points = []
        self.point_count = len(self.points)

    def count(self):
        return self.point_count

    def insert(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            self.point_count += 1
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northEast.insert(point):
                self.point_count += 1
                return True
            elif self.northWest.insert(point):
                self.point_count += 1
                return True
            elif self.southEast.insert(point):
                self.point_count += 1
                return True
            elif self.southWest.insert(point):
                self.point_count += 1
                return True

        return False

    def remove(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        for i, p in enumerate(self.points):
            if p is point:
                self.points.pop(i)
                self.point_count -= 1
                self.check_collapse()
                return True

        if self.divided:
            removed = (self.northWest.remove(point) or
                       self.northEast.remove(point) or
                       self.southWest.remove(point) or
                       self.southEast.remove(point))
            if removed:
                self.point_count -= 1
                self.check_collapse()
            return removed

        return False

    def clear(self):
        self.points.clear()
        self.point_count = 0
        if self.divided:
            self.northEast.clear()
            self.northWest.clear()
            self.southEast.clear()
            self.southWest.clear()
            self.divided = False

    def query(self, area: Rect, found=None):
        if found is None:
            found = []
        if not self.boundary.colliderect(area):
            return found

        for p in self.points:
            if area.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            self.northWest.query(area, found)
            self.northEast.query(area, found)
            self.southWest.query(area, found)
            self.southEast.query(area, found)

        return found

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.width / 2, self.boundary.height / 2

        self.northWest = QuadTree(Rect(x, y, w, h), self.capacity)
        self.northEast = QuadTree(Rect(x + w, y, w, h), self.capacity)
        self.southWest = QuadTree(Rect(x, y + h, w, h), self.capacity)
        self.southEast = QuadTree(Rect(x + w, y + h, w, h), self.capacity)

        self.divided = True

    def check_collapse(self):
        if self.divided and self.point_count <= self.capacity:
            self.collapse()

    def collapse(self):
        if self.divided:
            self.points.extend(self.northWest.points)
            self.points.extend(self.northEast.points)
            self.points.extend(self.southWest.points)
            self.points.extend(self.southEast.points)
            self.northWest = self.northEast = self.southWest = self.southEast = None
            self.divided = False
