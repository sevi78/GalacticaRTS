import copy

import pygame

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, outline_image, scale_image_cached


class ContainerWidgetItemButton:
    def __init__(self, win, x, y, width, height, name, image_name, container_name, function, **kwargs):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

        self.init_image(image_name)

        # self.image_name = image_name
        #
        # self.image = scale_image_cached(get_image(self.image_name), (self.width, self.height))
        # self.image_raw = copy.copy(self.image)
        # self.image_outlined = outline_image(copy.copy(self.image), colors.frame_color, 0, 1)
        self.rect = self.image.get_rect()
        self.parent = None
        self.container_name = container_name
        self.container = kwargs.get("container", None)
        self.tooltip = kwargs.get("tooltip", "")
        self.function = function
        self._disabled = False

    def __repr__(self):
        return f"ContainerWidgetItemButton: name:{self.name}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, image_name: {self.image_name}\n"

    def init_image(self, image_name):
        self.image_name = image_name
        self.image = scale_image_cached(get_image(self.image_name), (self.width, self.height))
        self.image_raw = copy.copy(self.image)
        self.image_outlined = outline_image(copy.copy(self.image), colors.frame_color, 0, 1)

    def set_image(self, outline):
        if outline:
            self.image = self.image_outlined
        else:
            self.image = self.image_raw

    def set_position(self, position):
        if not self.parent:
            if not hasattr(config.app, self.container_name):
                return
        else:
            if not hasattr(config.app, self.container_name):
                # self.container = self.parent.parent.container
                x, y = position
                self.x = x + self.container.rect.x + self.container.rect.width - (
                        (self.parent.item_buttons.index(self) + 1) * (self.height + 10))
                self.y = y + self.container.rect.y
                self.rect.x = self.x
                self.rect.y = self.y
                return

        self.container = getattr(config.app, self.container_name)
        x, y = position
        self.x = x + self.container.rect.x + self.container.rect.width - (
                (self.parent.item_buttons.index(self) + 1) * (self.height + 10))
        self.y = y + self.container.rect.y
        self.rect.x = self.x
        self.rect.y = self.y

    def disable(self):
        self._disabled = True

    def listen(self, events):
        if self._disabled:
            return

        if self.parent:
            self.set_position(self.parent.rect.topleft)

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.image_outlined
                if self.tooltip != "":
                    config.tooltip_text = self.tooltip

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        getattr(self, "function")()
            else:
                self.image = self.image_raw

    def draw(self):
        if self._disabled:
            return

        if self.container:
            x = self.rect.x - self.container.rect.x
            y = self.rect.y - self.container.rect.y
            self.win.blit(self.image, (x, y))
