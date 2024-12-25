import copy
import math
import sys
import time

import pygame
from pygame import Vector2, Rect

from database.config.universe_config import WORLD_RECT
from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, scale_image_cached, rotate_image_cached, get_gif_duration, \
    get_gif_frames, get_gif_fps

"""
WARNING!!!!!
never store the screen position, otherwise position will not be accurate!!!

"""

"""
TODO: 
-   check if really all functoin calls only been done if neccesary, such as rotating and sclaing ect 
-   adjust sizes of asteroids ect
-   find ut the maximum size that is not impacting the performance too much: create simple test app with one Image
    rotating and scaling
-   implement game_speed
-   add doc strings, comments
-   implement proper slots
- add a docstring here that explains the usage of all classes

"""


# all_sprites = sprite_groups.universe


class PanZoomSpriteBase(pygame.sprite.Sprite):
    """
            the base class for pan_zoom_sprites:
            attributes:
            -   the world rect, boundaries of the universe
            -   the win surface
            -   the world x, y, width and height


            win,
            world_x,
            world_y,
            world_width,
            world_height,
            layer=0,
            group=all_sprites

            """
    # optimized
    __slots__ = (
        '_layer', 'win', 'world_x', 'world_y', 'world_width', 'world_height',
        'inside_screen', 'debug', 'last_zoom', 'last_world_offset_x', 'last_world_offset_y',
        'rect', 'screen_position_changed'
        )

    def __init__(
            self,
            win,
            world_x,
            world_y,
            world_width,
            world_height,
            layer=0,
            group=None
            ):

        super().__init__()
        # the world rect, boundaries of the universe
        self.world_rect = WORLD_RECT

        self.win = win
        self.world_x = world_x
        self.world_y = world_y
        self.world_width = world_width
        self.world_height = world_height
        self._layer = layer
        self.rect = pygame.Rect(world_x, world_y, world_width, world_height)
        self.inside_screen = False
        self.debug = False
        self.screen_position_changed = True
        self.last_zoom = pan_zoom_handler.zoom
        self.last_world_offset_x = pan_zoom_handler.world_offset_x
        self.last_world_offset_y = pan_zoom_handler.world_offset_y
        self.visible = True
        # if group is None:
        #     group = all_sprites
        if group is not None:
            group.add(self)

    def _pan_zoom_changed(self):
        """
        this checks if the pan_zoom_handler has changed and then updates the screen position
        """
        changed = (self.last_zoom != pan_zoom_handler.zoom or
                   self.last_world_offset_x != pan_zoom_handler.world_offset_x or
                   self.last_world_offset_y != pan_zoom_handler.world_offset_y)
        if changed:
            # print(f"""_pan_zoom_changed: zoom: {pan_zoom_handler.zoom}, world_offset_x: {pan_zoom_handler.world_offset_x}, world_offset_y: {pan_zoom_handler.world_offset_y}""")
            self.last_zoom = pan_zoom_handler.zoom
            self.last_world_offset_x = pan_zoom_handler.world_offset_x
            self.last_world_offset_y = pan_zoom_handler.world_offset_y
        return changed

    def update(self):
        if self.screen_position_changed or self._pan_zoom_changed():
            self._update_screen_position()
            self.screen_position_changed = False

            self.inside_screen = level_of_detail.inside_screen(self.rect.center)

        self.additional_update_tasks()

    def additional_update_tasks(self):
        """
        this function is called after the screen position has been updated, use this for any oter update tasks to be done
        """
        pass

    # remove this after testing !!!
    def draw(self):
        pass

    def set_position(self, world_x, world_y):
        """
        set the position of the sprite, always use this function to set the world_position, because this then
        sets screen_position_changed to true, which then updates the screen position
        """
        self.world_x = world_x
        self.world_y = world_y
        self.screen_position_changed = True

    def _update_screen_position(self) -> tuple[float, float]:
        """
        this function updates the screen position of the sprite
        """

        # print (f"""update_screen_position: world_x: {self.world_x}, world_y: {self.world_y}, world_width: {self.world_width}, world_height: {self.world_height}""")
        screen_x, screen_y = pan_zoom_handler.world_2_screen(self.world_x, self.world_y)
        screen_width = self.world_width * pan_zoom_handler.zoom
        screen_height = self.world_height * pan_zoom_handler.zoom
        self.rect.center = (screen_x, screen_y)
        self.rect.size = (screen_width, screen_height)

        return screen_width, screen_height

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
            self.win.blit(text_surface, (self.rect.x, self.rect.y - y_offset))
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
            self.win.blit(text_surface, (self.rect.x, self.rect.bottom + y_offset))
            y_offset += fontsize  # Move down for next line of text


    def __delete__(self, instance):
        self.kill()


