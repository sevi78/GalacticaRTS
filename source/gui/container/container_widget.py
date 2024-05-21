import copy
import math

import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.widgets.frame import Frame
from source.gui.widgets.scroll_bar import ScrollBar
from source.handlers.mouse_handler import mouse_handler
from source.handlers.widget_handler import WidgetHandler
from source.interaction.interaction_handler import InteractionHandler

SCROLL_STEP = 25


class ContainerWidget(InteractionHandler):
    """
    The ContainerWidget class is a subclass of the InteractionHandler class and represents a container widget that can
    hold multiple child widgets. It provides functionalities for scrolling, dragging, and selecting widgets.
    Example Usage
    # Create a container widget
    container = ContainerWidget(win, x, y, width, height, widgets, function, parent=parent_widget)

    # Set the widgets of the container
    container.set_widgets(widgets)

    # Listen for events and update the container
    container.listen(events)

    # Draw the container and its widgets
    container.draw()
    Code Analysis
    Main functionalities
    Manages the position and size of the container and its child widgets
    Allows scrolling through the widgets using a scrollbar
    Enables dragging of the container and its child widgets
    Handles selection of widgets and executes a specified function when selected

    Methods
    __init__(self, win, x, y, width, height, widgets, function, **kwargs): Initializes the container widget with the
    specified parameters and optional keyword arguments.
    set_widgets(self, widgets): Sets the widgets of the container and resets offset values.
    set_x(self, value): Sets the x-coordinate of the container.
    set_y(self, value): Sets the y-coordinate of the container.
    get_max_scroll_y(self) -> int: Calculates and returns the maximum scroll position in the y-direction.
    get_scroll_step(self) -> int: Returns the scroll step size.
    select(self): Executes the specified function when a widget is selected.
    reposition_widgets(self): Repositions the child widgets based on the current scroll offset.
    draw_widgets(self): Draws the child widgets onto the container's surface.
    set_visible(self): Toggles the visibility of the container and its child widgets.
    reposition(self, x, y): Repositions the container and its components.
    update_scroll_position_from_scrollbar(self, scrollbar_value): Updates the scroll position based on the scrollbar value.
    listen(self, events): Listens for events and handles scrolling, hovering, dragging, and selection.
    draw(self): Draws the container and its components onto the window.

    Fields
    win: The window surface on which the container is drawn.
    world_x: The x-coordinate of the container in the world space.
    world_y: The y-coordinate of the container in the world space.
    world_width: The width of the container in the world space.
    world_height: The height of the container in the world space.
    widgets: The list of child widgets contained in the container.
    function: The function to be executed when a widget is selected.
    parent: The parent widget of the container.
    group: The group to which the container belongs.
    layer: The layer of the container.
    name: The name of the container.
    list_name: The name of the container in a list.
    filters: The list of filters applied to the container.
    filter_widget: The filter widget associated with the container.
    isSubWidget: A flag indicating if the container is a sub-widget.
    _hidden: A flag indicating if the container is hidden.
    surface: The surface on which the container and its child widgets are drawn.
    rect: The rectangle representing the position and size of the container.
    scroll_x: The current scroll position in the x-direction.
    scroll_y: The current scroll position in the y-direction.
    scroll_factor: The scroll step size.
    scroll_offset_x: The offset of the scroll position in the x-direction.
    scroll_offset_y: The offset of the scroll position in the y-direction.
    max_scroll_y: The maximum scroll position in the y-direction.
    frame_border: The border size of the container frame.
    frame: The frame widget that surrounds the container.
    scrollbar: The scrollbar widget associated with the container.
    save: A flag indicating if the container should be saved.
    """

    def __init__(self, win, x, y, width, height, widgets, function, **kwargs):
        """
        Initializes a new instance of the ContainerWidget class.

        Parameters:
            win (pygame.Surface): The surface on which the container will be drawn.
            x (int): The x-coordinate of the container's position.
            y (int): The y-coordinate of the container's position.
            width (int): The width of the container.
            height (int): The height of the container.
            widgets (list): The list of widgets to be added to the container.
            function (callable): The function to be executed when a widget is selected.
            **kwargs: Optional keyword arguments.
                parent (ContainerWidget): The parent container widget.
                group (str): The group to which the container belongs.
                layer (int): The layer of the container.
                name (str): The name of the container.
                list_name (str): The name of the container's list.
                filters (list): The list of filters to be applied to the container.
                filter_widget (WidgetBase): The widget used for filtering.
                save (bool): Whether to save the container.

        Raises:
            AssertionError: If the widgets list is empty.

        Returns:
            None
        """
        InteractionHandler.__init__(self)
        self.offset_index = 0
        self.offset_y = 0
        self.offset_x = 0
        self.moving = False
        self.drag_enabled = True

        # params
        self.win = win
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height
        self.widgets = widgets
        self.function = function

        assert len(self.widgets) > 0, f"widgets can not be len 0 !"

        # kwargs
        self.parent = kwargs.get("parent", None)
        self.layer = kwargs.get("layer", 10)
        self.name = kwargs.get("name", "container")
        self.list_name = kwargs.get("list_name", None)
        self.filter_widget = kwargs.get("filter_widget", None)
        if self.filter_widget:
            self.filter_widget.parent = self

        self.isSubWidget = True
        self._hidden = True

        # surface
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.set_x(x)
        self.set_y(y)

        # scrolling
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_factor = self.get_scroll_step()
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.visible_index_range = 0
        self.max_scroll_y = self.get_max_scroll_y()

        # frame
        self.frame_border = 10
        self.frame = Frame(self.win,
                0, 0,
                self.world_width + self.frame_border,
                self.world_height + self.frame_border)

        # scrollbar
        self.scrollbar = ScrollBar(win, 0, 0, 5, self.world_height, self)

        # initial positioning maybe not needed
        self.reposition_widgets()

        # register
        WidgetHandler.addWidget(self)

        # save
        self.save = kwargs.get("save", True)

    def set_widgets(self, widgets):
        """ sets the widgets and resets offset values """
        if widgets:
            if not isinstance(widgets[0], ContainerWidgetItem):
                self.set_widgets(
                        [ContainerWidgetItem(
                                self.win,
                                0,
                                WIDGET_SIZE * index,
                                WIDGET_SIZE,
                                WIDGET_SIZE,
                                image=copy.copy(_.image_raw),
                                index=index,
                                obj=_,
                                parent=self)
                            for index, _ in enumerate(widgets)])
            else:
                self.widgets = widgets

        self.offset_index = 0
        self.visible_index_range = 0
        # set offset_y to minus 1 !!!
        self.offset_y = -1
        self.scrollbar.value = 0.0
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_factor = self.get_scroll_step()
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.max_scroll_y = self.get_max_scroll_y()
        self.reposition_widgets()

        # hahahah :) !!! this makes is stay visible --- grotesque :)
        self.set_visible()
        self.set_visible()

    def set_x(self, value):
        self.world_x = value
        self.rect.x = value

    def set_y(self, value):
        self.world_y = value
        self.rect.y = value

    def get_max_scroll_y(self) -> int:
        """
        Get the number of child widgets and the width of the first child widget.
        Calculate the visible index range by dividing the height of the container by the width of the first child widget
        (self.rect.height) and rounding down (math.floor(self.rect.height / size)).
        Calculate the maximum scroll position in the y-direction by subtracting the visible index range from the total
        number of child widgets multiplied by the width of the first child widget ((len_ * size) - self.visible_index_range).
        Return the maximum scroll position.
        """
        len_ = len(self.widgets)
        size = self.widgets[0].world_width
        self.visible_index_range = math.floor(self.rect.height / size)
        max_scroll_y = (len_ * size) - self.visible_index_range
        return max_scroll_y

    def get_scroll_step(self) -> int:
        """
        The method retrieves the first child widget from the widgets list.
        It returns the height of the first child widget.
        """
        return self.widgets[0].world_height

    def select(self):
        # call the function
        if hasattr(self, "function"):
            if callable(self.function):
                getattr(self, "function")(self)

    def set_visible(self):
        self._hidden = not self._hidden
        # self.world_x, self.world_y = pygame.mouse.get_pos()[0], TOP_SPACING

        if self.filter_widget:
            if self._hidden:
                self.filter_widget.hide()
            else:
                self.filter_widget.show()

    def reposition(self, x, y):
        """
        The reposition method is responsible for repositioning the container and its components based on the specified
        x and y coordinates.
        """
        # set rect position
        self.rect.x = self.world_x
        self.rect.y = self.world_y
        if self.parent:
            self.rect.x = self.parent.rect.x
            self.rect.y = self.parent.rect.y

        # set surface position
        self.surface.get_rect().x = self.rect.x
        self.surface.get_rect().y = self.rect.y

        # set frame position
        self.frame.update_position((self.world_x, self.world_y))

        # scrollbar
        self.scrollbar.update_position()

        # filter widget
        if self.filter_widget:
            self.filter_widget.world_x = self.rect.x + self.rect.width - self.filter_widget.screen_width - 10
            self.filter_widget.world_y = self.rect.y - TOP_SPACING

    def reposition_widgets(self):
        """
        The reposition_widgets method is responsible for repositioning the child widgets of the container based on the
        current scroll offset.
        """
        # Check if the scroll offset is within the range of the number of widgets
        if not self.scroll_offset_y in range(-len(self.widgets), len(self.widgets)):
            return

        for widget in self.widgets:
            widget.win = self.surface
            widget.x = self.surface.get_rect().x
            widget.y = (self.widgets.index(widget) + self.scroll_offset_y) * widget.world_height

            # Apply the calculated position
            widget.set_position((widget.x, widget.y))

    def update_scroll_position_from_scrollbar(self, scrollbar_value):
        """
        The update_scroll_position_from_scrollbar method is responsible for updating the scroll position of the
        container based on the value of the scrollbar. It calculates the new scroll offset in the y-direction and
        repositions the child widgets accordingly.
        """
        self.scroll_offset_y = math.floor((len(self.widgets) - self.visible_index_range + 1) * scrollbar_value) * -1
        self.reposition_widgets()  # Reposition widgets based on the new scroll offset

    def draw_widgets(self):
        for widget in self.widgets:
            widget.draw()

    def listen(self, events):
        if self._hidden:
            return

        # all widgets listen
        self.scrollbar.listen(events)

        # set hovering
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover = True
            if config.app:
                config.app.cursor.set_cursor("scroll")
        else:
            self.on_hover = False

        # drag
        self.drag(events)

        # handle events
        for event in events:
            # scroll
            if event.type == pygame.MOUSEWHEEL:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll_y = event.y  # -1 , 0 , 1

                    if self.scroll_offset_y + self.scroll_y in range(-(
                            len(self.widgets) - self.visible_index_range), 1):
                        self.scroll_offset_y += self.scroll_y
                        self.scrollbar.value = abs(1 / (
                                len(self.widgets) - self.visible_index_range + 1) * self.scroll_offset_y)

                        self.reposition_widgets()

                        # set cursor
                        if config.app:
                            if event.y > 0:
                                config.app.cursor.set_cursor("scroll_up")
                            else:
                                config.app.cursor.set_cursor("scroll_down")

            # select
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        # ensure that only clicks if not hovering over filter widget
                        if self.filter_widget:
                            if self.filter_widget.on_hover:
                                return
                        offset_y = mouse_handler.get_mouse_pos()[1] - self.world_y
                        rel_offset_y = offset_y - (self.scroll_offset_y * WIDGET_SIZE)
                        offset_index = math.floor(rel_offset_y / WIDGET_SIZE)

                        self.offset_index = offset_index
                        self.select()

        # hover
        for i in self.widgets:
            if not i.parent:
                i.parent = self

    def draw(self):
        if self._hidden:
            return

        # fill surface
        self.surface.fill((0, 123, 0))  # Clear the container's surface

        # draw frame
        self.frame.draw()
        self.surface.blit(self.frame.surface, (0, 0))

        # draw widgets
        self.draw_widgets()  # Draw the widgets onto the container's surface
        self.win.blit(self.surface, self.rect)

        # draw scrollbar
        self.scrollbar.draw()
