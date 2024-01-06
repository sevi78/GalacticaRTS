import math

import pygame
import time

from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.text.text_wrap import TextWrap
from source.handlers.position_handler import get_distance

# Initialize Pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SPECIAL_FONT_SIZE = 16
SPECIAL_TEXT_COLOR = "palegreen4"

# # Define the main window
# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Pygame App")

# Load the image
#from source.multimedia_library.images import get_image


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
    def __init__(self, win, x, y, width, height, image, lifetime, velocity, text, text_color, fontname, loops, parent, **kwargs):
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
        self.image = pygame.transform.scale(self.image_raw, (width, height))
        self.lifetime = lifetime
        self.velocity = velocity
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.text_color = text_color
        self.font_size = SPECIAL_FONT_SIZE
        self.font = pygame.font.SysFont(fontname, self.font_size)
        self.start_time = time.time()
        self.alpha = 255
        self.loops = loops
        self.runs = 0
        self.parent = parent
        self.target = kwargs.get("target", None)
        self._hidden = False
        sprite_groups.moving_images.add(self)

    def reset(self):
        self.start_time = time.time()
        self.world_x = self.start_x
        self.world_y = self.start_y
        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)
        self.alpha = 255

    def update(self):
        if hasattr(self.parent, "rect"):
            self.start_x = self.parent.rect.right
            self.start_y = self.parent.rect.top
        else:
            self.start_x = self.parent[0]
            self.start_y = self.parent[1]

            # Calculate elapsed time
        elapsed_time = time.time() - self.start_time

        if elapsed_time < self.lifetime:
            # Check if the object has a target
            if self.target is not None:
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
            dist = get_distance(self.rect.center, self.target)
            if dist < 20:
                if self in sprite_groups.moving_images.sprites():
                    sprite_groups.moving_images.sprites().remove(self)
                self.kill()
                del self
                return
        self.draw(self.win)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.text_wrap.wrap_text(self.win, self.text, (self.rect.right - 10, self.rect.top - 40), (250, 20), self.font,
            self.text_color, fade_out=True, alpha=self.alpha)


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
