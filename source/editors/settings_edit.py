import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.selector import Selector
from source.handlers.file_handler import write_file, load_file
from source.handlers.widget_handler import WidgetHandler

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)


class SettingsEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        # lists
        self.selectors = []
        self.current_font = None
        self.font_name_list = pygame.sysfont.get_fonts()
        self.boolean_list = [True, False]
        self.selector_lists = {}

        self.selector_lists = { "fps": [25,60,90,120,1000],
                                "enable_game_events": self.boolean_list,
                                "draw_universe": self.boolean_list,
                                "ui_panel_alpha": [_ for _ in range(256)],
                                "ui_rounded_corner_radius_small": [_ for _ in range(11)],
                                "ui_rounded_corner_radius_big": [_ for _ in range(3, 25)],
                                "ui_rounded_corner_small_thickness": [_ for _ in range(0, 5)],
                                "ui_rounded_corner_big_thickness": [_ for _ in range(0, 15)]
                                }

        #  widgets
        self.widgets = []
        self.selector_font_name = None

        # create widgets
        self.create_selectors()
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

        for key, value in config.editable_params.items():
            # booleans
            if type(value) is bool:
                self.selector_lists[key] = self.boolean_list
                self.selectors.append(Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
                    self.spacing_x, {"list_name": f"{key}_list", "list": self.boolean_list}, self, FONT_SIZE))

                y += self.spacing_y

            # integers
            if type(value) is int:
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
        else:
            setattr(config, key, value)


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
