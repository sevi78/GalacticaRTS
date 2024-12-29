import pygame

from source.configuration.game_config import config
from source.gui.lod import level_of_detail
from source.gui.widgets.buttons.moveable import Moveable
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.mouse_handler import mouse_handler, MouseState

REPEAT_CLICK_EVENT = pygame.USEREVENT + 1
INITIAL_DELAY_EVENT = pygame.USEREVENT + 2


class Button(WidgetBase, Moveable):
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
        :param kwargs: Optional parameters
        """

    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.kwargs = kwargs
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 3)
        self.addition_value = kwargs.get("addition_value", None)
        self.repeat_clicks = kwargs.get("repeat_clicks", False)

        # self.selected = False
        self.center = (
            self.get_screen_x() + self.get_screen_width() / 2, self.get_screen_y() + self.get_screen_height() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")
        self.target = None

        # _color
        self.inactive_color = kwargs.get('inactive_color', (150, 150, 150))
        self.hover_color = kwargs.get('hover_color', (125, 125, 125))
        self.pressed_color = kwargs.get('pressed_color', (100, 100, 100))
        self.color = kwargs.get('color', self.inactive_color)  # Allows color to override inactive_color
        self.inactive_color = self.color
        self.shadow_distance = kwargs.get('shadow_distance', 0)
        self.shadow_color = kwargs.get('shadow_color', (210, 210, 180))
        self.hidden_color = kwargs.get('hidden_color', self.inactive_color)

        # Function
        self.on_click = kwargs.get('on_click', lambda *args: None)
        self.on_release = kwargs.get('on_release', lambda *args: None)
        self.on_click_params = kwargs.get('on_click_params', ())
        self.on_release_params = kwargs.get('on_release_params', ())
        self.clicked = False
        self.moveable = kwargs.get("moveable", False)
        self.moving = False
        self.property = kwargs.get("property")

        # Text (Remove if using PyInstaller)
        self.text_color = kwargs.get('text_color', (0, 0, 0))
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
        self.radius_extension = kwargs.get('radius_extension', 0)
        self.transparent = kwargs.get('transparent', False)
        self.image_hover_surface = pygame.surface.Surface((
            width + self.radius_extension, height + self.radius_extension), 0, self.win)
        self.image_hover_surface.set_alpha(kwargs.get("image_hover_surface_alpha", 0))
        self.image = kwargs.get('image', None)
        self.image_h_align = kwargs.get('image_h_align', 'centre')
        self.image_v_align = kwargs.get('image_v_align', 'centre')

        if self.image:
            self.rect = self.image.get_rect()
            self.align_image_rect()

        # Border
        self.border_thickness = kwargs.get('border_thickness', 0)
        self.inactive_border_color = kwargs.get('inactive_border_color', (0, 0, 0))
        self.hover_border_color = kwargs.get('hover_border_color', (80, 80, 80))
        self.pressed_border_color = kwargs.get('pressed_border_color', (100, 100, 100))
        self.border_color = kwargs.get('border_color', self.inactive_border_color)
        self.inactive_border_color = self.border_color
        self.radius = kwargs.get('radius', 0)

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

    def draw_circle(self, color, alpha):
        if self.transparent:
            self.circle = pygame.surface.Surface((self.get_screen_width(), self.get_screen_height()), 0, self.win)
            self.circle.set_alpha(0)
            circle = pygame.draw.circle(surface=self.circle, color=color,
                    center=self.rect.center,
                    radius=(self.get_screen_width() * 1.5))

            self.win.blit(self.circle, self.rect)

    def listen(self, events):  # _with_repeat not working yet
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not level_of_detail.inside_screen(self.get_position()):
            return

        config.app.tooltip_instance.reset_tooltip(self)

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.rect.collidepoint(x, y):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if mouse_state == MouseState.LEFT_CLICK:
                            self.clicked = True
                            self.on_click(*self.on_click_params)
                            self.color = self.pressed_color
                            self.border_color = self.pressed_border_color
                            self.draw_circle(self.pressed_color, 128)

                            # set planet on click of the building slot buttons
                            if self.parent:
                                if hasattr(self.parent, "property"):
                                    if self.parent.property == "planet":
                                        config.app.set_selected_planet(self.parent)

                                # set building_edit.input_box value
                                if hasattr(self.parent, "property"):
                                    if self.parent.property == "input_box":
                                        if hasattr(self, "addition_value"):
                                            value = int(self.parent.text) - int(self.addition_value)
                                            self.parent.set_text(str(value))

                            if self.string:
                                config.app.build(self.string, config.app.selected_planet)

                            # If repeat_clicks is True, set a timer to start repeating the click after 1 second
                            if self.repeat_clicks:
                                # pygame.time.set_timer(INITIAL_DELAY_EVENT, 700)  # 1000 milliseconds = 1 second
                                pygame.time.set_timer(REPEAT_CLICK_EVENT, 120)  # 200 milliseconds




                    # elif event.type == INITIAL_DELAY_EVENT:
                    #     # After the initial delay, start repeating the click every 200 milliseconds
                    #     pygame.time.set_timer(REPEAT_CLICK_EVENT, 120)  # 200 milliseconds
                    #     pygame.time.set_timer(INITIAL_DELAY_EVENT, 0)  # Stop the initial delay timer

                    elif event.type == REPEAT_CLICK_EVENT:
                        # The timer has triggered a repeat click event
                        self.on_click(*self.on_click_params)
                        self.color = self.pressed_color
                        self.border_color = self.pressed_border_color
                        self.draw_circle(self.pressed_color, 128)

                        # set cursor
                        if self.name == "minus_arrow":
                            config.app.cursor.set_cursor("left_arrow_repeated")

                        if self.name == "plus_arrow":
                            config.app.cursor.set_cursor("right_arrow_repeated")



                    elif event.type == pygame.MOUSEBUTTONUP:
                        if mouse_state == MouseState.LEFT_RELEASE and self.clicked:
                            self.clicked = False
                            self.on_release(*self.on_release_params)

                            # If repeat_clicks is True, stop the timer when the mouse button is released
                            if self.repeat_clicks:
                                pygame.time.set_timer(REPEAT_CLICK_EVENT, 0)  # Setting delay to 0 stops the timer

                    elif mouse_state == MouseState.LEFT_DRAG and self.clicked:
                        self.color = self.pressed_color
                        self.border_color = self.pressed_border_color
                        self.draw_circle(self.pressed_color, 128)

                    elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                        self.color = self.hover_color
                        self.border_color = self.hover_border_color
                        self.draw_circle(self.hover_color, 128)

                        # self.win.blit(outline_image(self.image, self.frame_color, 1), self.image.get_rect())

                        self.image = self.image_outline

                        # set tooltip
                        if self.tooltip:
                            if self.tooltip != "":
                                config.tooltip_text = self.tooltip

                        # set info_panel
                        if self.info_text:
                            if self.info_text != "":
                                config.app.info_panel.set_text(self.info_text)
                                config.app.info_panel.set_planet_image(self.image_raw, size=(
                                    85, 85), align="topright")

                        # set cursor
                        if self.name == "minus_arrow":
                            config.app.cursor.set_cursor("left_arrow")

                        if self.name == "plus_arrow":
                            config.app.cursor.set_cursor("right_arrow")
            else:
                self.image = self.image_raw
                self.clicked = False
                self.color = self.inactive_color
                self.border_color = self.inactive_border_color
                self.draw_circle(self.inactive_color, 0)

    def draw(self):
        # """ Display to surface """
        self.update_position()
        if not level_of_detail.inside_screen(self.get_position()):
            return

        if not self._hidden and not self._disabled:
            if not self.transparent:
                pygame.draw.rect(
                        self.win, self.shadow_color,
                        (self.screen_x + self.shadow_distance, self.screen_y + self.shadow_distance, self.screen_width,
                         self.screen_height),
                        border_radius=self.radius
                        )

                pygame.draw.rect(
                        self.win, self.border_color, (
                            self.screen_x, self.screen_y, self.screen_width, self.screen_height),
                        border_radius=self.radius
                        )

                pygame.draw.rect(
                        self.win, self.color, (
                            self.screen_x + self.border_thickness, self.screen_y + self.border_thickness,
                            self.screen_width - self.border_thickness * 2,
                            self.screen_height - self.border_thickness * 2),
                        border_radius=self.radius
                        )

            if self.image:
                self.rect = self.image.get_rect()
                self.align_image_rect()
                self.win.blit(self.image, self.rect)

            self.text = self.font.render(self.string, True, self.text_color)
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
