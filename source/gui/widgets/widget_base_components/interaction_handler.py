import pygame

from source.configuration import global_params
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class InteractionHandler:
    def __init__(self):
        self._on_hover = False
        self.on_hover_release = False

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value):
        self._on_hover = value
        if value:
            global_params.hover_object = self
        else:
            if global_params.hover_object == self:
                global_params.hover_object = None

    def on_hover_release_callback(self, x, y, rect):
        if self._hidden or self._disabled:
            return
        if not rect:
            return

        if rect.collidepoint(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False
            return True

        return False

    def set_global_variable(self, key, value, **kwargs):
        var = kwargs.get("var", None)
        button = kwargs.get("button", None)

        if var:
            if getattr(global_params, var):
                setattr(global_params, var, False)
            else:
                setattr(global_params, var, True)

        if getattr(global_params, key):
            setattr(global_params, key, False)

        else:
            setattr(global_params, key, True)

        self.overblit_button_image(button, "uncheck.png", getattr(global_params, key))

    def overblit_button_image(self, button, image_name, value):
        if not button:
            return
        if not value:
            size = (button.image.get_rect().width, button.image.get_rect().height)
            button.image.blit(pygame.transform.scale(get_image(image_name), size), (0, 0))  # Scale and blit the image
        else:
            # Restore the original image before overblitting
            button.image.fill((0, 0, 0, 0))  # Fill with transparent black
            button.image.blit(button.image_raw, (0, 0))  # Blit the original image

    def draw_hover_rect(self):
        pygame.draw.rect(self.win, colors.ui_dark, (
            self.get_screen_x(), self.get_screen_y(), self.get_screen_width() + 3, self.get_screen_height() + 3), 2, 3)
