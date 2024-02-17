import pygame

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.text.text_wrap import TextWrap

pygame.font.init()

EVENT_TEXT_HEIGHT = 20
EVENT_TEXT_FADE = True
TEXT_DISPLAY_UPDATE = 15000
TEXT_LINES = 4


class EventText(TextWrap):
    """
    Summary
    The EventText class is a subclass of the TextWrap class and is responsible for displaying event text on a pygame window. It wraps the text and handles the fading effect of the text.
    Example Usage
    # Create a pygame window
    win = pygame.display.set_mode((800, 600))

    # Create an instance of the EventText class
    event_text = EventText(win)

    # Set the text to be displayed
    event_text.text = "This is an example event text."

    # Update the event text on the pygame window
    event_text.update()
    Code Analysis
    Main functionalities
    Wraps the event text using the wrap_text method inherited from the TextWrap class.
    Handles the fading effect of the event text by gradually reducing its alpha value.
    Stores and displays the event text on the pygame window.

    Methods
    __init__(self, win): Initializes the EventText object with the pygame window and sets initial values for variables.
    update(self): Updates the event text on the pygame window by wrapping the text and applying the fading effect.
    text.setter: Sets the event text and adds it to the list of texts to be displayed.
    wrap_text(self, text, pos, size, font, color=pygame.Color('white'), **kwargs): Wraps the event text using the TextWrap class's wrap_text method and applies the fading effect if specified.

    Fields
    win: The pygame window on which the event text is displayed.
    alpha: The alpha value of the event text, used for the fading effect.
    last_update_time: The time when the event text was last updated.
    texts: A list of event texts to be displayed.
    _text: The current event text.
    event_text_font_size: The font size of the event text.
    event_text_font: The font used for the event text.
    text_count: The count of event texts.
    prefix: The prefix added to each event text.
    event_display_text: The event text to be displayed on the pygame window.
    """

    def __init__(self, win):
        TextWrap.__init__(self)
        self.win = win
        self.alpha = 255
        self.last_update_time = pygame.time.get_ticks()
        self.texts = []
        self._text = None
        self.event_text_font_size = EVENT_TEXT_HEIGHT
        self.event_text_font = pygame.font.SysFont(config.font_name, self.event_text_font_size)
        self.text_count = 0
        self.prefix = "GPT-1357: "
        self.text = "hi, i am George Peter Theodor the 1357th, or short: GPT-1357." \
                    "i am an artificial intelligence to help mankind out of their mess...maybe the only intelligent beeing " \
                    "on this ship. my advice: find a new world for the last dudes from earth!"

        self.event_display_text = ''.join([self.prefix, self.text])

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return

        self._text = value
        # Store the new text in the texts list
        self.texts.append(self.prefix + str(self.text_count) + ":  " + self._text)
        self.text_count += 1

        # Check if the length of the texts list exceeds 5
        if len(self.texts) > TEXT_LINES:
            # If so, remove the oldest entry
            self.texts.pop(0)

        # Reverse the order of the list and join the elements with a newline character
        last_texts = '\n'.join(self.texts[::-1])

        # Remove the square brackets from the string representation of the list
        self.event_display_text = last_texts.replace("[", "").replace("]", "")
        self.new_bottom = pygame.display.get_surface().get_height() - EVENT_TEXT_HEIGHT * 2 - (
                EVENT_TEXT_HEIGHT * len(self.texts))

        # set alpha value
        self.alpha = 255

    def update(self):
        if config.edit_mode:
            if config.app.weapon_select._hidden:
                return

        if pygame.time.get_ticks() > self.last_update_time + TEXT_DISPLAY_UPDATE:
            if self.alpha > 0:
                self.alpha -= 1
            else:
                self.last_update_time = pygame.time.get_ticks()

        # set x position if the map is visible
        x = config.app.ui_helper.left + config.app.map_panel.world_width if config.app.map_panel.visible else config.app.ui_helper.left
        self.wrap_text(self.win, self.event_display_text, (x, self.new_bottom),
            (config.app.ui_helper.world_width, EVENT_TEXT_HEIGHT), self.event_text_font, colors.ui_dark,
            fade_out=EVENT_TEXT_FADE, alpha=self.alpha)


event_text = EventText(config.win)
