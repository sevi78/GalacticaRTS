import pygame

from source.app.app_helper import select_next_item_in_list
from source.configuration.game_config import config
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.multimedia_library.images import get_image


class Selector(WidgetBase):
    def __init__(self, win, x, y, buttonsize, color, layer, spacing, data, parent, font_size, **kwargs):
        """
        Initializes a new instance of the Selector class.

        Args:
            win (pygame.Surface): The game window surface.
            x (int): The x-coordinate of the selector's position.
            y (int): The y-coordinate of the selector's position.
            buttonsize (int): The size of the selector's buttons.
            color (tuple): The color of the selector's frame.
            layer (int): The layer of the selector.
            spacing (int): The spacing between the selector's buttons.
            data (dict): A dictionary containing the list name and the list of values.
            parent (WidgetBase): The parent widget of the selector.
            font_size (int): The size of the selector's font.
            **kwargs: Additional keyword arguments.

            repeat_clicks (bool): Whether to repeat clicks on the selector's buttons. Defaults to False.
            restrict_list_jump (bool): Whether to restrict the selector from jumping to the beginning or end of the list
            when selecting. Defaults to False.
            text_adds (str): Additional text to display next to the selector's text. Defaults to an empty string.


        Returns:
            None

        Description:
            Initializes the Selector instance with the provided arguments.
            Creates the necessary widgets and registers the selector at the parent.
            Hides the selector initially.

        Note:
            The list_name key in the data dictionary should be in the format 'list_name'.
            The list key in the data dictionary should be a list of values.
        """
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
        self.restrict_list_jump = kwargs.get("restrict_list_jump", False)

        # widgets
        self.plus_arrow = None
        self.minus_arrow = None
        self.buttons = []
        self.font_size = font_size
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.text_adds = kwargs.get("text_adds", "")
        self.display_text = None

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
        Register the selector widget at the parent.

        This function appends the selector widget to the parent's widgets and selectors lists.
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

    def reposition(self):
        """
        Repositions the minus_arrow and plus_arrow buttons based on the current world_x and world_y coordinates.

        This function updates the screen_x and screen_y attributes of the minus_arrow and plus_arrow buttons to position
        them relative to the current world_x and world_y coordinates.
        The buttons are positioned with a spacing of self.spacing pixels between them.

        Parameters:
            self (Selector): The current instance of the Selector class.

        Returns:
            None
        """
        self.minus_arrow.screen_x = self.world_x - self.spacing
        self.minus_arrow.screen_y = self.world_y
        self.plus_arrow.screen_x = self.world_x + self.spacing
        self.plus_arrow.screen_y = self.world_y

    def select(self, value):
        """
        Selects the next item in the list based on the given value.
        This function updates the current_value attribute of the Selector class based on the given value.
        It also calls the selector_callback function of the parent class with the current_value, key, and
        self as arguments.

        Parameters:
            value (int): The value to determine the next item in the list.

        Returns:
            None
        """
        if (self.current_value == min(self.list) and value == -1) or (
                self.current_value == max(self.list) and value == 1):
            if self.restrict_list_jump:
                return

        self.current_value = select_next_item_in_list(self.list, self.current_value, value)
        self.parent.selector_callback(self.key, self.current_value, self)

    def draw_texts(self):
        """
        Draws the text on the screen based on the current state of the selector.

        This function first calls the `set_text` method to update the display text based on the current value.
        Then, it renders the text using the `font` attribute and the display text.
        The text is then positioned on the screen based on the position of the minus arrow and the spacing.
        Finally, the text is blitted onto the window using the `blit` method of the `win` attribute.

        Parameters:
            None

        Returns:
            None
        """
        self.set_text()

        text = self.font.render(self.display_text, True, self.color)
        text_rect = text.get_rect()
        text_rect.x = self.minus_arrow.get_screen_x() + self.spacing - text_rect.width / 2
        text_rect.y = self.minus_arrow.get_screen_y() + 6
        self.win.blit(text, text_rect)

    def set_text(self):
        """
        Sets the text to be displayed based on the current value.
        If the current value has a 'name' attribute, the display text is constructed using that.
        Otherwise, the display text is constructed using the current value.
        The resulting display text is stored in the display_text attribute of the Selector instance.
        """
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
            # for i in self.buttons:
            #     i.draw()
