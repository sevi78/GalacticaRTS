import pygame

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.gui.lod import level_of_detail
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.multimedia_library.images import overblit_button_image, scale_image_cached, rounded_surface


class Delegate:
    """ a simple delegate for a button:

        :param state_image: The image of the button
        :type state_image: str

        use: inject an instance of this class as kwarg to the ImageButton,
        the ImageButton then will call check_state()

    """
    def __init__(self, state_image: str) -> None:
        self.state_image = state_image
        self.trigger = None

    def check_state(self, parent: object, trigger: bool) -> None:
        # check if the state has changed
        if not trigger == self.trigger:
            # set the state
            self.trigger = trigger

            # set the image
            overblit_button_image(parent, self.state_image, not self.trigger)


class ImageButton(WidgetBase):
    """
    A customizable button widget with image and text support for Pygame.

    This class extends WidgetBase to create an interactive button that can display
    both an image and text. It supports various interactions such as clicking,
    hovering, and dragging.

    Attributes:
        win (pygame.Surface): Surface on which to draw the button.
        x (int): X-coordinate of the top-left corner.
        y (int): Y-coordinate of the top-left corner.
        width (int): Width of the button.
        height (int): Height of the button.
        is_sub_widget (bool): Indicates if this is a sub-widget of another widget.

    Optional Keyword Arguments:
        function (callable): Function to call when button is clicked.

        on_hover_function (callable): Function to call when button is hovered over.

        layer (int): Drawing layer of the button (default: 3).

        parent (object): Parent object of this button.

        name (str): Name identifier for the button.

        info_text (str): Information text to display when hovered.

        on_click (callable): Function to call on mouse click.

        on_release (callable): Function to call on mouse release.

        on_click_params (tuple): Parameters for the on_click function.

        on_release_params (tuple): Parameters for the on_release function.

        moveable (bool): Whether the button can be moved.

        property (any): Custom property for the button.

        delegate (object): Delegate object for additional functionality.

        text_color (tuple): RGB color of the text (default: (255, 255, 25)).

        font_size (int): Size of the font (default: 20).

        text (str): Text to display on the button.
        font (pygame.font.Font): Font to use for the text.

        text_h_align (str): Horizontal alignment of text ('left', 'centre', 'right').

        text_v_align (str): Vertical alignment of text ('top', 'centre', 'bottom').

        margin (int): Margin around the text (default: 20).

        transparent (bool): Whether the button background is transparent.

        image (pygame.Surface): Image to display on the button.

        image_h_align (str): Horizontal alignment of image.

        image_v_align (str): Vertical alignment of image.

        tooltip (str): Tooltip text to display on hover.

        infopanel (str): Information panel text.


    Methods:
        listen(events): Handle input events for the button.
        draw(): Display the button on the surface.
        set_on_click(on_click, params): Set the on-click function and parameters.
        set_on_release(on_release, params): Set the on-release function and parameters.
        set_inactive_color(color): Set the color when the button is inactive.
        set_pressed_color(color): Set the color when the button is pressed.
        set_hover_color(color): Set the color when the button is hovered over.
        get(attr): Get the value of an attribute.
        set(attr, value): Set the value of an attribute.

    Note:
        This class assumes the existence of various game components and global
        configurations, such as config.app, mouse_handler, and building_factory.
        """

    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
        self.function = kwargs.get("function", None)
        self.on_hover_function = kwargs.get("on_hover_function", None)
        self.layer = kwargs.get("layer", 3)
        self.parent = kwargs.get("parent")
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")

        # Function
        self.on_click = kwargs.get('on_click', lambda *args: None)
        self.on_release = kwargs.get('on_release', lambda *args: None)
        self.on_click_params = kwargs.get('on_click_params', ())
        self.on_release_params = kwargs.get('on_release_params', ())
        self.clicked = False
        self.moveable = kwargs.get("moveable", False)
        self.moving = False
        self.property = kwargs.get("property")
        self.delegate = kwargs.get("delegate", None)

        # Text (Remove if using PyInstaller)
        self.text_color = kwargs.get('text_color', (255, 255, 25))
        self.font_size = kwargs.get('font_size', 20)
        self.string = kwargs.get('text', '')
        self.font = kwargs.get('font', pygame.font.SysFont(config.font_name, self.font_size))
        self.text = self.font.render(self.string, True, self.text_color)
        self.text_h_align = kwargs.get('text_h_align', 'centre')
        self.text_v_align = kwargs.get('text_v_align', 'centre')
        self.margin = kwargs.get('margin', 20)
        self.text_rect = self.text.get_rect()
        self.align_text_rect()

        # Image
        self.transparent = kwargs.get('transparent', False)
        self.image = kwargs.get('image', None)
        self.image_h_align = kwargs.get('image_h_align', 'centre')
        self.image_v_align = kwargs.get('image_v_align', 'centre')



        if self.image:
            if self.corner_radius > 0:
                self.image = rounded_surface(self.image, self.corner_radius)
            self.rect = self.image.get_rect()
            self.align_image_rect()

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")
        self.info_panel_font_size = kwargs.get("info_panel_font_size", 18)

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if config.app:
            config.app.tooltip_instance.reset_tooltip(self)

        if self.delegate:
            self.delegate.check_state(self, config.app.game_client.connected)

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.rect.collidepoint(x, y):
                if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
                    self.clicked = False
                    self.on_release(*self.on_release_params)

                elif mouse_state == MouseState.LEFT_CLICK:
                    self.clicked = True
                    self.on_click(*self.on_click_params)

                    # this is used for build .... dirty hack, but leave it !
                    if self.string:
                        building_factory.build(self.string, config.app.selected_planet)

                    # another dirty hack
                    if hasattr(self.parent, "on_resource_click"):
                        self.parent.on_resource_click(self)

                elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
                    pass

                elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    self.win.blit(scale_image_cached(self.image_outline, self.rect.size), self.rect)
                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            config.app.info_panel.set_text(self.info_text, font_size=self.info_panel_font_size)
                            config.app.info_panel.set_planet_image(self.image_raw, align="topright", alpha=self.info_panel_alpha)

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            config.tooltip_text = self.tooltip

                    # set cursor
                    if hasattr(self, "parent"):
                        if self.parent.__class__.__name__ == "ToggleSwitch":
                            if not self.parent.parent._hidden:
                                config.app.cursor.set_cursor("toggle_up")
                            else:
                                config.app.cursor.set_cursor("toggle_down")

                    if self.name == "close_button":
                        config.app.cursor.set_cursor("close")

                    if self.on_hover_function:
                        self.on_hover_function()


            else:
                self.clicked = False

    def draw(self):
        """ Display to surface """
        # self.update_position()

        if not level_of_detail.inside_screen(self.get_position()):
            return

        if not self._hidden:
            if self.image:
                self.rect = self.image.get_rect()
                self.align_image_rect()
                self.win.blit(self.image, self.rect)

            self.text_rect = self.text.get_rect()
            self.align_text_rect()
            self.win.blit(self.text, self.text_rect)

    def set_on_click(self, on_click, params=()):
        self.on_click = on_click
        self.on_click_params = params

    def set_on_release(self, on_release, params=()):
        self.on_release = on_release
        self.on_release_params = params

    def set_inactive_color(self, color):
        self.inactive_color = color

    def set_pressed_color(self, color):
        self.pressed_color = color

    def set_hover_color(self, color):
        self.hover_color = color

    def get(self, attr):
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == 'color':
            return self.color

    def set(self, attr, value):
        super().set(attr, value)

        if attr == 'color':
            self.inactive_color = value
