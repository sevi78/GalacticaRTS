import pygame

from source.gui.widgets.widget_base_components.image_handler import ImageHandler
from source.gui.widgets.widget_base_components.interaction_handler import InteractionHandler
from source.gui.widgets.widget_base_components.position_handler import PositionHandler
from source.gui.widgets.widget_base_components.text_handler import TextHandler
from source.gui.widgets.widget_base_components.visibilty_handler import VisibilityHandler
from source.gui.widgets.widget_base_components.widget_base_methods import WidgetBaseMethods
from source.gui.widgets.widget_handler import WidgetHandler


class WidgetBase(WidgetBaseMethods, ImageHandler, TextHandler, PositionHandler, InteractionHandler, VisibilityHandler):
    """Main functionalities:
    The WidgetBase class is a base class for all widgets in a GUI. It provides common functionality for widgets such as
    handling position, size, visibility, and disabling. It also provides methods for loading settings, drawing,
    and listening for events. Additionally, it includes methods for handling orbiting and zooming.

    Methods:
    - __init__: Initializes the widget with a surface to draw on, position, size, and other optional properties.
    - load_settings: Loads settings from a file and applies them to the widget and all other widgets.
    - listen: Abstract method for handling events.
    - draw: Abstract method for drawing the widget.
    - contains: Checks if a given point is within the bounds of the widget.
    - hide: Hides the widget.
    - show: Shows the widget.
    - disable: Disables the widget.
    - enable: Enables the widget.
    - moveX: Moves the widget horizontally.
    - moveY: Moves the widget vertically.
    - get: Gets the value of a given attribute.
    - get_screen_x: Gets the x-coordinate of the widget.
    - get_screen_y: Gets the y-coordinate of the widget.
    - get_position: Gets the position of the widget as a tuple.
    - get_screen_width: Gets the width of the widget.
    - get_screen_height: Gets the height of the widget.
    - isVisible: Checks if the widget is visible.
    - isEnabled: Checks if the widget is enabled.
    - set: Sets the value of a given attribute.
    - setX: Sets the x-coordinate of the widget.
    - setY: Sets the y-coordinate of the widget.
    - setWidth: Sets the width of the widget.
    - setHeight: Sets the height of the widget.
    - setIsSubWidget: Sets whether the widget is a sub-widget.
    - set_orbit_object_id: Sets the ID of the object to orbit around.
    - set_orbit_object: Sets the object to orbit around.
    - set_orbit_distance: Sets the distance to the object being orbited.
    - orbit: Calculates the position of the widget in orbit around another object.
    - set_screen_position: Sets the position of the widget on the screen.
    - set_objects_screen_size: Scales the size of the widget based on the zoom level.

    Fields:
    - win: The surface to draw the widget on.
    - x: The x-coordinate of the widget.
    - y: The y-coordinate of the widget.
    - _x: The internal x-coordinate of the widget.
    - _y: The internal y-coordinate of the widget.
    - _width: The width of the widget.
    - _height: The height of the widget.
    - _isSubWidget: Whether the widget is a sub-widget.
    - size_x: The width of the widget.
    - size_y: The height of the widget.
    - enable_orbit: Whether orbiting is enabled.
    - orbit_distance: The distance to the object being orbited.
    - orbit_speed: The speed of orbiting.
    - orbit_angle: The angle of orbiting.
    - offset: The offset of the widget from the object being orbited.
    - _hidden: Whether the widget is hidden.
    - _disabled: Whether the widget is disabled.
    - zoomable: Whether the widget is zoomable.
    - property: The property of the widget.
    - layer: The layer of the widget.
    - layers: The layers of the widget.
    - image: The image of the widget.
    - image_raw: The raw image of the widget.
    - debug: Whether debug mode is enabled."""
    # __slots__ = ('world_width', 'world_height', 'screen_width', 'screen_height', 'world_x', 'world_y', 'screen_x', 'screen_y', 'pos', 'center', 'size_x', 'size_y', 'zoomable')
    # __slots__ += ('image', 'image_raw', 'rect', '_image_name_small', 'image_name_big')
    # __slots__ += ('_on_hover', 'on_hover_release')
    # __slots__ += ('_isSubWidget', '_hidden', '_disabled', 'layer', 'layers', 'widgets')
    # __slots__ += ('name', 'win', 'zoomable', 'property', 'debug', 'parent', 'key', 'id', 'children', 'info_text', 'frame_color', 'widgets')

    __slots__ = ('world_width', 'world_height', 'screen_width', 'screen_height', 'world_x', 'world_y', 'screen_x',
                 'screen_y', 'pos', 'center', 'size_x', 'size_y', 'zoomable', 'image', 'image_raw', 'rect',
                 '_image_name_small', 'image_name_big', '_on_hover', 'on_hover_release', '_isSubWidget', '_hidden',
                 '_disabled', 'layer', 'layers', 'widgets', 'name', 'win', 'property', 'debug', 'parent', 'key', 'id',
                 'children', 'info_text', 'frame_color')

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        """ Base for all widgets

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        """

        WidgetBaseMethods.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        ImageHandler.__init__(self, **kwargs)
        PositionHandler.__init__(self, x, y, width, height, **kwargs)
        TextHandler.__init__(self, **kwargs)
        InteractionHandler.__init__(self)
        VisibilityHandler.__init__(self, **kwargs)

        WidgetHandler.addWidget(self)

        # print (self,self.__dict__, self.__slots__)
