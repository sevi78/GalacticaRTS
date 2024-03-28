import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.selector import Selector
from source.handlers.file_handler import write_file, load_file
from source.handlers.widget_handler import WidgetHandler

TEXT_HEIGHT = 15


class AutoEconomyEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.enabled_input_boxes = []
        self.input_boxes = []
        self.input_boxes_value = []
        self.input_boxes_key = []
        self.buttonsize = 25
        self.player_id = 1
        self.player = self.get_player()
        self.is_attached = True
        self.drag_enabled = False

        # print("self.player:", self.player.auto_economy_handler.__dict__)
        #  widgets
        self.widgets = []

        # create widgets
        self.create_input_boxes()

        # hide initially
        self.hide()
        self.max_height = 200

    def set_player(self, player_index: int):
        self.player_id = player_index
        self.player = self.get_player()

    def get_player(self):
        if hasattr(config.app, 'players'):
            return config.app.players.get(self.player_id)
        return None

    def create_input_boxes(self):
        x = self.world_x + self.text_spacing
        y = self.world_y + TOP_SPACING + self.text_spacing + TEXT_HEIGHT + self.text_spacing
        input_box_key_width = self.screen_width - self.text_spacing * 6
        input_box_value_width = 160

        for key, value in self.player.auto_economy_handler.__dict__.items():
            input_box_key = InputBox(
                self.win,
                x,
                y,
                input_box_key_width,
                TEXT_HEIGHT,
                text=key,
                parent=self,
                key=key,
                disabled=True,
                text_input_type=str,
                draw_frame=False)
            self.input_boxes_key.append(input_box_key)

            input_box_value = InputBox(
                self.win,
                x + input_box_value_width,
                y,
                input_box_value_width,
                TEXT_HEIGHT,
                text=str(value),
                parent=self,
                key=key + "_value",
                text_input_type=type(value),
                disabled=True,
                draw_frame=False)

            self.input_boxes_value.append(input_box_value)
            self.widgets.append(input_box_key)
            self.input_boxes.append(input_box_key)
            self.widgets.append(input_box_value)
            self.input_boxes.append(input_box_value)
            y += TEXT_HEIGHT

        self.max_height = y + TOP_SPACING + TEXT_HEIGHT
        self.enabled_input_boxes = [_ for _ in self.input_boxes if not _._disabled]

    def update_input_boxes(self, events):
        for i in self.input_boxes:
            if i.key.endswith("_value"):
                text = str(getattr(self.player.auto_economy_handler, i.key.split("_value")[0]))
            else:
                text = i.key

            i.set_text(text)
            # setattr(i,"value",getattr(self.player.auto_economy_handler,i.key))
            i.update()
            i.handle_events(events)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.update_input_boxes(events)
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            # self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Economy:")