class PanZoomImage(PanZoomSpriteBase):
    """
    this is the base class for all images:

    it has the following attributes:
    image_name: the name of the image
    image_raw: the raw image
    image: the image
    image_alpha: the alpha value of the image
    rotation_angle: the rotation angle of the image
    initial_rotation: the initial rotation angle of the image

    it has the following methods:
    apply_transform: applies scaling and rotation transformations to the sprite's image
    rotation_angle_changed: checks if the rotation angle has changed
    set_rotation_angle: sets the rotation angle
    rotate: rotates the image
    set_image: sets the image
    draw: draws the image
    update: updates the image
    debug_object: draws a debug rectangle around the image

    :kwarg align_image: alignment of the image:

        -top, left, bottom, right
        -topleft, bottomleft, topright, bottomright
        -midtop, midleft, midbottom, midright



    """

    # __slots__ = (
    #     'image_name',
    #     'image_raw',
    #     'image',
    #     'image_alpha',
    #     'rotation_angle',
    #     '_last_rotation_angle',
    #     'initial_rotation',
    #     'debug'
    #     )

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group=None,
            image_name: str = "no_image.png",
            image_alpha: int = None,
            rotation_angle: int = 0,
            initial_rotation: int = 0,
            **kwargs
            ) -> None:
        super().__init__( win, world_x, world_y, world_width, world_height, layer, group)

        # image init
        self.image_name = image_name
        self.image_raw = get_image(self.image_name)
        self.image = copy.copy(self.image_raw)
        self.image_alpha = image_alpha
        self.rotation_angle = rotation_angle
        self._last_rotation_angle = 0
        self.ignore_rotation_angle_changed = True
        self.initial_rotation = initial_rotation
        self.debug = False
        self.visible = True

        if self.image_alpha:
            self.image_raw.set_alpha(self.image_alpha)
            self.image.set_alpha(self.image_alpha)

        self.align_image = kwargs.get("align_image", "center")

        # set the rw rect for later use for racks
        self.rect_raw = self.image_raw.get_rect(centerx=self.world_width / 2, centery=self.world_width / 2)
        self.scaled_rect = self.rect_raw
        # self.rect_unrotated = self.rect_raw

        # apply transform
        self.apply_transform(self.world_width, self.world_height)

    def rotation_angle_changed(self) -> bool:
        return self.rotation_angle != self._last_rotation_angle

    def set_rotation_angle(self, rotation_angle):
        self.rotation_angle = rotation_angle % 360
        self.screen_position_changed = True

    def apply_transform(self, screen_width: float, screen_height: float) -> None:
        """
        Applies scaling and rotation transformations to the sprite's image.
        This method updates the sprite's image based on its current zoom level and rotation angle.
        """
        # Scale and rotate the image accordingly
        scaled_image = scale_image_cached(self.image_raw, (screen_width, screen_height))

        # set the scaled rect
        self.scaled_rect = scaled_image.get_rect(**{self.align_image: pan_zoom_handler.world_2_screen(self.world_x, self.world_y)})

        # Rotate the scaled image to get the final image for rendering
        if self.rotation_angle_changed() or self.ignore_rotation_angle_changed:
            # print ("apply_transform:rotating image")
            self.image = rotate_image_cached(scaled_image, self.rotation_angle)
            self._last_rotation_angle = self.rotation_angle
            if self.initial_rotation:
                print(f"apply_transform:initial rotation on {self.image_name}, rotation_angle: {self.rotation_angle}")
                self.image_raw = rotate_image_cached(scaled_image, self.rotation_angle)
                self.image = copy.copy(self.image_raw)
                self.initial_rotation = False
        else:
            self.image = scaled_image

        """
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        """
        self.rect = self.image.get_rect(**{self.align_image: pan_zoom_handler.world_2_screen(self.world_x, self.world_y)})

    def rotate(self, angle):
        self.rotation_angle += angle
        self.screen_position_changed = True

    def update(self):
        if self.screen_position_changed or self._pan_zoom_changed():
            screen_width, screen_height = self._update_screen_position()
            self.apply_transform(screen_width, screen_height)
            self.screen_position_changed = False

        self.inside_screen = level_of_detail.inside_screen(self.rect.center)

    def draw(self):
        if self.visible:
            self.win.blit(self.image, self.rect)



