import pygame

from source.game_play.navigation import navigate_to_position
from source.configuration import global_params
from source.configuration.global_params import ui_rounded_corner_small_thickness
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups

PLANET_IMAGE_SIZE = 125
TOGGLESIZE = 20
MIN_OBJECT_SIZE = 2
MIN_MAP_SIZE = 240

SHIP_COLOR = pygame.color.THECOLORS["red"]
MOON_COLOR = pygame.color.THECOLORS["grey"]
PLANET_COLOR = pygame.color.THECOLORS["green"]
SUN_COLOR = pygame.color.THECOLORS["yellow"]
ITEM_COLOR = pygame.color.THECOLORS["brown"]
UFO_COLOR = pygame.color.THECOLORS["purple"]


class MapPanel():

    def __init__(self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int) -> None:
        # params
        self.win = win
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height

        # vars
        self.app = global_params.app
        self.scale = 1
        self.scale_factor = 10
        self.name = "map panel"
        self.frame_color = colors.frame_color
        self.factor = self.app.level_handler.data["globals"]["width"] / self.world_width

        # surfaces, rect
        self.background_surface = pygame.Surface((self.world_width, self.world_height))
        self.frame_rect = pygame.Rect(self.world_x, self.world_y, self.world_width, self.world_height)

        # interaction stuff
        self.ctrl_pressed = False
        self.left_mouse_button_pressed = False

    def draw_camera_focus(self, pan_zoom_handler) -> None:
        # calculate the position
        x, y = (pan_zoom_handler.world_offset_x / self.factor), (pan_zoom_handler.world_offset_y / self.factor)

        # Calculate the width and height of the rectangle
        width = global_params.WIDTH / self.factor / pan_zoom_handler.zoom
        height = global_params.HEIGHT / self.factor / pan_zoom_handler.zoom

        # draw the rect onto background_surface
        pygame.draw.rect(self.background_surface, colors.ui_dark, pygame.Rect(x, y, width, height), 1, 3)

    def draw_objects(self, sprites: list, surface: pygame.surface.Surface) -> None:
        # update factor 
        self.factor = self.app.level_handler.data["globals"]["width"] / self.world_width

        # init radius
        radius = MIN_OBJECT_SIZE

        # get all objects to display
        for sprite in sprites:
            # get average color of object
            color = sprite.average_color

            # planets, sun, moons
            if hasattr(sprite, "type"):
                radius = sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE

                # draw orbits
                orbit_objects = [_ for _ in sprite_groups.planets.sprites() if _.orbit_object == sprite]
                for i in orbit_objects:
                    pygame.draw.circle(
                        surface=surface,
                        color=colors.ui_darker,
                        center=((sprite.world_x / self.factor),
                                (sprite.world_y / self.factor)),
                        radius=i.orbit_radius / self.factor,
                        width=1)

            # ships
            if hasattr(sprite, "property"):
                if sprite.property == "ship":
                    radius = sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE

                    # display selection
                    if sprite == self.app.ship:
                        pygame.draw.circle(
                            surface=surface,
                            color=colors.select_color,
                            center=(
                                (sprite.world_x / self.factor),
                                (sprite.world_y / self.factor)),
                            radius=radius * 2, width=1)

                # set rqdius
                if sprite.property == "ufo":
                    radius = sprite.world_width / self.factor if sprite.world_width / self.factor > MIN_OBJECT_SIZE else MIN_OBJECT_SIZE

                if sprite.property == "item":
                    radius = 1

            # draw object
            pos = ((sprite.world_x / self.factor), (sprite.world_y / self.factor))
            pygame.draw.circle(
                surface=surface,
                color=color,
                center=pos,
                radius=radius)

    def reposition(self) -> None:
        self.world_y = self.win.get_size()[1] - self.world_height

    def listen(self, events) -> None:
        for event in events:
            # ctrl_pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True

            elif event.type == pygame.KEYUP:
                self.ctrl_pressed = False

            # on hover
            if self.frame_rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEWHEEL and not self.ctrl_pressed:
                    self.scale_map(event)

                # navigate
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.ctrl_pressed:
                    # left button
                    if pygame.mouse.get_pressed()[0]:
                        self.left_mouse_button_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.left_mouse_button_pressed = False

        if self.left_mouse_button_pressed:
            self.update_camera_position()

    def scale_map(self, event):
        # get scale direction
        self.scale = event.y

        # recalculate scale, set world_position
        self.world_width += self.scale * self.scale_factor
        self.world_height += self.scale * self.scale_factor

        # limit size
        if self.world_width < MIN_MAP_SIZE:
            self.world_width = MIN_MAP_SIZE
        if self.world_height < MIN_MAP_SIZE:
            self.world_height = MIN_MAP_SIZE

    def update_camera_position(self):
        # get the mouse position
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        # calculate the relative mouse position when clicked on the map
        dist_x, dist_y = abs(self.world_x - mx), abs(self.world_y - my)

        # multiply with factor to make sure world position is correct
        x, y = dist_x * self.factor, dist_y * self.factor

        # navigate to position
        navigate_to_position(x, y)

    def draw(self) -> None:
        self.reposition()
        # generate rect
        self.frame_rect = pygame.Rect(self.world_x, self.world_y, self.world_width, self.world_height)

        # draw the panel
        self.background_surface = pygame.Surface((self.world_width, self.world_height))
        self.background_surface.fill((0, 0, 0))
        self.background_surface.set_alpha(global_params.ui_panel_alpha)

        # draw the objects
        self.draw_objects(sprite_groups.planets.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.ships.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.collectable_items.sprites(), self.background_surface)
        self.draw_objects(sprite_groups.ufos.sprites(), self.background_surface)

        # draw camera focus
        self.draw_camera_focus(pan_zoom_handler)

        # draw the map_image
        self.win.blit(self.background_surface, self.frame_rect)

        # draw the frame
        pygame.draw.rect(self.win, self.frame_color, pygame.Rect(self.world_x, self.world_y, self.world_width,
            self.world_height), int(ui_rounded_corner_small_thickness), int(global_params.ui_rounded_corner_radius_small))
