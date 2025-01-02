import math

import pygame

from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import scale_image_cached, get_image
from source.text.text_wrap import TextWrap

# Initialize Pygame
# pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SPECIAL_FONT_SIZE = 16
SPECIAL_TEXT_COLOR = "palegreen4"


# # Define the main window
# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Pygame App")

# Load the image
# from source.multimedia_library.images import get_image


class MovingImage(pygame.sprite.Sprite):
    """
    The MovingImage class is a subclass of the TextWrap class and represents a moving surface with text on it in a Pygame window.
    Example Usage
    # Create an instance of the MovingImage class
    moving_surface = MovingImage(win, 300, 700, 30, 30, get_image("food_25x25.png"),
        3, (0.1, -0.3), "2x", SPECIAL_TEXT_COLOR, "georgiaproblack", 3)
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((0, 0, 0))  # Fill the screen with black

        # Update and draw the moving surface
        moving_surface.update()
        moving_surface.draw(win)

        pygame.display.update()  # Update the display

    pygame.quit()
    Code Analysis
    Main functionalities
    The MovingImage class inherits from the TextWrap class and adds functionality for a moving surface with text.
    It updates the position and transparency of the surface based on elapsed time.
    It resets the position and transparency when the lifetime of the surface is reached.
    It draws the surface and wraps the text on it.

    Methods
    __init__(self, win, x, y, width, height, image, lifetime, velocity, text, text_color, fontname, loops): Initializes the MovingImage object with the given parameters.
    reset(self): Resets the position and transparency of the surface.
    update(self): Updates the position and transparency of the surface based on elapsed time.
    draw(self, surface): Draws the surface and wraps the text on it.

    Fields
    win: The Pygame window surface.
    start_x: The initial x-coordinate of the surface.
    start_y: The initial y-coordinate of the surface.
    world_x: The current x-coordinate of the surface.
    world_y: The current y-coordinate of the surface.
    world_width: The width of the surface.
    world_height: The height of the surface.
    image_raw: The original image of the surface.
    image: The scaled image of the surface.
    lifetime: The lifetime of the surface in seconds.
    velocity: The velocity of the surface as a tuple of x and y components.
    rect: The rectangle representing the position and size of the surface.
    text: The text to be displayed on the surface.
    text_color: The color of the text.
    font_size: The size of the font for the text.
    font: The font object for rendering the text.
    start_time: The time when the surface was created or reset.
    alpha: The transparency of the surface.
    loops: The number of times the surface should repeat its movement before disappearing.
    """

    def __init__(
            self,
            win: pygame.surface,
            x: int,
            y: int,
            width: int,
            height: int,
            image: pygame.surface,
            lifetime: int,
            velocity: tuple,
            text: str,
            text_color: tuple[int, int, int, int],
            fontname: str,
            loops: int,
            parent: pygame.rect.Rect = None,
            target: tuple[int, int] or None = None,
            ):
        pygame.sprite.Sprite.__init__(self)
        self.text_wrap = TextWrap()
        self.win = win
        self.start_x = x
        self.start_y = y
        self.world_x = 0
        self.world_y = 0
        self.world_width = width
        self.world_height = height
        self.image_raw = image
        self.image = scale_image_cached(self.image_raw, (width, height))
        self.lifetime = lifetime
        self.velocity = velocity

        self.text = text
        self.text_color = text_color
        self.font_size = SPECIAL_FONT_SIZE
        self.font = pygame.font.SysFont(fontname, self.font_size)
        self.start_time = time_handler.time
        self.alpha = 255
        self.loops = loops
        self.runs = 0
        self.parent = parent
        self.target = target
        self.rect = self.image.get_rect(topleft=self.parent.topleft if parent else (x, y))
        self._hidden = False
        sprite_groups.moving_images.add(self)

        assert isinstance(self.parent, (
            pygame.rect.Rect, type(None))), "parent must be a pygame.rect.Rect object or None"
        assert isinstance(self.target, (tuple, type(None))), "target must be a tuple of (x, y) coordinates or None"

    def reset(self):
        self.start_time = time_handler.time
        self.world_x = self.start_x
        self.world_y = self.start_y
        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)
        self.alpha = 255

    def update(self):
        if self.parent:
            self.start_x = self.parent.right
            self.start_y = self.parent.top

        # self.rect = self.image.get_rect(topleft=(self.start_x, self.start_y))

        # Calculate elapsed time
        elapsed_time = time_handler.time - self.start_time

        if elapsed_time < self.lifetime:
            # Check if the object has a target
            if self.target:
                # Calculate the direction vector to the target
                dir_x = self.target[0] - self.rect.x
                dir_y = self.target[1] - self.rect.y

                # Normalize the direction vector
                dir_length = math.sqrt(dir_x ** 2 + dir_y ** 2)
                if dir_length != 0:
                    dir_x /= dir_length
                    dir_y /= dir_length

                # Multiply the direction by the speed to get the velocity
                speed = 6  # Set the speed to whatever value you want
                self.velocity = (dir_x * speed, dir_y * speed)

            # Move the object
            self.world_x += self.velocity[0]
            self.world_y += self.velocity[1]
            self.rect.x = self.start_x + int(self.world_x)
            self.rect.y = self.start_y + int(self.world_y)

            # Adjust alpha based on the remaining lifetime
            self.alpha = (1 - elapsed_time / self.lifetime) * 255
            self.image.set_alpha(int(self.alpha))
        else:
            self.runs += 1
            if self.runs < self.loops:
                self.reset()
            else:
                if self in sprite_groups.moving_images.sprites():
                    sprite_groups.moving_images.sprites().remove(self)
                self.kill()
                del self
                return

        if self.target:
            dist = math.dist(self.rect.center, self.target)
            if dist < 20:
                if self in sprite_groups.moving_images.sprites():
                    sprite_groups.moving_images.sprites().remove(self)
                self.kill()
                del self
                return

        self.text_wrap.wrap_text(self.win, self.text, (int(self.rect.right - 10), int(self.rect.top - 40)), (
            250, 20), self.font,
                self.text_color, fade_out=True, alpha=self.alpha)


