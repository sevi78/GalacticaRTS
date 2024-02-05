import pygame

from source.configuration import global_params
from source.handlers.pan_zoom_handler import pan_zoom_handler


class PanZoomMouseHandler:
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

    def draw_hover_circle(self):
        panzoom = pan_zoom_handler
        pygame.draw.circle(
            self.win,
            self.frame_color,
            self.rect.center,
            (self.rect.height / 2) + 4, int(6 * panzoom.zoom))
