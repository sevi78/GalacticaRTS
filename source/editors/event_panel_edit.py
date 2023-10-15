import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.selector import Selector
from source.gui.widgets.widget_handler import WidgetHandler
from source.interfaces.interface import Interface
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.saveload import write_file, load_file




class EventPanelEdit(Interface):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        Interface.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        #self.create_selectors()
        self.create_save_button(lambda: self.parent.save_objects("event_panel.json",[self.obj]),"save event panel settings")
        self.create_close_button()

    # def create_selectors(self):
    #     """"""
    #     x = self.world_x - ARROW_SIZE / 2 + self.world_width / 2
    #     y = self.world_y + self.text_spacing + TOP_SPACING * 2
    #     self.selector_ship = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
    #         self.spacing_x, {"list_name": "ships_list", "list": sprite_groups.ships.sprites()}, self, FONT_SIZE)
    #
    #     self.selectors.append(self.selector_ship)
    #
    # def selector_callback(self, key, value):
    #     """this is the selector_callback function called from the selector to return the values to the editor"""
    #     if key == "ships":
    #         self.parent.ship = value


class GamePlayEdit__(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        # lists
        self.selectors = []
        #self.font_name_list = pygame.sysfont.get_fonts()

        #  widgets
        self.widgets = []
        #self.selector_font_name = None

        # create widgets
        #self.create_selectors()
        self.create_close_button()
        #self.set_selector_current_value()

        self.max_height = 200
        # hide initially
        self.hide()

    # def create_selectors(self):
    #     """
    #     """
    #     x = self.world_x - ARROW_SIZE / 2 + self.world_width / 2
    #     y = 200
    #     self.selector_font_name = Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9,
    #         self.spacing_x, {"list_name": "font_name_list", "list": self.font_name_list}, self, FONT_SIZE)
    #
    #     self.max_height = y
    #
    # def set_selector_current_value(self):
    #     """updates the selectors values
    #     """
    #     for i in self.selectors:
    #         i.set_current_value(global_params.font_name)
    #
    # def selector_callback(self, key, value):
    #     if key == "font_name":
    #         for key, widgetlist in WidgetHandler.layers.items():
    #             # get widget
    #             for widget in widgetlist:
    #                 if hasattr(widget, "font_size"):
    #                     widget.font = pygame.font.SysFont(value, widget.font_size)
    #                     global_params.font_name = value
    #                     data = load_file("settings.json")
    #                     data["font_name"] = value
    #                     write_file("settings.json", data)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "GamePlay:")
