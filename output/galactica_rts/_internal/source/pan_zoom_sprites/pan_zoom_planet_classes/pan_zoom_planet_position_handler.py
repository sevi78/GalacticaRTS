import pygame

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import scale_image_cached

MIN_IMAGE_ZOOM_SIZE = 1
MAX_IMAGE_ZOOM_SIZE = 1000


class PanZoomPlanetPositionHandler:
    def __init__(self, x, y, width, height, **kwargs):
        self.size_x = width
        self.size_y = height

    def get_position(self):
        return self.screen_x, self.screen_y

    def set_screen_position(self):
        x, y = self.pan_zoom.world_2_screen(self.world_x, self.world_y)

        # set new position
        self.set_position((x - self.get_screen_width() / 2, y - self.get_screen_height() / 2))

        # set new size
        self.set_objects_screen_size()

    def set_objects_screen_size(self):
        # get new_size size
        new_size = (self.size_x * pan_zoom_handler.get_zoom(), self.size_y * pan_zoom_handler.get_zoom())
        if new_size[0] < MIN_IMAGE_ZOOM_SIZE or new_size[1] < MIN_IMAGE_ZOOM_SIZE:
            new_size = (MIN_IMAGE_ZOOM_SIZE, MIN_IMAGE_ZOOM_SIZE)
        if new_size[0] > MAX_IMAGE_ZOOM_SIZE or new_size[1] > MAX_IMAGE_ZOOM_SIZE:
            new_size = (MAX_IMAGE_ZOOM_SIZE, MAX_IMAGE_ZOOM_SIZE)

        # set new image size
        self.image = scale_image_cached(self.image_raw, new_size)

        # set new size
        self.set_screen_width(new_size[0] * pan_zoom_handler.get_zoom())
        self.set_screen_height(new_size[1] * pan_zoom_handler.get_zoom())

    def set_position(self, pos):
        self.screen_x = pos[0]
        self.screen_y = pos[1]
        self.set_center()

    def set_screen_width(self, width):
        self.screen_width = width

    def set_screen_height(self, height):
        self.screen_height = height

    def set_center(self):
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