class PanZoomGif(PanZoomImage):  # working
    __slots__ = (
        'gif_name',
        'gif_frames',
        'gif_fps',
        'gif_animation_time',
        'gif_index',
        'loop_gif',
        'kill_after_gif_loop',
        'gif_start',
        )

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group=None,
            gif_name: str = None,
            gif_index: int = 0,
            gif_animation_time: float = None,
            loop_gif: bool = True,
            kill_after_gif_loop: bool = False,
            image_alpha: int = None,
            rotation_angle: int = 0,
            **kwargs
            ) -> None:
        super().__init__(win, world_x, world_y, world_width, world_height, layer, group, **kwargs)
        # gif init
        self.gif_name = gif_name
        self.gif_frames = get_gif_frames(self.gif_name)
        self.gif_fps = get_gif_fps(self.gif_name)

        # if gif_animation_time is not set, use the duration of the first frame
        self.gif_animation_time = gif_animation_time
        self.gif_animation_time = get_gif_duration(self.gif_name) / 1000 if not self.gif_animation_time else self.gif_animation_time
        self.gif_index = gif_index
        self.loop_gif = loop_gif
        self.kill_after_gif_loop = kill_after_gif_loop
        self.gif_start = time.time()

        # image init
        self.image_raw = self.gif_frames[1]  # ?? self.gif_frames[gif_index]
        self.image = copy.copy(self.image_raw)
        self.image_alpha = image_alpha
        self.rotation_angle = rotation_angle

        # set image alpha
        if self.image_alpha:
            self.image_raw.set_alpha(self.image_alpha)
            self.image.set_alpha(self.image_alpha)

        self.apply_transform(self.world_width, self.world_height)
        self.debug = False

    def update(self):
        old_gif_index = self.gif_index
        self.update_gif_index()

        if self.screen_position_changed or self._pan_zoom_changed() or self.gif_index != old_gif_index:
            screen_width, screen_height = self._update_screen_position()
            self.apply_transform(screen_width, screen_height)
            self.screen_position_changed = False

        self.inside_screen = level_of_detail.inside_screen(self.rect.center)

    def update_gif_index(self):
        """
        updates gif index, sets new image frame
        """
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

    def draw(self):
        if self.visible:
            self.win.blit(self.image, self.rect)


