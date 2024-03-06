import pygame.mouse

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.handlers.image_handler import change_non_transparent_pixels
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image

CURSOR_SIZE = 50


class Cursor:
    def __init__(self):
        self.win = config.app.win
        self.cursor_size = (config.ui_cursor_size, config.ui_cursor_size)
        self.cursor = "idle"
        self.color = pygame.color.THECOLORS.get("white")  # colors.frame_color
        self.layer = 10
        self.isSubWidget = False
        self.name = "cursor"

        self.cursors = {"idle": pygame.transform.scale(get_image(f"crosshair003.png"), self.cursor_size),
                        "click": pygame.transform.scale(get_image(f"crosshair002.png"), self.cursor_size),
                        "drag": pygame.transform.scale(get_image(f"crosshair185.png"), self.cursor_size),
                        "box_select": pygame.transform.scale(get_image(f"crosshair030.png"), self.cursor_size),
                        "navigate": pygame.transform.scale(get_image(f"crosshair186.png"), self.cursor_size),
                        "zoom_out": pygame.transform.scale(get_image(f"crosshair139.png"), self.cursor_size),
                        "zoom_in": pygame.transform.scale(get_image(f"crosshair146.png"), self.cursor_size),
                        "watch": pygame.transform.scale(get_image(f"crosshair140.png"), self.cursor_size),
                        "ship": pygame.transform.scale(get_image(f"crosshair138.png"), self.cursor_size),
                        "toggle_up": pygame.transform.scale(get_image(f"crosshair022.png"), self.cursor_size),
                        "toggle_down": pygame.transform.flip(pygame.transform.scale(get_image(f"crosshair022.png"), self.cursor_size), False, True),
                        "scroll": pygame.transform.scale(get_image(f"crosshair017.png"), self.cursor_size),
                        "scroll_up": pygame.transform.scale(get_image(f"crosshair023.png"), self.cursor_size),
                        "scroll_down": pygame.transform.flip(pygame.transform.scale(get_image(f"crosshair023.png"), self.cursor_size), False, True),
                        "left_arrow": pygame.transform.rotate(pygame.transform.scale(get_image(f"crosshair022.png"), self.cursor_size), 90),
                        "right_arrow": pygame.transform.rotate(pygame.transform.flip(pygame.transform.scale(get_image(f"crosshair022.png"), self.cursor_size), False, True), 90),
                        "left_arrow_repeated": pygame.transform.rotate(pygame.transform.scale(get_image(f"crosshair023.png"), self.cursor_size), 90),
                        "right_arrow_repeated": pygame.transform.rotate(pygame.transform.flip(pygame.transform.scale(get_image(f"crosshair023.png"), self.cursor_size), False, True), 90),
                        "close": pygame.transform.scale(get_image(f"crosshair005.png"), self.cursor_size),
                        }

        # change image color
        self.change_image_color()

        # set initial cursor image
        self.image = self.cursors.get(self.cursor)

        # register
        WidgetHandler.addWidget(self)

    def change_image_color(self):
        for key, value in self.cursors.items():
            self.cursors[key] = change_non_transparent_pixels(value, self.color)

    def set_cursor(self, value):
        self.cursor = value
        self.image = self.cursors.get(self.cursor)

    def draw(self):
        if config.ui_show_cursor:
            pygame.mouse.set_visible(False)
            pos = (pygame.mouse.get_pos()[0] - self.image.get_rect().width / 2,
                   pygame.mouse.get_pos()[1] - self.image.get_rect().height / 2)
            self.win.blit(self.image, pos)
        else:
            pygame.mouse.set_visible(True)
