import pygame

from source.utils import global_params


class TextHandler:
    def __init__(self, **kwargs):
        pass

    def alignTextRect(self):

        self.textRect.center = (self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height // 2)

        if self.textHAlign == 'left':
            self.textRect.left = self.screen_x + self.margin
        elif self.textHAlign == 'right':
            self.textRect.right = self.screen_x + self.screen_width - self.margin

        if self.textVAlign == 'top':
            self.textRect.top = self.screen_y + self.margin
        elif self.textVAlign == 'bottom':
            self.textRect.bottom = self.screen_y + self.screen_height - self.margin

        elif self.textVAlign == 'over_the_top':
            self.textRect.bottom = self.screen_y - self.margin // 2
        elif self.textVAlign == 'below_the_bottom':
            # self.textRect.bottom = self.screen_y + self.margin // 2
            # self.textRect.bottom = self.screen_y + self.get_screen_height() + (self.margin // 2)
            self.textRect.bottom = self.center[1] + self.screen_height / 2
