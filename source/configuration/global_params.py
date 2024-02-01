# initialize pygame and window
import os
import ctypes
import pygame
from source.handlers.file_handler import load_file
from source.multimedia_library.sounds import Sounds

# load settings
settings = load_file("settings.json", "config")

# setup globals
global font_name
font_name = settings["font_name"]  # "bahnschrift"#'comicsansms'#'corbel'#"consolas"#"candara"

global WIDTH
WIDTH = int(settings["WIDTH"][0][0])  # windowsize[0]

global HEIGHT
HEIGHT = int(settings["HEIGHT"][0][0])  # windowsize[1]

global WIDTH_MINIMIZED
WIDTH_MINIMIZED = 1920

global HEIGHT_MINIMIZED
HEIGHT_MINIMIZED = 800

global WIDTH_CURRENT
WIDTH_CURRENT = WIDTH

global HEIGHT_CURRENT
HEIGHT_CURRENT = HEIGHT

global win

# Call the GetSystemMetrics function with index 80 to get the number of monitors
number_of_monitors = ctypes.windll.user32.GetSystemMetrics(80)

if number_of_monitors > 1:
    print("Multiple monitors detected")
else:
    print("Only one monitor detected")
# Set the position of the window to the second monitor
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, -1080)
# Set the display mode to full screen on the second monitor
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Sounds
global sounds
sounds = Sounds()

# Game variables
global moveable
moveable = settings["moveable"]  # True

global app
app = None

global level
level = 1

global tooltip_text
tooltip_text = ""

global game_paused
game_paused = False

global time_factor
time_factor = int(settings["time_factor"])  # 1

global game_speed
game_speed = int(settings["game_speed"])  # 10

global fps
fps = int(settings["fps"])  # 60

global scene_width
scene_width = int(settings["scene_width"])  # 60

global scene_height
scene_height = int(settings["scene_height"])  # 60

global quadrant_amount
quadrant_amount = 1

global draw_background_image
draw_background_image = settings["draw_background_image"]

global building_editor_draw
building_editor_draw = False

global enable_zoom
enable_zoom = settings["enable_zoom"]  # False

global enable_pan
enable_pan = settings["enable_pan"]

global debug
debug = settings["debug"]

global enable_orbit
enable_orbit = settings["enable_orbit"]

global enable_game_events
enable_game_events = settings["enable_game_events"]

global show_orbit
show_orbit = True

global show_grid
show_grid = False

global show_map_panel
show_map_panel = True

global text_input_active
text_input_active = False

global copy_object
copy_object = None

global hover_object
hover_object = None

global edit_mode
edit_mode = False

global show_overview_buttons
show_overview_buttons = True

global ui_rounded_corner_radius_small
ui_rounded_corner_radius_small = int(settings["ui_rounded_corner_radius_small"])

global ui_rounded_corner_radius_big
ui_rounded_corner_radius_big = settings["ui_rounded_corner_radius_big"]

global ui_rounded_corner_small_thickness
ui_rounded_corner_small_thickness = settings["ui_rounded_corner_small_thickness"]

global ui_rounded_corner_big_thickness
ui_rounded_corner_big_thickness = settings["ui_rounded_corner_big_thickness"]

global ui_panel_alpha
ui_panel_alpha = settings["ui_panel_alpha"]  # 160

global draw_universe
draw_universe = settings["draw_universe"]
