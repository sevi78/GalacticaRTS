import pygame

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.gui.lod import level_of_detail
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.multimedia_library.images import overblit_button_image


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
    """ A customisable button for Pygame

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
        :param kwargs: Optional parameters:
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
            self.rect = self.image.get_rect()
            self.align_image_rect()

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

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
                    self.win.blit(pygame.transform.scale(self.image_outline, self.rect.size), self.rect)
                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            config.app.info_panel.set_text(self.info_text)
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
