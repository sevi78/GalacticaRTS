import math

from pygame import Vector2

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import scale_image_cached

MIN_IMAGE_ZOOM_SIZE = 1
MAX_IMAGE_ZOOM_SIZE = 1000


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
            if not level_of_detail.inside_screen(self.get_position()):
                return

        panzoom = pan_zoom_handler

        # get new_size size
        if self.zoomable:
            new_size = (self.size_x * panzoom.zoom, self.size_y * panzoom.zoom)
        else:
            new_size = (self.size_x, self.size_y)

        if new_size[0] < MIN_IMAGE_ZOOM_SIZE or new_size[1] < MIN_IMAGE_ZOOM_SIZE:
            new_size = (MIN_IMAGE_ZOOM_SIZE, MIN_IMAGE_ZOOM_SIZE)
        if new_size[0] > MAX_IMAGE_ZOOM_SIZE or new_size[1] > MAX_IMAGE_ZOOM_SIZE:
            new_size = (MAX_IMAGE_ZOOM_SIZE, MAX_IMAGE_ZOOM_SIZE)

        # set new image size
        # if hasattr(self, "image_raw") and hasattr(self, "image"):
        if self.image:
            self.image = scale_image_cached(self.image_raw, new_size)

        if hasattr(self, "atmosphere"):
            if self.atmosphere:
                self.atmosphere = scale_image_cached(self.atmosphere_raw, new_size)

        # set new size
        self.set_screen_width(new_size[0] * panzoom.zoom)
        self.set_screen_height(new_size[1] * panzoom.zoom)

    def get_zoom(self):
        if config.app:
            return pan_zoom_handler.zoom
        else:
            return 1

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

    def calculate_grid(self, item_amount, width, height):
        """Calculate the optimal grid size and item size based on the number of items and display surface dimensions."""
        columns = math.ceil(math.sqrt(item_amount))
        rows = math.ceil(item_amount / columns)

        # Adjust rows and columns to fit the items optimally
        while columns * rows < item_amount:
            if columns <= rows:
                columns += 1
            else:
                rows += 1

        # Ensure items are square and maintain the aspect ratio of the display surface
        item_size = min(width // columns, height // rows)
        item_width = item_size
        item_height = item_size

        return rows, columns, item_width, item_height
