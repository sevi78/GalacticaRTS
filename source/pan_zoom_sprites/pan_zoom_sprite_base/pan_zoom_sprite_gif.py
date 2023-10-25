import copy
import random

import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE

from source.multimedia_library.images import get_image, load_gif, get_gif_frames
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_debug import GameObjectDebug
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_visibility_handler import PanZoomVisibilityHandler
from source.utils import global_params
from source.utils.colors import colors

# pygame.init()
WIDTH = 800
HEIGHT = 600
EXPLOSION_RELATIVE_GIF_SIZE = 0.3

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen = global_params.win


class PanZoomSprite(pygame.sprite.Sprite, PanZoomVisibilityHandler, GameObjectDebug):
    """
    this is the base class for game_objects that are sprite based.
    it has the ability to pan_zoom, means: scale and reposition the images or gif based on the pan_zoom_handler
    to run it, add the instance to a sprite.group.
    the sprite group will then be updated from the main loop and updates all its members
    always set the world position of the object, the screen position will be calculated automaticaly
    """

    # PanZoomSprite
    __slots__ = (
        'layer', 'group', 'property', 'zoomable', 'win', 'pan_zoom', 'image_name', 'gif', 'gif_frames',
        'relative_gif_size', 'loop_gif', 'kill_after_gif_loop', 'gif_index', 'counter', 'image_raw', 'image',
        'align_image', 'rect', 'screen_x', 'screen_y', 'screen_width', 'screen_height', 'screen_position',
        'previous_world_x', 'previous_world_y', 'world_x', 'world_y', 'world_width', 'world_height',
        'orbit_angle', 'sound', 'debug'
        )

    # __slots__ = (
    #     'layer', 'group', 'property', 'zoomable', 'win', 'pan_zoom', 'image_name', 'gif', 'gif_frames',
    #     'relative_gif_size', 'loop_gif', 'kill_after_gif_loop', 'gif_index', 'counter', 'image_raw', 'image',
    #     'align_image', 'rect', 'screen_x', 'screen_y', 'screen_width', 'screen_height', 'screen_position',
    #     'previous_world_x', 'previous_world_y', 'world_x', 'world_y', 'world_width', 'world_height',
    #     'orbit_angle', 'sound', 'debug'
    #     )
    #
    # PanZoomVisibilityHandler
    __slots__ += ('children', '_hidden', '_disabled', 'widgets')

    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        GameObjectDebug.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        PanZoomVisibilityHandler.__init__(self)
        self.layer = kwargs.get("layer", 0)
        self.group = kwargs.get("group", None)
        self.property = ""
        self.name = "noname"
        self.zoomable = kwargs.get("zoomable", True)
        self.frame_color = colors.frame_color

        # image/gif
        self.win = win
        self.pan_zoom = pan_zoom
        self.image_name = image_name
        self.gif = None
        self.gif_frames = None
        self.relative_gif_size = kwargs.get("relative_gif_size", 1.0)
        self.loop_gif = kwargs.get("loop_gif", True)
        self.kill_after_gif_loop = kwargs.get("kill_after_gif_loop", False)
        self.gif_index = 0
        self.counter = 0

        if not self.image_name:
            self.image_name = "no_icon.png"

        if self.image_name.endswith(".png"):
            self.image_raw = get_image(self.image_name)
            self.image = copy.copy(self.image_raw)

        elif self.image_name.endswith(".gif"):
            self.gif = load_gif(self.image_name)
            self.gif_frames = get_gif_frames(self.gif)
            self.image_raw = self.gif_frames[1]
            self.image = copy.copy(self.image_raw)

        self.align_image = kwargs.get("align_image", "topleft")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # screen
        self.screen_x = x
        self.screen_y = y
        self.screen_width = width
        self.screen_height = height
        self.screen_position = (self.screen_x, self.screen_y)

        # world
        self.previous_world_x = None
        self.previous_world_y = None
        self.world_x = x
        self.world_y = y
        self.world_width = self.image.get_rect().width
        self.world_height = self.image.get_rect().height
        self.world_position = (self.world_x, self.world_y)

        # orbit
        self.orbit_angle = None

        # sound
        self.sound = kwargs.get("sound", None)
        self.debug = kwargs.get("debug", False)

        # register
        if self.group:
            getattr(sprite_groups, self.group).add(self)

    def get_zoom(self):
        return self.pan_zoom.zoom

    @property
    def world_position(self):
        return self._world_x, self._world_y

    @world_position.setter
    def world_position(self, position):
        self.world_x, self.world_y = position
        self.screen_position = self.pan_zoom.world_2_screen(self.world_x, self.world_y)

        if self.zoomable:
            self.screen_width = self.world_width * self.pan_zoom.zoom * self.relative_gif_size
            self.screen_height = self.world_height * self.pan_zoom.zoom * self.relative_gif_size
        else:
            self.screen_width = self.world_width
            self.screen_height = self.world_height

        self.update_rect()

    # @world_position.setter
    # def world_position(self, position):
    #     if not self.previous_world_x:
    #         self.previous_world_x, self.previous_world_y = position
    #
    #     self.world_x, self.world_y = position
    #     smooth_position(position[0], position[1], self.previous_world_x, self.previous_world_y, 30)
    #
    #     #self.screen_position = self.pan_zoom.world_2_screen(self.world_x, self.world_y)
    #     x,y = smooth_position(self.world_x, self.world_y, self.previous_world_x, self.previous_world_y, 0.1)
    #     self.screen_position = self.pan_zoom.world_2_screen(x,y)
    #
    #
    #     self.previous_world_x, self.previous_world_y = position
    #
    #
    #     if self.zoomable:
    #         self.set_screen_size(self.world_width * self.pan_zoom.zoom * self.relative_gif_size,
    #                              self.world_height * self.pan_zoom.zoom * self.relative_gif_size)
    #     else:
    #         self.set_screen_size(self.world_width,
    #             self.world_height)
    #     self.update_rect()

    # @world_position.setter
    # def world_position(self, position):
    #     self.world_x, self.world_y = position
    #     diff_x = self.world_x - self.screen_position[0]
    #     diff_y = self.world_y - self.screen_position[1]
    #     if abs(diff_x) > 10:
    #         diff_x = 10 if diff_x > 0 else -10
    #     if abs(diff_y) > 10:
    #         diff_y = 10 if diff_y > 0 else -10
    #     self.screen_position = (self.screen_position[0] + diff_x, self.screen_position[1] + diff_y)
    #     self.world_x, self.world_y = self.pan_zoom.screen_2_world(*self.screen_position)
    #
    #     if self.zoomable:
    #         self.set_screen_size(self.world_width * self.pan_zoom.zoom * self.relative_gif_size,
    #                              self.world_height * self.pan_zoom.zoom * self.relative_gif_size)
    #     else:
    #         self.set_screen_size(self.world_width,
    #             self.world_height)
    #     self.update_rect()

    # @world_position.setter
    # def world_position(self, position):
    #     prev_position = (self.world_x, self.world_y)
    #     self.world_x, self.world_y = position
    #     distance = math.sqrt((self.world_x - prev_position[0]) ** 2 + (self.world_y - prev_position[1]) ** 2)
    #
    #     # Smoothing algorithm
    #     if distance > 1000:
    #         dx = self.world_x - prev_position[0]
    #         dy = self.world_y - prev_position[1]
    #         angle = math.atan2(dy, dx)
    #         self.world_x = prev_position[0] + 15 * math.cos(angle)
    #         self.world_y = prev_position[1] + 15 * math.sin(angle)
    #
    #     self.screen_position = self.pan_zoom.world_2_screen(self.world_x, self.world_y)
    #     self.screen_width = self.world_width * self.pan_zoom.zoom * self.relative_gif_size
    #     self.screen_height = self.world_height * self.pan_zoom.zoom * self.relative_gif_size
    #     self.update_rect()

    def set_world_position(self, position):
        self.world_position = position

    def get_screen_x(self):
        return self.screen_x

    def get_screen_y(self):
        return self.screen_y

    def get_screen_position(self):
        return self.screen_position

    def get_screen_width(self):
        return self.screen_width

    def set_screen_width(self, value):
        self.screen_width = value

    def set_screen_height(self, value):
        self.screen_height = value

    def get_screen_height(self):
        return self.screen_height

    def set_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update_rect(self):
        if not self.image_raw:
            return
        # if hasattr(self, "prev_angle"):
        #     if self.prev_angle and not self.moving:
        #         image = pygame.transform.scale(self.image_raw, (self.screen_width, self.screen_height))
        #
        #         self.image = pygame.transform.rotate(image, self.prev_angle)
        # else:
        self.image = pygame.transform.scale(self.image_raw, (self.screen_width, self.screen_height))
        self.rect = self.image.get_rect()

        self.align_image_rect()

    def align_image_rect(self):
        if self.align_image == "center":
            self.rect.center = self.screen_position

        elif self.align_image == "topleft":
            self.rect.topleft = self.screen_position

        elif self.align_image == "bottomleft":
            self.rect.bottomleft = self.screen_position

        elif self.align_image == "topright":
            self.rect.topright = self.screen_position

        elif self.align_image == "bottomright":
            self.rect.bottomright = self.screen_position

    def update_gif_index(self):
        if not self.gif:
            return

        if not self.gif_frames:
            return

        self.counter += 1
        if self.counter % 5 == 0:
            self.gif_index += 1
            if self.gif_index == 1:
                if self.sound:
                    sounds.play_sound(self.sound)

            if self.gif_index >= len(self.gif_frames):
                if self.loop_gif:
                    self.gif_index = 0
                elif self.kill_after_gif_loop:
                    self.kill()
            else:
                self.image_raw = self.gif_frames[self.gif_index]

    def get_game_paused(self):
        return global_params.game_paused

    def update_pan_zoom_sprite(self):
        # if self.get_game_paused():
        #     return

        self.set_world_position((self.world_x, self.world_y))
        self.update_gif_index()

        if self.debug:
            self.debug_object()

    def update(self):
        self.update_pan_zoom_sprite()

