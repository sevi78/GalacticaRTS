import pygame
from pygame import Vector2

from source.draw.cross import draw_cross_in_circle
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomImage
"""
TODO:
- proper error handling
"""

class Rack:
    def __init__(self, width, height, pivot: Vector2, points: list):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.pivot = Vector2(pivot)
        self.points_raw = points
        self.points = points
        self.scale = 1.0
        self.angle = 0

        self.debug = True

    def set_points(self, points):
        self.points_raw = points

    def add_point(self, point):
        self.points_raw.append(Vector2(point))

    def update(
            self, x=None, y=None, width=None, height=None, pivot=None, points=None, scale=None, angle=None
            ):
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.width = width if width is not None else self.width
        self.height = height if height is not None else self.height
        self.pivot = pivot if pivot is not None else self.pivot
        self.points = points if points is not None else self.points
        self.scale = scale if scale is not None else self.scale
        self.angle = angle if angle is not None else self.angle

        # update positions, width, height, rotation
        self.update_points()

    def update_points(self):  # working!!!
        self.points = []

        for point in self.points_raw:
            self.points.append(
                    ((int(point[0] * self.scale + self.x) - (self.width / 2)),
                     (int(point[1] * self.scale + self.y) - (self.height / 2))
                     )
                    )

        pts = [(Vector2(p) - self.pivot).rotate(-self.angle) + self.pivot for p in self.points]
        self.points = pts

    def draw(self, screen):
        # pivot
        draw_cross_in_circle(screen, (0, 0, 255), [int(self.pivot[0]), int(self.pivot[1])], 15)

        # points
        for point in self.points:
            draw_cross_in_circle(screen, (255, 0, 0), point, 15)


def create_rack(width, height, points):
    rack = Rack(
            width=width,
            height=height,
            pivot=(int(width / 2), int(height / 2)),
            points=points
            )
    return rack


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Create a PanZoomImage object for testing alongside RotRect
    ship = PanZoomImage(
            win=screen,
            world_x=200,
            world_y=200,
            world_width=50,
            world_height=50,
            layer=0,
            group=sprite_groups.universe,
            image_name="spaceship.png",
            image_alpha=None,
            rotation_angle=0,
            initial_rotation=True
            )

    points = [ship.rect_raw.center,
              ship.rect_raw.topleft,
              ship.rect_raw.topright,
              ship.rect_raw.bottomright,
              ship.rect_raw.bottomleft,
              ship.rect_raw.midleft,
              ship.rect_raw.midright,
              ship.rect_raw.midtop,
              ship.rect_raw.midbottom]

    rack = create_rack(ship.rect.width, ship.rect.height, points)

    angle = 0

    running = True
    while running:
        events = pygame.event.get()

        # Listen for pan/zoom events from pan_zoom_handler
        pan_zoom_handler.listen(events)

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        sprite_groups.universe.update()

        # Clear the screen with a white background
        screen.fill((255, 255, 255))

        rack.update(
                x=ship.rect.centerx,
                y=ship.rect.centery,
                width=ship.rect.width,
                height=ship.rect.height,
                pivot=ship.rect.center,
                angle=angle,
                scale=pan_zoom_handler.zoom
                )

        sprite_groups.universe.draw(screen)
        rack.draw(screen)
        pygame.display.flip()

        angle += 1
        if angle >= 360:
            angle = 0

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
