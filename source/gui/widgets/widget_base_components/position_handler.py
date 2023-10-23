import pygame
from pygame import Vector2

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils import global_params


class PositionHandler:

    def __init__(self, x, y, width, height, **kwargs):
        self.world_width = width
        self.world_height = height
        self.screen_width = width
        self.screen_height = height

        # world position
        self.world_x = x
        self.world_y = y

        # screen position
        self.screen_x = x
        self.screen_y = y

        self.pos = Vector2(self.get_screen_x(), self.get_screen_y())
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        self.size_x = width
        self.size_y = height

        self.zoomable = False

    def get_screen_x(self):
        return self.screen_x

    def get_screen_y(self):
        return self.screen_y

    def get_position(self):
        return self.screen_x, self.screen_y

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def set_screen_position(self, **kwargs):
        offset_x = kwargs.get("offset_x", 0)
        offset_y = kwargs.get("offset_y", 0)

        panzoom = pan_zoom_handler

        # get new coordinates
        if self.zoomable:
            x, y = panzoom.world_2_screen(self.world_x, self.world_y)
        else:
            x, y = self.world_x, self.world_y

        # if it is button
        if hasattr(self, "ui_parent"):
            if self.ui_parent:
                x, y = self.ui_parent.get_screen_x() + offset_x, self.ui_parent.get_screen_y() + offset_y

        # set new position
        self.set_position((x - self.get_screen_width() / 2, y - self.get_screen_height() / 2))

        # set new size
        self.set_objects_screen_size()

    def set_objects_screen_size(self):
        if not self.property == "ship":
            if not inside_screen(self.get_position(), border=0):
                return

        panzoom = pan_zoom_handler

        # get new_size size
        if self.zoomable:
            new_size = (self.size_x * panzoom.zoom, self.size_y * panzoom.zoom)
        else:
            new_size = (self.size_x, self.size_y)

        # set new image size
        if hasattr(self, "image_raw") and hasattr(self, "image"):
            if self.image:
                self.image = pygame.transform.scale(self.image_raw, new_size)

        if hasattr(self, "atmosphere"):
            if self.atmosphere:
                self.atmosphere = pygame.transform.scale(self.atmosphere_raw, new_size)

        # set new size
        self.setWidth(new_size[0] * panzoom.zoom)
        self.setHeight(new_size[1] * panzoom.zoom)

    def get_zoom(self):
        if global_params.app:
            return pan_zoom_handler.zoom
        else:
            return 1

    def setX__(self, x):
        self.screen_x = x
        self.set_center()

    def setY__(self, y):
        self.screen_y = y
        self.set_center()

    def set_position(self, pos):
        self.screen_x = pos[0]
        self.screen_y = pos[1]
        self.set_center()

    def setWidth(self, width):
        self.screen_width = width

    def setHeight(self, height):
        self.screen_height = height

    def set_center(self):
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
