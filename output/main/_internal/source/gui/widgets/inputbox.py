import pygame as pg

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.configuration import global_params
from source.handlers.color_handler import colors

COLOR_INACTIVE = colors.frame_color
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONTSIZE = 32


class InputBox(WidgetBase):
    def __init__(self, win, x, y, w, h, text, **kwargs):
        WidgetBase.__init__(self, win, x, y, w, h, isSubWidget=False, **kwargs)

        self.win = win
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font_size = int(h * 0.8)
        self.font = pg.sysfont.SysFont(global_params.font_name, self.font_size)
        self.text_offset_y = int(self.font_size * 0.2)
        self.txt_surface = self.font.render(text, True, self.color)
        self._active = False
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 9)
        self._disabled = kwargs.get("disabled", False)
        self.text_input_type = kwargs.get("text_input_type", str)
        self.property = "input_box"
        self.draw_frame = kwargs.get("draw_frame", True)

        self.hide()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self.on_active_change()

    def on_active_change(self):
        # Your function to be called every time the active property changes
        global_params.text_input_active = self._active
        self.set_color()

        if not self._disabled and not self._hidden:
            if self.text_input_type == int:
                text = int(self.text)
            else:
                text = self.text
            self.parent.get_input_box_values(self, self.key, text)

    def set_color(self):
        # Change the current color of the input box.
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        self.txt_surface = self.font.render(self.text, True, self.color)

    def set_text(self, text):
        if not self.active:
            self.text = text
            # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.color)

    def handle_events(self, events):
        if self._disabled:
            return

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False

            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        self.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        if self.text_input_type == int:
                            if event.unicode.isdigit() or (event.unicode == '-' and len(self.text) == 0):
                                self.text += event.unicode
                        elif self.text_input_type == str:
                            if event.unicode.isalpha():
                                self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.screen_width / 2, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        if not self._hidden:
            # Blit the text.
            self.win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.text_offset_y))
            # Blit the rect.
            if not self.draw_frame:
                return

            pg.draw.rect(self.win, self.color, self.rect, 2)
