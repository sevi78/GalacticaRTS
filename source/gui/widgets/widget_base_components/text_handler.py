import pygame

from source.configuration.game_config import config
from source.handlers.color_handler import colors


class TextHandler:
    def __init__(self, **kwargs):
        pass

    def set_text(self, text):
        self.string = text
        self.text = self.font.render(self.string, True, self.text_color)
        self.align_text_rect()

    def align_text_rect(self):
        self.text_rect.center = (self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height // 2)

        if self.text_h_align == 'left':
            self.text_rect.left = self.screen_x + self.margin

        if self.text_h_align == 'left_outside':
            self.text_rect.left = self.screen_x + self.screen_width + self.margin

        elif self.text_h_align == 'right':
            self.text_rect.right = self.screen_x + self.screen_width - self.margin

        elif self.text_h_align == 'right_outside':
            self.text_rect.right = self.screen_x + self.screen_width * 2

        if self.text_v_align == 'top':
            self.text_rect.top = self.screen_y + self.margin
        elif self.text_v_align == 'bottom':
            self.text_rect.bottom = self.screen_y + self.screen_height - self.margin

        elif self.text_v_align == 'over_the_top':
            self.text_rect.bottom = self.screen_y - self.margin // 2

        elif self.text_v_align == 'below_the_bottom':
            self.text_rect.bottom = self.center[1] + self.screen_height / 2 + self.font_size

    def draw_text(self, x, y, width, height, text, **kwargs):
        """ draws text:
        kwargs:
        win = the surface to draw on
        font = the font to use, default is config.font_name

        """
        win = kwargs.get("win", self.win)
        font = kwargs.get("font", pygame.font.SysFont(config.font_name, height - 1))

        text = font.render(text, 1, self.frame_color)
        win.blit(text, (x, y))
