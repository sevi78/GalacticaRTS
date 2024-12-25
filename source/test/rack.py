import pygame
from pygame.math import Vector2

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image


def create_rack(rect_: pygame.Rect, pivot: tuple, angle: int, points: dict, scale: float) -> dict:
    rect_center = Vector2(rect_.center)
    rotated_points = {}

    for key, point in points.items():
        scaled_point = Vector2(point) * scale
        global_point = scaled_point + rect_center
        rotated_point = (global_point - Vector2(pivot)).rotate(-angle) + Vector2(pivot)
        rotated_points[key] = (int(rotated_point.x), int(rotated_point.y))

    return rotated_points


def main():
    pygame.init()
    window = pygame.display.set_mode((400, 400))

    clock = pygame.time.Clock()

    orig_image = get_image("spaceship.png")
    angle = 0
    run = True

    while run:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        pan_zoom_handler.listen(events)

        window.fill(0)
        window_center = window.get_rect().center

        scaled_image = pygame.transform.scale(orig_image, (
            orig_image.get_width() * pan_zoom_handler.zoom, orig_image.get_height() * pan_zoom_handler.zoom))
        rotated_image = pygame.transform.rotate(scaled_image, angle)

        window.blit(rotated_image, rotated_image.get_rect(center=window_center))

        rect = rotated_image.get_rect(center=window_center)
        rack_points = create_rack(
                rect_=rect,
                pivot=window_center,
                angle=angle,
                points={
                    "a": (-10, 10),
                    "b": (10, 10),
                    "c": (10, -10),
                    "d": (-10, -10)
                    },
                scale=pan_zoom_handler.zoom
                )

        for point in rack_points.values():
            pygame.draw.circle(window, (255, 0, 0), point, 3)

        pygame.display.flip()

        angle += 1

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()


import pygame
from pygame.math import Vector2

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image

