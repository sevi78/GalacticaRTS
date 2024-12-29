import copy

import pygame

from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import scale_image_cached


class ImageSprite(pygame.sprite.Sprite):
    """ simplest class to display an image on screen"""

    def __init__(self, win, x, y, width, height, image, **kwargs):
        super().__init__()
        # define image_raw, to ensure scaling does not pixelize the image
        self.win = win
        self.image_raw = image

        # scale image
        self.image = scale_image_cached(copy.copy(self.image_raw), (width, height))
        self.rect = self.image.get_rect()

        # set initial position
        self.set_position(x, y, "center")

        # initialize kwargs
        self.parent = kwargs.pop("parent", None)
        self.layer = kwargs.pop("layer", 4)
        self.image_alpha = kwargs.pop("image_alpha", None)

        # set _hidden variable to ensure objet can be hidden
        self._hidden = kwargs.get("hidden", False)
        sprite_groups.state_images.add(self)

    def end_object(self):
        sprite_groups.state_images.remove(self)
        self.kill()

    def show(self):
        self._hidden = False

    def hide(self):
        self._hidden = True

    def set_image(self, image):
        self.image_raw = image
        self.image = image

    def set_position(self, x, y, align):
        setattr(self.rect, align, (x, y))
