import ctypes
import os
import pygame
from source.handlers.file_handler import load_file

class GameConfig:
    def __init__(self):
        # Load settings from a JSON file
        self.settings = load_file("settings.json", "config")

        # Initialize configuration variables
        self.font_name = self.settings["font_name"]
        self.WIDTH = int(self.settings["WIDTH"])
        self.HEIGHT = int(self.settings["HEIGHT"])
        self.WIDTH_MINIMIZED = 1920
        self.HEIGHT_MINIMIZED = 800
        self.WIDTH_CURRENT = self.WIDTH
        self.HEIGHT_CURRENT = self.HEIGHT
        self.moveable = self.settings["moveable"]
        self.app = None
        self.tooltip_text = ""
        self.game_paused = False
        self.game_speed = int(self.settings["game_speed"])
        self.fps = int(self.settings["fps"])
        self.scene_width = int(self.settings["scene_width"])
        self.scene_height = int(self.settings["scene_height"])
        self.quadrant_amount = 1
        self.building_editor_draw = False
        self.enable_zoom = True
        self.enable_pan = True
        self.debug = self.settings["debug"]
        self.enable_orbit = True
        self.enable_game_events = self.settings["enable_game_events"]
        self.show_orbit = True
        self.show_grid = False
        self.show_map_panel = True
        self.text_input_active = False
        self.copy_object = None
        self.hover_object = None
        self.edit_mode = False
        self.show_overview_buttons = True
        self.ui_rounded_corner_radius_small = int(self.settings["ui_rounded_corner_radius_small"])
        self.ui_rounded_corner_radius_big = self.settings["ui_rounded_corner_radius_big"]
        self.ui_rounded_corner_small_thickness = self.settings["ui_rounded_corner_small_thickness"]
        self.ui_rounded_corner_big_thickness = self.settings["ui_rounded_corner_big_thickness"]
        self.ui_panel_alpha = self.settings["ui_panel_alpha"]
        self.draw_universe = True

        # Initialize pygame and window
        pygame.init()
        self.init_window()

    def init_window(self):
        # Call the GetSystemMetrics function with index 80 to get the number of monitors
        number_of_monitors = ctypes.windll.user32.GetSystemMetrics(80)
        if number_of_monitors > 1:
            print("Multiple monitors detected")
        else:
            print("Only one monitor detected")

        # Set the position of the window to the second monitor
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, -1080)

        # Set the display mode to full screen on the second monitor
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)

# Usage
config = GameConfig()
