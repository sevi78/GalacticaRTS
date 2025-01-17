import copy
import time

import pygame

from source.configuration.game_config import config
from source.gui.widgets.widget_base_components.visibilty_handler import VisibilityHandler
from source.handlers.color_handler import colors, get_average_color
from source.handlers.pan_zoom_handler import PanZoomHandler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, get_gif_frames, get_gif, get_gif_fps, get_gif_duration, \
    outline_image, scale_image_cached
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_debug import GameObjectDebug

WIDTH = 800
HEIGHT = 600
EXPLOSION_RELATIVE_GIF_SIZE = 0.3
SHRINK_FACTOR = 0.005


class PanZoomSprite(pygame.sprite.Sprite, VisibilityHandler, GameObjectDebug):  # cached images
    """
    This is the base class for game objects that are sprite based.
    It has the ability to pan_zoom, means: scale and reposition the images or gif based on the pan_zoom_handler
    To run it, add the instance to a sprite.group.
    The sprite group will then be updated from the main loop and updates all its members
    Always set the world position of the object, the screen position will be calculated automatically

    Args:
        win (pygame.Surface): The window surface
        x (int): The x-coordinate of the object
        y (int): The y-coordinate of the object
        width (int): The width of the object
        height (int): The height of the object
        pan_zoom (PanZoomHandler): The pan zoom handler
        image_name (str): The name of the image
        kwargs: Additional keyword arguments

    Attributes:
        layer (int): The layer of the object
        group (pygame.sprite.Group): The sprite group
        name (str): The name of the object
        zoomable (bool): Whether the object is zoomable
        align_image (str): The alignment of the image
        relative_gif_size (float): The relative size of the gif
        loop_gif (bool): Whether to loop the gif
        kill_after_gif_loop (bool): Whether to kill the object after the gif loop
        appear_at_start (bool): Whether the object appears at the start
        outline_thickness (int): The thickness of the outline
        outline_threshold (int): The threshold of the outline
        sound (str): The sound associated with the object
        debug (bool): Whether the object is in debug mode
        property (str): The property of the object
        gif (pygame.Surface): The gif surface
        gif_frames (list): The list of gif frames
        gif_fps (int): The frames per second of the gif
        gif_index (int): The current index of the gif
        counter (int): The counter of the gif
        image_raw (pygame.Surface): The raw image surface
        rect (pygame.Rect): The rectangle of the object
        screen_x (int): The x-coordinate of the object on the screen
        screen_y (int): The y-coordinate of the object on the screen
        screen_width (int): The width of the object on the screen
        screen_height (int): The height of the object on the screen
        screen_position (tuple): The position of the object on the screen
        previous_world_x (int): The previous x-coordinate of the object in the world
        previous_world_y (int): The previous y-coordinate of the object in the world
        world_x (int): The x-coordinate of the object in the world
        world_y (int): The y-coordinate of the object in the world
        world_width (int): The width of the object in the world
        world_height (int): The height of the object in the world
        orbit_angle (float): The orbit angle of the object
    """

    # PanZoomSprite
    __slots__ = (
        'layer', 'group', 'property', 'zoomable', 'win', 'pan_zoom', 'image_name', 'gif', 'gif_frames',
        'relative_gif_size', 'loop_gif', 'kill_after_gif_loop', 'gif_index', 'counter', 'image_raw',
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

    def __init__(
            self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
            image_name: str, **kwargs
            ):

        GameObjectDebug.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        VisibilityHandler.__init__(self)
        self.layer = kwargs.get("layer", 0)
        self.group = kwargs.get("group", None)
        self.property = ""
        self.name = kwargs.get("name", "no_name")
        self.zoomable = kwargs.get("zoomable", True)
        self.frame_color = colors.frame_color

        # image/gif
        self.win = win
        self.pan_zoom = pan_zoom
        self.image_name = image_name
        self.gif = None
        self.gif_frames = None
        self.gif_fps = None
        self.relative_gif_size = kwargs.get("relative_gif_size", 1.0)
        self.loop_gif = kwargs.get("loop_gif", True)
        self.kill_after_gif_loop = kwargs.get("kill_after_gif_loop", False)
        self.appear_at_start = kwargs.get("appear_at_start", False)
        self.shrink = 0.0 if self.appear_at_start else 1.0
        self.gif_index = kwargs.get("gif_index", 1)
        self.gif_start = time.time()
        self.gif_animation_time = 0.1
        self.current_time = 0
        self.counter = 0
        self.image_alpha = kwargs.get("image_alpha", None)

        self.outline_thickness = kwargs.get("outline_thickness", 0)
        self.outline_threshold = kwargs.get("outline_threshold", 0)

        if not self.image_name:
            self.image_name = "no_icon.png"

        if self.image_name.endswith(".png"):
            self.image_raw = get_image(self.image_name)
            self.image = copy.copy(self.image_raw)

        elif self.image_name.endswith(".gif"):
            self.gif = get_gif(self.image_name)
            self.gif_frames = get_gif_frames(self.image_name)
            self.gif_fps = get_gif_fps(self.image_name)
            self.gif_animation_time = kwargs.get("gif_animation_time", get_gif_duration(self.image_name) / 1000)
            self.image_raw = self.gif_frames[1]
            self.image = copy.copy(self.image_raw)

        if self.image_alpha:
            self.image_raw.set_alpha(self.image_alpha)
            self.image.set_alpha(self.image_alpha)

        # self.image_rotated = copy.copy(self.image)
        self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
        self.average_color = get_average_color(self.image_raw)

        self.align_image = kwargs.get("align_image", "topleft")
        self.enable_rotate = kwargs.get("enable_rotate", False)
        self.rect = self.image.get_rect()
        # self.rect_raw = self.image_raw.get_rect()
        # self.rect_raw = self.image_raw.get_rect(centerx=self.world_width / 2, centery=self.world_width / 2)
        self.collide_rect = pygame.Rect(x, y, 20, 20)
        self.rect.x = x
        self.rect.y = y

        # screen
        self.lod = 0
        self.screen_x = x
        self.screen_y = y
        self.screen_width = width
        self.screen_height = height
        self.screen_position = (self.screen_x, self.screen_y)

        # world
        self.previous_world_x = None
        self.previous_world_y = None
        self.world_x = 0
        self.world_y = 0
        self.world_width = width  # kwargs.get("width", self.image.get_rect().width)
        self.world_height = height  # kwargs.get("height", self.image.get_rect().height)
        self.world_position = (0, 0)
        self.set_world_position((x, y))
        self.rect_raw = pygame.Rect(0, 0, self.world_width, self.world_height)

        # orbit
        self.orbit_angle = None

        # sound
        self.sound = kwargs.get("sound", None)
        self.debug = kwargs.get("debug", False)

        # register
        if self.group:
            getattr(sprite_groups, self.group).add(self)



    def set_world_position(self, position):
        self.world_position = position
        self.world_x, self.world_y = position
        self.screen_position = self.pan_zoom.world_2_screen(self.world_x, self.world_y)

        if self.zoomable:
            self.screen_width = self.world_width * self.pan_zoom.zoom * self.relative_gif_size
            self.screen_height = self.world_height * self.pan_zoom.zoom * self.relative_gif_size
        else:
            self.screen_width = self.world_width
            self.screen_height = self.world_height

        self.update_rect()

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

    # def set_screen_size(self, screen_width, screen_height):
    #     self.screen_width = screen_width
    #     self.screen_height = screen_height

    def update_rect(self):
        if not self.image_raw:
            return

        if self._hidden:
            print (f"update_rect while hidden:{self}")

        self.image = scale_image_cached(self.image_raw, (self.screen_width * self.shrink, self.screen_height * self.shrink))

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

        self.collide_rect.center = self.rect.center

    def update_gif_index(self):
        if not self.gif:
            return

        if not self.gif_frames:
            return

        if self.gif_index == len(self.gif_frames):
            if self.loop_gif:
                self.gif_index = 0
            if self.kill_after_gif_loop:
                self.kill()
                return
        else:
            if self.gif_index == 1:
                if self.sound:
                    sounds.play_sound(self.sound)

        if time.time() > self.gif_start + self.gif_animation_time:
            self.image_raw = self.gif_frames[self.gif_index]
            self.gif_index += 1
            self.gif_start += self.gif_animation_time

    def appear(self):
        if self.shrink >= 1.0:
            self.appear_at_start = False
            return
        self.shrink += SHRINK_FACTOR * time_handler.game_speed

    def disappear(self):
        self.shrink -= SHRINK_FACTOR
        if self.shrink <= SHRINK_FACTOR:
            self.end_object(explode=False)

    def update_pan_zoom_sprite(self):
        # if self.get_game_paused():
        #     return

        if self.appear_at_start:
            self.appear()
        self.set_world_position((self.world_x, self.world_y))
        self.update_gif_index()

        if self.debug or config.debug:
            self.debug_object()

    def update(self):
        self.update_pan_zoom_sprite()  # with caching# with cchaching

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


# if __name__ == "__main__":
#     main()


# class PanZoomSprite(PanZoomMovingRotatingImage,  GameObjectDebug):  # cached images, PanZoomMovingRotatingImage, not working
#     """
#     This is the base class for game objects that are sprite based.
#     It has the ability to pan_zoom, means: scale and reposition the images or gif based on the pan_zoom_handler
#     To run it, add the instance to a sprite.group.
#     The sprite group will then be updated from the main loop and updates all its members
#     Always set the world position of the object, the screen position will be calculated automatically
#
#     Args:
#         win (pygame.Surface): The window surface
#         x (int): The x-coordinate of the object
#         y (int): The y-coordinate of the object
#         width (int): The width of the object
#         height (int): The height of the object
#         pan_zoom (PanZoomHandler): The pan zoom handler
#         image_name (str): The name of the image
#         kwargs: Additional keyword arguments
#
#     Attributes:
#         layer (int): The layer of the object
#         group (pygame.sprite.Group): The sprite group
#         name (str): The name of the object
#         zoomable (bool): Whether the object is zoomable
#         align_image (str): The alignment of the image
#         relative_gif_size (float): The relative size of the gif
#         loop_gif (bool): Whether to loop the gif
#         kill_after_gif_loop (bool): Whether to kill the object after the gif loop
#         appear_at_start (bool): Whether the object appears at the start
#         outline_thickness (int): The thickness of the outline
#         outline_threshold (int): The threshold of the outline
#         sound (str): The sound associated with the object
#         debug (bool): Whether the object is in debug mode
#         property (str): The property of the object
#         gif (pygame.Surface): The gif surface
#         gif_frames (list): The list of gif frames
#         gif_fps (int): The frames per second of the gif
#         gif_index (int): The current index of the gif
#         counter (int): The counter of the gif
#         image_raw (pygame.Surface): The raw image surface
#         rect (pygame.Rect): The rectangle of the object
#         screen_x (int): The x-coordinate of the object on the screen
#         screen_y (int): The y-coordinate of the object on the screen
#         screen_width (int): The width of the object on the screen
#         screen_height (int): The height of the object on the screen
#         screen_position (tuple): The position of the object on the screen
#         previous_world_x (int): The previous x-coordinate of the object in the world
#         previous_world_y (int): The previous y-coordinate of the object in the world
#         world_x (int): The x-coordinate of the object in the world
#         world_y (int): The y-coordinate of the object in the world
#         world_width (int): The width of the object in the world
#         world_height (int): The height of the object in the world
#         orbit_angle (float): The orbit angle of the object
#     """
#
#     # PanZoomSprite
#     # __slots__ = (
#     #     'layer', 'group', 'property', 'zoomable', 'win', 'pan_zoom', 'image_name', 'gif', 'gif_frames',
#     #     'relative_gif_size', 'loop_gif', 'kill_after_gif_loop', 'gif_index', 'counter', 'image_raw',
#     #     'align_image', 'rect', 'screen_x', 'screen_y', 'screen_width', 'screen_height', 'screen_position',
#     #     'previous_world_x', 'previous_world_y', 'world_x', 'world_y', 'world_width', 'world_height',
#     #     'orbit_angle', 'sound', 'debug'
#     #     )
#
#     # __slots__ = (
#     #     'layer', 'group', 'property', 'zoomable', 'win', 'pan_zoom', 'image_name', 'gif', 'gif_frames',
#     #     'relative_gif_size', 'loop_gif', 'kill_after_gif_loop', 'gif_index', 'counter', 'image_raw', 'image',
#     #     'align_image', 'rect', 'screen_x', 'screen_y', 'screen_width', 'screen_height', 'screen_position',
#     #     'previous_world_x', 'previous_world_y', 'world_x', 'world_y', 'world_width', 'world_height',
#     #     'orbit_angle', 'sound', 'debug'
#     #     )
#     #
#     # PanZoomVisibilityHandler
#     # __slots__ += ('children', '_hidden', '_disabled', 'widgets')
#
#     def __init__(
#             self, win: pygame.Surface, x: int, y: int, width: int, height: int, pan_zoom: PanZoomHandler,
#             image_name: str, **kwargs
#             ):
#
#         GameObjectDebug.__init__(self)
#         # pygame.sprite.Sprite.__init__(self)
#         # VisibilityHandler.__init__(self)
#
#         # self.layer = kwargs.get("layer", 0)
#         self.group = kwargs.get("group", None)
#         self.property = ""
#         self.name = kwargs.get("name", "no_name")
#         self.zoomable = kwargs.get("zoomable", True)
#         self.frame_color = colors.frame_color
#
#         # image/gif
#         self.win = win
#         self.pan_zoom = pan_zoom
#         self.image_name = image_name
#         self.gif = None
#         self.gif_frames = None
#         self.gif_fps = None
#         self.relative_gif_size = kwargs.get("relative_gif_size", 1.0)
#         self.loop_gif = kwargs.get("loop_gif", True)
#         self.kill_after_gif_loop = kwargs.get("kill_after_gif_loop", False)
#         self.appear_at_start = kwargs.get("appear_at_start", False)
#         self.shrink = 0.0 if self.appear_at_start else 1.0
#         self.gif_index = kwargs.get("gif_index", 1)
#         self.gif_start = time.time()
#         self.gif_animation_time = 0.1
#         self.current_time = 0
#         self.counter = 0
#         self.image_alpha = kwargs.get("image_alpha", None)
#
#
#         self.outline_thickness = kwargs.get("outline_thickness", 0)
#         self.outline_threshold = kwargs.get("outline_threshold", 0)
#
#         if not self.image_name:
#             self.image_name = "no_icon.png"
#
#         if self.image_name.endswith(".png"):
#             self.image_raw = get_image(self.image_name)
#             self.image = copy.copy(self.image_raw)
#
#         elif self.image_name.endswith(".gif"):
#             self.gif = get_gif(self.image_name)
#             self.gif_frames = get_gif_frames(self.image_name)
#             self.gif_fps = get_gif_fps(self.image_name)
#             self.gif_animation_time = kwargs.get("gif_animation_time", get_gif_duration(self.image_name) / 1000)
#             self.image_raw = self.gif_frames[1]
#             self.image = copy.copy(self.image_raw)
#
#         if self.image_alpha:
#             self.image_raw.set_alpha(self.image_alpha)
#             self.image.set_alpha(self.image_alpha)
#
#         self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
#         self.average_color = get_average_color(self.image_raw)
#
#         self.align_image = kwargs.get("align_image", "topleft")
#         self.enable_rotate = kwargs.get("enable_rotate", False)
#         self.rect = self.image.get_rect()
#         self.collide_rect = pygame.Rect(x, y, 20, 20)
#         self.rect.x = x
#         self.rect.y = y
#
#         # screen
#         self.lod = 0
#         self.screen_x = x
#         self.screen_y = y
#         self.screen_width = width
#         self.screen_height = height
#         self.screen_position = (self.screen_x, self.screen_y)
#
#         # world
#         self.previous_world_x = None
#         self.previous_world_y = None
#         self.world_x = 0
#         self.world_y = 0
#         # self._world_x = x
#         # self._world_y = y
#         self.world_width = width  # kwargs.get("width", self.image.get_rect().width)
#         self.world_height = height  # kwargs.get("height", self.image.get_rect().height)
#         self.world_position = (0,0)
#         # # rotate
#         # self.rotation_direction = kwargs.get("rotation_direction", random.choice([1, -1]))
#         # self.rotation_speed = kwargs.get("rotation_speed", random.uniform(0.1, 1.0))
#         # self.rotation = 0
#         self.set_world_position((x, y))
#
#
#         # orbit
#         self.orbit_angle = None
#
#         # sound
#         self.sound = kwargs.get("sound", None)
#         self.debug = kwargs.get("debug", False)
#
#         # register
#         # if self.group:
#         #     getattr(sprite_groups, self.group).add(self)
#         if not self.group:
#              self.group = getattr(sprite_groups, "universe")
#         else:
#             self.group = getattr(sprite_groups, self.group)
#
#         # self.layer = kwargs.get("layer", 0)
#
#         self._is_sub_widget = False
#         self._hidden = False
#         self._disabled = False
#         # self.layer = kwargs.get("layer", 9)
#         self.widgets = []
#         if self._is_sub_widget:
#             self.hide()
#
#         super().__init__(win, x, y, width, height)
#
#
#
#     def set_visible(self):
#         if self._hidden:
#             self.show()
#         else:
#             self.hide()
#
#     def hide(self):
#         """hides self and its widgets
#         """
#         self._hidden = True
#         for i in self.widgets:
#             i.hide()
#
#     def show(self):
#         """shows self and its widgets
#         """
#         self._hidden = False
#         for i in self.widgets:
#             i.show()
#
#     def disable(self):
#         self._disabled = True
#
#     def enable(self):
#         self._disabled = False
#
#     def is_sub_widget(self):
#         return self._is_sub_widget
#
#     # def set_is_sub_widget(self, is_sub_widget):
#     #     self._is_sub_widget = is_sub_widget
#     #     if is_sub_widget:
#     #         WidgetHandler.remove_widget(self)
#     #     else:
#     #         WidgetHandler.add_widget(self)
#
#     def is_visible(self):
#         return not self._hidden
#
#
#     def get_zoom(self):
#         return self.pan_zoom.zoom
#
#
#
#     def set_world_position(self, position):
#         self.world_position = position
#         self.world_x, self.world_y = position
#         self.screen_position = self.pan_zoom.world_2_screen(self.world_x, self.world_y)
#
#         if self.zoomable:
#             self.screen_width = self.world_width * self.pan_zoom.zoom * self.relative_gif_size
#             self.screen_height = self.world_height * self.pan_zoom.zoom * self.relative_gif_size
#         else:
#             self.screen_width = self.world_width
#             self.screen_height = self.world_height
#
#         self.update_rect()
#
#     def get_screen_x(self):
#         return self.screen_x
#
#     def get_screen_y(self):
#         return self.screen_y
#
#     def get_screen_position(self):
#         return self.screen_position
#
#     def get_screen_width(self):
#         return self.screen_width
#
#     def set_screen_width(self, value):
#         self.screen_width = value
#
#     def set_screen_height(self, value):
#         self.screen_height = value
#
#     def get_screen_height(self):
#         return self.screen_height
#
#     # def set_screen_size(self, screen_width, screen_height):
#     #     self.screen_width = screen_width
#     #     self.screen_height = screen_height
#
#     def update_rect(self):
#         if not self.image_raw:
#             return
#
#         self.image = scale_image_cached(self.image_raw, (self.screen_width * self.shrink, self.screen_height * self.shrink))
#
#         self.rect = self.image.get_rect()
#
#         self.align_image_rect()
#
#     def align_image_rect(self):
#         if self.align_image == "center":
#             self.rect.center = self.screen_position
#
#         elif self.align_image == "topleft":
#             self.rect.topleft = self.screen_position
#
#         elif self.align_image == "bottomleft":
#             self.rect.bottomleft = self.screen_position
#
#         elif self.align_image == "topright":
#             self.rect.topright = self.screen_position
#
#         elif self.align_image == "bottomright":
#             self.rect.bottomright = self.screen_position
#
#         self.collide_rect.center = self.rect.center
#
#     def update_gif_index(self):
#         if not self.gif:
#             return
#
#         if not self.gif_frames:
#             return
#
#         if self.gif_index == len(self.gif_frames):
#             if self.loop_gif:
#                 self.gif_index = 0
#             if self.kill_after_gif_loop:
#                 self.kill()
#                 return
#         else:
#             if self.gif_index == 1:
#                 if self.sound:
#                     sounds.play_sound(self.sound)
#
#         if time.time() > self.gif_start + self.gif_animation_time:
#             self.image_raw = self.gif_frames[self.gif_index]
#             self.gif_index += 1
#             self.gif_start += self.gif_animation_time
#
#     def appear(self):
#         if self.shrink >= 1.0:
#             self.appear_at_start = False
#             return
#         self.shrink += SHRINK_FACTOR
#
#     def disappear(self):
#         self.shrink -= SHRINK_FACTOR
#         if self.shrink <= SHRINK_FACTOR:
#             self.end_object(explode=False)
#
#     def update_pan_zoom_sprite(self):
#         # if self.get_game_paused():
#         #     return
#
#         if self.appear_at_start:
#             self.appear()
#         self.set_world_position((self.world_x, self.world_y))
#         self.update_gif_index()
#
#         if self.debug or config.debug:
#             self.debug_object()
#
#     def update(self):
#         self.update_pan_zoom_sprite()  # with caching# with cchaching
