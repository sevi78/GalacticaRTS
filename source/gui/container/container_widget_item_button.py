import copy

import pygame

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, outline_image


class ContainerWidgetItemButton:
    def __init__(self, win, x, y, width, height, name, image_name, container_name, function):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.image_name = image_name

        self.image = pygame.transform.scale(get_image(self.image_name), (self.width, self.height))
        self.image_raw = copy.copy(self.image)
        self.image_outlined = outline_image(copy.copy(self.image), colors.frame_color, 0, 1)
        self.rect = self.image.get_rect()
        self.parent = None
        self.container_name = container_name
        self.container = None
        self.function = function

    def __repr__(self):
        return f"ContainerWidgetItemButton: name:{self.name}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, image_name: {self.image_name}\n"

    def set_image(self, outline):
        if outline:
            self.image = self.image_outlined
        else:
            self.image = self.image_raw

    def set_position(self, position):
        if not self.parent or not hasattr(config.app, self.container_name):
            return

        self.container = getattr(config.app, self.container_name)
        x, y = position
        self.x = x + self.container.rect.x + self.container.rect.width - (
                    (self.parent.item_buttons.index(self) + 1) * (self.height + 10))
        self.y = y + self.container.rect.y
        self.rect.x = self.x
        self.rect.y = self.y

    def listen(self, events):
        if self.parent:
            self.set_position(self.parent.rect.topleft)

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.image_outlined

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        getattr(self, "function")()
            else:
                self.image = self.image_raw

    def draw(self):
        if self.container:
            x = self.rect.x - self.container.rect.x
            y = self.rect.y - self.container.rect.y
            self.win.blit(self.image, (x, y))
