from source.auto_economy.economy_calculator import economy_calculator
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.handlers.file_handler import write_file


class AutoEconomyCalculatorEdit(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()

        # hide initially
        self.hide()

        # attach to parent
        # self.parent.editors.append(self)
        self.settings = economy_calculator.settings
        self.create_selectors_from_dict(self.world_x + self.world_width / 2, self.world_y + TOP_SPACING + self.text_spacing * 4, self.settings.items())
        self.set_selectors_current_value()
        self.create_save_button(lambda: self.save_settings(), "save settings")

    def set_selectors_current_value(self):
        for i in self.selectors:
            i.set_current_value(self.settings[i.key])

    def selector_callback(self, key, value, selector) -> None:
        self.settings[key] = value

    def save_settings(self):
        write_file("auto_economy_calculator_settings.json", "config", self.settings)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "AutoEconomyCalculatorEdit:")
