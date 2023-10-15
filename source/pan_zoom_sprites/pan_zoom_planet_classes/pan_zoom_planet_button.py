import pygame

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params


class PanZoomPlanetButton():
    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        pass
        # WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        # self.center = (
        # self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        #
        # # Text
        # self.textColour = kwargs.get('textColour', (0, 0, 0))
        # self.font_name = global_params.font_name
        #self.font_size = kwargs.get('font_size', 20)
        # self.string = kwargs.get('text', '')
        #self.font = kwargs.get('font', pygame.font.SysFont(global_params.font_name, self.font_size))
        # self.text = self.font.render(self.string, True, self.textColour)
        # self.textHAlign = kwargs.get('textHAlign', 'centre')
        # self.textVAlign = kwargs.get('textVAlign', 'centre')
        # self.margin = kwargs.get('margin', 20)
        # self.textRect = self.text.get_rect()
        # # self.alignTextRect()
        # self.text.set_alpha(0)
        #
        # # Image
        # self.radius_extension = kwargs.get('radius_extension', 0)
        # self.transparent = kwargs.get('transparent', False)
        # self.image_hover_surface = pygame.surface.Surface((
        #     width + self.radius_extension, height + self.radius_extension), 0, self.win)
        # self.image_hover_surface.set_alpha(kwargs.get("image_hover_surface_alpha", 0))
        # self.image = kwargs.get('image', None)
        # self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        # self.imageVAlign = kwargs.get('imageVAlign', 'centre')
        #
        # if self.image:
        #     self.rect = self.image.get_rect()
        #     # self.alignImageRect()
        #     self.align_image_rect()
        #
        # # Function
        # self.onClick = kwargs.get('onClick', lambda *args: None)
        # self.onRelease = kwargs.get('onRelease', lambda *args: None)
        # self.onClickParams = kwargs.get('onClickParams', ())
        # self.onReleaseParams = kwargs.get('onReleaseParams', ())
        # self.clicked = False
