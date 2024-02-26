import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.event_text import event_text
from source.gui.widgets.selector import Selector
from source.gui.widgets.slider import Slider
from source.handlers.color_handler import colors
from source.handlers.file_handler import write_file
from source.handlers.widget_handler import WidgetHandler

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)


class SettingsEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        # lists
        self.selectors = []
        self.sliders = {}
        self.current_font = None
        self.font_name_list = pygame.sysfont.get_fonts()
        self.boolean_list = [True, False]

        self.default_list = [_ for _ in range(100)]
        self.selector_lists = {"player": [_ for _ in range(config.players)],
                               "fps": [25, 60, 90, 120, 1000],
                               "enable_game_events": self.boolean_list,
                               "draw_universe": self.boolean_list,
                               "ui_panel_alpha": [_ for _ in range(256)],
                               "ui_rounded_corner_radius_small": [_ for _ in range(11)],
                               "ui_rounded_corner_radius_big": [_ for _ in range(3, 25)],
                               "ui_rounded_corner_small_thickness": [_ for _ in range(0, 5)],
                               "ui_rounded_corner_big_thickness": [_ for _ in range(0, 15)],
                               "ui_cross_size": [_ for _ in range(3, 50)],
                               "ui_cross_dash_length": [_ for _ in range(1, 20)],
                               "ui_cross_thickness": [_ for _ in range(1, 10)],
                               "game_speed": [_ for _ in range(1, 10)],
                               "ui_tooltip_size": [_ for _ in range(10, 50)],
                               }

        #  widgets
        self.widgets = []
        self.selector_font_name = None

        # create widgets
        self.create_selectors()
        # self.create_color_sliders()
        self.create_close_button()
        self.create_save_button(lambda: self.save_settings(), "save settings")
        self.set_selector_current_value()

        # hide initially
        self.hide()

    def create_selectors(self):
        """
        """
        x = self.world_x - ARROW_SIZE / 2 + self.world_width / 2
        y = 130

        # for key, value in config.editable_params.items():
        for key, value in config.settings.items():  # booleans
            if type(value) is bool:
                self.selector_lists[key] = self.boolean_list
                self.selectors.append(Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                    self.spacing_x, {"list_name": f"{key}_list", "list": self.boolean_list}, self, FONT_SIZE))

                y += self.spacing_y

            # integers
            if type(value) is int:
                if not key in self.selector_lists.keys():
                    self.selector_lists[key] = self.default_list

                self.selectors.append(Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                    self.spacing_x, {"list_name": f"{key}_list", "list": self.selector_lists[key]}, self, FONT_SIZE,
                    repeat_clicks=True))

                y += self.spacing_y

        # fonts
        self.selector_font_name = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "font_name_list", "list": self.font_name_list}, self, FONT_SIZE)
        y += self.spacing_y

        # set max height to draw the frame dynamical
        self.max_height = y + ARROW_SIZE

    def create_color_sliders(self):
        width = self.get_screen_width() / 2 - self.text_spacing
        height = 10
        x = self.world_x + self.world_width / 2
        y = self.world_y + self.max_height
        rgb = {"R": 0, "G": 0, "B": 0}
        for key, value in rgb.items():
            if type(value) == int:
                step = 1
            if type(value) == float:
                step = 0.001

            slider = Slider(win=self.win,
                x=x,
                y=y,
                width=width,
                height=height,
                min=0,
                max=255,
                step=step,
                initial=value,
                handleColour=colors.ui_dark,
                layer=self.layer,
                parent=self)

            slider.colour = colors.ui_darker

            y += self.spacing_y

            self.sliders[key] = slider
            self.widgets.append(slider)

        self.max_height += y

    def get_slider_data(self):
        data = {}
        for name, slider in self.sliders.items():
            data[name] = slider.getValue()

        return data

    def set_slider_data(self):
        if not hasattr(self, "sliders"):
            return

        for key, value in self.sliders.items():
            self.sliders[key].setValue(getattr(self.obj, key))

    def set_selector_current_value(self):
        """updates the selectors values
        """
        for i in self.selectors:
            i.set_current_value(getattr(config, i.key))

    def selector_callback(self, key, value):
        if key == "font_name":
            self.current_font = value
            config.font_name = value
            # get all layers
            for key, widgetlist in WidgetHandler.layers.items():
                # get widget
                for widget in widgetlist:
                    # check if widget can draw text
                    if hasattr(widget, "font_size"):
                        # set the font
                        widget.font = pygame.font.SysFont(value, widget.font_size)

        elif key == "game_speed":
            config.game_speed = value
            config.app.game_time.game_speed = value

        elif key == "ui_tooltip_size":
            config.app.tooltip_instance.font_size = value
            config.app.tooltip_instance.font = pygame.font.SysFont(config.font_name, config.app.tooltip_instance.font_size)

        elif key == "ui_event_text_size":
            event_text.event_text_font_size = value

        else:
            setattr(config, key, value)
            if key == "player":
                config.app.player = config.app.players[value]

    def save_settings(self):
        data = {}
        for i in self.selectors:
            data[i.key] = i.current_value
        write_file("settings.json", "config", data)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Settings:")