#
# class Rack:
#     """
#     Rack class:
#
#     Attributes:
#         rect: pygame.Rect
#         pivot: tuple
#         points: dict
#         rotated_points: dict
#         angle: int
#         scale: float
#         debug: bool
#
#     Methods:
#         update(self, angle: int, scale: float)
#         draw(self, surface)
#
#     Usage:
#         rack = Rack(rect, pivot, points)
#         rack.update(rect, pivot, scale, angle)
#         rack.draw(surface)
#
#     Note:
#         Rack is a class that represents a dictionary of points, for example a rack of weapons on a ship.
#         It takes in a rectangle, a pivot point, and a dictionary of points.
#         It has methods to update the rack's position and draw it on a surface.
#
#         The update method takes in a rectangle, a pivot point, a scale factor, and an angle.
#         It updates the rack's position by scaling and rotating the points around the pivot point.
#     """
#
#     def __init__(self, rect: pygame.Rect, pivot: tuple, points: dict) -> None:
#         """
#         Initializes a Rack object.
#
#         Args:
#             rect (pygame.Rect): The rectangle representing the rack.
#             pivot (tuple): The pivot point of the rack.
#             points (dict): A dictionary of points representing the rack.
#
#         Note:
#             This constructor creates a Rack object with the given rectangle, pivot point, and points.
#             It sets the attributes of the object to the given values.
#             The points are scaled and rotated around the pivot point.
#             The rotated points are stored in a dictionary.
#             The scale factor is set to 1.0 by default.
#             The angle is set to 0 by default.
#
#         """
#         self.rect = rect
#         self.pivot = Vector2(pivot)
#         self.points = points
#         self.rotated_points = {}
#         self.scaled_points = {}
#         self.global_points = {}
#         self.angle = 0
#         self.scale = 1.0
#
#         self.debug = True
#
#     def update_(self, rect: pygame.Rect, pivot: tuple, scale: float, angle: int) -> None:
#         """
#         Updates the rack's position by scaling and rotating the points around the pivot point.
#
#         Args:
#             rect (pygame.Rect): The rectangle representing the rack.
#             pivot (tuple): The pivot point of the rack.
#             scale (float): The scale factor of the rack.
#             angle (int): The angle of the rack.
#         """
#         self.rect = rect
#         self.angle = angle
#         self.scale = scale
#         self.pivot = pivot
#         self.rotated_points = \
#             {k: (Vector2(p) - self.pivot).rotate(-self.angle) * self.scale + self.pivot for k, p in self.points.items()}
#
#
#     def update(self, rect: pygame.Rect, pivot: tuple, scale: float, angle: int) -> None:
#         """
#         Updates the rack's position by scaling and rotating the points around the pivot point.
#
#         Args:
#             rect (pygame.Rect): The rectangle representing the rack.
#             pivot (tuple): The pivot point of the rack.
#             scale (float): The scale factor of the rack.
#             angle (int): The angle of the rack.
#         """
#         self.rect = rect
#         self.angle = angle
#         self.scale = scale
#         self.pivot = pivot
#         pos = Vector2(self.rect.topleft)
#         # pos = Vector2(self.rect.topleft)
#
#         # self.rotated_points = \
#         #     {k: (Vector2(p) - self.pivot - pos).rotate(-self.angle) * self.scale + self.pivot + pos for k, p in self.points.items()}
#
#         # self.rotated_points = \
#         #     {k: Vector2(p) +  self.pivot for k, p in self.points.items()}
#
#
#         self.rotated_points = self.points
#
#         print(f"self.rect: {self.rect}")
#         print(f"self.rect.center: {self.rect.center}")
#         print(f"self.pivot: {self.pivot}")
#         print(f"self.angle: {self.angle}")
#         print(f"self.scale: {self.scale}")
#
#
#         # for i in self.points:
#         #
#         #     print(f"self.points[{i}]: {self.points[i]}")
#
#         scaled_points = \
#             {k: (Vector2(p) +  pos )  for k, p in self.points.items()}
#
#         self.rotated_points = \
#             {k: (Vector2(p) - self.pivot) * self.scale for k, p in scaled_points.items()}
#
#     def get_rotated_points(self) -> dict:
#         """
#         Returns the dictionary of rotated points.
#         """
#         return self.rotated_points
#
#     def draw(self, surface) -> None:
#         """
#         Draws the rack on a surface if self.rotated_points is not empty and self.debug is True.
#         """
#         for point in self.rotated_points.values():
#             pygame.draw.circle(surface, (0, 255, 0), point, 5, 1)
#
#
# def main():
#     pygame.init()
#     window = pygame.display.set_mode((800,800), pygame.RESIZABLE)
#
#     clock = pygame.time.Clock()
#
#     x, y = 0,0
#     orig_image = get_image("spaceship.png")
#     orig_rect = orig_image.get_rect()
#     angle = 0
#     run = True
#
#     window_center = window.get_rect().center
#
#     rack = Rack(
#             rect=orig_rect,
#             pivot=orig_rect.center,
#             points={0: orig_rect.topleft, 1: orig_rect.topright, 2: orig_rect.bottomright, 3: orig_rect.bottomleft})
#
#     while run:
#         clock.tick(60)
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 run = False
#
#         pan_zoom_handler.listen(events)
#
#         window.fill(0)
#
#         scaled_image = pygame.transform.scale(orig_image, (
#             orig_image.get_width() * pan_zoom_handler.zoom, orig_image.get_height() * pan_zoom_handler.zoom))
#
#         rotated_image = pygame.transform.rotate(scaled_image, angle)
#         rot_rect = rotated_image.get_rect(center=(x,y))
#
#         window.blit(rotated_image, rot_rect)
#
#         rect = pygame.rect.Rect()
#         # rect.x = x
#         # rect.y = y
#         # rect.center = (x,y )
#         rack.update(rot_rect, rot_rect.center, pan_zoom_handler.zoom, angle)
#         rack.draw(window)
#
#         pygame.display.flip()
#
#         # angle += 1
#         x += 1
#         y += 1
#
#     pygame.quit()
#     exit()
#
#
# if __name__ == "__main__":
#     main()
