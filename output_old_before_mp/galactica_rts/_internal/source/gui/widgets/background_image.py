import pygame

from source.configuration.game_config import config
from source.draw.gradient_background import draw_gradient
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class BackgroundImage(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 0)
        self.surface = pygame.Surface((config.width, config.height))
        self.surface.set_colorkey((60, 60, 60))
        self.surface.set_alpha(0)
        self.image = kwargs.get("image", None)
        self.image = pygame.transform.scale(self.image, (self.win.get_width(), self.win.get_height()))
        self.color = colors.background_color

    def draw(self):
        if config.draw_background_image:
            self.win.blit(self.image, (self.world_x, self.world_y))
        else:
            pygame.draw.rect(self.win, self.color, (0, 0, self.screen_width, self.screen_height))


class BackgroundGradient(WidgetBase):  # bad performance
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 8)
        self.draw_gradient = kwargs.get("draw_gradient", True)
        self.fade_range = kwargs.get("fade_range", 50)

        # set images
        self.image_left = pygame.transform.scale(get_image("gradient_transparent_left.png"), (self.fade_range, height))
        self.image_right = pygame.transform.scale(get_image("gradient_transparent_right.png"), (
            self.fade_range, height))
        self.image_top = pygame.transform.scale(get_image("gradient_transparent_top.png"), (
            width - (self.fade_range * 2), self.fade_range))
        self.image_bottom = pygame.transform.scale(get_image("gradient_transparent_bottom.png"), (
            width - (self.fade_range * 2), self.fade_range))

        # set image positions
        self.image_left_pos = (x, y)
        self.image_right_pos = (win.get_width() - self.image_right.get_width(), y)
        self.image_top_pos = (self.image_top.get_height(), y)
        self.image_bottom_pos = (self.image_bottom.get_height(), win.get_height() - self.image_bottom.get_height())

    def draw(self):
        if not self.draw_gradient:
            return

        self.win.blit(self.image_left, self.image_left_pos)
        self.win.blit(self.image_right, self.image_right_pos)
        self.win.blit(self.image_top, self.image_top_pos)
        self.win.blit(self.image_bottom, self.image_bottom_pos)

        # pygame.draw.rect(self.win, colors.frame_color, (self.image_left_pos[0], self.image_left_pos[1], self.image_left.get_width(), self.image_left.get_height()), 1)
        # pygame.draw.rect(self.win, colors.frame_color, (self.image_right_pos[0], self.image_right_pos[1], self.image_right.get_width(), self.image_right.get_height()), 1)
        # pygame.draw.rect(self.win, colors.frame_color, (self.image_top_pos[0], self.image_top_pos[1], self.image_top.get_width(), self.image_top.get_height()), 1)
        # pygame.draw.rect(self.win, colors.frame_color, (self.image_bottom_pos[0], self.image_bottom_pos[1], self.image_bottom.get_width(),self.image_bottom.get_height()), 1)


class BackgroundGradient_ki(WidgetBase):  # doesnt work at all
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 10)
        self.draw_gradient = kwargs.get("draw_gradient", True)
        self.fade_range = kwargs.get("fade_range", 100)

    def draw(self):
        if not self.draw_gradient:
            return

        draw_gradient(self.win, self.world_x, self.world_y, self.world_width, self.world_height, self.fade_range, colors.frame_color)
