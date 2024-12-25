import math
import random

import pygame
from pygame import gfxdraw

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import PanZoomHandler
from source.handlers.position_handler import rot_center, wraparound
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import scale_image_cached
# from source.test.sprite_test import PanZoomSpriteBase
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_gif import PanZoomSprite
from database.config.universe_config import LEFT_END, RIGHT_END, TOP_END, BOTTOM_END


class CelestialObject(PanZoomSprite):
    """
    Represents a celestial object in the game universe.

    This class extends PanZoomSprite to create celestial objects with additional
    features such as rotation and size adjustment.

    Attributes:
        max_size (int): The maximum size of the celestial object.
        initial_rotation (float): The initial rotation angle of the object.
        rotation (float): The current rotation angle of the object.
        rotated_image (pygame.Surface): The rotated image of the object.
        rotated_rect (pygame.Rect): The rectangle of the rotated image.
    """

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
            image_name: str, **kwargs
            ) -> None:
        """
        Initialize a CelestialObject.

        Args:
            win (pygame.Surface): The window surface to draw on.
            x (int): The x-coordinate of the object.
            y (int): The y-coordinate of the object.
            width (int): The width of the object.
            height (int): The height of the object.
            pan_zoom (PanZoomHandler): The pan and zoom handler.
            image_name (str): The name of the image file for the object.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.max_size = None
        self.initial_rotation = kwargs.get("initial_rotation", None)
        self.type = kwargs.get("type", None)
        # rotate
        self.rotation_direction = kwargs.get("rotation_direction", random.choice([1, -1]))
        self.rotation_speed = kwargs.get("rotation_speed", random.uniform(0.1, 1.0))
        self.rotation = 0
        if self.initial_rotation:
            self.rotation = self.initial_rotation
            self.rotated_image, self.rotated_rect = rot_center(self.image, self.rotation, self.screen_x, self.screen_y)
            self.image_raw = self.rotated_image
            self.image = self.image_raw
            self.rect = self.rotated_rect

    def set_size(self) -> None:
        """
        Set the size of the celestial object.

        This method calculates and sets the size of the object based on its
        relative GIF size or scales it to fit its rectangle.
        """
        # Calculate the maximum size based on the relative GIF size
        if self.relative_gif_size:
            self.max_size = max(self.rect.width, self.rect.height) * self.relative_gif_size

            # Set the image rect according to its parent, including the size
            self.rect.width = self.max_size
            self.rect.height = self.max_size
            self.image = scale_image_cached(self.image_raw, (self.max_size, self.max_size))

        else:
            self.image = scale_image_cached(self.image_raw, (self.rect.width, self.rect.height))
            self.rect = self.image.get_rect()

    def draw(self) -> None:
        """
        Draw the celestial object on the window surface.

        This method handles the drawing of the object, including size adjustment
        and visibility checks.
        """
        if not level_of_detail.inside_screen(self.rect.center):
            return

        if not self._hidden:
            self.set_size()
            self.win.blit(self.image, self.rect)


class FlickeringStar(CelestialObject):
    """
    Represents a flickering star in the game universe.

    This class extends CelestialObject to create stars with a flickering effect.

    Attributes:
        colors (list): A list of random colors for the flickering effect.
        color_index (int): The current index in the colors list.
    """

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
            image_name: str, **kwargs
            ) -> None:
        """
        Initialize a FlickeringStar.

        Args:
            win (pygame.Surface): The window surface to draw on.
            x (int): The x-coordinate of the star.
            y (int): The y-coordinate of the star.
            width (int): The width of the star.
            height (int): The height of the star.
            pan_zoom (PanZoomHandler): The pan and zoom handler.
            image_name (str): The name of the image file for the star.
            **kwargs: Additional keyword arguments.
        """
        CelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        # colors
        # Generate a list of random colors
        self.colors = [(random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
                        random.randint(0, config.star_brightness)) for _ in range(10)]

        # Initialize the color index
        self.color_index = 0

    def draw(self) -> None:
        """
        Draw the flickering star on the window surface.

        This method handles the drawing of the star with a flickering effect
        by cycling through different colors.
        """
        if not level_of_detail.inside_screen(self.rect.center):
            return

        if not self._hidden:
            # Get the current color from the colors list
            color = self.colors[self.color_index]

            # Update the color index for the next iteration
            self.color_index = (self.color_index + 1) % len(self.colors)

            # Draw the flickering star using the current color
            pygame.draw.lines(self.win, color, True, [(self.rect.x + 1, self.rect.y),
                                                      (self.rect.x + 1, self.rect.y)])


class PulsatingStar(CelestialObject):
    """
    Represents a pulsating star in the game universe.

    This class extends CelestialObject to create stars with a pulsating effect.

    Attributes:
        start_pulse (float): The starting point of the pulse effect.
        pulse_time (float): The duration of one pulse cycle.
        pulsating_star_size (int): The size of the pulsating star.
        pulsating_star_color (tuple): The RGB color of the pulsating star.
    """

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
            image_name: str, **kwargs
            ):
        """
        Initialize a PulsatingStar.

        Args:
            win (pygame.Surface): The window surface to draw on.
            x (int): The x-coordinate of the star.
            y (int): The y-coordinate of the star.
            width (int): The width of the star.
            height (int): The height of the star.
            pan_zoom (PanZoomHandler): The pan and zoom handler.
            image_name (str): The name of the image file for the star.
            **kwargs: Additional keyword arguments.
        """
        CelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        # start pulse
        self.start_pulse = random.random()
        self.pulse_time = random.uniform(0.5, 3.0)
        self.pulsating_star_size = self.world_width  # random.randint(1, 3)
        self.pulsating_star_color = (
            random.randint(0, config.star_brightness), random.randint(0, config.star_brightness),
            random.randint(0, config.star_brightness))

    def draw(self) -> None:
        """
        Draw the pulsating star on the window surface.

        This method handles the drawing of the star with a pulsating effect
        by varying its size and brightness over time.
        """
        if not level_of_detail.inside_screen(self.rect.center):
            return

        if not self._hidden:
            t = pygame.time.get_ticks() % (self.pulse_time * 1000) / (self.pulse_time * 1000)
            c = int(config.star_brightness / 2 * max(0.5, 1 + math.cos(2 * math.pi * t)))
            gfxdraw.filled_circle(
                    self.win,
                    int(self.rect.x),
                    int(self.rect.y),
                    int(self.pulsating_star_size * self.get_zoom()),
                    (c, c, c))


class MovingCelestialObject(CelestialObject):
    """
    Represents a moving celestial object in the game universe.

    This class extends CelestialObject to create objects that can move and rotate.

    Attributes:
        speed (float): The speed of the object's movement.
        direction (tuple): The direction of the object's movement.
        rotation_direction (int): The direction of rotation (1 or -1).
        rotation_speed (float): The speed of rotation.
        enable_rotate (bool): Whether rotation is enabled for this object.
        rotation (float): The current rotation angle of the object.
    """

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
            image_name: str, **kwargs
            ) -> None:
        """
        Initialize a MovingCelestialObject.

        Args:
            win (pygame.Surface): The window surface to draw on.
            x (int): The x-coordinate of the object.
            y (int): The y-coordinate of the object.
            width (int): The width of the object.
            height (int): The height of the object.
            pan_zoom (PanZoomHandler): The pan and zoom handler.
            image_name (str): The name of the image file for the object.
            **kwargs: Additional keyword arguments.
        """
        CelestialObject.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        # moving
        self.speed = kwargs.get("speed", 0.5)
        self.direction = kwargs.get("direction", (
            random.uniform(-self.speed, self.speed), random.uniform(-self.speed, self.speed)))







    def move(self) -> None:
        """
        Move the celestial object.

        This method updates the object's position based on its speed and direction,
        and applies wraparound to keep it within the universe boundaries.
        """


        self.set_world_position(wraparound(
                self.world_x + self.direction[0] * time_handler.game_speed * self.speed,
                self.world_y + self.direction[1] * time_handler.game_speed * self.speed,
                LEFT_END, RIGHT_END, TOP_END, BOTTOM_END
                ))



    # def update_rect(self):
    #     if not self.image_raw:
    #         return
    #
    #     self.image = scale_image_cached(self.image_raw, (self.screen_width * self.shrink, self.screen_height * self.shrink))
    #     if self.enable_rotate:
    #         rotated_image, new_rect = rot_center(self.image, self.rotation, self.rect.x, self.rect.y)
    #         self.image = rotated_image
    #         self.rect = new_rect
    #         self.rotation += self.rotation_speed * self.rotation_direction
    #     else:
    #
    #         self.rect = self.image.get_rect()
    #
    #     self.align_image_rect()

    def draw(self) -> None:
        """
        Draw the moving celestial object on the window surface.

        This method handles the movement, rotation, and drawing of the object.
        """

        self.move()
        if not level_of_detail.inside_screen(self.rect.center):
            return

        if not self._hidden:


            # if not set align_image_rect, the rect is not correct, if set the rotation does not rotate around the center ????
            # self.align_image_rect()
            self.win.blit(self.image, self.rect)
