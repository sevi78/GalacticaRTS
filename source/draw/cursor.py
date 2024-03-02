import pygame.mouse

from source.configuration.game_config import config
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image

CURSOR_SIZE = 50
class Cursor:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.win = config.app.win
        self.cursor_size = (CURSOR_SIZE,CURSOR_SIZE)
        self.cursor = 3
        self.layer = 10
        self.isSubWidget = True
        self.cursor_states = {0:"idle",
                              1:"drag"}

        self.image = pygame.transform.scale(get_image(f"crosshair00{self.cursor}.png"), self.cursor_size)
        # self.image = get_image(f"crosshair00{self.cursor}.png")

        WidgetHandler.addWidget(self)


    def set_cursor(self, value):
        self.cursor = value
        self.image = get_image(f"crosshair00{self.cursor}.png")

    def draw(self):
        pos = pygame.mouse.get_pos()[0] - self.image.get_rect().width/2, pygame.mouse.get_pos()[1] - self.image.get_rect().height/2
        self.win.blit(self.image, pos)