class MovableRotatableBase:
    def __init__(self):
        self.enable_wrap_around = True

    """
    Mixin for a sprite that can be moved and rotated.

    This mixin provides functionality for moving and rotating sprites in a circular universe,
    with wraparound behavior at the universe boundaries. It also incorporates a game speed
    factor to adjust movement based on frame rate.

    Attributes:
        world_x (float): The x-coordinate of the object in world space.
        world_y (float): The y-coordinate of the object in world space.
        rotation_angle (float): The current rotation angle of the sprite.
        world_rect (pygame.Rect): The rectangle representing the world boundaries.
        screen_position_changed (bool): Flag to indicate if the sprite's position has changed.
        game_speed (float): Factor to adjust movement speed based on frame rate.
    """

    def move(self, dx: float, dy: float) -> None:
        """
        Move the sprite by the given delta x and y, adjusted for game speed.

        Args:
            dx (float): The change in x-coordinate.
            dy (float): The change in y-coordinate.
        """
        # Adjust movement by game speed to ensure consistent speed across different frame rates
        self.world_x += dx * time_handler.game_speed  # type: ignore
        self.world_y += dy * time_handler.game_speed  # type: ignore
        if self.enable_wrap_around:  # type: ignore
            self.world_x, self.world_y = self.wraparound(self.world_x, self.world_y)  # type: ignore
        self.screen_position_changed = True  # type: ignore

    def wraparound(self, world_x: float, world_y: float) -> tuple[float, float]:
        """
        Implements a wraparound mechanism for a circular universe boundary.

        This function checks if a given point is outside a circular area defined by the universe boundaries,
        which is defined by self.world_rect.
        If the point is outside the circle, it wraps it around to the opposite side.
        If the point is inside the circle, it returns the original point.

        Args:
            world_x (float): The x-coordinate of the object in world space.
            world_y (float): The y-coordinate of the object in world space.

        Returns:
            tuple[float, float]: The (x, y) coordinates after applying wraparound.
        """
        center_x, center_y = self.world_rect.center  # type: ignore
        radius = min(self.world_rect.width, self.world_rect.height) / 2  # type: ignore
        dx = world_x - center_x
        dy = world_y - center_y
        distance_squared = dx ** 2 + dy ** 2
        if distance_squared > radius ** 2:
            angle = math.atan2(dy, dx)
            new_x = center_x - radius * math.cos(angle)
            new_y = center_y - radius * math.sin(angle)
            return new_x, new_y
        else:
            return world_x, world_y

    def rotate(self, angle: float) -> None:
        """
        Rotate the sprite by the given angle, adjusted for game speed.

        Args:
            angle (float): The angle to rotate by, in degrees.
        """
        self.rotation_angle += angle  # type: ignore
        self.screen_position_changed = True  # type: ignore

    def draw(self):
        if self.visible:
            self.win.blit(self.image, self.rect)


class PanZoomMovingRotatingImage(PanZoomImage, MovableRotatableBase):
    # __slots__ = ('rotation_speed', 'movement_speed', 'direction')/

    __slots__ = PanZoomImage.__slots__ + ('rotation_speed', 'movement_speed', 'direction', 'world_rect')

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group=None,
            image_name: str = "no_image.png",
            image_alpha: int = None,
            rotation_angle: int = 0,
            initial_rotation: int = 0,
            rotation_speed: float = 0,
            movement_speed: float = 0,
            direction: Vector2 = (0, 0),
            world_rect: Rect = Rect(0, 0, 0, 0),
            **kwargs
            ):
        super().__init__(win, world_x, world_y, world_width, world_height,
                layer, group, image_name, image_alpha, rotation_angle, initial_rotation, **kwargs)

        MovableRotatableBase.__init__(self)
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.direction = Vector2(direction)
        self.world_rect = world_rect

        self.enable_wrap_around = True

        self.debug = False

    def update(self):
        self.rotate(self.rotation_speed)
        self.move(self.direction.x * self.movement_speed,
                  self.direction.y * self.movement_speed)
        super().update()

    def draw(self):
        if self.visible:
            self.win.blit(self.image, self.rect)


