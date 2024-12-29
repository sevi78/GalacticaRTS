import pygame.mouse

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, change_non_transparent_pixels, scale_image_cached

CURSOR_SIZE = 50


class Cursor:
    def __init__(self):
        self.win = config.app.win
        self.cursor_size = (config.ui_cursor_size, config.ui_cursor_size)
        self.cursor = "idle"
        self.color = colors.frame_color#pygame.color.THECOLORS.get("white")  # colors.frame_color
        self.layer = 10
        self.is_sub_widget = False
        self.name = "cursor"

        self.cursors = {
            "idle": scale_image_cached(get_image(f"crosshair003.png"), self.cursor_size),
            "click": scale_image_cached(get_image(f"crosshair002.png"), self.cursor_size),
            "drag": scale_image_cached(get_image(f"crosshair185.png"), self.cursor_size),
            "box_select": scale_image_cached(get_image(f"crosshair030.png"), self.cursor_size),
            "navigate": scale_image_cached(get_image(f"crosshair186.png"), self.cursor_size),
            "zoom_out": scale_image_cached(get_image(f"crosshair139.png"), self.cursor_size),
            "zoom_in": scale_image_cached(get_image(f"crosshair146.png"), self.cursor_size),
            "watch": scale_image_cached(get_image(f"crosshair140.png"), self.cursor_size),
            "ship": scale_image_cached(get_image(f"crosshair138.png"), self.cursor_size),
            "toggle_up": scale_image_cached(get_image(f"crosshair022.png"), self.cursor_size),
            "toggle_down": pygame.transform.flip(scale_image_cached(get_image(f"crosshair022.png"), self.cursor_size), False, True),
            "scroll": scale_image_cached(get_image(f"crosshair017.png"), self.cursor_size),
            "scroll_up": scale_image_cached(get_image(f"crosshair023.png"), self.cursor_size),
            "scroll_down": pygame.transform.flip(scale_image_cached(get_image(f"crosshair023.png"), self.cursor_size), False, True),
            "left_arrow": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair022.png"), self.cursor_size), 90),
            "right_arrow": pygame.transform.rotate(pygame.transform.flip(scale_image_cached(get_image(f"crosshair022.png"), self.cursor_size), False, True), 90),
            "left_arrow_repeated": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair023.png"), self.cursor_size), 90),
            "right_arrow_repeated": pygame.transform.rotate(pygame.transform.flip(scale_image_cached(get_image(f"crosshair023.png"), self.cursor_size), False, True), 90),
            "close": scale_image_cached(get_image(f"crosshair005.png"), self.cursor_size),
            "resize_0": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair015.png"), self.cursor_size), 0),
            "resize_45": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair015.png"), self.cursor_size), 45),
            "resize_90": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair015.png"), self.cursor_size), 90),
            "resize_135": pygame.transform.rotate(scale_image_cached(get_image(f"crosshair015.png"), self.cursor_size), 135),
            }

        self.resize_cursor_orientations = {
            "top": 90,
            "bottom": 90,
            "left": 0,
            "right": 0,
            "top-left": 135,
            "bottom-left": 45,
            "top-right": 45,
            "bottom-right": 135
            }

        # change image color
        self.change_image_color()

        # set initial cursor image
        self.image = self.cursors.get(self.cursor)

        # register
        WidgetHandler.add_widget(self)

    def change_image_color(self):
        for key, value in self.cursors.items():
            self.cursors[key] = change_non_transparent_pixels(value, self.color)

    def set_cursor(self, value):
        self.cursor = value
        self.image = self.cursors.get(self.cursor)

    def get_resize_cursor_orientation(self, resize_side):
        if resize_side:
            return self.resize_cursor_orientations[resize_side]
        else:
            return self.resize_cursor_orientations["top"]

    def get_resize_cursor(self, angle):
        return f"resize_{angle}"

    def draw(self):
        if config.ui_show_cursor:
            if not self.cursor == "idle":
                pygame.mouse.set_visible(False)
                if self.image:
                    pos = (pygame.mouse.get_pos()[0] - self.image.get_rect().width / 2,
                           pygame.mouse.get_pos()[1] - self.image.get_rect().height / 2)
                    self.win.blit(self.image, pos)
            else:
                pygame.mouse.set_visible(True)

        else:
            pygame.mouse.set_visible(True)
