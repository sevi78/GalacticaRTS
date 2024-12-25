import pygame
from pygame.math import Vector2

from source.draw.cross import draw_cross_in_circle
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomImage
from source.pan_zoom_sprites.rack import Rack


class RotRect(Rack):
    def __init__(self, rect: pygame.Rect):
        super().__init__(
                width=rect.width,
                height=rect.height,
                pivot=Vector2(rect.center),
                points=[
                    Vector2(rect.topleft),
                    Vector2(rect.bottomleft),
                    Vector2(rect.topright),
                    Vector2(rect.bottomright),
                    Vector2(rect.midtop),
                    Vector2(rect.midleft),
                    Vector2(rect.midbottom),
                    Vector2(rect.midright),
                    Vector2(rect.center),
                    ]
                )
        self._rect = rect
        self.angle = 0

        self.point_names = {
            0: "topleft",
            1: "bottomleft",
            2: "topright",
            3: "bottomright",
            4: "midtop",
            5: "midleft",
            6: "midbottom",
            7: "midright",
            8: "center"
            }

        self._generate_properties()

    def _generate_properties(self):
        for index, name in self.point_names.items():
            if name != "center":  # Skip center as it's handled separately
                setattr(RotRect, name, property(lambda self, i=index: self.points[i]))

    @property
    def center(self) -> Vector2:
        """Get the center point of the rectangle."""
        return Vector2(self.pivot)

    @center.setter
    def center(self, value: Vector2):
        """Set the center point of the rectangle."""
        self.pivot = value
        self._rect.center = value
        self.update()

    def add_point(self, point: Vector2, point_name: str):
        self.points.append(Vector2(point))
        index = len(self.points) - 1
        self.point_names[index] = point_name

        # Dynamically create a property for the new point
        setattr(RotRect, point_name, property(lambda self, i=index: self.points[i]))

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        # No need to update properties here as they are dynamically accessed

    def draw(self, screen: pygame.Surface):
        # Draw pivot point (blue)
        draw_cross_in_circle(screen, (0, 0, 255), [int(self.pivot.x), int(self.pivot.y)], 15)

        # Font for labeling points
        font = pygame.font.Font(None, 14)

        # Draw and label each point
        for i, point in enumerate(self.points):
            if i == 8:  # Skip center point (already drawn as pivot)
                continue

            # Determine color based on point type
            color = pygame.color.THECOLORS["green"] if i < 4 else pygame.color.THECOLORS["orange"]

            # Draw point
            draw_cross_in_circle(screen, color, point.xy, 5)

            # Render and draw point label
            label = self.point_names.get(i, f"no name({i})")
            text_str = f"{label}({i})"

            text = font.render(text_str, True, colors.frame_color)
            text_rect = text.get_rect(center=(point.x, point.y + 15))
            screen.blit(text, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # sprt_grp = LayeredDirty()

    # Create a PanZoomImage object for testing alongside RotRect
    ship = PanZoomImage(
            win=screen,
            world_x=200,
            world_y=200,
            world_width=30,
            world_height=30,
            layer=0,
            group=None,
            image_name="spaceship.png",
            image_alpha=None,
            rotation_angle=0,
            initial_rotation=True
            )

    rack = RotRect(ship.rect_raw)

    angle = 0

    running = True
    while running:
        events = pygame.event.get()

        # Listen for pan/zoom events from pan_zoom_handler
        pan_zoom_handler.listen(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.visible = not ship.visible
            if event.type == pygame.QUIT:
                running = False

        # sprt_grp.update()

        # Clear the screen with a white background
        screen.fill((255, 255, 255))

        ship.set_rotation_angle(angle)
        rack.update(
                x=ship.rect.centerx,
                y=ship.rect.centery,
                width=ship.world_width * pan_zoom_handler.zoom,
                height=ship.world_height * pan_zoom_handler.zoom,
                pivot=Vector2(ship.rect.center),
                angle=angle,
                scale=pan_zoom_handler.zoom
                )

        # sprt_grp.draw(screen)
        rack.draw(screen)
        ship.update()
        ship.draw()
        pygame.display.update()

        angle += 1
        if angle >= 360:
            angle = 0

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
