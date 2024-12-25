import copy
import math
import random
import sys
import time

import pygame
from pygame.math import Vector2

from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image, scale_image_cached, rotate_image_cached, get_gif_frames, \
    get_gif_fps, get_gif_duration
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomSpriteBase, PanZoomImage
from source.pan_zoom_sprites.pan_zoom_stars.pan_zoom_stars import PanZoomFlickeringStar, PanZoomPulsatingStar


class PanZoomLayeredUpdates(pygame.sprite.LayeredUpdates):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.inside_screen:
                if spr.image:
                    self.spritedict[spr] = surface_blit(spr.image, spr.rect)
                else:
                    spr.draw()
            if spr.debug:
                spr.debug_object()
        self.lostsprites = []


class PanZoomSpriteBase__(pygame.sprite.Sprite):
    """
    A sprite class that supports pan and zoom functionality, as well as GIF animations and rotations.

    This class extends pygame.sprite.Sprite and provides additional features:
    - Handling of both static images (.png) and animated GIFs
    - Support for world coordinates and screen coordinates
    - Automatic scaling based on zoom level
    - Rotation of sprites
    - Movement in a specified direction
    - GIF animation with looping and timing controls
    - Debug visualization options

    The sprite can be updated and drawn on a pygame surface, with its appearance and position
    adjusting dynamically based on the current pan and zoom settings.
    """
    __slots__ = (
        'win', 'world_x', 'world_y', 'world_width', 'world_height', 'image_name', 'image_raw', 'image', 'rect',
        'image_alpha', 'gif_frames', 'gif_fps', 'gif_animation_time', 'gif_index', 'loop_gif',
        'kill_after_gif_loop', 'gif_start', 'angle', 'rotation_angle', 'rotation_speed',
        'movement_speed',
        'direction', 'inside_screen', 'debug'
        )

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            image_name: str,
            image_alpha: int = None,
            gif_index: int = 1,
            loop_gif: bool = True,
            kill_after_gif_loop: bool = False,
            gif_animation_time: float = None,
            rotation_angle: float = 0.0,
            rotation_speed: float = 0.0,
            movement_speed: float = 0.0,
            direction: Vector2 = Vector2(0.0, 0.0),
            layer: int = 0,
            group: PanZoomLayeredUpdates = None
            ):
        """
        Initializes a PanZoomSprite instance.

        :param win: The window surface to draw the sprite on.
        :param world_x: The initial x-coordinate in the world.
        :param world_y: The initial y-coordinate in the world.
        :param world_width: The width of the sprite in the world.
        :param world_height: The height of the sprite in the world.
        :param image_name: The name of the image file.
        :param image_alpha: The alpha value for the image. Defaults to None.
        :param gif_index: The index of the current frame in the GIF animation. Defaults to 1.
        :param loop_gif: Whether to loop the GIF animation. Defaults to True.
        :param kill_after_gif_loop: Whether to kill the sprite after the GIF animation loop. Defaults to False.
        :param gif_animation_time: The duration of the GIF animation in seconds. Defaults to None.
        :param rotation_angle: The rotation angle in degrees. Defaults to 0.0. set this for initial rotation
        :param rotation_speed: The speed at which the sprite rotates. Defaults to 0.0. -> no rotation
        :param movement_speed: The speed at which the sprite moves. Defaults to 0.0. -> no movement
        :param direction: A tuple representing the movement direction as (dx, dy). Defaults to (0.0, 0.0) -> no movement.
        """
        # super init
        super().__init__()
        self._layer = layer

        # thw window to draw to
        self.win = win

        # image init
        self.image_name = image_name
        self.image = None
        self.image_raw = None
        self.image_alpha = image_alpha

        # gif init
        self.gif_frames = None
        self.gif_fps = None
        self.gif_animation_time = gif_animation_time
        self.gif_index = gif_index
        self.loop_gif = loop_gif
        self.kill_after_gif_loop = kill_after_gif_loop
        self.gif_start = time.time()

        # rect init
        self.rect = None

        # check if image is png or gif ant initialize the image/gif
        if self.image_name:
            if self.image_name.endswith(".png"):
                self.image_raw = get_image(self.image_name)
                self.image = copy.copy(self.image_raw)

            elif self.image_name.endswith(".gif"):
                self.gif_frames = get_gif_frames(self.image_name)
                self.gif_fps = get_gif_fps(self.image_name)

                # if gif_animation_time is not set, use the duration of the first frame
                self.gif_animation_time = get_gif_duration(self.image_name) / 1000 if not self.gif_animation_time else self.gif_animation_time
                self.image_raw = self.gif_frames[1]
                self.image = copy.copy(self.image_raw)

            if self.image_alpha:
                self.image_raw.set_alpha(self.image_alpha)
                self.image.set_alpha(self.image_alpha)

            self.rect = self.image.get_rect()
            self.update_rect(center=self.rect.center)

        # world position
        self.world_x = world_x
        self.world_y = world_y

        # world_size
        self.world_width = world_width
        self.world_height = world_height

        # rotation
        self.rotation_speed = rotation_speed
        self.rotation_angle = rotation_angle

        # movement
        self.movement_speed = movement_speed
        self.direction = direction

        # lod
        self.inside_screen = False

        # debug
        self.debug = False

        # group
        group.add(self)

    def move(self, delta: Vector2) -> None:
        """
        Moves the sprite by the specified delta vector.
        :param delta: The change in position as a Vector2.
        """
        self.world_x += delta.x
        self.world_y += delta.y

    def update_gif_index(self):
        """
        updates gif index, sets new image frame
        """
        if not self.gif_frames:
            return
        # update gif index and image
        current_time = time.time()
        if current_time > self.gif_start + self.gif_animation_time:
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.image_raw = self.gif_frames[self.gif_index]
            self.gif_start = current_time

            # kill sprite after gif loop
            if self.gif_index == 0 and not self.loop_gif:
                if self.kill_after_gif_loop:
                    self.kill()
                return

    def update_rect(self, center: tuple[float, float]) -> None:
        """Updates the rect based on the current image size and center position."""
        self.rect = self.image.get_rect(center=center)

    def apply_transform(self) -> None:
        """
        Applies scaling and rotation transformations to the sprite's image.
        This method updates the sprite's image based on its current zoom level and rotation angle.
        """

        scaled_width = self.world_width * pan_zoom_handler.zoom
        scaled_height = self.world_height * pan_zoom_handler.zoom

        # Scale and rotate the image accordingly
        scaled_image = scale_image_cached(self.image_raw, (scaled_width, scaled_height))

        # Rotate the scaled image to get the final image for rendering
        # TODO: make shure ist not rotated if the rotation is not changed for initial rotation
        self.image = rotate_image_cached(scaled_image, self.rotation_angle)

        # Update rect based on new image size while keeping its center position
        self.update_rect(center=(self.world_x, self.world_y))

    def set_world_position(self, position: tuple[float, float]) -> None:
        """
        Sets the world position of the sprite and updates its screen position and the rect center.

        :param position: A tuple containing the new (world_x, world_y) coordinates.
        """
        self.world_x, self.world_y = position

        # Convert world coordinates to screen coordinates
        screen_x, screen_y = pan_zoom_handler.world_2_screen(self.world_x, self.world_y)

        # Update rect center based on screen coordinates
        self.update_rect(center=(screen_x, screen_y))

    def debug_object(self):
        """
        Draws a debug rectangle around the sprite and displays text for all attributes.
        The rectangle color is blue if the sprite is inside the screen, green otherwise.
        """
        rect_color = (0, 0, 255) if self.inside_screen else (0, 255, 0)
        pygame.draw.rect(self.win, rect_color, self.rect.inflate(2, 2), 2)  # Draw border rectangle

        fontsize = 15
        font = pygame.font.Font(None, fontsize)  # You might want to store this as a class attribute for efficiency
        y_offset = 0
        for attr, value in self.__dict__.items():
            if attr.startswith('__'):  # Skip private attributes
                continue
            text = f"{attr}: {value}"
            text_surface = font.render(text, True, (255, 255, 255))  # White text
            self.win.blit(text_surface, (self.rect.x, self.rect.y + y_offset))
            y_offset += fontsize  # Move down for next line of text

        # Handle attributes defined in __slots__ but not in __dict__
        for attr in self.__slots__:
            if not hasattr(self, attr):
                continue
            if attr in self.__dict__:
                continue  # Already handled above
            value = getattr(self, attr)
            text = f"{attr}: {value}"
            text_surface = font.render(text, True, (255, 255, 255))  # White text
            self.win.blit(text_surface, (self.rect.x, self.rect.y + y_offset))
            y_offset += fontsize  # Move down for next line of text

    def update(self) -> None:
        """
        Updates the sprite's position and rotation based on its current direction.
        This method is called every frame to update the sprite's state.
        """
        # check if sprite is inside screen bounds
        self.inside_screen = level_of_detail.inside_screen(self.rect.center)

        # Move the sprite in the current direction
        self.move(self.direction * self.movement_speed)

        # Rotate and scale only if on screen
        if self.inside_screen:
            self.update_gif_index()
            # update rotation angle
            self.rotation_angle = self.rotation_angle + self.rotation_speed
            self.apply_transform()

        # Set the world position based on updated coordinates, this must be last !
        self.set_world_position((self.world_x, self.world_y))


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display dimensions and create a window
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PanZoomSprite Demo")

    # Create sprite group for managing all sprites together
    all_sprites = PanZoomLayeredUpdates()



    # create reference sprite
    reference_image_name = "galaxy_2.png"
    reference_sprite = PanZoomSpriteBase(
            win=screen,
            world_x=WIDTH // 2,
            world_y=HEIGHT // 2,
            world_width=300,
            world_height=300,
            # image_name=reference_image_name,
            # image_alpha=50,
            # gif_index=1,
            # loop_gif=True,
            # kill_after_gif_loop=False,
            # gif_animation_time=None,
            # rotation_angle=0.0,
            # rotation_speed=0.1,
            # movement_speed=0,
            # direction=Vector2(0.0, 0.0),
            layer=0,
            group=all_sprites)

    # create reference sprite
    ship_name = "spaceship.png"
    ship = PanZoomSpriteBase(
            win=screen,
            world_x=WIDTH // 2,
            world_y=HEIGHT // 2,
            world_width=30,
            world_height=30,
            # image_name=ship_name,
            # image_alpha=None,
            # gif_index=1,
            # loop_gif=True,
            # kill_after_gif_loop=False,
            # gif_animation_time=None,
            # rotation_angle=100.0,
            # rotation_speed=0.0,
            # movement_speed=0,
            # direction=Vector2(0.0, 0.0),
            layer=1,
            group=all_sprites)

    # Create sprites with initial direction for circular movement
    sprite_image_name = "asteroid.gif"
    image = get_image(sprite_image_name)

    w = int(image.get_rect().width / 3)
    h = int(image.get_rect().height / 3)

    sprite = PanZoomSpriteBase(
            win=screen,
            world_x=WIDTH // 2,
            world_y=HEIGHT // 2,
            world_width=w,
            world_height=h,
            # image_name=sprite_image_name,
            # image_alpha=None,
            # gif_index=1,
            # loop_gif=True,
            # kill_after_gif_loop=False,
            # gif_animation_time=None,
            # rotation_angle=0.0,
            # rotation_speed=0,
            # movement_speed=2,
            # direction=Vector2(1.0, 0.0),
            layer=2,
            group=all_sprites)

    # create stars
    # flickering star
    for i in range(200):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        base = PanZoomFlickeringStar(
                win=screen,
                world_x=x,
                world_y=y,
                world_width=10,
                world_height=10,
                layer=0,
                group=all_sprites)

    # pulsating star
    for i in range(200):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        base = PanZoomPulsatingStar(
                win=screen,
                world_x=x,
                world_y=y,
                world_width=3,
                world_height=3,
                layer=0,
                group=all_sprites)

    # pan zoom image
    for i in range(10):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        r = random.randint(0, 360)
        base = PanZoomImage(
                win=screen,
                world_x=x,
                world_y=y,
                world_width=200,
                world_height=200,
                layer=0,
                group=all_sprites,
                image_name="galaxy_2.png",
                image_alpha=50,
                rotation_angle=r
                )


    # Initialize font for displaying FPS
    font = pygame.font.Font(None, 36)  # Default font with size 36
    # Main game loop to run until quit event occurs
    clock = pygame.time.Clock()
    running = True
    angle_increment = 0.02
    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Adjust direction for circular movement by calculating new angle using cosine/sine functions
        angle_increment += 0.02
        sprite.direction = Vector2(math.cos(angle_increment), math.sin(angle_increment))

        # Update all sprites in the group based on their logic defined in update method
        all_sprites.update()

        # Clear screen with black background before drawing new frame
        screen.fill((0, 0, 0))

        # Draw each sprite onto the screen using their draw method
        all_sprites.draw(screen)

        # Draw debugging rect for level of detail if needed
        level_of_detail.draw_debug_rect()

        # Calculate and display FPS in upper left corner of screen
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))  # Positioning text at top-left corner

        # Update display with drawn content for this frame
        pygame.display.update()

        # Cap frame rate to control game speed and performance consistency
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
