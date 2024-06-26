import pygame
from pygame.locals import MOUSEMOTION

from source.configuration.game_config import config
from source.gui.widgets.frame import Frame
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.mouse_handler import mouse_handler

INVISIBLE_X = -1000
INVISIBLE_Y = -1000
INVISIBLE_X_OFFSET = 10
INVISIBLE_Y_OFFSET = 10
TOOLTIP_ALPHA = 200


class ToolTip(WidgetBase):
    """Main functionalities:
    The ToolTip class is responsible for creating and displaying a tooltip on the screen. It receives a surface, position, size, color, and text color as parameters, and it can be a subwidget. It moves with the mouse and displays the text passed to it through the config module. It draws a filled rectangle with a border and the text passed to it.

    Methods:
    - __init__: initializes the ToolTip object with the given parameters and sets some default values.
    - move: moves the tooltip with the mouse and limits its position to the screen size.
    - get_text: gets the text to be displayed from the config module and sets the visibility of the tooltip accordingly.
    - draw_bordered_rect: draws a bordered rectangle around the tooltip.
    - draw: renders the tooltip on the screen with a filled rectangle, border, and text.
    - listen: listens to events, but does not do anything.
    - update: updates the tooltip by getting the text, moving it, and drawing it.

    Fields:
    - win: the surface on which the tooltip is drawn.
    - color: the color of the filled rectangle.
    - text_color: the color of the text.
    - x, y: the position of the tooltip.
    - width, height: the size of the tooltip.
    - size: a tuple containing the width and height of the tooltip.
    - rect_filled: a surface representing the filled rectangle of the tooltip.
    - parent: the parent widget of the tooltip.
    - _text: the text to be displayed.
    - font: the font used for the text.
    - text_img: a surface representing the rendered text.
    - txt_rect: the rectangle containing the rendered text.
    - visible: a boolean indicating whether the tooltip is visible or not.
    - active: a boolean indicating whether the tooltip is active or not, could be set by a button """

    def __init__(self, surface, x, y, width, height, color, text_color, isSubWidget, parent, **kwargs):
        super().__init__(surface, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 10)
        self.visible = False
        self.win = surface
        self.color = color
        self.text_color = text_color
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height
        self.size = (self.world_width, self.world_height)
        self.parent = parent

        # text
        self._text = ""
        self.font_size = config.ui_tooltip_size
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.text_img = None
        self.txt_rect = None
        self.active = config.ui_tooltip_enabled

        self.frame = Frame(self.win, self.world_x, self.world_y, self.world_width, self.world_height)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value

    def move(self, event):
        if self.visible and self.text_img:
            cursor_space = 13
            # limit position x
            max_x = pygame.display.get_surface().get_width()
            x = event.pos[0] + self.text_img.get_width() / 2
            min_x = 0
            x1 = event.pos[0] - self.text_img.get_width() / 2

            if x > max_x:
                self.world_x = max_x - self.text_img.get_width() - INVISIBLE_X_OFFSET
            elif x1 < min_x:
                self.world_x = min_x
            else:
                self.world_x = event.pos[0] - self.text_img.get_width() / 2

            # limit position y
            max_y = pygame.display.get_surface().get_height() - self.text_img.get_height()
            y = event.pos[1] + self.text_img.get_height()
            min_y = 0
            y1 = event.pos[1] - self.text_img.get_height()

            if y > max_y:
                self.world_y = max_y - self.text_img.get_height() - INVISIBLE_Y_OFFSET
            elif y1 < min_y:
                self.world_y = min_y
            else:
                self.world_y = event.pos[1] + self.text_img.get_height() + cursor_space

        else:
            self.world_x = INVISIBLE_X
            self.world_y = INVISIBLE_Y

    def get_text(self):
        if not self.active:
            return
        self._text = config.tooltip_text
        if self._text != "":
            self.visible = True
            # pygame.mouse.set_visible(False)  # hide cursor when tooltip is visible
        else:
            self.visible = False
            # pygame.mouse.set_visible(True)  # show cursor when tooltip is not visible

    def on_hover_release_callback(self, x, y, obj):
        # if self._hidden or self._disabled:
        #     return

        # handle AttributeError: 'NoneType' object has no attribute 'collidepoint'
        if not obj.rect:
            return

        if obj.rect.collidepoint(x, y):
            obj.on_hover = True
            obj.on_hover_release = False
        else:
            obj.on_hover_release = True

        if obj.on_hover and obj.on_hover_release:
            obj.on_hover = False
            return True

        return False

    def reset_tooltip(self, obj):
        x, y = mouse_handler.get_mouse_pos()
        if self.on_hover_release_callback(x, y, obj):
            config.tooltip_text = ""
            config.app.cursor.set_cursor("idle")

    def listen(self, events):
        if not self.active:
            return
        for event in events:
            if event.type == MOUSEMOTION:
                self.update(event)

    def update(self, events):
        if not self.active:
            return
        self.get_text()
        self.move(events)

    def draw(self):
        if not self.active:
            return
        # render text
        self.text_img = self.font.render(self._text, True, self.text_color)

        # update pos, size
        self.world_width = self.text_img.get_rect().width + config.ui_rounded_corner_radius_small * 2
        self.world_height = self.text_img.get_rect().height + 7
        self.size = (self.world_width, self.world_height)

        # draw frame
        self.frame.update(self.world_x, self.world_y, self.world_width, self.world_height)
        self.frame.draw()

        # draw text
        self.win.blit(self.text_img, (self.world_x + 5, self.world_y))

        # hide mouse cursor if tooltip is visible
        # pygame.mouse.set_visible(not self.visible)
