from abc import ABC, abstractmethod

import pygame

from source.configuration.game_config import config
from source.draw.rectangle import draw_transparent_rounded_rect
from source.handlers.color_handler import colors
from source.handlers.widget_handler import WidgetHandler


class WidgetBaseMethods(ABC):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        """
            Initialize a new widget instance.

            This constructor sets up the basic properties of a widget, including its position,
            size, and various optional attributes.

            Args:
                win (pygame.Surface): The surface on which the widget will be drawn.
                x (int): The x-coordinate of the widget's top-left corner.
                y (int): The y-coordinate of the widget's top-left corner.
                width (int): The width of the widget.
                height (int): The height of the widget.
                is_sub_widget (bool, optional): Indicates if this widget is a sub-widget of another. Defaults to False.

            Keyword Args:
                name (str, optional): The name of the widget. Defaults to the class name.
                property (any, optional): A custom property for the widget. Defaults to None.
                debug (bool, optional): Enable debug mode for the widget. Defaults to False.
                parent (object, optional): The parent object of this widget. Defaults to None.
                key (any, optional): A key identifier for the widget. Defaults to None.
                id (any, optional): An ID for the widget. Defaults to None.
                info_text (str, optional): Information text associated with the widget. Defaults to an empty string.
                info_panel_alpha (int, optional): Alpha value for the info panel. Defaults to 255.

            Attributes:
                zoomable (bool): Indicates if the widget can be zoomed. Set to False.
                children (list): A list to store child widgets.
                widgets (list): A list to store associated widgets.
                frame_color (tuple): The color of the widget's frame. Set to colors.frame_color.

            Note:
                This method assumes the existence of a 'colors' module or object with a 'frame_color' attribute.
            """
        self.name = kwargs.get("name", self.__class__.__name__)
        self.win = win
        self.zoomable = False
        self.property = kwargs.get("property", None)
        self.debug = kwargs.get("debug", False)
        self.parent = kwargs.get("parent", None)
        self.key = kwargs.get("key", None)
        self.id = kwargs.get("id", None)
        self.children = []
        self.info_text = kwargs.get("info_text", "")
        self.frame_color = colors.frame_color
        self.info_panel_alpha = kwargs.get("info_panel_alpha", 255)

        #  widgets
        self.widgets = []

    def __repr__(self):
        return f'{type(self).__name__}(x = {self.screen_x}, y = {self.screen_y}, width = {self.screen_width}, height = {self.screen_height})'

    def __del__(self):
        """ pffff  how to clean delete ?? still some junk in the memory """
        for key, widget_list in WidgetHandler.layers.items():
            if self in widget_list:
                widget_list.remove(self)

        for i in self.widgets:
            i.__del__()

        if hasattr(self, 'editors'):
            for i in self.editors:
                i.__del__()

        # garbage_handler.delete_all_references(self,self)
        # garbage_handler.delete_references(self)

    def set_screen_size(self, screen_size):
        self.screen_size = screen_size

    def get(self, attr):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to get
        :return: Value of the attribute
        """
        if attr == 'x':
            return self.screen_x

        if attr == 'y':
            return self.screen_y

        if attr == 'width':
            return self.screen_width

        if attr == 'height':
            return self.screen_height

    def is_enabled(self):
        return not self._disabled

    def set(self, attr, value):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to set
        :param value: Value to set
        """
        if attr == 'x':
            self.screen_x = value

        if attr == 'y':
            self.screen_y = value

        if attr == 'width':
            self.screen_width = value

        if attr == 'height':
            self.screen_height = value

    def draw_frame(self, **kwargs):
        image = kwargs.get('image', None)
        rect = kwargs.get('rect', None)

        rect_surface = draw_transparent_rounded_rect(self.win, (0, 0, 0), self.surface_rect,
                config.ui_rounded_corner_radius_small, config.ui_panel_alpha)

        if image and rect:
            rect_surface.blit(image, rect)
            self.win.blit(rect_surface, self.surface_rect)

        pygame.draw.rect(self.win, self.frame_color, self.surface_rect,
                config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)
        return rect_surface

    @abstractmethod
    def draw(self, **kwargs):
        pass
