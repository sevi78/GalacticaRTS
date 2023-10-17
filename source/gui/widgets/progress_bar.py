from typing import Callable

import pygame

from source.gui.widgets.widget_base_components.widget_base import WidgetBase


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
    - completedColour: the color of the completed portion of the progress bar
    - incompletedColour: the color of the incomplete portion of the progress bar
    - percent: the current progress value of the bar (between 0 and 1)
    - radius: the radius of the curved progress bar (half of the height)"""

    def __init__(self, win, x, y, width, height, progress: Callable[[], float], **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        self.layer = kwargs.get("layer")
        self.parent = kwargs.get("parent", None)
        self.progress = progress
        self.curved = kwargs.get('curved', False)
        self.completedColour = kwargs.get('completedColour', (0, 200, 0))
        self.incompletedColour = kwargs.get('incompletedColour', (100, 100, 100))
        self.percent = self.progress()
        self.radius = self.screen_height / 2 if self.curved else 0

        self.disable()

    def set_progressbar_position(self):
        """
         # set progress bar position based on the images ccordinates
        """
        self.set_position((self.parent.rect.x, self.parent.rect.y + self.parent.rect.height * 1.3))
        self.setWidth(self.parent.rect.width)

    def draw(self):
        """ Display to surface """
        self.percent = min(max(self.progress(), 0), 1)
        if self.parent:
            if self.parent._disabled:
                return

        if not self._hidden:
            if self.curved:
                if self.percent == 0:
                    pygame.draw.circle(self.win, self.incompletedColour,
                        (self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.incompletedColour,
                        (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                        self.radius)
                elif self.percent == 1:
                    pygame.draw.circle(self.win, self.completedColour,
                        (self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.completedColour,
                        (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                        self.radius)
                else:
                    pygame.draw.circle(self.win, self.completedColour, (
                        self.screen_x, self.screen_y + self.screen_height // 2),
                        self.radius)
                    pygame.draw.circle(self.win, self.incompletedColour,
                        (self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                        self.radius)

            pygame.draw.rect(self.win, self.completedColour,
                (self.screen_x, self.screen_y, int(self.screen_width * self.percent), self.screen_height))
            pygame.draw.rect(self.win, self.incompletedColour,
                (self.screen_x + int(self.screen_width * self.percent), self.screen_y,
                 int(self.screen_width * (1 - self.percent)), self.screen_height))

#
# if __name__ == '__main__':
#     import time
#
#     startTime = time.time()
#
#     pygame.init()
#     win = pygame.display.set_mode((1000, 600))
#
#     progressBar = ProgressBar(win, 100, 100, 500, 40, lambda: 1 - (time.time() - startTime) / 10, curved=True, layer = 9)
#
#     run = True
#     while run:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#                 quit()
#
#         win.fill((255, 255, 255))
#
#         update(events)
#         pygame.display.update()
