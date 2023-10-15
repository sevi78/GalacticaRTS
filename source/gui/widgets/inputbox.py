import pygame as pg

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params
from source.utils.colors import colors

#
# pg.init()
# screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = colors.frame_color
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.sysfont.SysFont(global_params.font_name, 32)


class InputBox(WidgetBase):
    def __init__(self, win, x, y, w, h, text, **kwargs):
        WidgetBase.__init__(self, win, x, y, w, h, isSubWidget=False, **kwargs)
        self.win = win
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self._active = False
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 9)
        self.hide()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self.on_active_change()

    def set_text(self, text):
        if not self.active:
            self.text = text
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)

    def on_active_change(self):
        # Your function to be called every time the active property changes
        global_params.text_input_active = self._active

        # don't know why i need to set both, name and string to make the text appear ??
        self.parent.set_new_value_to_planet("name", self.text)
        self.parent.set_new_value_to_planet("string", self.text)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def listen_(self, events):
        pass

    def draw(self):
        if not self._hidden or self._disabled:
            # Blit the text.
            self.win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            # Blit the rect.
            pg.draw.rect(self.win, self.color, self.rect, 2)

#
# def main():
#     clock = pg.time.Clock()
#     input_box1 = InputBox(100, 100, 140, 32)
#     input_box2 = InputBox(100, 300, 140, 32)
#     input_boxes = [input_box1, input_box2]
#     done = False
#
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)
#
#         for box in input_boxes:
#             box.update()
#
#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)
#
#         pg.display.flip()
#         clock.tick(30)
#
#
# if __name__ == '__main__':
#     main()
#     pg.quit()
