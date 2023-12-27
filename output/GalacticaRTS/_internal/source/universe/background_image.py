import pygame

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params
from source.utils.colors import colors


class BackgroundImage(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 0)
        self.surface = pygame.Surface((global_params.WIDTH, global_params.HEIGHT))
        self.surface.set_colorkey((60, 60, 60))
        self.surface.set_alpha(0)
        self.image = kwargs.get("image", None)
        self.image = pygame.transform.scale(self.image, (self.win.get_width(), self.win.get_height()))
        self.color = colors.background_color

    def draw(self):
        if global_params.draw_background_image:
            self.win.blit(self.image, (self.world_x, self.world_y))
        else:
            pygame.draw.rect(self.win, self.color, (0, 0, self.screen_width, self.screen_height))
