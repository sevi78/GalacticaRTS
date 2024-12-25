import os
import pygame

from source.handlers.file_handler import load_file, get_player_list
from source.handlers.image_handler import overblit_button_image


class ScreenConfig:
    def set_monitor(self, monitor_index=0):
        """
        Sets the monitor at runtime and initializes a Pygame window on the selected monitor.
        :param monitor_index: The index of the monitor where the window should be displayed. Defaults to 0.
        this funtion has some problems.
        some windows are not shown up after calling
        """
        # Get the list of available monitors
        monitors = pygame.display.get_desktop_sizes()

        # Check if the monitor_index is within the range of connected monitors
        if monitor_index >= len(monitors):
            print(f"cant choose monitor:{monitor_index}, index out of range")
            return

        # Get the resolution of the selected monitor
        monitor_resolution = monitors[monitor_index]

        # set the window position(vertical stack)
        window_position_x = 0
        window_position_y = monitor_resolution[1] * monitor_index

        # Set the SDL environment variable to position the window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_position_x, window_position_y)

        # Initialize the window on the selected monitor
        win = pygame.display.set_mode(monitor_resolution, pygame.HWSURFACE | pygame.DOUBLEBUF, display=monitor_index)
        return win


class GameConfig:
    """
    simply write new elements into settings.json
    """

    def __init__(self):
        self.screen_config = ScreenConfig()

        # Initialize configuration variables
        self.width = 1920
        self.height = 1080
        self.width_minimized = 1920
        self.height_minimized = 800
        self.width_current = self.width
        self.height_current = self.height
        self.moveable = True
        self.app = None
        self.players = len(get_player_list())
        self.player = 0
        self.tooltip_text = ""
        self.game_paused = False
        self.scene_width = 14000
        self.scene_height = 14000
        self.quadrant_amount = 1
        self.enable_zoom = True
        self.enable_pan = True
        self.enable_cross = True
        self.cross_view_start = 0.2
        self.debug = False
        self.enable_orbit = True
        self.enable_autopilot = False
        self.show_orbit = True
        self.show_grid = False
        self.show_map_panel = True
        self.text_input_active = False
        self.copy_object = None
        self.hover_object = None
        self.edit_mode = False
        self.show_overview_buttons = True
        self.draw_universe = True
        self.universe_density = 25
        self.view_explored_planets = True
        self.selected_monitor = 1

        # Load settings from a JSON file
        self.settings = load_file("settings.json", "config")
        for key, value in self.settings.items():
            setattr(self, key, value)

        # Initialize pygame and window
        self.win = self.screen_config.set_monitor(self.monitor)

    @property
    def monitor(self):
        return self._monitor

    @monitor.setter
    def monitor(self, value):
        self._monitor = value
        self.win = self.screen_config.set_monitor(self._monitor)

    @property
    def enable_autopilot(self):
        return self._enable_autopilot

    @enable_autopilot.setter
    def enable_autopilot(self, value):
        self._enable_autopilot = value

    def set_global_variable(self, key, value, **kwargs):
        var = kwargs.get("var", None)
        button = kwargs.get("button", None)

        if var:
            if getattr(config, var):
                setattr(config, var, False)
            else:
                setattr(config, var, True)

        if not hasattr(config, key):
            setattr(config, key, value)

        if getattr(config, key):
            setattr(config, key, False)

        else:
            setattr(config, key, True)

        overblit_button_image(button, "uncheck.png", getattr(config, key))


# Usage
config = GameConfig()