def add_moving_image(
        surface: pygame.surface,
        x: int,
        y: int,
        width: int,
        height: int,
        key: str,
        operand: str,
        value: float,
        velocity: tuple[float, float],
        lifetime: int,
        parent: pygame.rect.Rect,
        target: tuple[int, int] or None
        ):
    """
    Add a moving image to the given surface.

    :param surface: The surface to add the moving image to.
    :param x: The x position of the moving image.
    :param y: The y position of the moving image.
    :param width: The width of the moving image.
    :param height: The height of the moving image.
    :param key: The key of the moving image. this is used to select a resource image
    :param operand: The operand of the moving image.
    :param value: The value of the moving image.
    :param velocity: The velocity of the moving image.
    :param lifetime: The lifetime of the moving image.
    :param parent: The parent of the moving image. must be pygame rect
    :param target: The target of the moving image. must be pygame rect
    """
    if operand == "*":
        operand = "x"

    if key == "buildings_max":
        image_name = "building_icon.png"
    else:
        image_name = f"{key}_25x25.png"

    image = get_image(image_name)
    MovingImage(
            win=surface,
            x=x,
            y=y,
            width=width,
            height=height,
            image=image,
            lifetime=lifetime,
            velocity=velocity,
            text=f"{value}{operand}",
            text_color=pygame.color.THECOLORS[SPECIAL_TEXT_COLOR],
            fontname="georgiaproblack",
            loops=1,
            parent=parent,
            target=target)

    # def add_moving_image(self, key, operand, value, velocity, lifetime, width, height, parent, target):
    #     if operand == "*":
    #         operand = "x"
    #
    #     if key == "buildings_max":
    #         image_name = "building_icon.png"
    #     else:
    #         image_name = f"{key}_25x25.png"
    #
    #     image = get_image(image_name)
    #     MovingImage(
    #             self.win,
    #             self.get_screen_x(),
    #             self.get_screen_y(),
    #             width,
    #             height,
    #             image,
    #             lifetime,
    #             velocity,
    #             f" {value}{operand}", SPECIAL_TEXT_COLOR,
    #             "georgiaproblack", 1, parent, target=target)
# def draw_moving_image():
#
#     pass
#
#  def draw_moving_image(self, defender: object, power: int, velocity: tuple):
#         MovingImage(
#             self.parent.win,
#             defender.rect.top,
#             defender.rect.right,
#             18,
#             18,
#             get_image("energy_25x25.png"),
#             1,
#             velocity,
#             f"-{power}", pygame.color.THECOLORS["red"],
#             "georgiaproblack", 1, defender, target=None)
#
# def draw_moving_image(self, win, x, y, width,  defender, power):
#     MovingImage(
#         self.parent.win,
#         defender.rect.top,
#         defender.rect.right,
#         18,
#         18,
#         get_image("energy_25x25.png"),
#         1,
#         (random.randint(-1, 1), 2),
#         f"-{power}", pygame.color.THECOLORS["red"],
#         "georgiaproblack", 1, defender, target=None)

# def main():
#     # Create an instance of the MovingImage class
#     moving_surface = MovingImage(win, 300, 700, 30, 30, get_image("food_25x25.png"),
#         3, (0.1, -0.3), "2x", SPECIAL_TEXT_COLOR, "georgiaproblack", 3)
#     # Main loop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         win.fill((0, 0, 0))  # Fill the screen with black
#
#         # Update and draw the moving surface
#         moving_surface.update()
#         moving_surface.draw(win)
#         # print (moving_surface.__dict__)
#
#         pygame.display.update()  # Update the display
#
#     pygame.quit()
#
#
# if __name__ == "__main__":
#     main()
