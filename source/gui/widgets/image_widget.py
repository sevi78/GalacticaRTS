import copy

import pygame
import pygame.sprite

from source.handlers.pan_zoom_sprite_handler import sprite_groups


class ImageSprite:
    """ simplest class to display an image on screen"""

    def __init__(self, win, x, y, width, height, image, **kwargs):
        # define image_raw, to ensure scaling does not pixelize the image
        self.win = win
        self.image_raw = image

        # scale image
        self.image = pygame.transform.scale(copy.copy(self.image_raw), (width, height))
        self.rect = self.image.get_rect()

        # set initial position
        self.set_position(x, y, "center")

        # initialize kwargs
        self.parent = kwargs.pop("parent", None)
        self.layer = kwargs.pop("layer", 8)
        self.image_alpha = kwargs.pop("image_alpha", None)

        # set _hidden variable to ensure objet can be hidden
        self._hidden = kwargs.get("hidden", False)


    def show(self):
        self._hidden = False

    def hide(self):
        self._hidden = True

    def set_image(self, image):
        self.image_raw = image
        self.image = image

    def set_position(self, x, y, align):
        setattr(self.rect, align, (x, y))

    def draw(self):
        if not self._hidden:
            self.win.blit(self.image, self.rect)
