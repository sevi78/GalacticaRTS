import pygame

from source.app.app_helper import select_next_item_in_list
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.button import Button
from source.utils import global_params
from source.multimedia_library.images import get_image


class Selector(WidgetBase):
    def __init__(self, win, x, y, buttonsize, color, layer, spacing, data, parent, font_size, **kwargs):
        WidgetBase.__init__(self, win, x, y, buttonsize, buttonsize, isSubWidget=False)
        # args
        self.win = win
        self.world_x = x
        self.world_y = y
        self.buttonsize = buttonsize
        self.color = color
        self.layer = layer
        self.spacing = spacing
        self.parent = parent
        self.repeat_clicks = kwargs.get("repeat_clicks", False)

        # widgets
        self.plus_arrow = None
        self.minus_arrow = None
        self.buttons = []
        self.font_size = font_size
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.text_adds = ""

        #  lists, data
        self.list_name = data["list_name"]
        self.list = data["list"]
        self.key = self.list_name.split("_list")[0]
        self.value = data["list"][0]
        self.current_value = data["list"][0]

        # construct and register @ parent
        self.create_buttons()
        self.hide()
        self.register()

    def register(self):
        """
        """
        self.parent.widgets.append(self)
        self.parent.selectors.append(self)

    def set_current_value(self, value):
        """
        """
        self.current_value = value

    def create_buttons(self):
        """
        """
        self.minus_arrow = Button(win=pygame.display.get_surface(),
            x=self.world_x - self.spacing,
            y=self.world_y,
            width=self.buttonsize,
            height=self.buttonsize,
            isSubWidget=False,
            image=pygame.transform.scale(
                get_image("arrow-left.png"), (self.buttonsize, self.buttonsize)),
            tooltip=f"choose {self.list_name.split('_list')[0]}",
            frame_color=self.color,
            transparent=True,
            onClick=lambda: self.select(-1),
            parent=self.parent,
            layer=self.layer,
            name="minus_arrow",
            repeat_clicks=self.repeat_clicks
            )

        self.plus_arrow = Button(win=pygame.display.get_surface(),
            x=self.world_x + self.spacing,
            y=self.world_y,
            width=self.buttonsize,
            height=self.buttonsize,
            isSubWidget=False,
            image=pygame.transform.scale(
                get_image("arrow-right.png"), (self.buttonsize, self.buttonsize)),
            tooltip=f"choose {self.list_name.split('_list')[0]}",
            frame_color=self.color,
            transparent=True,
            onClick=lambda: self.select(1),
            parent=self.parent,
            layer=self.layer,
            name="plus_arrow",
            repeat_clicks=self.repeat_clicks
            )

        self.buttons.append(self.minus_arrow)
        self.buttons.append(self.plus_arrow)
        self.widgets.append(self.minus_arrow)
        self.widgets.append(self.plus_arrow)

    def select(self, value):
        """
        """
        self.current_value = select_next_item_in_list(self.list, self.current_value, value)
        self.parent.selector_callback(self.key, self.current_value)

    def draw_texts(self):
        """
        """
        self.set_text()

        text = self.font.render(self.display_text, True, self.color)
        text_rect = text.get_rect()
        text_rect.x = self.minus_arrow.get_screen_x() + self.spacing - text_rect.width / 2
        text_rect.y = self.minus_arrow.get_screen_y() + 6
        self.win.blit(text, text_rect)

    def set_text(self):
        if hasattr(self.current_value, "name"):
            display_text = f"{self.list_name.split('_list')[0]} : {self.current_value.name}"
        else:
            display_text = f"{self.list_name.split('_list')[0]} : {self.current_value}"

        self.display_text = display_text + self.text_adds

    def draw(self):
        """
        """
        if not self._hidden or self._disabled:
            self.draw_texts()
            for i in self.buttons:
                i.draw()
