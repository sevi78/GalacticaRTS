import inspect

import pygame

from source.configuration.game_config import config
from source.draw.rect import draw_transparent_rounded_rect
from source.editors.editor_base.editor_config import ARROW_SIZE, SPACING_Y, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.selector import Selector
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class EditorBase(WidgetBase):
    """
    The EditorBase class is a base class for editors in a pygame application. It provides methods for setting the
    object to be edited, setting the edit mode, drawing text and frames, and initializing the class with necessary
    parameters.

    Example Usage:
    # Create an instance of the EditorBase class
    editor = EditorBase(win, x, y, width, height)

    # Set the object to be edited
    editor.set_obj(obj)

    # Set the edit mode
    editor.set_edit_mode()

    # Draw text on the window
    editor.draw_text(x, y, width, height, text)

    # Draw a frame on the window
    editor.draw_frame()
    Code Analysis
    Main functionalities
    Initializing the class with necessary parameters
    Setting the object to be edited
    Setting the edit mode
    Drawing text on the window
    Drawing a frame on the window

    Methods:

    __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs): Initializes the class with the window, position,
    size, and other optional parameters.
    set_obj(self, obj): Sets the object to be edited.
    set_edit_mode(self): Sets the edit mode.
    draw_text(self, x, y, width, height, text): Draws text on the window.
    draw_frame(self): Draws a frame on the window.


    args:
    
        win                     the surface to blit on
        x                       The x-coordinate of the editor's position: world_x position
        y                       The y-coordinate of the editor's position.: world_y position
        width                   world_width
        height                  world_height
        isSubWidget             default = False, use this for sub_widgets that need to listen the events

    **kwargs:

        EditorBase:
        obj                     the object to be edited. default None
        parent                  the widgets parent. default None
        layer                   the layer to blit on. default 9
        ignore_other_editors    if set to true, the widget is getting hidden if any other editor is open, default False
        drag_enabled            enables dragging for the editor. default True
        save                    allows the editor to save its position after app quit(use settings_edit to save)
        frame_corner_radius     the radius of the frame_corner, default config.ui_rounded_corner_radius_big
        frame_corner_thickness  the thickness of the frame_corner, default config.ui_rounded_corner_big_thickness
    
    
        WidgetBaseMethods:
        name                    the name of the widget. default __class__.__name__
        property                some property variable. default None
        key                     is used for some Buttons to display images generated
        id                      id of the widget, don't mess around with this
        info_text               if info_text is set, it will send some data to info_panel on_hover
        info_panel_alpha        the alpha value to display the info_panel image send via info_text
    
        ImageHandler:
        image_name_small        the name of the small image to display
        image_name_big          the name of the big image to display
        image                   the image to display (pygame.Surface)
        image_alpha             alpha value for the image
        image_raw               the backup for image, used as non pixelated reference for scaling
        outline_thickness       thickness of the image outline
        outline_threshold       threshold to define the outline


    Fields:

    spacing_x                   The horizontal spacing.
    spacing_y                   The vertical spacing.
    text_spacing                the spacing between frame border and text
    font                        The font used for text.
    frame_color                 The color of the frame.
    frame                       The surface for the frame.
    rect                        the rect of the frame
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self._obj = kwargs.get("obj", None)
        self.obj = kwargs.get("obj", None)
        # self.game_paused = kwargs.get("game_paused", False)

        self.win = win
        self.world_x = x
        self.world_y = y
        self.screen_width = width
        self.screen_height = height
        self.max_height = 0
        self.arrow_size = ARROW_SIZE
        self.spacing_x = width / 2 * .8
        self.spacing_y = SPACING_Y
        self.parent = kwargs.get("parent", None)
        self.ignore_other_editors = kwargs.get("ignore_other_editors", False)
        self.font = pygame.font.SysFont(config.font_name, FONT_SIZE)
        self.text_spacing = 20
        self.frame_color = colors.ui_dark
        self.frame_corner_radius = kwargs.get("frame_corner_radius", config.ui_rounded_corner_radius_big)
        self.frame_corner_thickness = kwargs.get("frame_corner_thickness", config.ui_rounded_corner_big_thickness)
        self.frame = pygame.surface.Surface((self.world_width, self.world_height))
        self.rect = self.frame.get_rect()
        self.rect.x, self.rect.y = self.world_x, self.world_y

        # drag/move
        self.moving = False
        self.drag_enabled = kwargs.get("drag_enabled", True)
        self._on_hover = False

        # register
        self.boolean_list = [True, False]
        self.selector_lists = {}
        self.default_list = [_ for _ in range(100)]

        self.buttons = []
        self.selectors = []
        self.checkboxes = []
        self.checkbox_values = []

        self.editors = []
        if config.app:
            config.app.editors.append(self)

        # save
        self.save = kwargs.get("save", True)

    @property
    def on_hover(self):
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value):
        self._on_hover = value
        if value:
            config.hover_object = self
        else:
            if config.hover_object == self:
                config.hover_object = None

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        self._obj = value
        if hasattr(self, "set_slider_data"):
            self.set_slider_data()

    def set_obj(self, obj):
        self.obj = obj

    def set_edit_mode(self):
        config.edit_mode = not self._hidden
        config.enable_orbit = self._hidden

    def hide_other_editors(self):
        if self.ignore_other_editors:
            return
        for i in self.parent.editors:
            if not i == self:
                if not i.ignore_other_editors:
                    i.hide()

    def set_visible(self):
        # toggle visibility of the editor
        if self._hidden:
            self.show()
        else:
            self.hide()

        # toggle edit_mode
        config.edit_mode = not self._hidden

        # toggle editors attached the editor itself
        for i in self.editors:
            # hide if the editor is hidden
            if self._hidden:
                i.hide()
            else:
                # only show if the attached editor is enabled!
                if i.isEnabled():
                    i.show()

        self.hide_other_editors()

    def create_save_button(self, function, tooltip, **kwargs):
        name = kwargs.get("name", "no_name")
        button_size = 32
        save_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2 - button_size,
                y=self.max_height + button_size / 2,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("save_icon.png"), (button_size, button_size)),
                tooltip=tooltip,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=function,
                name=name
                )
        save_icon.hide()

        self.buttons.append(save_icon)
        self.widgets.append(save_icon)

    def create_load_button(self, function, tooltip, **kwargs):
        name = kwargs.get("name", "no_name")
        button_size = 32
        load_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2 + button_size,
                y=self.max_height + button_size / 2,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("load_icon.png"), (button_size, button_size)),
                tooltip=tooltip,
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=function,
                name=name
                )

        load_button.hide()

        self.buttons.append(load_button)
        self.widgets.append(load_button)

    def create_close_button(self, **kwargs):
        button_size = 32
        x = kwargs.get("x", self.get_screen_x() + self.get_screen_width() - button_size - button_size / 2)
        y = kwargs.get("y", self.world_y + TOP_SPACING + button_size / 2)

        close_icon = ImageButton(win=self.win,
                x=x,
                y=y,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("close_icon.png"), (button_size / 2, button_size / 2)),
                tooltip="close editor",
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: self.close(),
                name="close_button"
                )

        close_icon.hide()

        self.buttons.append(close_icon)
        self.widgets.append(close_icon)

    def create_selectors_from_dict(self, x, y, dict_, **kwargs):
        arrow_size = kwargs.get("arrow_size", ARROW_SIZE)
        font_size = int(arrow_size * .8)
        self.spacing_y = arrow_size * 1.3

        for key, value in dict_:
            # booleans
            if type(value) is bool:
                self.selector_lists[key] = self.boolean_list
                self.selectors.append(Selector(self.win, x, self.world_y + y, arrow_size, self.frame_color, 9,
                        self.spacing_x, {"list_name": f"{key}_list", "list": self.boolean_list}, self, font_size))

                y += self.spacing_y

            # integers
            if type(value) is int:
                if not key in self.selector_lists.keys():
                    self.selector_lists[key] = self.default_list

                self.selectors.append(Selector(self.win, x, self.world_y + y, arrow_size, self.frame_color, 9,
                        self.spacing_x, {"list_name": f"{key}_list", "list": self.selector_lists[key]}, self, font_size,
                        repeat_clicks=False))

                y += self.spacing_y

        # set max height to draw the frame dynamical
        self.max_height = y + arrow_size

    def close(self):
        config.set_global_variable("edit_mode", False)
        # if self.game_paused:
        #     config.game_paused = False

        config.tooltip_text = ""
        # self.hide()
        self.set_visible()

        for i in self.editors:
            i.hide()

    def handle_hovering(self):
        if self._hidden:
            return

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover = True
        else:
            self.on_hover = False

    def is_same_or_subclass(self, other_obj):
        # Check if other_obj is an instance of the same class as self
        if isinstance(other_obj, self.__class__):
            return True

        # Check if self is an instance of any subclass of other_obj's class
        if issubclass(self.__class__, other_obj.__class__):
            return True

        # Check if other_obj is an instance of any subclass of self's class
        if issubclass(other_obj.__class__, self.__class__):
            return True

        return False

    def reposition(self, old_x, old_y):
        # calculate the difference
        diff_x = self.world_x - old_x
        diff_y = self.world_y - old_y

        # editors
        for editor in self.editors:
            editor.world_x += diff_x
            editor.world_y += diff_y
            # apply the difference to each widget
            for widget in editor.widgets:
                widget.world_x += diff_x
                widget.world_y += diff_y

                widget.screen_x += diff_x
                widget.screen_y += diff_y
                if hasattr(widget, "reposition"):
                    # Get the signature of the reposition method
                    sig = inspect.signature(widget.reposition)
                    params = sig.parameters

                    # Check if 'old_x' and 'old_y' are in the parameters of the reposition method
                    if 'old_x' in params and 'old_y' in params:
                        widget.reposition(old_x, old_y)
                    else:
                        widget.reposition()

                if hasattr(widget, "set_center"):
                    widget.set_center()

        # apply the difference to each widget
        for widget in self.widgets:
            widget.world_x += diff_x
            widget.world_y += diff_y

            widget.screen_x += diff_x
            widget.screen_y += diff_y
            if hasattr(widget, "reposition"):
                # Get the signature of the reposition method
                sig = inspect.signature(widget.reposition)
                params = sig.parameters

                # Check if 'old_x' and 'old_y' are in the parameters of the reposition method
                if 'old_x' in params and 'old_y' in params:
                    widget.reposition(old_x, old_y)
                else:
                    widget.reposition()

            if hasattr(widget, "set_center"):
                widget.set_center()

    def draw_frame(self, **kwargs):
        # get corner radius and thickness
        corner_radius = kwargs.get("corner_radius", self.frame_corner_radius)
        corner_thickness = kwargs.get("corner_thickness", self.frame_corner_thickness)

        # scale frame
        self.frame = pygame.transform.scale(self.frame, (self.get_screen_width(), self.max_height))

        # set rect
        self.rect = pygame.Rect((
            self.world_x, self.world_y + TOP_SPACING, self.frame.get_rect().width, self.frame.get_rect().height))

        # draw rounded rect
        draw_transparent_rounded_rect(self.win, (0, 0, 0), self.rect, corner_radius, config.ui_panel_alpha)
        pygame.draw.rect(self.win, self.frame_color, self.rect, corner_thickness, corner_radius)
