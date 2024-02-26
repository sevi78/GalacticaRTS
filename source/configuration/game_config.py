# initialize pygame and window
import ctypes
import os

import pygame

from source.handlers.file_handler import load_file
from source.handlers.image_handler import overblit_button_image


class GameConfig:
    def __init__(self):
        # Load settings from a JSON file

        self.settings = load_file("settings.json", "config")

        # Initialize configuration variables
        self.font_name = self.settings["font_name"]
        self.width = 1920
        self.height = 1080
        self.width_minimized = 1920
        self.height_minimized = 800
        self.width_current = self.width
        self.height_current = self.height
        self.moveable = True
        self.app = None
        self.players = 2
        self.player = None
        self.tooltip_text = ""
        self.game_paused = False
        self.game_speed = self.settings["game_speed"]
        self.fps = int(self.settings["fps"])
        self.scene_width = 14000
        self.scene_height = 14000
        self.quadrant_amount = 1
        self.enable_zoom = True
        self.enable_pan = True
        self.enable_cross = True
        self.cross_view_start = 0.2
        self.debug = False
        self.enable_orbit = True
        self.enable_game_events = self.settings["enable_game_events"]
        self.enable_autopilot = False
        self.show_orbit = True
        self.show_grid = False
        self.show_map_panel = True
        self.text_input_active = False
        self.copy_object = None
        self.hover_object = None
        self.edit_mode = False
        self.show_overview_buttons = True
        self.ui_rounded_corner_radius_small = self.settings["ui_rounded_corner_radius_small"]
        self.ui_rounded_corner_radius_big = self.settings["ui_rounded_corner_radius_big"]
        self.ui_rounded_corner_small_thickness = self.settings["ui_rounded_corner_small_thickness"]
        self.ui_rounded_corner_big_thickness = self.settings["ui_rounded_corner_big_thickness"]
        self.ui_panel_alpha = self.settings["ui_panel_alpha"]
        self.ui_cross_size = self.settings["ui_cross_size"]
        self.ui_cross_dash_length = self.settings["ui_cross_dash_length"]
        self.ui_cross_thickness = self.settings["ui_cross_thickness"]
        self.ui_tooltip_size = self.settings["ui_tooltip_size"]
        self.draw_universe = True
        self.universe_density = 25

        self.view_explored_planets = True

        self.selected_monitor = 1

        # set a list of editable params for setting_editor
        self.editable_params = {"player": 0,
                                "fps": self.fps,
                                "enable_game_events": self.enable_game_events,
                                "draw_universe": self.draw_universe,
                                "ui_panel_alpha": self.ui_panel_alpha,
                                "ui_rounded_corner_radius_small": self.ui_rounded_corner_radius_small,
                                "ui_rounded_corner_radius_big": self.ui_rounded_corner_radius_big,
                                "ui_rounded_corner_small_thickness": self.ui_rounded_corner_small_thickness,
                                "ui_rounded_corner_big_thickness": self.ui_rounded_corner_big_thickness,
                                "ui_cross_size": self.ui_cross_size,
                                "ui_cross_dash_length": self.ui_cross_dash_length,
                                "ui_cross_thickness": self.ui_cross_thickness,
                                "ui_tooltip_size": self.ui_tooltip_size,
                                "game_speed": self.game_speed
                                }

        # Initialize pygame and window
        self.init_window()

    @property
    def enable_autopilot(self):
        return self._enable_autopilot

    @enable_autopilot.setter
    def enable_autopilot(self, value):
        self._enable_autopilot = value


    def init_window(self):
        # Call the GetSystemMetrics function with index 80 to get the number of monitors
        number_of_monitors = ctypes.windll.user32.GetSystemMetrics(80)
        if number_of_monitors > 1:
            print("Multiple monitors detected")
        else:
            print("Only one monitor detected")

        # Set the position of the window to the selected monitor
        if self.selected_monitor <= number_of_monitors:
            os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (self.width * self.selected_monitor, 0)
        else:
            print("Selected monitor index is out of range")

        # Set the display mode to full screen on the selected monitor
        # self.win = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN, pygame.DOUBLEBUF)
        self.win = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE, pygame.DOUBLEBUF)

    def set_global_variable(self, key, value, **kwargs):
        var = kwargs.get("var", None)
        button = kwargs.get("button", None)

        if var:
            if getattr(config, var):
                setattr(config, var, False)
            else:
                setattr(config, var, True)

        if getattr(config, key):
            setattr(config, key, False)

        else:
            setattr(config, key, True)

        overblit_button_image(button, "uncheck.png", getattr(config, key))


# Usage
config = GameConfig()
