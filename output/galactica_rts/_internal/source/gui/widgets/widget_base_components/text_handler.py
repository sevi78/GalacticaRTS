import pygame

from source.configuration.game_config import config


class TextHandler:
    def __init__(self, **kwargs):
        pass

    def set_text(self, text):
        self.string = text
        self.text = self.font.render(self.string, True, self.textColour)
        self.alignTextRect()

    def alignTextRect(self):

        self.textRect.center = (self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height // 2)

        if self.textHAlign == 'left':
            self.textRect.left = self.screen_x + self.margin

        if self.textHAlign == 'left_outside':
            self.textRect.left = self.screen_x + self.screen_width + self.margin

        elif self.textHAlign == 'right':
            self.textRect.right = self.screen_x + self.screen_width - self.margin

        elif self.textHAlign == 'right_outside':
            self.textRect.right = self.screen_x + self.screen_width * 2

        if self.textVAlign == 'top':
            self.textRect.top = self.screen_y + self.margin
        elif self.textVAlign == 'bottom':
            self.textRect.bottom = self.screen_y + self.screen_height - self.margin

        elif self.textVAlign == 'over_the_top':
            self.textRect.bottom = self.screen_y - self.margin // 2

        elif self.textVAlign == 'below_the_bottom':
            self.textRect.bottom = self.center[1] + self.screen_height / 2 + self.font_size

    def draw_text(self, x, y, width, height, text, **kwargs):
        win = kwargs.get("win", self.win)
        font = kwargs.get("font", pygame.font.SysFont(config.font_name, height - 1))

        text = font.render(text, 1, self.frame_color)
        win.blit(text, (x, y))
