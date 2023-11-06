import pygame

from source.editors.editor_base.editor_config import ARROW_SIZE, SPACING_X, SPACING_Y, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_big_thickness
from source.multimedia_library.images import get_image
from source.gui.widgets.widget_base_components.widget_base import WidgetBase


class EditorBase(WidgetBase):
    """The EditorBase class is a base class for editors in a pygame application. It provides methods for setting the
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

    Fields:

    obj: The object to be edited.
    win: The window to draw on.
    x: The x-coordinate of the editor's position.
    y: The y-coordinate of the editor's position.
    _width: The width of the editor.
    _height: The height of the editor.
    arrow_size: The size of the arrow.
    spacing_x: The horizontal spacing.
    spacing_y: The vertical spacing.
    parent: The parent object.
    layer: The layer of the editor.
    font: The font used for text.
    frame_color: The color of the frame.
    frame: The surface for the frame.
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self._obj = kwargs.get("obj", None)
        self.obj = kwargs.get("obj", None)

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
        self.layer = kwargs.get("layer", 9)
        self.font = pygame.font.SysFont(global_params.font_name, FONT_SIZE)
        self.text_spacing = 20
        self.frame_color = colors.ui_dark
        self.frame = pygame.surface.Surface((self.world_width, self.world_height))
        self.frame.set_alpha(global_params.ui_panel_alpha)

        # register
        self.buttons = []
        self.selectors = []
        self.checkboxes = []
        self.checkbox_values = []
        self.parent.editors.append(self)

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
        global_params.edit_mode = not self._hidden
        global_params.enable_orbit = self._hidden

    def draw_text(self, x, y, width, height, text):
        font = pygame.font.SysFont(global_params.font_name, height - 1)
        text = font.render(text, 1, self.frame_color)
        self.win.blit(text, (x, y))

    def draw_frame(self):
        height = self.max_height
        self.frame = pygame.transform.scale(self.frame, (self.get_screen_width(), height))
        self.frame.fill((0,0,0))
        rect = pygame.draw.rect(self.frame, self.frame_color, self.frame.get_rect(), int(ui_rounded_corner_big_thickness), int(global_params.ui_rounded_corner_radius_big))
        rect.x = self.world_x
        rect.y = self.world_y + 60

        self.win.blit(self.frame, rect)

    def hide_other_editors(self):
        for i in self.parent.editors:
            if not i == self:
                i.hide()

    def set_visible(self):
        if self._hidden:
            self.show()
        else:
            self.hide()

        global_params.edit_mode = not self._hidden
        self.hide_other_editors()

    def create_save_button(self, function, tooltip):
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
            )
        save_icon.hide()

        self.buttons.append(save_icon)
        self.widgets.append(save_icon)

    def create_close_button(self):
        button_size = 32
        close_icon = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() - button_size - button_size / 2,
            y=self.world_y + TOP_SPACING + button_size / 2,
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
            )

        close_icon.hide()

        self.buttons.append(close_icon)
        self.widgets.append(close_icon)

    def close(self):
        self.set_global_variable("edit_mode", True)
        global_params.tooltip_text = ""
        self.hide()
