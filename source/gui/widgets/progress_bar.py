from typing import Callable

import pygame
from pygame_widgets.util import drawText

from source.configuration.game_config import config
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import calculate_gradient_color
from source.handlers.position_handler import align_vertical, align_horizontal


class ProgressBar(WidgetBase):
    """Main functionalities:
    The ProgressBar class is a subclass of WidgetBase and represents a progress bar widget that can be displayed on a
    pygame surface. It can be either straight or curved and can be customized with different colors for the completed
     and incomplete portions of the bar. The progress of the bar is determined by a callable function that returns a
     float value between 0 and 1.

    Methods:
    - __init__: initializes the ProgressBar object with the given parameters and sets default values for some optional
      parameters
    - listen: listens for events (not used in this class)
    - draw: draws the progress bar on the pygame surface based on the current progress value
    - contains: checks if the given coordinates are within the bounds of the progress bar
    - hide: hides the progress bar
    - show: shows the progress bar
    - disable: disables the progress bar
    - enable: enables the progress bar

    Fields:
    - win: the pygame surface on which to draw the progress bar
    - x, y: the coordinates of the top left corner of the progress bar
    - _x, _y: the screen coordinates of the progress bar (updated by set_screen_position method)
    - _width, _height: the width and height of the progress bar
    - _hidden: a boolean indicating whether the progress bar is hidden or not
    - _disabled: a boolean indicating whether the progress bar is disabled or not
    - progress: a callable function that returns the current progress value of the bar
    - curved: a boolean indicating whether the progress bar is curved or not
    - completed_color: the color of the completed portion of the progress bar
    - incompleted_color: the color of the incomplete portion of the progress bar
    - percent: the current progress value of the bar (between 0 and 1)
    - radius: the radius of the curved progress bar (half of the height)"""

    # doesnt work yet
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, win, x, y, width, height, progress: Callable[[], float], **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, **kwargs)
        self.orientation = kwargs.get('orientation', self.HORIZONTAL)
        self.layer = kwargs.get("layer")
        self.parent = kwargs.get("parent", None)
        self.progress = progress
        self.curved = kwargs.get('curved', False)
        self.completed_color = kwargs.get('completed_color', (0, 200, 0))
        self.incompleted_color = kwargs.get('incompleted_color', (100, 100, 100))
        self.percent = self.progress()
        self.ignore_progress = kwargs.get("ignore_progress", False)
        self.radius = self.screen_height / 2 if self.curved else 0

        self.h_align = kwargs.get("h_align", None)
        self.v_align = kwargs.get("v_align", None)
        self.h_size = kwargs.get("h_size", None)
        self.v_size = kwargs.get("v_size", None)

        self.string = kwargs.get("text", None)
        self.font = pygame.font.SysFont(config.font_name, 12)
        self.gradient_color = kwargs.get("gradient_color", True)
        self.disable()

    def set_progressbar_position(self):
        """
         # set progress bar position based on the images ccordinates
        """
        x, y = self.parent.rect.x, self.parent.rect.y + self.parent.rect.height * 1.3

        if self.h_align:
            x = align_horizontal(self.parent.rect, self.h_align)

        if self.v_align:
            y = align_vertical(self.parent.rect, self.v_align)

        self.set_position((x, y))
        if self.h_size:
            self.set_screen_width(self.h_size)
        else:
            self.set_screen_width(self.parent.rect.width)

    def draw(self):
        """ Display to surface """
        if not self.ignore_progress:
            self.percent = min(max(self.progress(), 0), 1)
        # else:
        #     if self.percent > 1.0:
        #         self.percent = 1

        if self.gradient_color:
            self.completed_color = calculate_gradient_color((200, 0, 0),
                    pygame.color.THECOLORS["darkgreen"], self.percent, ignore_colors=["b"])

        if self.parent:
            if self.parent._disabled:
                return

        if not self._hidden:
            if self.curved:
                if self.percent == 0:
                    pygame.draw.circle(self.win, self.incompleted_color,
                            (self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.incompleted_color,
                            (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                            self.radius)
                elif self.percent == 1:
                    pygame.draw.circle(self.win, self.completed_color,
                            (self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.completed_color,
                            (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                            self.radius)
                else:
                    pygame.draw.circle(self.win, self.completed_color, (
                        self.screen_x, self.screen_y + self.screen_height // 2),
                            self.radius)
                    pygame.draw.circle(self.win, self.incompleted_color,
                            (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                            self.radius)

            pygame.draw.rect(self.win, self.completed_color,
                    (self.screen_x, self.screen_y, int(self.screen_width * self.percent), self.screen_height))
            pygame.draw.rect(self.win, self.incompleted_color,
                    (self.screen_x + int(self.screen_width * self.percent), self.screen_y,
                     int(self.screen_width * (1 - self.percent)), self.screen_height))

            if self.string:
                drawText(self.win, self.string, self.frame_color, (
                    self.screen_x - 40, self.screen_y - self.font.get_height() / 6, 200,
                    self.font.get_height()), self.font, align="left")