# def main():
#     pan_zoom_handler = PanZoomHandler(screen, WIDTH, HEIGHT)
#     target = PanZoomSprite(screen, 300, 400, 74, 30, pan_zoom_handler, "ufo_74x30.png", align_image="bottomright")
#     sprites.add(target)
#
#     sprite = GameObject(screen, 200, 300, 42, 17, pan_zoom_handler, "missile_42x17.gif", loop_gif=True, move_to_target=True, align_image="center")
#     sprite.set_target(target)
#     sprites.add(sprite)
#
#     # Main game loop
#     running = True
#     while running:
#         print("sprites", sprites)
#         clock.tick(25)
#         screen.fill((0, 0, 0))
#         events = pygame.event.get()
#         # Event handling
#         for event in events:
#             if event.type == QUIT:
#                 running = False
#             elif event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#         if len(sprites) == 1:
#             x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
#
#             sprite = GameObject(screen, x, y, 42, 17, pan_zoom_handler, "missile_42x17.gif", loop_gif=True, move_to_target=True, align_image="topleft")
#             sprite.set_target(target)
#             sprites.add(sprite)
#
#         pan_zoom_handler.listen(events, True)
#         sprites.update()
#         sprites.draw(screen)
#
#         # Update the display
#         pygame.display.flip()
#
#
# if __name__ == "__main__":
#     main()
