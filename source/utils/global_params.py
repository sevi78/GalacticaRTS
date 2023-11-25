# initialize pygame and window
import os
import pygame
from source.database.saveload import load_file
from source.multimedia_library.sounds import Sounds

# load settings
settings = load_file("settings.json")

# setup globals
global font_name
font_name = settings["font_name"]  # "bahnschrift"#'comicsansms'#'corbel'#"consolas"#"candara"

global WIDTH
WIDTH = int(settings["WIDTH"][0][0])  # windowsize[0]

global HEIGHT
HEIGHT = int(settings["HEIGHT"][0][0])  # windowsize[1]

global WIDTH_MINIMIZED
WIDTH_MINIMIZED = 1400

global HEIGHT_MINIMIZED
HEIGHT_MINIMIZED = 800

global WIDTH_CURRENT
WIDTH_CURRENT = WIDTH

global HEIGHT_CURRENT
HEIGHT_CURRENT = HEIGHT

global win
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)

# root path
# dirty hack to get version of the game based on the folder name
file_path = os.path.dirname(os.path.realpath(__file__))
abs_root = os.path.split(file_path)[0]

global root
root = abs_root.split(os.sep)[-1]
dirpath = os.path.dirname(os.path.realpath(__file__))

global pictures_path
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep

# Sounds
global sounds
sounds = Sounds()

# Game variables
global moveable
moveable = settings["moveable"]  # True

global app
app = None

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

global text_input_active
text_input_active = False

global copy_object
copy_object = None

global hover_object
hover_object = None

global edit_mode
edit_mode = False

global planet_button_display_on_panel
planet_button_display_on_panel = True

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
