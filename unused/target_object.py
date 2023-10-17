import pygame
from pygame_widgets import Mouse
from pygame_widgets.mouse import MouseState

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler


class TargetObject(WidgetBase):
    """Main functionalities:
    The TargetObject class is a subclass of WidgetBase and represents a target object that can be moved.
    It has a center point, x and y coordinates, width and height, and can be a sub-widget.
    It listens to mouse events and can be moved by right-clicking. It can also be drawn on the screen as a circle with a
    frame color.

    Methods:
    - set_center(): sets the center point of the target object based on its x, y, width, and height.
    - listen(events): listens to mouse events and moves the target object if right-clicked.
    - set_position(): sets the x and y coordinates of the target object based on the current mouse position.
    - draw(**kwargs): draws the target object on the screen as a circle with a frame color.

    Fields:
    - x: the x coordinate of the target object.
    - y: the y coordinate of the target object.
    - _x: the initial x coordinate of the target object.
    - _y: the initial y coordinate of the target object.
    - width: the width of the target object.
    - height: the height of the target object.
    - zoomable: a boolean indicating whether the target object can be zoomed in/out.
    - moveable: a boolean indicating whether the target object can be moved.
    - parent: the parent widget of the target object.
    - center: the center point of the target object.
    - property: a string indicating the type of widget.
    - init: a boolean indicating whether the target object has been initialized.
    - name: the name of the target object."""

    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        self.world_x = x
        self.world_y = y
        self.screen_x = x
        self.screen_y = y
        self.world_width = width
        self.height = height
        self.zoomable = True
        self.moveable = True
        self.parent = kwargs.get("parent")
        self.center = (self.screen_x, self.screen_y)
        self.property = "target_object"
        self.init = False
        self.name = "target_object"
        self.layer = kwargs.get("layer", 3)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            if mouseState == MouseState.RIGHT_CLICK:
                if not self.parent.moving:
                    self.set_world_position()

    def set_world_position(self):
        self.world_x, self.world_y = pan_zoom_handler.screen_2_world(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def draw(self, **kwargs):
        if not self.parent.target or self.parent.target != self:
            return

        panzoom = pan_zoom_handler
        x, y = panzoom.world_2_screen(self.world_x, self.world_y)

        self.set_position((x, y))

        self.setWidth(self.world_width * panzoom.zoom)
        pygame.draw.circle(self.win, self.frame_color, (
            self.screen_x + self.get_screen_width() / 2,
            self.screen_y + self.get_screen_height() / 2), self.get_screen_width(), 1)
        pygame.draw.circle(self.win, self.frame_color, (
            self.screen_x + self.get_screen_width() / 2,
            self.screen_y + self.get_screen_height() / 2), self.get_screen_width() * .75, 1)