class PanZoomMovingRotatingGif( PanZoomGif, MovableRotatableBase):
    """
    A subclass of PanZoomGif that allows for movement and rotation.

    Attributes:
        movement_speed (float): The speed at which the sprite moves.
        direction (Vector2): The direction in which the sprite moves.

    """
    __slots__ = ('movement_speed', 'direction')

    def __init__(
            self,
            win: pygame.Surface,
            world_x: int,
            world_y: int,
            world_width: int,
            world_height: int,
            layer: int = 0,
            group=None,
            gif_name: str = None,
            gif_index: int = 0,
            gif_animation_time: float = None,
            loop_gif: bool = True,
            kill_after_gif_loop: bool = False,
            image_alpha: int = None,
            rotation_angle: int = 0,
            movement_speed: float = 0,
            direction: Vector2 = (0, 0),
            world_rect: Rect = Rect(0, 0, 0, 0),
            **kwargs
            ):
        super().__init__( win, world_x, world_y, world_width, world_height,
                layer, group, gif_name, gif_index, gif_animation_time,
                loop_gif, kill_after_gif_loop, image_alpha, rotation_angle, **kwargs)
        MovableRotatableBase.__init__(self)
        self.movement_speed = movement_speed
        self.direction = Vector2(direction)
        self.world_rect = world_rect
        self.debug = False

        # self.enable_wrap_around = True

    def update(self):
        self.move(self.direction.x * self.movement_speed,
                  self.direction.y * self.movement_speed)
        super().update()

    def draw(self):
        if self.visible:
            self.win.blit(self.image, self.rect)


class CurveMove:
    def __init__(self, world_x, world_y, direction, gravity=0.05, friction=0.99):
        self.pos = pygame.math.Vector2(world_x, world_y)
        self.direction = direction
        self.gravity = gravity
        self.friction = friction
        self.debug = True

    def get_curve_position(self, obj, target):
        dir_vec = pygame.math.Vector2(target.rect.center) - obj.rect.center
        v_len_sq = dir_vec.length_squared()
        game_speed = time_handler.game_speed
        gravity = self.gravity * game_speed
        friction = self.friction  # * game_speed
        if v_len_sq > 0:
            dir_vec.scale_to_length(gravity)
            self.direction = (self.direction + dir_vec) * friction
            self.pos += self.direction * game_speed

        return self.pos


class CurveMoveSprite(PanZoomSpriteBase):
    def __init__(
            self,
            win,
            world_x,
            world_y,
            world_width,
            world_height,
            layer=0,
            group=sprite_groups.universe,
            target=None
            ):
        super().__init__(win=win, world_x=world_x, world_y=world_y, world_width=world_width, world_height=world_height, layer=layer, group=group)

        self.pos = pygame.math.Vector2(world_x, world_y)
        self.color = pygame.color.THECOLORS["red"]
        self.speed = pygame.math.Vector2(1.5, 0)
        self.gravity = 0.05
        self.friction = 0.99
        self.target = target

    def move_towards_target(self):
        dir_vec = pygame.math.Vector2(self.target.rect.center) - self.rect.center
        v_len_sq = dir_vec.length_squared()
        if v_len_sq > 0:
            dir_vec.scale_to_length(self.gravity)
            self.speed = (self.speed + dir_vec) * self.friction
            self.pos += self.speed

            self.set_position(self.pos.x, self.pos.y)

    def additional_update_tasks(self):
        self.move_towards_target()

    # def draw(self):
    #     pygame.draw.circle(window, self.color, (self.rect.centerx, self.rect.centery), self.rect.width // 2)


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display dimensions and create a window
    WIDTH, HEIGHT = 1820, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("PanZoomSprite Demo")

    # Create sprite group for managing all sprites together
    world_width, world_height = 5000, 5000

    # box_selection = BoxSelection(screen, all_sprites)

    # Initialize font for displaying FPS
    font = pygame.font.Font(None, 36)  # Default font with size 36

    # Main game loop to run until quit event occurs
    clock = pygame.time.Clock()
    running = True
    angle_increment = 0.02
    while running:
        events = pygame.event.get()
        pan_zoom_handler.listen(events)

        # Adjust direction for circular movement by calculating new angle using cosine/sine functions
        angle_increment += 0.02
        # sprite.direction = Vector2(math.cos(angle_increment), math.sin(angle_increment))

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

        for event in events:
            # box_selection.listen(events)
            if event.type == pygame.QUIT:
                running = False
        # Update display with drawn content for this frame
        pygame.display.update()

        # Cap frame rate to control game speed and performance consistency
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
