import pygame

from source.utils import global_params
from source.utils.colors import colors


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

        if var:
            if getattr(global_params, var):
                setattr(global_params, var, False)
            else:
                setattr(global_params, var, True)

        if getattr(global_params, key):
            setattr(global_params, key, False)
        else:
            setattr(global_params, key, True)

    def draw_hover_rect(self):
        pygame.draw.rect(self.win, colors.ui_dark, (
        self.get_screen_x(), self.get_screen_y(), self.get_screen_width() + 3, self.get_screen_height() + 3), 2, 3)
