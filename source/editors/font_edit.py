import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.selector import Selector
from source.handlers.widget_handler import WidgetHandler
from source.configuration import global_params
from source.handlers.file_handler import write_file, load_file


class FontEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        # lists
        self.selectors = []
        self.current_font = None
        self.font_name_list = pygame.sysfont.get_fonts()

        #  widgets
        self.widgets = []
        self.selector_font_name = None

        # create widgets
        self.create_selectors()
        self.create_close_button()
        self.create_save_button(lambda: self.save_font(self.current_font), "save font")
        self.set_selector_current_value()

        # hide initially
        self.hide()

    def create_selectors(self):
        """
        """
        x = self.world_x - ARROW_SIZE / 2 + self.world_width / 2
        y = 130
        self.selector_font_name = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
            self.spacing_x, {"list_name": "font_name_list", "list": self.font_name_list}, self, FONT_SIZE)

        self.max_height = y + ARROW_SIZE

    def set_selector_current_value(self):
        """updates the selectors values
        """
        for i in self.selectors:
            i.set_current_value(global_params.font_name)

    def selector_callback(self, key, value):
        if key == "font_name":
            self.current_font = value
            for key, widgetlist in WidgetHandler.layers.items():
                # get widget
                for widget in widgetlist:
                    if hasattr(widget, "font_size"):
                        widget.font = pygame.font.SysFont(value, widget.font_size)
                        global_params.font_name = value

    def save_font(self, value):
        data = load_file("settings.json", "config")
        data["font_name"] = value
        write_file("settings.json", "config", data)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Select Font:")
