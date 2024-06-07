from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING


class DefaultEdit(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)

        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        # self.create_save_button(lambda: self.save_font(self.current_font), "save font")

        # hide initially
        self.hide()

        # set max_height, important to remove the default value of 200 after create_widgets() !!!
        # otherwise the display is terribly wrong !!
        self.max_height = 200

        # attach to parent
        # self.parent.editors.append(self)
        # use this if its a sûb widget, it will be repositions automatically!

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "DefaultEdit:")
